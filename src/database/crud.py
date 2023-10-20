import json
import os
import shutil

from sqlalchemy import and_
from sqlalchemy.orm import Session
from typing import Union
from fastapi import UploadFile

from src.database.models import Object


def create_json_object(db: Session, data: dict) -> Object:
    object = Object(type="json", data=json.dumps(data))
    db.add(object)
    db.commit()
    db.refresh(object)
    return object


def create_file_object(db: Session, file: UploadFile) -> Object:
    directory = os.path.join(os.getcwd(), "files")
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(os.path.join(directory, file.filename), "wb+") as f:
            shutil.copyfileobj(file.file, f)
    finally:
        file.file.close()

    object = Object(type="file", data=file.filename)
    db.add(object)
    db.commit()
    db.refresh(object)
    return object


def get_object(db: Session, id: int | str) -> Union[Object, None]:
    if isinstance(id, int) or id.isdigit():
        return db.query(Object).filter(Object.id == id).first()
    elif isinstance(id, str):
        return (
            db.query(Object)
            .filter(and_(Object.data == id, Object.type == "file"))
            .first()
        )


def get_all_objects(db: Session) -> list[Object]:
    return db.query(Object).all()


def delete_object(db: Session, id: int | str) -> None:
    if isinstance(id, int):
        db.query(Object).filter(Object.id == id).delete()
    elif isinstance(id, str):
        (
            db.query(Object)
            .filter(and_(Object.data == id, Object.type == "file"))
            .delete()
        )
    db.commit()
