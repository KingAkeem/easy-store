from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app, get_db

# must be imported last
from tests.mock_db import override_get_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_file() -> None:
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


def test_get_file_by_id() -> None:
    response = client.get("/file/1")
    assert response.status_code == HTTPStatus.OK

    file_object = response.json()
    assert file_object["file_name"] == "mock.txt"
    assert file_object["file_type"] == ".txt"


def test_get_file_by_name() -> None:
    response = client.get("/file/mock.txt")
    assert response.status_code == HTTPStatus.OK

    file_object = response.json()
    assert file_object["file_name"] == "mock.txt"
    assert file_object["file_type"] == ".txt"


def test_get_all_files() -> None:
    response = client.get("/file")
    assert response.status_code == HTTPStatus.OK

    file_objects = response.json()
    assert len(file_objects) == 1

    file_object = file_objects[0]
    assert file_object["file_name"] == "mock.txt"
    assert file_object["file_type"] == ".txt"
