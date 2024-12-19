from sqlalchemy import Column, Integer, String, ForeignKey, Date
from app.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=False)

    otp = relationship("OneTimePasscode", back_populates="owner", uselist=False)
    api_key = relationship("ApiKey", back_populates="owner", uselist=False)

class OneTimePasscode(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey(User.id))
    owner = relationship(User, back_populates="otp")

class ApiKey(Base):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, nullable=False, unique=True, index=True)
    create_at = Column(Date, default=datetime.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(User, back_populates="api_key")