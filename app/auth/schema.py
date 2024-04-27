from pydantic import BaseModel, Field, conint
from typing import Optional



class SignUpSchema(BaseModel):
    email: str = Field(example="1")
    password: str = Field(example="1")
    full_name: str = Field(example="Abdula Mahachkambaev")

class LogInSchema(BaseModel):
    email: str = Field(example="1")
    password: str = Field(example="1")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None