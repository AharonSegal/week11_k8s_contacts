from fastapi import APIRouter
from mysql.connector import Error as MySQLError
from data.db_use import get_connection

router = APIRouter(prefix="/test",tags=["DB Test"])

#api util test
@router.get("/health", status_code=201)
def health():
    return {"status": "ok"}

@router.get("/db")
def test_db_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "status": "ok",
            "db_result": result[0] if result else None
        }

    except MySQLError as e:
        return {
            "status": "error",
            "error": str(e)
        }
