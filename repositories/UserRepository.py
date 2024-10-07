from sqlalchemy.orm import Session

from models.User import User
from schema.UserSchema import UserUpdate

from database.database import SessionLocal, get_db, FastAPI
from fastapi import Depends


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, db_user: User):
    # Hashing the password to be done
    db.add(db_user)
    db.commit()
    # we refresh the database so that the created instance would contain the generated value of the id
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    for field, value in user.__dict__.items():
        if value is not None:
            setattr(db_user, field, value)  # Update the invoice field with the new value
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user