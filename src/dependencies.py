from fastapi import Depends
from src.services.database import generate_db_conn
import psycopg2

def get_db_conn(db_conn: psycopg2.extensions.connection = Depends(generate_db_conn)):
    """
    Dependency to get the DB connection for FastAPI.
    """
    try:
        yield db_conn
    finally:
        db_conn.close()
