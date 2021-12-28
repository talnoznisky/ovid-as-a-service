from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .ovid_as_a_service.main import OvidAsAService

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
@app.get("/v1/text")
def get_text(query: str):
    return JSONResponse(ovid.query_text(query))

@app.get("/v1/text/random")
def get_random_text():
    return JSONResponse(ovid.query_random_line())

# chapter query endpoints
@app.get("/v1/chapter")
def get_text(query: str):
    return JSONResponse(ovid.query_chapter(query))

@app.get("v1/chapter/random")
def get_random_chapter():
    return JSONResponse(ovid.query_random_chapter())

# book query endpoints
@app.get("/v1/book")
def get_book(query: int):
    return JSONResponse(ovid.query_book(query))

@app.get("/v1/book/random")
def get_book():
    return JSONResponse(ovid.query_random_book())

# get credits
@app.get("/v1/credits")
def get_credits():
    return JSONResponse(ovid.return_credits())

