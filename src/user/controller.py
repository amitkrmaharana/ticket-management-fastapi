from src.user.dtos import UserSchema, UserResponseSchema
from src.user.models import UserModel
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime

password_hash = PasswordHash.recommended()

def get_hash_password(password: str):
    return password_hash.hash(password)

def registration(body: UserSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email Id already registered. Try with a different Email"
        )
    new_user = UserModel(
        username=body.email.split("@")[0],
        email=body.email,
        hash_password=get_hash_password(body.password),
        role=body.role,
        last_active=int(datetime.now().timestamp())
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user