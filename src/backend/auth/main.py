import os
from supabase import create_client
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,EmailStr,Field


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)




class RegistrationModel(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8, max_length=50)

class CompanyModel(BaseModel):
    company_name : str =Field(min_length=2, max_length=30)


app=FastAPI()



@app.post("/signup")
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/login")
def login_user(request: RegistrationModel):
    email = request.email
    password = request.password
    try:
        user_record = supabase.table("User").select("*").eq("email", request.email).execute()
        if not user_record.data:
            #Supabase auth
            user = supabase.auth.sign_in_with_password({
                "email": request.email, 
                "password": request.password
            })


        return {"message": f"User logged in successfully .check {email} for verification"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/company_registration")
def add_company(request: CompanyModel):
    company = request.company_name
    try:
    # Create a company
        insert_1 = supabase.table("Company").insert({'company': company}).execute()
        return {"message": f"Company registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class PasswordResetModel(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=50)

@app.patch("/reset_password")
def update_password_by_email(request: PasswordResetModel):
    email = request.email
    new_password = request.new_password
    try:
        insert_1 = supabase.table("User").eq({'email': email}).update({'password': new_password}).execute()
        return {"message": f"Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


