from fastapi import  status, HTTPException, Depends, APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
router= APIRouter(
    
    prefix="/tableau",
    tags=["Tableau"]
)

@router.get("/")
async def root():
    return {"message": "Hello World"}