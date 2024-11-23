from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import database, schemas, models
from hashing import Hashing

router = APIRouter(prefix="/users", tags=["Users"])
get_db = database.get_db


@router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user by creating a user record with hashed password.
    - Parameters:
      - user: UserCreate schema with username, email, full name, and password
      - db: Database session
    - Returns: New user record
    """
    # Hash the password
    hashed_password = Hashing.bcrypt(user.password)

    # Create and add new user record
    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """
    Fetches user details by user ID.
    - Parameters:
      - id: User ID
      - db: Database session
    - Returns: User record if found
    - Raises: HTTPException if user ID not found
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")

    return user
