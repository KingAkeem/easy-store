import json

from sqlalchemy.orm import Session
from typing import Union

from src.database.models import Object


def create_object(db: Session, data: dict) -> Object:
    object = Object(data=json.dumps(data))
    db.add(object)
    db.commit()
    db.refresh(object)
    return object


def get_object(db: Session, id: int) -> Union[Object, None]:
    return db.query(Object).filter(Object.id == id).first()


def get_all_objects(db: Session) -> list[Object]:
    return db.query(Object).all()


def delete_object(db: Session, id: int) -> None:
    db.query(Object).filter(Object.id == id).delete()
    db.commit()
