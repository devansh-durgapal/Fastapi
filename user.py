from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from config import settings
from auth import (
    hash_password,
    verify_password,
    oauth2_schema,
    create_access_token,
    verify_access_token,
    get_current_user,
    require_role,
)
from schema import UserCreate, UserBase, UserPrivate, UserPublic, Token
from database import Base, engine, get_db
from model import UserData

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post(
    "/create-user", response_model=UserPrivate, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(UserData).where(user.username.lower() == func.lower(UserData.username))
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exit"
        )
    new_user = UserData(
        username=user.username,
        name=user.name,
        email=user.email.lower(),
        password_hash=hash_password(user.password),
        role=user.role,  # Added: persist the role passed at signup
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(
        select(UserData).where(
            func.lower(UserData.username) == form_data.username.lower()
        )
    )
    existing_user = result.scalars().first()
    if not existing_user or not verify_password(
        form_data.password, existing_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(existing_user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/profile", response_model=UserPrivate)
def get_profile(current_user: Annotated[UserData, Depends(get_current_user)]):
    """Authenticated user can view their profile"""
    return current_user


@app.get("/admin/dashboard")
def admin_dashboard(current_user: Annotated[UserData, Depends(require_role("admin"))]):
    """Authorised to admin only"""
    return {"message": f"Welcome admin {current_user.username}"}


@app.get("/reports")
def reports_module(
    current_user: Annotated[UserData, Depends(require_role("admin", "user"))],
):
    """Authorised to user and admin"""
    return {"message": f"Reports module accessed by {current_user.username}"}
