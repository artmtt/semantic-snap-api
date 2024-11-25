from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.image import ImageData
from src.dependencies import get_db_conn
from src.services.embedding_database import similarity_image_search, get_image_by_id
from src.utils.request_validations import is_query_text_valid, is_limit_valid, is_id_valid

router = APIRouter()


@router.get('/', response_model = List[ImageData])
async def search_images(query_text: str, limit: int = 1, db_conn = Depends(get_db_conn)):
    if not is_query_text_valid(query_text):
        raise HTTPException(status_code=400, detail='Parameter query_text is not valid')
    
    if not is_limit_valid(limit):
        raise HTTPException(status_code=400, detail='Parameter limit is not valid')

    try:
        return similarity_image_search(query_text, limit, db_conn)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/id/{value}', response_model = ImageData)
async def search_image(value: int, db_conn = Depends(get_db_conn)):
    if not is_id_valid(value):
        raise HTTPException(status_code=400, detail='Parameter value is not valid')

    try:
        img_data = get_image_by_id(value, db_conn)
        return {
            'title': img_data.title,
            'url': img_data.url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
