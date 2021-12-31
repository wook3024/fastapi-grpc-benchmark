from httpx import Client
from pathlib import Path

from celery.result import AsyncResult


def test_redirect(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_save_image_task(test_client):
    image_path = Path("assets", "fluentd-icon-color.png")
    data = image_path.read_bytes()
    delay = 1
    client = Client()
    background_task_url = "http://localhost:8000/background_task"
    response = client.post(
        url=background_task_url,
        files={
            "delay": (None, str(delay).encode()),
            "file": (image_path.name, data, "image/png"),
        },
    )
    result = response.json()
    task_id = result.get("id")
    assert response.status_code == 201
    assert task_id

    response = client.get(url=background_task_url, params={"id": task_id})
    result = response.json()
    assert response.status_code == 200
    assert result.get("id") == task_id
    assert result.get("state") == "PENDING"

    while result.get("state") == "PENDING":
        response = client.get(url=background_task_url, params={"id": task_id})
        result = response.json()
    assert result.get("id") == task_id
    assert result.get("state") == "SUCCESS"

    task_result = AsyncResult(task_id)
    result = task_result.result
    assert result.get("delay") == delay
    assert result.get("save_path") is not None
    assert "×" in result.get("image_shape")
    client.close()
