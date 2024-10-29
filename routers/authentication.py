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
    user = (
        db.query(models.User)
        .filter(models.User.username == authentication.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username"
        )
    if not Hashing.verify(user.hashed_password, authentication.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password"
        )

    access_token = JWTtoken.create_access_token(
        data={"sub": user.username, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/home")
async def home(current_user: models.User = Depends(JWTtoken.get_current_user)):
    return {
        "message": f"Hello, {current_user.username}, you are successfully logged in!"
    }
