"""Auth + tenant dependencies shared by every router.

Every database call a request makes goes through a Supabase client that carries
THAT user's JWT, so Postgres row level security (see 001_multitenant_schema.sql)
is what actually enforces tenant isolation. The checks below only turn RLS
outcomes into clean HTTP errors.
"""
import logging
from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from postgrest.exceptions import APIError
from supabase import Client, create_client

from src.backend.config import Config

logger = logging.getLogger(__name__)
bearer = HTTPBearer()


def new_client() -> Client:
    """A fresh client for every use.

    Never share one module-level client: supabase-py stores the session of the last
    sign-in on the client, so a shared client would run later requests as that user.
    """
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)


@dataclass
class CurrentUser:
    id: str
    db: Client  # PostgREST calls made with the user's JWT -> RLS applies


@dataclass
class Membership:
    user: CurrentUser
    company_id: str
    role: str  # 'owner' | 'member'


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> CurrentUser:
    token = creds.credentials
    client = new_client()
    try:
        res = client.auth.get_user(token)
        user = res.user if res else None
    except Exception:
        user = None
    if user is None:
        raise HTTPException(401, "Invalid or expired access token. Please log in.")
    client.postgrest.auth(token)
    return CurrentUser(id=str(user.id), db=client)


def my_membership(user: CurrentUser) -> dict | None:
    rows = (
        user.db.table("company_members")
        .select("company_id,role,status")
        .eq("user_id", user.id)
        .limit(1)
        .execute()
        .data
    )
    return rows[0] if rows else None


def active_member(user: CurrentUser = Depends(current_user)) -> Membership:
    row = my_membership(user)
    if not row:
        raise HTTPException(403, "Create a company or join one with a join code first.")
    if row["status"] != "active":
        raise HTTPException(403, "Your request to join is waiting for the owner's approval.")
    return Membership(user=user, company_id=row["company_id"], role=row["role"])


def owner_member(m: Membership = Depends(active_member)) -> Membership:
    if m.role != "owner":
        raise HTTPException(403, "Only the company owner can do this.")
    return m


def db_error(e: APIError) -> HTTPException:
    """Translate a Postgres/PostgREST error into an HTTP error without leaking internals."""
    code = getattr(e, "code", None)
    if code == "P0001":  # RAISE EXCEPTION inside our RPCs: message is written for the user
        return HTTPException(400, getattr(e, "message", "Request refused."))
    if code == "23505":
        return HTTPException(409, "That already exists.")
    if code in ("42501", "PGRST301"):
        return HTTPException(403, "Not allowed.")
    if code == "23503":
        return HTTPException(400, "A referenced record does not exist.")
    logger.error("database error: %s", e)
    return HTTPException(400, "Database error.")
