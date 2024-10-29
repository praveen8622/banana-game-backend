from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, models
from hashing import Hashing

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username"
        )
    if not Hashing.verify(user.hashed_password, password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password"
        )

    return {"message": f"Welcome, {user.username}!"}


@router.get("/home")
async def home():
    return {"message": "Hello, you are successfully connected to the home route!"}
