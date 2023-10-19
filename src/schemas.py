from pydantic import BaseModel


class StrObject(BaseModel):
    id: int
    data: str


class JSONObject(BaseModel):
    id: int
    data: dict
