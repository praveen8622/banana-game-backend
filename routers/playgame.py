from fastapi import APIRouter, HTTPException, Depends
import httpx
import models
from JWTtoken import get_current_user


router = APIRouter(prefix="/banana_api", tags=["BananaGame"])


@router.get("/")
async def get_data(current_user: models.User = Depends(get_current_user)):
    url = "https://marcconrad.com/uob/banana/api.php?out=json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching data"
        )
    return response.json()
