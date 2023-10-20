from pydantic import BaseModel

class JSONObject(BaseModel):
    id: int
    data: dict

class FileObject(BaseModel):
    id: int
    file_name: str
