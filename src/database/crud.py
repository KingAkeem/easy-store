import json
import os

from pathlib import Path
from shutil import copyfileobj
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import UploadFile

from src.database.models import JSONObject, FileObject


def create_json_object(db: Session, data: dict) -> JSONObject:
    object = JSONObject(data=json.dumps(data))
    db.add(object)
    db.commit()
    db.refresh(object)
    return object


def create_file_object(db: Session, file: UploadFile) -> FileObject:
    directory = os.path.join(os.getcwd(), "files")
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file.filename)
    try:
        with open(file_path, "wb+") as f:
            copyfileobj(file.file, f)
    finally:
        file.file.close()

    file_type = "".join(Path(file.filename).suffixes)
    object = FileObject(
        file_path=file_path, file_name=file.filename, file_type=file_type
    )
    db.add(object)
    db.commit()
    db.refresh(object)
    return object


def get_json_object(db: Session, id: str) -> JSONObject | None:
    return db.query(JSONObject).filter(JSONObject.id == id).first()


def get_file_object(db: Session, id: str) -> FileObject | None:
    # ID could be the database ID or the file name since both are unique
    return (
        db.query(FileObject)
        .filter(or_(FileObject.id == id, FileObject.file_name == id))
        .first()
    )


def get_all_json_objects(db: Session) -> list[JSONObject]:
    return db.query(JSONObject).all()


def get_all_file_objects(db: Session) -> list[FileObject]:
    return db.query(FileObject).all()


def delete_json_object(db: Session, id: str) -> None:
    db.query(JSONObject).filter(JSONObject.id == id).delete()
    db.commit()


def delete_file_object(db: Session, id: str) -> None:
    db.query(FileObject).filter(
        or_(FileObject.id == id, FileObject.file_name == id)
    ).delete()
    db.commit()
