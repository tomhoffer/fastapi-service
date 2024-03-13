from typing import Dict

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/json2xml")
async def json2xml(request: Request):
    return await request.body()


@app.post("/xml2json")
async def json2xml(request: Request):
    return await request.body()
