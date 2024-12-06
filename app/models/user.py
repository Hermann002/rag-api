from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, unique=True, index=True)
    is_active = Column(Integer, default=False)

    otp = relationship("OneTimePasscode", back_populates="owner", uselist=False)

class OneTimePasscode(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey(User.id))
    owner = relationship(User, back_populates="otp")
