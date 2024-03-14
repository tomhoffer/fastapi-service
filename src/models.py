from pydantic import BaseModel


class EmailRecord(BaseModel):
    text: str
