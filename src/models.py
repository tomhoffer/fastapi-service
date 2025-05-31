from pydantic import BaseModel


class EmailRecord(BaseModel):
    text: str


class RecordOutput(BaseModel):
    id: int
    email: str
    text: str
