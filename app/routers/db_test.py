from fastapi import APIRouter
from data.db_use import db

router = APIRouter(prefix="/test",tags=["DB Test"])

#api util test
@router.get("/health", status_code=201)
def health():
    return {"status": "ok"}

@router.get("/db")
def test_db_connection():
    ...