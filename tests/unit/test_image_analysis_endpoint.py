from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from server.src.main import app


def test_image_analysis_endpoint() -> None:
    client = TestClient(app)
    patch_path = "server.src.api.endpoints.image_analysis.service"
    with patch(patch_path) as mock_service:
        mock_service.analyze.return_value = "a character is cooking"
        files = {"image": ("test.png", BytesIO(b"img"), "image/png")}
        resp = client.post("/api/v1/image/analyze", files=files)
        assert resp.status_code == 200
        assert resp.json()["description"] == "a character is cooking"
