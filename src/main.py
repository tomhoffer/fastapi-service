from fastapi import FastAPI, Request, HTTPException
from src.exceptions import JsonToXmlConversionException, XmlToJsonConversionException
from src.json2xml import JsonToXmlParser
from src.xml2json import XmlToJsonParser

app = FastAPI()
json_to_xml_parser = JsonToXmlParser()
xml_to_json_parser = XmlToJsonParser()


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
