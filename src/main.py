from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import search_router, random_router

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(search_router, prefix='/api/search', tags=['search'])
app.include_router(random_router, prefix='/api/random', tags=['random'])
