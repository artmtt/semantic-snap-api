from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.image import ImageData
from src.dependencies import get_db_conn
from src.services.embedding_database import get_random_images
from src.utils.request_validations import is_limit_valid

router = APIRouter()


@router.get('/', response_model = List[ImageData])
async def search_images(limit: int = 1, db_conn = Depends(get_db_conn)):
    if not is_limit_valid(limit):
        raise HTTPException(status_code=400, detail='Parameter limit is not valid')
    
    try:
        return get_random_images(limit, db_conn)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
