import os
from mem0 import MemoryClient  
from dotenv import load_dotenv

from datetime import datetime


load_dotenv()

MEM0_API_KEY = os.environ["MEM0_API_KEY"]

mem_client = MemoryClient(api_key=MEM0_API_KEY)


class Memory:
    """Long-term memory on Mem0, scoped per tenant.

    Mem0 stores one record per entity: a write that carries both user_id and agent_id
    becomes two separate records, so an AND filter on both ids can never match anything.
    So here:
      * user_id  = "<company_id>:<client_id>"  -> facts about ONE client firm of ONE company
                   (shared by every worker of that company, invisible to everyone else)
      * agent_id = "<company_id>"              -> optional firm-wide notes (how the fiduciary
                   works), searched together with the client scope through an OR filter
    Writes from chat only ever go to the client scope.
    """

    def __init__(self,user_prompt:str,user_id:str,agent_id:str|None=None,limit:int=5):
        self.user_prompt = user_prompt
        self.user_id = user_id
        self.limit = limit
        self.agent_id = agent_id

    @classmethod
    def for_client(cls, user_prompt: str, company_id: str, client_id: str, limit: int = 5):
        """Build the memory scope from IDs read from the database, never from request input."""
        return cls(
            user_prompt,
            user_id=f"{company_id}:{client_id}",
            agent_id=str(company_id),
            limit=limit,
        )

    def _search_filters(self) -> dict:
        if self.agent_id:
            return {"OR": [{"user_id": self.user_id}, {"agent_id": self.agent_id}]}
        return {"user_id": self.user_id}

    def retrive(self):
        return mem_client.search(
            query=self.user_prompt,
            filters=self._search_filters(),
            limit=self.limit,
        )

    def store_memory(self,memory_data: dict[str, str]):
        """Store a conversation turn in the client scope (user_id only, on purpose)."""
        mem_client.add(
            user_id=memory_data["user_id"],
            messages=[
                {"role": "user", "content": memory_data["text"]},
                {"role": "assistant", "content": memory_data["llm_output"]},
            ],
        )

    def store_company_note(self, text: str):
        """Firm-wide knowledge (agent scope), e.g. the fiduciary's own conventions."""
        if not self.agent_id:
            raise ValueError("no company scope on this Memory")
        mem_client.add(
            agent_id=self.agent_id,
            messages=[{"role": "user", "content": text}],
        )

    def format_context_for_systeme(self, memories) -> str:
        """Format the Mem0 response for the system prompt (accepts a list or {"results": [...]})."""
        items = memories.get("results", []) if isinstance(memories, dict) else (memories or [])
        lines = []
        for m in items:
            text = m.get("memory") if isinstance(m, dict) else str(m)
            if text:
                lines.append(f"- {text}")
        return "\n".join(lines)

    def build_prompt(self, memories: list[dict]) -> str:
        """Deprecated: baked a rival system persona + the raw user turn into
        one HumanMessage, which then got permanently written into the
        LangGraph checkpointer's thread history on every call. Kept only for
        reference; use format_context() + chat_node's config instead."""
        memory_block = ""
        if memories:
            context = "\n".join(f"- {m}" for m in memories)
            memory_block = f"Known user context:\n{context}\n\n"

        system = (
            "You are a helpful support agent. Use the known user context when relevant, "
            "and avoid asking for information already present there."
        )
        return f"{system}\n\n{memory_block}User: {self.user_prompt}\nAssistant:"

    def semantic_memory_for_facts(self,llm_output: str) -> dict [str, str] | None:
        return {"user_id": self.user_id, "agent_id": self.agent_id, "text": self.user_prompt,"llm_output": llm_output,"timestamp": datetime.now().isoformat()}