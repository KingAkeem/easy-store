from src.database.core import Base
from sqlalchemy import Column, Integer, String


class Object(Base):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, unique=True)
    type = Column(String)
