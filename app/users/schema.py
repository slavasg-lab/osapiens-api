from pydantic import BaseModel, Field, conint
from typing import Optional



class UserSchema(BaseModel):
    email: str = Field(example="1@gmail.com")
    full_name: str = Field(example="Abdula Mahachkambaev")
