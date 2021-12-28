from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .ovid_as_a_service.main import OvidAsAService
from typing import Optional

app = FastAPI()
ovid = OvidAsAService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# text query endpoints
@app.get("/v1/full_text")
def get_text(query: str):
    return JSONResponse(ovid.query_text(query))


# chapter query endpoints
@app.get("/v1/chapter")
def get_text(query: str):
    return JSONResponse(ovid.query_chapter(query))


# book query endpoints
@app.get("/v1/book/{book_num}")
def get_book(book_num: int, chapter: Optional[int] = None, query: Optional[str] = None):
    return JSONResponse(ovid.query_book(book_num, chapter, query))


# random endpoints
@app.get("/v1/random/{resource}")
def get_random(resource: str):
    if resource == 'book':
        return JSONResponse(ovid.query_random_book())
    elif resource == 'line':
        return JSONResponse(ovid.query_random_line())
    elif resource =='chapter':
        return JSONResponse(ovid.query_random_chapter())


# get credits
@app.get("/v1/credits")
def get_credits():
    return JSONResponse(ovid.return_credits())

