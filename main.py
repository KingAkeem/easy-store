import json
import os

from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from typing import Any

from src import schemas
from src.database.core import SessionLocal, engine, Base
from src.database import crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_json(object: models.Object) -> models.Object:
    str_data = object.data
    object.data = json.loads(str_data)
    return object


@app.post("/", response_model=schemas.StrObject)
def create_object(
    json_data: dict, file_data: UploadFile, db: Session = Depends(get_db)
):
    objects = list()
    try:
        if json_data:
            objects.append(crud.create_json_object(db, data=json_data))

        if file_data:
            objects.append(crud.create_file_object(db, file=file_data))

        return objects

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Object already exists."
        )


@app.get("/{object_id}")
def get_object(object_id: int | str, db: Session = Depends(get_db)):  # noqa E501
    object = crud.get_object(db, id=object_id)
    if object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Object not found."
        )
    if object.type == "json":
        return to_json(object)
    elif object.type == "file":
        return FileResponse(os.path.join("files", object.data))
    return object


@app.get("/", response_model=list[schemas.StrObject])
def get_all_objects(db: Session = Depends(get_db)):
    objects = crud.get_all_objects(db)
    return objects


@app.delete("/{object_id}")
def delete_object(object_id: int, db: Session = Depends(get_db)):
    crud.delete_object(db, id=object_id)
    return {"message": "Object successfully deleted."}
