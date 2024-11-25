import os
import psycopg2

# Future: Implement DB connection pool?

def generate_db_conn():
    try:
        db_conn = psycopg2.connect(
            user=os.getenv('EMBEDDING_DB_USER'),
            password=os.getenv('EMBEDDING_DB_PASSWORD'),
            host=os.getenv('EMBEDDING_DB_HOST'),
            port=os.getenv('EMBEDDING_DB_PORT'),  # Port exposed in docker-compose.yml
            database=os.getenv('EMBEDDING_DB_NAME')
        )
        return db_conn
    except Exception as e:
        print(f'Error connecting to the DB: {str(e)}')
        raise
