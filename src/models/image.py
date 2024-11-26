from pydantic import BaseModel

class ImageData(BaseModel):
    id: int
    title: str
    url: str

class BasicImageData(BaseModel):
    title: str
    url: str
