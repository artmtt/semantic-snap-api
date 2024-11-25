from typing import List
import psycopg2
from src.models.image import ImageData
from src.utils.embedding import generate_embeddings

# TODO: Change to real table and column names
def similarity_image_search(query_text: str, limit: int, db_conn: psycopg2.extensions.connection) -> List[ImageData]:
    cursor = db_conn.cursor()
    query_embedding = generate_embeddings(query_text)

    try:
        cursor.execute(
            """SELECT id, title, url, 1 - (embedding <=> %s) AS cos_similarity
            FROM images
            ORDER BY cos_similarity DESC
            LIMIT %s;
            """,
            (query_embedding, limit,)
        )

        # Yield instead of waiting?
        imgs = [ImageData(row[0], row[1], row[2]) for row in cursor.fetchall()]
        return imgs

    except Exception as e:
        print(f'Error in similarity search: {str(e)}')
        raise
    finally:
        cursor.close()


def get_image_by_id(id: int, db_conn: psycopg2.extensions.connection) -> ImageData:
    cursor = db_conn.cursor()

    try:
        cursor.execute(
            """SELECT id, title, url
            FROM images
            WHERE id = %s;
            """,
            (id,)
        )

        row = cursor.fetchall()
        return ImageData(id, row[1], row[2])

    except Exception as e:
        print(f'Error in image search by ID: {str(e)}')
        raise
    finally:
        cursor.close()


def get_random_images(limit: int, db_conn: psycopg2.extensions.connection) -> List[ImageData]:
    cursor = db_conn.cursor()

    try:
        # Get a 10% sample of the table
        cursor.execute(
            """SELECT id, title, url
            FROM images
            TAMBLESAMPLE SYSTEM(10)
            LIMIT %s;
            """,
            (limit,)
        )

        imgs = [ImageData(row[0], row[1], row[2]) for row in cursor.fetchall()]
        return imgs

    except Exception as e:
        print(f'Error in image search by ID: {str(e)}')
        raise
    finally:
        cursor.close()
