import re
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional

STUDENT_EMAIL = re.compile(r"[0-9]{10}@student\.csn\.edu")
FACULTY_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@csn\.edu")
class UserRegister(BaseModel):
    first_name: str = Field(max_length=35)
    last_name: str = Field(max_length=35)
    email: EmailStr
    password: str = Field(max_length=10)
    @field_validator("email")
    @classmethod
    def check_student_email(cls, email: str) -> str:
        if not (STUDENT_EMAIL.fullmatch(email) or FACULTY_EMAIL.fullmatch(email)):
            raise ValueError("must be a CSN email address")
        return email

    @property
    def role(self) -> str:
        return "Student" if STUDENT_EMAIL.fullmatch(self.email) else "Faculty"
 

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(max_length=10)

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_name: str
    user_email: str
