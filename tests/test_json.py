import json

from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app, get_db

# must be imported last
from .mock_db import TestingSessionLocal


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


test_data = {"test_data": {"nested_obj": "something else"}}


class TestJson:
    def test_create_json(self) -> None:
        response = client.post("/json", json=test_data)

        json_object = response.json()
        assert response.status_code == HTTPStatus.CREATED
        assert json_object["data"] == json.dumps(test_data)

    def test_get_json_string(self) -> None:
        response = client.get("/json/1")
        assert response.status_code == HTTPStatus.OK

        json_object = response.json()
        assert json_object["data"] == json.dumps(test_data)

    def test_get_json_object(self) -> None:
        response = client.get("/json/1?convert=True")
        assert response.status_code == HTTPStatus.OK

        json_object = response.json()
        assert json_object["data"] == test_data

    def test_get_all_json(self) -> None:
        response = client.get("/json")
        assert response.status_code == HTTPStatus.OK

        json_objects = response.json()
        assert len(json_objects) == 1

        json_object = json_objects[0]
        assert json_object["data"] == json.dumps(test_data)

    def test_delete_json(self) -> None:
        response = client.delete("/json/1")
        assert response.status_code == HTTPStatus.OK
