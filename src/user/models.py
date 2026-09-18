from sqlalchemy import Column, String, Integer, BigInteger, Enum
from src.utils.db import Base
from src.utils.enum import UserRole

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    last_active = Column(BigInteger)

    role = Column(
        Enum(UserRole, name="user_role"), 
        default=UserRole.USER
    )