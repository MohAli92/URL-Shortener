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
        data={"url": "google.com"}
    )

    assert response.status_code == 200

    json_data = response.get_json()
    assert "short_url" in json_data
    assert json_data["short_url"].startswith("/")


def test_redirect_to_original_url(client):
    # 1️⃣ shorten URL
    shorten_response = client.post(
        "/shorten",
        data={"url": "google.com"}
    )
    short_url = shorten_response.get_json()["short_url"]

    # 2️⃣ request short URL (without following redirect)
    redirect_response = client.get(short_url, follow_redirects=False)

    # 3️⃣ assertions
    assert redirect_response.status_code == 302
    assert redirect_response.headers["Location"] == "https://google.com"
