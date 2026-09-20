from src.user.dtos import UserSchema, UserLoginResponseSchema
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.enum import UserRole
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt

password_hash = PasswordHash.recommended()

def get_hash_password(password: str):
    return password_hash.hash(password)

def verify_password(body: OAuth2PasswordRequestForm, user: UserModel):
    return password_hash.verify(body.password, user.hash_password)

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

def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email id not registered")
    if not verify_password(form_data, user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    exp_time = datetime.now() + timedelta(seconds=settings.EXP_TIME)
    token = jwt.encode(
        {
            "id": user.id,
            "exp": exp_time.timestamp()
        },
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return UserLoginResponseSchema(
        token=token
    )

def get_users(current_user: UserModel, db: Session):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized for this data"
        )
    users = db.query(UserModel).all()
    return users