Here’s a focused MVP checklist tailored for two users. Suggested file name: MVP_MUST_HAVE.md

# MVP Must-Haves (Two-User Setup)

Goal: Reliable local usage on two Windows 11 PCs with minimal friction, safe defaults, and predictable behavior.

## 1) Setup and Run

- Single-command startup scripts
    - Windows: scripts/start_server.bat to start FastAPI; scripts/start_client.bat to launch client.
    - Validate Python, PortAudio, ffmpeg, and CUDA (optional) before starting; show actionable messages if missing.

- Configuration
    - .env with placeholders only (e.g., OPENAI_API_KEY=<your_api_key>); app loads settings from a single source of truth.
    - Feature flags: ENABLE_OPENAI, USE_GPU, MAX_IMAGE_SIZE, AUDIO_SAMPLE_RATE, LOG_LEVEL.

- Clear onboarding
    - Short README “Quickstart for Windows 11” section with exact steps and screenshots.
    - Pre-flight check script scripts/verify_environment.py that prints OK/FAIL for mic, speaker, screenshot, server connectivity.

Acceptance:
- On a fresh Windows 11 with Python installed, both users can: run start_server.bat, start_client.bat, press the main hotkey, and get a spoken response without manual package tinkering.

## 2) Core Functionality

- Primary flow (single hotkey)
    - Press Ctrl+Shift+V: capture active game window, record voice with start/end chime, auto-stop on silence, send to server, receive spoken response.
    - Guard re-entrancy: ignore new hotkeys while one is in flight.

- Offline baseline
    - If ENABLE_OPENAI=false, still works with local STT (if available) or at minimum records audio and returns a text placeholder response so the UI flow doesn’t break.

- OpenAI path (optional)
    - If ENABLE_OPENAI=true and OPENAI_API_KEY present, use OpenAI-based analysis endpoints with a strict timeout.

Acceptance:
- Both users can consistently complete the flow in <8 seconds on CPU-only, faster on GPU if enabled.
- Hotkey spamming doesn’t crash or stack requests.

## 3) Stability and Safety

- Request size limits
    - Server caps: image <= 3 MB, audio <= 20 MB, duration <= 60s; reject oversize with clear error.

- Content type + schema validation
    - Enforce multipart/form-data for media and validate mime types (image/*, audio/*).
    - Pydantic models for all requests/responses.

- Timeouts and retries
    - External calls capped at 20s; 2 retries with exponential backoff for transient errors; fail fast with user-friendly message.

- Resource lifecycle
    - Microphone/speaker handles are always released (even on exceptions).
    - Background threads/timers shut down cleanly when client closes.

Acceptance:
- No leaks or zombie processes after 20 rapid invocations.
- Oversized files and wrong formats yield a clear client toast and server error JSON with code/message.

## 4) Performance Essentials

- Client image pipeline
    - Downscale screenshot to max dimension 1280 px; JPEG quality ~80 before upload.

- Server model warmup
    - Load TTS and (if used) STT/vision models at startup; first request latency < 2x steady-state.

- Concurrency control
    - Simple queue or semaphore: max N concurrent TTS/STT tasks (configurable, default 1–2).

Acceptance:
- P95 end-to-end latency under 8s (OpenAI), 12s (local) on CPU-only; on RTX, under 5s local for TTS.

## 5) Logging and Diagnostics

- Structured logs
    - Request_id, endpoint, latency_ms, status, provider, device (cpu/gpu). Redact content.

- Minimal metrics
    - Count + p95 latency per endpoint (in logs is fine for MVP).

- User-visible diagnostics
    - Client “Diagnostics” dialog: mic detected, speaker device, GPU detected, server reachable, last error.

Acceptance:
- When a failure occurs, both users can open Diagnostics to identify the cause in under 1 minute.

## 6) Testing and Recovery

- Happy-path tests
    - One integration test per core endpoint: image analyze, stt transcribe (mock if needed), tts speak, combined flow.
    - Mark slow tests and skip by default.

- Manual recovery guide
    - Short doc: how to kill stuck processes, clear temp files, reset logs, re-run setup.

Acceptance:
- Running pytest -q on the dev machine passes fast tests; slow tests run on demand.
- Recovery guide resolves common failures in under 5 minutes.

## 7) Privacy Defaults

- Window-targeted screenshot
    - Capture current active window (game) instead of full desktop by default.

- Local-first processing
    - Media never leaves the machine unless ENABLE_OPENAI=true; show a subtle indicator when cloud mode is active.

Acceptance:
- No accidental capture of other monitors/desktop UI in normal use.
- A visible “Cloud Mode” pill or icon when cloud calls are enabled.

## 8) Minimal UX Polish

- Feedback sounds and states
    - Distinct chime at recording start and end, with a short visual indicator (overlay or tray tooltip).
    - Progress indicator during analysis; cancel button that actually cancels client tasks.

- Errors that help
    - Human-readable toasts (e.g., “Microphone not found. Open Settings to choose a device.” with a button to settings).

Acceptance:
- Users always know whether it’s listening, thinking, or speaking, and can cancel without hanging the app.

---

Implementation Order

1) Stabilize core path: hotkey -> capture -> record -> send -> TTS response with strict timeouts and size limits.
2) Add client downscaling, server validations, and model warmup.
3) Introduce diagnostics and structured logs.
4) Polish UX (sounds, states), implement re-entrancy guard.
5) Finalize OpenAI toggle path; ensure offline still works.
6) Ship start scripts and verification script; update quickstart.

Done Criteria for MVP
- Two Windows 11 machines can run start scripts and use the hotkey end-to-end reliably for 20 consecutive attempts without a crash, hang, or leaked audio device.
- Clear errors for oversized inputs, missing mic, missing API key, or disabled GPU; user can recover using the provided guide.