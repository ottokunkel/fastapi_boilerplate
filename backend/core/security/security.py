from passlib.context import CryptContext
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
JWT_CONFIG = {
    "secret_key": os.getenv("JWT_SECRET_KEY"),
    "algorithm": os.getenv("HASH_ALGORITHM"),
    "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
}

# Validate required settings
if not JWT_CONFIG["secret_key"]:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")
if not JWT_CONFIG["algorithm"]:
    raise ValueError("HASH_ALGORITHM environment variable is not set")

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#===============================================#
# Password hashing
#===============================================#
def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)



#===============================================#
# Token verification
#===============================================#
def verify_token(token: str) -> dict | None:
    """
    Verify a token
    
    Args:
        token (str): JWT token
    
    Returns:
        dict | None: Payload if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_CONFIG["secret_key"], algorithms=[JWT_CONFIG["algorithm"]])
        return payload
    except jwt.InvalidTokenError:
        return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token
    
    Args:
        data (dict): Data to encode in the token
        expires_delta (timedelta | None, optional): Expiration time for the token. Defaults to 15 minutes.
    
    Returns:
        str: JWT token
    """

    # Copy data
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Update token with expiration time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_CONFIG["secret_key"], algorithm=JWT_CONFIG["algorithm"])
    return encoded_jwt

if __name__ == "__main__":
    # print(create_access_token(data={"sub": "test@test.com"}))
    pass_hash = get_password_hash("test")
    print(pass_hash)
    print(verify_password("test", pass_hash))
    print(verify_password("test1", pass_hash))