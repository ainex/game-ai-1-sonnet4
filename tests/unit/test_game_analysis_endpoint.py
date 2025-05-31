from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from server.src.main import app


def test_game_analyze_and_speak() -> None:
    client = TestClient(app)
    image_patch = "server.src.api.endpoints.game_analysis.image_service"
    tts_patch = "server.src.api.endpoints.game_analysis.tts_service"
    with (
        patch(image_patch) as mock_image,
        patch(tts_patch) as mock_tts,
    ):
        mock_image.analyze.return_value = "desc"
        mock_tts.speak.return_value = b"audio"
        files = {"image": ("test.png", BytesIO(b"img"), "image/png")}
        resp = client.post("/api/v1/game/analyze-and-speak", files=files)
        assert resp.status_code == 200
        assert resp.content == b"audio"
