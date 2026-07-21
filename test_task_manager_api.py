import pytest

from task_manager_api import app, create_task, get_task, mark_done, reset_store


@pytest.fixture
def client():
    reset_store()
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_store():
    reset_store()


def test_create_task_assigns_incrementing_ids():
    first = create_task("Buy milk")
    second = create_task("Walk dog")
    assert first == {"id": 1, "title": "Buy milk", "done": False}
    assert second["id"] == 2


def test_get_task_returns_none_when_missing():
    create_task("One")
    assert get_task(99) is None


def test_mark_done_updates_task():
    task = create_task("Read")
    updated = mark_done(task["id"])
    assert updated is not None
    assert updated["done"] is True
    assert get_task(task["id"])["done"] is True


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_task_requires_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "title is required"}


def test_add_and_list_tasks(client):
    create = client.post("/tasks", json={"title": "Write tests"})
    assert create.status_code == 201
    assert create.get_json() == {"id": 1, "title": "Write tests", "done": False}

    listing = client.get("/tasks")
    assert listing.status_code == 200
    assert len(listing.get_json()) == 1


def test_complete_task(client):
    client.post("/tasks", json={"title": "Ship it"})
    response = client.patch("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_complete_task_not_found(client):
    response = client.patch("/tasks/1")
    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}
