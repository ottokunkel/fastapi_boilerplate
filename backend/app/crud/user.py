from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserUpdate
from core.security import get_password_hash
from core.database.connect import init_db
from datetime import timedelta


def create_user(user: UserCreate, db: Session) -> User:
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        refresh_token=None
    )
    db.add(db_user)
    return db_user
    
def get_user(email: str, db: Session) -> Optional[User]:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()
    

def update_user(email: str, user_update: UserUpdate, db: Session) -> Optional[User]:
    """Update a user's information"""
    db_user = db.query(User).filter(User.email == email).first()
    
    if not db_user:
        return None

    # updates email
    if user_update.email:
        # Check if new email already exists for another user
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != db_user.id
        ).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        db_user.email = user_update.email

    # updates password
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)

    # updates refresh token
    if user_update.refresh_token:
        db_user.refresh_token = user_update.refresh_token

    return db_user
    
def delete_user(email: str, db: Session) -> Optional[User]:
    """Delete a user"""
    db_user = db.query(User).filter(User.email == email).first()
    
    if not db_user:
        return None

    db.delete(db_user)
    return db_user



if __name__ == "__main__":
    from core.database.connect import SessionLocal
    
    db = SessionLocal()
    try:
        init_db()
        create_user(UserCreate(email="test@test.com", password="test"), db)
        db.commit()
    finally:
        db.close()