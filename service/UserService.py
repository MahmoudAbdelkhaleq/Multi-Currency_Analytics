from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session

from typing import Annotated
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

import repositories.UserRepository as UserRepository
from schema.UserSchema import UserCreate, UserUpdate
from models.User import User
from models.Token import Token, TokenData



from utils.hashing import verify_password, get_password_hash

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, user_id: int) -> User:
    return UserRepository.get_user(db, user_id)

def get_user_by_email(db: Session, email: str):
    return UserRepository.get_user_by_email(db, email)

def get_user_by_username(db: Session, username: str):
    return UserRepository.get_user_by_username(db, username)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return UserRepository.get_users(db, skip, limit)

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = get_password_hash(user.password) 
    db_user = User(username = user.username, email=user.email, hashed_password=fake_hashed_password)
    return UserRepository.create_user(db, db_user)

def update_user(db: Session, user_id: int, user: UserUpdate):
    if user.password:
        fake_hashed_password = get_password_hash(user.password)
        user.password = fake_hashed_password
    return UserRepository.update_user(db, user_id, user)

def delete_user(db: Session, user_id: int):
    return UserRepository.delete_user(db, user_id)

def login_user(db: Session, email: str, password: str):
    return UserRepository.login_user(db, email, password)


def fake_decode_token(db: Session, usernmae_token:str):
    return UserRepository.get_user_by_username(db, usernmae_token)


async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt