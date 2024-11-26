from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.models.image import ImageData, BasicImageData
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
        images = similarity_image_search(query_text, limit, db_conn)

        if len(images) == 0:
            return HTTPException(status_code=404, detail='No images were found')

        return images

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/id/{value}', response_model = BasicImageData)
async def search_image(value: int, db_conn = Depends(get_db_conn)):
    if not is_id_valid(value):
        raise HTTPException(status_code=400, detail='Parameter value is not valid')

    try:
        img_data = get_image_by_id(value, db_conn)

        if img_data is None:
            return HTTPException(status_code=404, detail='The image was not found')

        return {
            'title': img_data.title,
            'url': img_data.url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
