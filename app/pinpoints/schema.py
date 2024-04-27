from pydantic import BaseModel, Field, conint
from typing import Optional



class CreatePinpointPayloadSchema(BaseModel):
    latitude: float
    longitude: float
    comment: str

class LogInSchema(BaseModel):
    email: str = Field(example="1")
    password: str = Field(example="1")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None