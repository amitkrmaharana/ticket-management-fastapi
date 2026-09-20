from pydantic import BaseModel, EmailStr, field_validator
from src.utils.enum import UserRole
from fastapi.exceptions import HTTPException
from fastapi import status

class UserSchema(BaseModel):
    email : EmailStr
    password : str
    role : UserRole | None = UserRole.USER

    @field_validator("password")
    @classmethod
    def validate_password(cls, value : str):
        if len(value) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password length should be minimum 8 characters")
        if not any(char.isupper() for char in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Atleast 1 character should be upper case")
        if not any(char.islower() for char in value):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Atleast 1 character should be lower case")

        return value

class UserResponseSchema(BaseModel):
    username : str
    email : str
    role : UserRole

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponseSchema(BaseModel):
    token: str
    type: str | None = "Bearer"