from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import database
import models
from sqlalchemy.orm import Session

# JWT secret key and algorithm configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    """
    Creates a JWT access token.
    - Parameters: data (dict)
    - Returns: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """
    Retrieves the current user from the token.
    - Parameters: token, db session
    - Returns: User object if token is valid
    - Raises: HTTPException if validation fails
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")

        if username is None or id is None:
            raise get_user_exception()

        user = db.query(models.User).filter(models.User.id == id).first()
        if user is None:
            raise get_user_exception()

        return user
    except JWTError:
        raise get_user_exception()


def get_user_exception():
    """
    Helper function for generating user validation exception.
    - Returns: HTTPException for user validation error
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
