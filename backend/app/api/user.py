from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.crud.user import create_user, get_user
from app.models.user.schema import UserCreate
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from core.security.security import verify_token, verify_password, create_access_token
from core.database.connect import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#===============================================#
# Exceptions
#===============================================#
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

#===============================================#
# Pydantic models
#===============================================#
class Token(BaseModel):
    access_token: str
    token_type: str

#===============================================#
# Helper functions
#===============================================#
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Verify JWT token and return user
    
    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): JWT token

    Returns:
        User: User object
    """

    # Verify JWT token
    payload = verify_token(token)

    # If token is invalid, raise exception
    if payload is None:
        raise credentials_exception

    # Get user from database
    email: str = payload.get("sub")
    user = get_user(email)

    # If user does not exist, raise exception
    if user is None:
        raise credentials_exception
    
    # Return user
    return user

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user"""
    user = get_user(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#===============================================#
# Routes
#===============================================#
@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Login for access token"""

    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)

    # If user does not exist, raise exception
    if not user:
        raise invalid_credentials_exception

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")    

@router.post("/register", response_model=Token)
async def register_user_endpoint(user: UserCreate):
    """Create a new user"""
    try:
        create_user(user)

        access_token = create_access_token(
            data={"sub": user.email}
        )

        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
