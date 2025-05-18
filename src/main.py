import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse
from starlette.staticfiles import StaticFiles
from src.config import Config
from src.db import RecordsDbRepository
from src.exceptions import DbUnableToInsertRowException,
from src.models import EmailRecord


logger = logging.getLogger(__name__)
records_db = RecordsDbRepository()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await records_db.init_pool(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
    )
    yield
    await records_db.close_pool()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static", html=True), name="static")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Use 400 Bad request status code and replace the default Pydantic message
    # as it exposes the Pydantic version used (security)
    return PlainTextResponse(
        "Invalid payload provided! Please check the API documentation.", status_code=400
    )


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    logger.error(repr(exc))
    return await http_exception_handler(request, exc)


@app.get("/user")
async def get_record_by_email(email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")

    record = await records_db.get_record_by_email(email)
    if not record:
        raise HTTPException(
            status_code=404, detail=f"Record for email {email} was not found! "
        )

    return record


@app.post("/user")
async def post_record_by_email(payload: EmailRecord, email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")
    try:
        await records_db.create_record(email, payload.text)
    except DbUnableToInsertRowException as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.delete("/user")
async def delete_record_by_email(email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")
    await records_db.delete_record(email)


@app.get("/users")
async def get_multiple_users(limit: int | None = 10, offset: int | None = 0):
    if limit < 0 or offset < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid limit or offset provided! Limit: {limit} Offset: {offset}",
        )
    return await records_db.get_multiple_records(limit, offset)
