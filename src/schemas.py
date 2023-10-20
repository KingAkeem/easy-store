from pydantic import BaseModel


class JSONObject(BaseModel):
    id: int
    data: dict | str


class FileObject(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_path: str
