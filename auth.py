from datetime import datetime, UTC, timedelta
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from config import settings
from database import get_db
from model import UserData

password_hash = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

def hash_password(password: str) -> str:
    '''Hash the password'''
    return password_hash.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    return password_hash.verify(plain_password, hash_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm
    )
    return encode_jwt

def verify_access_token(token: str) -> str:
    try:
        playload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=settings.algorithm,
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return playload.get("sub")

def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Annotated[Session, Depends(get_db)],
) -> UserData:
    '''Verify  token,then if user exit return it '''
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = db.execute(select(UserData).where(UserData.id == int(user_id)))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_role(*allowed_roles: str):
    """Restrict user accessibility"""
    def role_checker(
        current_user: Annotated[UserData, Depends(get_current_user)]
    ) -> UserData:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this module",
            )
        return current_user
    return role_checker