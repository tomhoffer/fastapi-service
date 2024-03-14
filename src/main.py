from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse
from src.db import RecordsDbRepository
from src.exceptions import JsonToXmlConversionException, XmlToJsonConversionException
from src.json2xml import JsonToXmlParser
from src.models import EmailRecord
from src.xml2json import XmlToJsonParser

app = FastAPI()
json_to_xml_parser = JsonToXmlParser()
xml_to_json_parser = XmlToJsonParser()

records_db = RecordsDbRepository(dbname="pm_assignment", user="PM_user", password="PM_password",
                                 host="localhost")  # TODO load configuration from env vars


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Use 400 Bad request status code and replace the default Pydantic message
    # as it exposes the Pydantic version used (security)
    return PlainTextResponse("Invalid payload provided! Please check the API documentation.", status_code=400)


@app.post("/json2xml")
async def json2xml(request: Request):
    body_raw = await request.body()
    try:
        return json_to_xml_parser.convert_to_xml(body_raw.decode("utf-8"))
    except JsonToXmlConversionException as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.post("/xml2json")
async def xml2json(request: Request):
    body_raw = await request.body()
    try:
        return xml_to_json_parser.convert_xml_to_json(body_raw.decode("utf-8"))
    except XmlToJsonConversionException as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.get("/user")
async def get_record_by_email(email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")

    record = records_db.get_record_by_email(email)

    if not record:
        raise HTTPException(status_code=404, detail="Record for given email was not found")

    return record


@app.post("/user")
async def post_record_by_email(payload: EmailRecord, email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")
    records_db.create_record(email, payload.text)


@app.delete("/user")
async def delete_record_by_email(email: str | None = None):
    if not email:
        raise HTTPException(status_code=400, detail="No email provided")
    records_db.delete_record(email)


@app.get("/users")
async def get_multiple_users(limit: int | None = 10, offset: int | None = 0):
    if limit < 0 or offset < 0:
        raise HTTPException(status_code=400, detail="Invalid limit or offset provided!")
    return records_db.get_multiple_records(limit, offset)
