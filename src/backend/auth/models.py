from pydantic import BaseModel,EmailStr,Field


class RegistrationModel(BaseModel):
    email: EmailStr 
    password: str = Field(min_length=8, max_length=50)
class CompanyModel(BaseModel):
    company_name : str =Field(min_length=2, max_length=30)
class PasswordResetModel(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=50)