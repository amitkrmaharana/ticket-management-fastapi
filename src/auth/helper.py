from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.settings import settings
from src.user.models import UserModel
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM
        )
        user_id = payload.get("id")
        if not user_id:
            raise credential_exception
    except InvalidTokenError:
        raise credential_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise credential_exception

    return user