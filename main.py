import json

from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

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


def to_json(object: models.JSONObject) -> models.JSONObject:
    str_data = object.data
    object.data = json.loads(str_data)
    return object


@app.post("/json", response_model=schemas.JSONObject)
def create_json_object(data: dict, db: Session = Depends(get_db)):
    try:
        return crud.create_json_object(db, data=data)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Object already exists."
        )


@app.put("/json/{object_id}", response_model=schemas.JSONObject)
def update_json_object(
    object_id: str, data: dict, db: Session = Depends(get_db)
):  # noqa E501
    return crud.update_json_object(db, id=object_id, data=data)


@app.post("/file", response_model=schemas.FileObject)
def create_file_object(data: UploadFile, db: Session = Depends(get_db)):
    try:
        return crud.create_file_object(db, file=data)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Object already exists."
        )


@app.put("/file/{object_id}", response_model=schemas.FileObject)
def update_file_object(
    object_id: str, data: UploadFile, db: Session = Depends(get_db)
):  # noqa E501
    return crud.update_file_object(db, id=object_id, file=data)


@app.get("/json/{object_id}")
def get_json_object(
    object_id: str, convert: bool = False, db: Session = Depends(get_db)
):  # noqa E501
    object = crud.get_json_object(db, id=object_id)
    if object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Object not found."
        )

    if convert:
        return to_json(object)

    return object


@app.get("/file/{object_id}")
def get_file_object(
    object_id: str, convert: bool = False, db: Session = Depends(get_db)
):  # noqa E501
    object = crud.get_file_object(db, id=object_id)
    if object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Object not found."
        )

    if convert:
        return FileResponse(object.file_path)

    return object


@app.get("/json", response_model=list[schemas.JSONObject])
def get_all_json_objects(db: Session = Depends(get_db)):
    objects = crud.get_all_json_objects(db)
    return objects


@app.get("/file", response_model=list[schemas.FileObject])
def get_all_file_objects(db: Session = Depends(get_db)):
    objects = crud.get_all_file_objects(db)
    return objects


@app.delete("/json/{object_id}")
def delete_json_object(object_id: str, db: Session = Depends(get_db)):
    crud.delete_json_object(db, id=object_id)
    return {"message": "Object successfully deleted."}


@app.delete("/file/{object_id}")
def delete_file_object(object_id: str, db: Session = Depends(get_db)):
    try:
        crud.delete_file_object(db, id=object_id)
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="File does not exist."
        )
    return {"message": "Object successfully deleted."}
