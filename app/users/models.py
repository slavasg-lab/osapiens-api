from sqlalchemy import Column, Integer, String
from app.core.db.session import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    full_name = Column(String, index=True)

    class Config:
        orm_mode = True
