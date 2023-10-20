from src.database.core import Base
from sqlalchemy import Column, Integer, String


class JSONObject(Base):
    __tablename__ = "json_objects"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, unique=True)


class FileObject(Base):
    __tablename__ = "file_objects"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, unique=True)
    file_name = Column(String, unique=True)
    file_type = Column(String)
