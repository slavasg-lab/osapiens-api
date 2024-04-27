from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.core.db.session import Base
from sqlalchemy.orm import relationship



class Pinpoint(Base):
    __tablename__ = "pinpoint"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    comment = Column(String)

    user = relationship("User", backref="pinpoints")

    class Config:
        orm_mode = True
