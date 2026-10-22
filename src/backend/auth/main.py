import os
from supabase import create_client
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI,HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.backend.auth.models import RegistrationModel, CompanyModel, PasswordResetModel



security = HTTPBearer()

def require_authenticated_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            raise HTTPException(
                status_code=401,
                detail="You must register or log in first"
            )

        return response.user.id

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token. Please log in."
        )

auth_router=APIRouter()

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)



@auth_router.post("/signup")
def Create_user(request: RegistrationModel):
    email = request.email
    password = request.password

    try:
        # Check if the user already exists
        existing = supabase.table("User").select("*").eq("email", request.email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="User already exists")
    # Create a new user in Supabase
        user = supabase.auth.sign_up({"email": email, "password": password})
        insert_1 = supabase.table("User").insert({'email': email, 'password': password}).execute()


        return {"message": f"User created successfully .check {email} for verification"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@auth_router.post("/login")
def login_user(request: RegistrationModel):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        if not response.session:
            raise HTTPException(
                status_code=401,
                detail="Login failed. Please verify your email if required."
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials, unverified email, or login failed."
        )




@auth_router.post("/company_registration")
def add_company(
    request: CompanyModel,
    user_id: str = Depends(require_authenticated_user)
):
    try:
        result = supabase.table("Company").insert({
            "name": request.company_name,
            "user_id": user_id
        }).execute()

        return {
            "message": "Company registered successfully",
            "company": result.data[0]
        }

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@auth_router.patch("/reset_password")
def update_password_by_email(request: PasswordResetModel):
    email = request.email
    new_password = request.new_password
    try:
        insert_1 = supabase.table("User").eq({'email': email}).update({'password': new_password}).execute()
        return {"message": f"Password reset successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


