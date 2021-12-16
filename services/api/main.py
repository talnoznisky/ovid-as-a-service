from fastapi import FastAPI
from .ovid_as_a_service.main import OvidAsAService

app = FastAPI()
ovid = OvidAsAService()


@app.post("/v1/lines")
def get_lines(query: str):
    return ovid.query_text(query)


@app.post("/v1/books")
def get_book(query: int):
    return ovid.query_book(query)
