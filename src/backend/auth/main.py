from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from postgrest.exceptions import APIError
from supabase_auth.errors import AuthApiError

from src.backend.auth.models import (
    CompanyModel,
    ForgotPasswordModel,
    JoinCompanyModel,
    LoginModel,
    RefreshModel,
    SignupModel,
)
from src.backend.config import Config
from src.backend.dependencies import (
    CurrentUser,
    Membership,
    current_user,
    db_error,
    my_membership,
    new_client,
    owner_member,
)

auth_router = APIRouter()


def _session_payload(session) -> dict:
    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "expires_in": session.expires_in,
        "token_type": "bearer",
    }


# ------------------------------------------------------------------ identity
# Passwords live only in Supabase Auth. There is no public."User" table any more.

@auth_router.post("/signup", status_code=201)
def signup(request: SignupModel):
    try:
        new_client().auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
                # the on_auth_user_created trigger copies full_name into public.profiles
                "options": {"data": {"full_name": request.full_name.strip()}},
            }
        )
    except AuthApiError as e:
        raise HTTPException(400, e.message)
    return {"message": "Account created. Confirm your e-mail if asked, then log in."}


@auth_router.post("/login")
def login(request: LoginModel):
    try:
        res = new_client().auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
    except AuthApiError:
        raise HTTPException(401, "Invalid credentials, or the e-mail is not confirmed yet.")
    if not res.session:
        raise HTTPException(401, "Login failed. Please confirm your e-mail first.")
    return _session_payload(res.session)


@auth_router.post("/refresh")
def refresh(request: RefreshModel):
    try:
        res = new_client().auth.refresh_session(request.refresh_token)
    except AuthApiError:
        raise HTTPException(401, "Session expired. Please log in again.")
    if not res.session:
        raise HTTPException(401, "Session expired. Please log in again.")
    return _session_payload(res.session)


@auth_router.post("/password/forgot")
def forgot_password(request: ForgotPasswordModel):
    """Sends Supabase's reset e-mail. The old /reset_password endpoint let anyone
    change anyone's password knowing only the e-mail address; it is gone."""
    options = {"redirect_to": Config.PASSWORD_RESET_REDIRECT} if Config.PASSWORD_RESET_REDIRECT else None
    try:
        new_client().auth.reset_password_for_email(request.email, options)
    except Exception:
        pass  # never reveal whether the address has an account
    return {"message": "If that address has an account, a reset link was sent."}


@auth_router.get("/me")
def me(user: CurrentUser = Depends(current_user)):
    profile = user.db.table("profiles").select("full_name").eq("id", user.id).limit(1).execute().data
    out = {
        "user_id": user.id,
        "full_name": profile[0]["full_name"] if profile else None,
        "membership": None,
    }
    row = my_membership(user)
    if row:
        membership = {"company_id": row["company_id"], "role": row["role"], "status": row["status"]}
        if row["status"] == "active":  # RLS hides the company row from pending members
            company = (
                user.db.table("companies").select("name,join_code")
                .eq("id", row["company_id"]).limit(1).execute().data
            )
            if company:
                membership["company_name"] = company[0]["name"]
                if row["role"] == "owner":
                    membership["join_code"] = company[0]["join_code"]
        out["membership"] = membership
    return out


# ------------------------------------------------------------------ company

@auth_router.post("/company", status_code=201)
def create_company(request: CompanyModel, user: CurrentUser = Depends(current_user)):
    """Owner flow: becomes the company's owner (the RPC refuses users who already belong to one)."""
    try:
        res = user.db.rpc("create_company", {"p_name": request.company_name}).execute()
    except APIError as e:
        raise db_error(e)
    return {"company_id": res.data, "role": "owner", "status": "active"}


@auth_router.post("/company/join", status_code=202)
def join_company(request: JoinCompanyModel, user: CurrentUser = Depends(current_user)):
    """Worker flow: needs the company's join code, then waits for the owner's approval."""
    try:
        res = user.db.rpc("join_company", {"p_code": request.join_code}).execute()
    except APIError as e:
        raise db_error(e)
    return {"company_id": res.data, "role": "member", "status": "pending"}


@auth_router.get("/company/members")
def list_members(m: Membership = Depends(owner_member)):
    members = (
        m.user.db.table("company_members").select("user_id,role,status,created_at")
        .eq("company_id", m.company_id).order("created_at").execute().data
    )
    ids = [row["user_id"] for row in members]
    names = {}
    if ids:
        profiles = m.user.db.table("profiles").select("id,full_name").in_("id", ids).execute().data
        names = {p["id"]: p["full_name"] for p in profiles}
    return [{**row, "full_name": names.get(row["user_id"])} for row in members]


@auth_router.post("/company/members/{user_id}/approve")
def approve_member(user_id: UUID, m: Membership = Depends(owner_member)):
    try:
        rows = (
            m.user.db.table("company_members").update({"status": "active"})
            .eq("company_id", m.company_id).eq("user_id", str(user_id)).eq("status", "pending")
            .execute().data
        )
    except APIError as e:
        raise db_error(e)
    if not rows:
        raise HTTPException(404, "No pending request from that user.")
    return {"user_id": str(user_id), "status": "active"}


@auth_router.delete("/company/members/{user_id}")
def remove_member(user_id: UUID, m: Membership = Depends(owner_member)):
    """Owner removes a worker or rejects a join request."""
    try:
        rows = (
            m.user.db.table("company_members").delete()
            .eq("company_id", m.company_id).eq("user_id", str(user_id)).eq("role", "member")
            .execute().data
        )
    except APIError as e:
        raise db_error(e)
    if not rows:
        raise HTTPException(404, "No such member.")
    return {"removed": str(user_id)}


@auth_router.post("/company/join-code/rotate")
def rotate_join_code(m: Membership = Depends(owner_member)):
    try:
        res = m.user.db.rpc("rotate_join_code").execute()
    except APIError as e:
        raise db_error(e)
    return {"join_code": res.data}


@auth_router.delete("/company/leave")
def leave_company(user: CurrentUser = Depends(current_user)):
    """A worker (pending or active) leaves. Owners cannot leave: the RLS policy only deletes role='member' rows."""
    try:
        rows = (
            user.db.table("company_members").delete()
            .eq("user_id", user.id).eq("role", "member").execute().data
        )
    except APIError as e:
        raise db_error(e)
    if not rows:
        raise HTTPException(404, "You are not a member of any company (owners cannot leave).")
    return {"left": True}
