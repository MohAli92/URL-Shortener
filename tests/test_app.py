import sys
import os
import pytest

# نضيف root المشروع للـ path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_shorten_url(client):
    response = client.post(
        "/shorten",
        data={"url": "https://www.google.com"}
    )

    assert response.status_code == 200

    json_data = response.get_json()
    assert "short_url" in json_data
    assert json_data["short_url"].endswith("/1")
