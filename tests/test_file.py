import os

from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app, get_db

from .mock_db import TestingSessionLocal


def teardown_module(module):
    os.remove("mock.txt")


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestFile:
    def test_create_file(self) -> None:
        with open("mock.txt", "+wb") as test_file:
            test_file.write(b"something")
            response = client.post(
                "/file",
                files={"data": test_file},
            )

            file_object = response.json()
            assert response.status_code == HTTPStatus.CREATED
            assert file_object["file_name"] == "mock.txt"
            assert file_object["file_type"] == ".txt"

    def test_get_file_by_id(self) -> None:
        response = client.get("/file/1")
        assert response.status_code == HTTPStatus.OK

        file_object = response.json()
        assert file_object["file_name"] == "mock.txt"
        assert file_object["file_type"] == ".txt"

    def test_get_file_binary(self) -> None:
        response = client.get("/file/1?convert=True")
        assert response.status_code == HTTPStatus.OK

        with open("mock.txt", "rb") as test_file:
            assert response.read() == test_file.read()

    def test_get_file_by_name(self) -> None:
        response = client.get("/file/mock.txt")
        assert response.status_code == HTTPStatus.OK

        file_object = response.json()
        assert file_object["file_name"] == "mock.txt"
        assert file_object["file_type"] == ".txt"

    def test_get_all_files(self) -> None:
        response = client.get("/file")
        assert response.status_code == HTTPStatus.OK

        file_objects = response.json()
        assert len(file_objects) == 1

        file_object = file_objects[0]
        assert file_object["file_name"] == "mock.txt"
        assert file_object["file_type"] == ".txt"

    def test_delete_file(self) -> None:
        response = client.delete("/file/1")
        assert response.status_code == HTTPStatus.OK
