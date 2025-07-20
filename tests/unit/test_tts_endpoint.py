from unittest.mock import patch

from fastapi.testclient import TestClient

from server.src.main import app


def test_tts_endpoint() -> None:
    client = TestClient(app)
    with patch("server.src.api.endpoints.tts.service") as mock_service:
        mock_service.speak.return_value = b"audio"
        resp = client.post(
            "/api/v1/tts/speak", json={"text": "hello", "language": "en"}
        )
        assert resp.status_code == 200
        assert resp.content == b"audio"
        assert resp.headers["content-type"].startswith("audio/")
