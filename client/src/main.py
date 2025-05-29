import io

import keyboard
import requests
from PIL import ImageGrab


def capture_and_send() -> None:
    """Capture screenshot and send to server."""
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    files = {"image": ("screenshot.png", buffer, "image/png")}
    data = {"query": "What should I do next?"}
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/analyze_situation",
            files=files,
            data=data,
            timeout=10,
        )
        print(response.json())
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")


def main() -> None:
    """Entry point for the client."""
    keyboard.add_hotkey("ctrl+shift+i", capture_and_send)
    print("Press Ctrl+Shift+I to analyze situation. Press Esc to quit.")
    keyboard.wait("esc")


if __name__ == "__main__":
    main()
