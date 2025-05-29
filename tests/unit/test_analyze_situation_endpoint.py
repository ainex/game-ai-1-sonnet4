from io import BytesIO

from fastapi.testclient import TestClient

from server.src.main import app


def test_analyze_situation_endpoint() -> None:
    client = TestClient(app)
    image_content = b"fakeimage"
    files = {"image": ("test.png", BytesIO(image_content), "image/png")}
    data = {"query": "What should I do next?"}
    response = client.post("/api/v1/analyze_situation", files=files, data=data)
    assert response.status_code == 200
    payload = response.json()
    assert payload["image_size_bytes"] == len(image_content)
    assert "Screenshot and query received" in payload["message"]
