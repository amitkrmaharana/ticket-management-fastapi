from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema, UserLoginResponseSchema
from src.user import controller
from src.user.models import UserModel
from src.auth.helper import get_current_user

user_routes = APIRouter(prefix="/user")

@user_routes.post("/registration", response_model=UserResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def registration(body: UserSchema, db : Session = Depends(get_db)):
    return controller.registration(body, db)

@user_routes.post("/login", response_model=UserLoginResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_routes.get("/get_users", response_model=list[UserResponseSchema], status_code=status.HTTP_200_OK)
def get_users(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.get_users(current_user, db)