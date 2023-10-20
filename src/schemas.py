from pydantic import BaseModel


class StrObject(BaseModel):
    id: int
    type: str
    data: str


class JSONObject(BaseModel):
    id: int
    data: dict
