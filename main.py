import json

from fastapi import FastAPI, Depends, HTTPException
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


def to_json(object: models.Object) -> models.Object:
    str_data = object.data
    object.data = json.loads(str_data)
    return object


@app.post("/", response_model=schemas.StrObject)
def create_object(data: dict, db: Session = Depends(get_db)):
    try:
        return crud.create_object(db, data=data)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Object already exists."
        )


@app.get("/{object_id}", response_model=schemas.StrObject | schemas.JSONObject)
def get_object(object_id: str, json: bool = False, db: Session = Depends(get_db)):
    object = crud.get_object(db, id=object_id)
    if object is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Object not found."
        )
    if json:
        return to_json(object)
    return object


@app.get("/", response_model=list[schemas.StrObject | schemas.JSONObject])
def get_all_objects(json: bool = False, db: Session = Depends(get_db)):
    objects = crud.get_all_objects(db)
    if json:
        json_objects = [to_json(object) for object in objects]
        return json_objects
    return objects
