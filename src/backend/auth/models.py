from pydantic import BaseModel, EmailStr, Field


class SignupModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=80)


class LoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class RefreshModel(BaseModel):
    refresh_token: str = Field(min_length=10)


class ForgotPasswordModel(BaseModel):
    email: EmailStr


class CompanyModel(BaseModel):
    company_name: str = Field(min_length=2, max_length=60)


class JoinCompanyModel(BaseModel):
    join_code: str = Field(min_length=4, max_length=16)
