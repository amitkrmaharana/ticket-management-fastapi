from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.dtos import UserSchema, UserResponseSchema
from src.user import controller

user_routes = APIRouter(prefix="/user")

@user_routes.post("/registration", response_model=UserResponseSchema, status_code=status.HTTP_202_ACCEPTED)
def registration(body: UserSchema, db : Session = Depends(get_db)):
    return controller.registration(body, db)