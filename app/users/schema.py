from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(example="1")
    email: str = Field(example="1")
    password: str = Field(example="1")