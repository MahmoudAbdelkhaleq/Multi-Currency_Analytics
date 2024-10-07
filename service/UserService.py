from sqlalchemy.orm import Session

import repositories.UserRepository as UserRepository
from schema.UserSchema import UserCreate, UserUpdate
from models.User import User

def get_user(db: Session, user_id: int):
    return UserRepository.get_user(db, user_id)

def get_user_by_email(db: Session, email: str):
    return UserRepository.get_user_by_email(db, email)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return UserRepository.get_users(db, skip, limit)

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    return UserRepository.create_user(db, db_user)

def update_user(db: Session, user_id: int, user: UserUpdate):
    if user.password:
        fake_hashed_password = user.password + "notreallyhashed"
        user.password = fake_hashed_password
    return UserRepository.update_user(db, user_id, user)

def delete_user(db: Session, user_id: int):
    return UserRepository.delete_user(db, user_id)