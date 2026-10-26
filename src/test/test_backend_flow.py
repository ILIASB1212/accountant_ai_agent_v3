"""Flow test for the multi-tenant API: owner -> join code -> approval -> client firm -> session -> chat.

Supabase and the LangGraph agent are replaced by in-memory fakes, and the fake
database emulates the RLS rules (tenant isolation). This checks the API logic only:
the real isolation guarantee comes from the SQL policies, so also test those in Supabase.
Run from the repo root:  pytest src/test/test_backend_flow.py
"""
import itertools
import sys
import types
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest
from postgrest.exceptions import APIError

# make `import src...` work whatever directory pytest is started from (local or CI)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

ALICE, BOB, MALLORY = (str(uuid.UUID(int=i)) for i in (1, 2, 3))
TOKENS = {"tok-alice": ALICE, "tok-bob": BOB, "tok-mallory": MALLORY}


class Res:
    def __init__(self, data):
        self.data = data


class FakeDB:
    def __init__(self):
        self.t = {n: [] for n in ("profiles", "companies", "company_members", "clients", "chat_sessions", "messages")}
        self.ids = itertools.count(1)
        for u in TOKENS.values():
            self.t["profiles"].append({"id": u, "full_name": "User " + u[-1]})

    def company_of(self, uid):  # what my_company_id() returns inside RLS policies
        for r in self.t["company_members"]:
            if r["user_id"] == uid and r["status"] == "active":
                return r["company_id"]


class Query:
    def __init__(self, db, uid, name):
        self.db, self.uid, self.name, self.f, self.op, self.payload = db, uid, name, [], "select", None

    def select(self, *_): self.op = "select"; return self
    def insert(self, rows): self.op, self.payload = "insert", rows; return self
    def update(self, vals): self.op, self.payload = "update", vals; return self
    def delete(self): self.op = "delete"; return self
    def eq(self, c, v): self.f.append((c, v)); return self
    def in_(self, c, vs): self.f.append((c, set(vs))); return self
    def order(self, *a, **k): return self
    def limit(self, n): return self

    def _match(self, r):
        return all((r.get(c) in v) if isinstance(v, set) else r.get(c) == v for c, v in self.f)

    def _visible(self, r):  # RLS emulation
        if self.name in ("clients", "chat_sessions"):
            return r["company_id"] == self.db.company_of(self.uid)
        if self.name == "messages":
            s = next((x for x in self.db.t["chat_sessions"] if x["id"] == r["session_id"]), None)
            return bool(s) and s["company_id"] == self.db.company_of(self.uid)
        if self.name == "company_members":
            return r["user_id"] == self.uid or r["company_id"] == self.db.company_of(self.uid)
        if self.name == "companies":
            return r["id"] == self.db.company_of(self.uid)
        return True

    def execute(self):
        rows = self.db.t[self.name]
        if self.op == "insert":
            items = self.payload if isinstance(self.payload, list) else [self.payload]
            out = []
            for it in items:
                row = {"id": str(uuid.uuid4()) if self.name != "messages" else next(self.db.ids), "created_at": "now", **it}
                if self.name in ("clients", "chat_sessions") and row["company_id"] != self.db.company_of(self.uid):
                    raise APIError({"code": "42501", "message": "rls"})
                rows.append(row)
                out.append(row)
            return Res(out)
        hit = [r for r in rows if self._match(r) and self._visible(r)]
        if self.op == "update":
            for r in hit:
                r.update(self.payload)
        if self.op == "delete":
            for r in hit:
                rows.remove(r)
        return Res([dict(r) for r in hit])


class Rpc:
    def __init__(self, db, uid, name, params):
        self.db, self.uid, self.name, self.p = db, uid, name, params

    def execute(self):
        db, uid = self.db, self.uid
        if self.name == "create_company":
            if any(m["user_id"] == uid for m in db.t["company_members"]):
                raise APIError({"code": "P0001", "message": "you already belong to a company"})
            cid = str(uuid.uuid4())
            db.t["companies"].append({"id": cid, "name": self.p["p_name"], "join_code": "ABCD1234"})
            db.t["company_members"].append({"company_id": cid, "user_id": uid, "role": "owner", "status": "active", "created_at": "1"})
            return Res(cid)
        if self.name == "join_company":
            c = next((c for c in db.t["companies"] if c["join_code"] == self.p["p_code"].upper()), None)
            if not c:
                raise APIError({"code": "P0001", "message": "invalid join code"})
            db.t["company_members"].append({"company_id": c["id"], "user_id": uid, "role": "member", "status": "pending", "created_at": "2"})
            return Res(c["id"])
        if self.name == "rotate_join_code":
            return Res("NEWCODE99")


class FakeClient:
    def __init__(self, db):
        self.db, self.uid = db, None
        self.postgrest = SimpleNamespace(auth=self._set_token)
        self.auth = SimpleNamespace(get_user=self._get_user)

    def _get_user(self, token):
        if token not in TOKENS:
            raise Exception("bad token")
        return SimpleNamespace(user=SimpleNamespace(id=TOKENS[token]))

    def _set_token(self, token):
        self.uid = TOKENS[token]

    def table(self, name): return Query(self.db, self.uid, name)
    def rpc(self, name, params=None): return Rpc(self.db, self.uid, name, params or {})


class FakeGraph:
    def __init__(self): self.calls = []

    def invoke(self, state, config):
        self.calls.append((state, config))
        return {"messages": [SimpleNamespace(content="Réponse test")]}


class FakeMem0:
    searches, adds = [], []

    def __init__(self, api_key=None): pass
    def search(self, **kw): FakeMem0.searches.append(kw); return {"results": [{"memory": "TVA trimestrielle"}]}
    def add(self, **kw): FakeMem0.adds.append(kw)


@pytest.fixture()
def api(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://x.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "anon")
    monkeypatch.setenv("DATABASE_URL", "postgresql://x")
    monkeypatch.setenv("MEM0_API_KEY", "k")
    agent_stub = types.ModuleType("src.agentic_workflow.agent")
    agent_stub.build_graph = lambda cp: None
    monkeypatch.setitem(sys.modules, "src.agentic_workflow.agent", agent_stub)
    monkeypatch.setitem(sys.modules, "mem0", SimpleNamespace(MemoryClient=FakeMem0))
    for m in [m for m in sys.modules if m.startswith(("src.backend", "src.memory"))]:
        monkeypatch.delitem(sys.modules, m)

    from fastapi.testclient import TestClient
    import src.backend as backend
    import src.backend.dependencies as deps

    db, graph = FakeDB(), FakeGraph()
    monkeypatch.setattr(deps, "create_client", lambda *a, **k: FakeClient(db))
    backend.app.state.graph = graph
    FakeMem0.searches.clear(); FakeMem0.adds.clear()
    yield TestClient(backend.app), db, graph
    # don't leave modules bound to the fakes behind for other test files
    for m in [m for m in sys.modules if m.startswith(("src.backend", "src.memory"))]:
        del sys.modules[m]


def h(who): return {"Authorization": f"Bearer tok-{who}"}
REG, AG = "/api/v3/registration", "/api/v3/agents"


def test_full_flow(api):
    c, db, graph = api

    # owner registers a company
    r = c.post(f"{REG}/company", json={"company_name": "Fiduciaire Luisiano"}, headers=h("alice"))
    assert r.status_code == 201
    company_id = r.json()["company_id"]
    assert c.get(f"{REG}/me", headers=h("alice")).json()["membership"]["join_code"] == "ABCD1234"
    # an owner cannot create a second company
    assert c.post(f"{REG}/company", json={"company_name": "Another one"}, headers=h("alice")).status_code == 400

    # a worker joins with the code but is pending: no access yet
    assert c.post(f"{REG}/company/join", json={"join_code": "abcd1234"}, headers=h("bob")).status_code == 202
    assert c.post(f"{REG}/company/join", json={"join_code": "WRONG000"}, headers=h("mallory")).status_code == 400
    assert c.get(f"{AG}/clients", headers=h("bob")).status_code == 403
    # a worker cannot approve themselves or list members
    assert c.post(f"{REG}/company/members/{BOB}/approve", headers=h("bob")).status_code == 403
    assert c.get(f"{REG}/company/members", headers=h("bob")).status_code == 403

    # owner sees and approves the request
    members = c.get(f"{REG}/company/members", headers=h("alice")).json()
    assert {m["user_id"]: m["status"] for m in members} == {ALICE: "active", BOB: "pending"}
    assert c.post(f"{REG}/company/members/{BOB}/approve", headers=h("alice")).status_code == 200

    # the worker, now active, adds a client firm and opens a session
    hb = h("bob")
    cl = c.post(f"{AG}/clients", json={"name": "Société Atlas SARL"}, headers=hb)
    assert cl.status_code == 201
    client_id = cl.json()["id"]
    s = c.post(f"{AG}/sessions", json={"client_id": client_id}, headers=hb)
    assert s.status_code == 201 and s.json()["title"] == "Société Atlas SARL"
    session_id = s.json()["id"]

    # chat: thread id = session id, memory scoped to company+client, history saved
    r = c.post(f"{AG}/invoke", json={"session_id": session_id, "message": "Taux de TVA ?"}, headers=hb)
    assert r.status_code == 200 and "Réponse test" in r.text
    state, config = graph.calls[-1]
    assert config["configurable"]["thread_id"] == session_id
    assert config["configurable"]["client_name"] == "Société Atlas SARL"
    assert "TVA trimestrielle" in config["configurable"]["memory_context"]
    assert FakeMem0.searches[-1]["filters"] == {"OR": [{"user_id": f"{company_id}:{client_id}"}, {"agent_id": company_id}]}
    assert FakeMem0.adds[-1]["user_id"] == f"{company_id}:{client_id}" and "agent_id" not in FakeMem0.adds[-1]
    assert [m["role"] for m in db.t["messages"]] == ["user", "assistant"]
    hist = c.get(f"{AG}/sessions/{session_id}/messages", headers=h("alice")).json()
    assert [m["role"] for m in hist] == ["user", "assistant"]  # owner sees the colleague's session

    # another company's owner cannot touch the session or the client
    c.post(f"{REG}/company", json={"company_name": "Cabinet Rival"}, headers=h("mallory"))
    assert c.post(f"{AG}/invoke", json={"session_id": session_id, "message": "hi"}, headers=h("mallory")).status_code == 404
    assert c.get(f"{AG}/sessions/{session_id}/messages", headers=h("mallory")).status_code == 404
    assert c.post(f"{AG}/sessions", json={"client_id": client_id}, headers=h("mallory")).status_code == 404
    assert c.get(f"{AG}/clients", headers=h("mallory")).json() == []

    # bad token
    assert c.get(f"{REG}/me", headers={"Authorization": "Bearer nope"}).status_code == 401