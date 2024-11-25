from pydantic import BaseModel

class ImageData(BaseModel):
    id: int
    title: str
    url: str
