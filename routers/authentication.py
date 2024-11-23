from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, models, JWTtoken
from hashing import Hashing

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    authentication: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    Authenticates a user by verifying username and password.
    - Parameters:
      - authentication: OAuth2PasswordRequestForm containing username and password
      - db: Database session
    - Returns: JWT access token upon successful authentication
    """
    # Query user in the database by username
    user = (
        db.query(models.User)
        .filter(models.User.username == authentication.username)
        .first()
    )

    # Raise error if user not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username"
        )

    # Verify password
    if not Hashing.verify(user.hashed_password, authentication.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password"
        )

    # Generate JWT access token
    access_token = JWTtoken.create_access_token(
        data={"sub": user.username, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/home")
async def home(current_user: models.User = Depends(JWTtoken.get_current_user)):
    """
    Home endpoint for authenticated users.
    - Parameters:
      - current_user: Authenticated user (injected by JWT token)
    - Returns: Personalized welcome message for the authenticated user
    """
    return {
        "message": f"Hello, {current_user.username}, you are successfully logged in!"
    }
