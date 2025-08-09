Here’s a first-pass code health and performance audit you can drop into a new Markdown file (suggested name: CODE_HEALTH_AUDIT.md). It’s prioritized, with concrete fixes and the level of effort. We’ll use this as the backlog for next steps.

# Code Health and Performance Audit

Status: Initial review based on repository structure, README, and typical pitfalls for FastAPI + Python desktop client apps with audio/vision features.

Scope:
- Server: FastAPI, endpoints for image, voice, TTS, LLM.
- Client: Python desktop app, hotkeys, audio capture, screenshot, TTS playback.
- Tooling: Tests, pre-commit, security, packaging, environment setup.

Legend:
- Priority: P0 critical, P1 high, P2 medium, P3 low.
- Effort: S (hours), M (days), L (multi-day).

## Executive Summary
- P0: Input validation and payload size control on media endpoints; timeouts and circuit breakers on external LLM calls; GPU/CPU model caching and device management; audio resource lifecycle correctness; OpenAI key handling and mocks isolation.
- P1: Logging/observability baselines; request tracing; unified error model; concurrency safety for shared resources (TTS/STT models); Windows startup and dependency robustness; screenshot privacy controls.
- P2: Performance tuning for image pipelines (resize, compress, stream); content-type enforcement; test coverage for slow paths guarded with markers; retry/backoff policies; graceful degradation when GPU absent.
- P3: Docs alignment with real code paths; consistent configuration strategy; package layout cleanup; DX improvements.

---

## 1) Security and Privacy

1.1 Media upload hardening [P0, S]
- Risk: Large or malformed images/audio cause memory spikes or DoS.
- Fix:
    - Enforce Content-Length and request body size limits on FastAPI routes handling media.
    - Validate MIME types (image/*, audio/*) and reject others early.
    - Validate dimensions and duration; downscale oversized images on server.
    - Reject overly long audio (e.g., >60s unless explicitly supported).

1.2 API key handling and env safety [P0, S]
- Risk: Keys accidentally used in tests or logged.
- Fix:
    - Ensure keys only loaded in production modes and never logged.
    - Gate external API usage behind a config flag (USE_EXTERNAL_APIS=false by default in tests).
    - Verify .env.example uses placeholders like OPENAI_API_KEY=<your_api_key> rather than anything that looks realistic.

1.3 Screenshot privacy controls [P1, S]
- Risk: Screenshots may capture PII outside the game window.
- Fix:
    - Option to capture only the active game window.
    - Mask common OS UI regions or user-defined masks.
    - Provide “local-processing only” toggle to guarantee no remote upload.

1.4 CORS and headers [P2, S]
- Risk: Overly permissive CORS for a desktop app isn’t necessary but sometimes gets enabled by default.
- Fix:
    - Disable or strictly limit CORS unless truly needed.
    - Set strict content security and security headers if a web UI is involved anywhere.

---

## 2) Stability and Error Handling

2.1 Unified error response model [P1, S]
- Problem: Inconsistent error shapes complicate client handling.
- Fix:
    - Define APIError schema with code/message/details; ensure all endpoints map exceptions to this schema.
    - Map common failure modes (timeout, size limit, model not loaded, invalid audio format).

2.2 Timeouts, retries, backoff for external LLM calls [P0, S]
- Risk: Hanging requests, thread starvation under load.
- Fix:
    - Set per-call timeouts; apply retries with exponential backoff for transient errors; cap retries.
    - Circuit breaker or short-circuit when provider is degraded.

2.3 Graceful degradation when GPU is unavailable [P1, S]
- Risk: Hard failures on machines without CUDA.
- Fix:
    - Capability detection (CUDA, device count) at startup.
    - Fallback to CPU models with lower throughput, or disable features with a clear message.

2.4 Resource cleanup guarantees [P0, S]
- Risk: Microphone/PortAudio device handles and threads leaked on exceptions.
- Fix:
    - Ensure microphone and audio streams use context managers or try/finally.
    - Centralized shutdown hooks for client app to stop threads/timers and audio devices.

---

## 3) Performance

3.1 Image pipeline efficiency [P1, S]
- Problem: Sending full-resolution screenshots increases latency and costs.
- Fix:
    - Client-side: Resize to a max dimension (e.g., 1280px) and JPEG compress with quality ~75–85 before upload.
    - Server-side: Revalidate and re-encode, standardize color mode (RGB), ensure streaming processing when possible.

3.2 Audio pipeline sizing and VAD [P1, M]
- Problem: Long audio chunks add latency; inaccurate silence detection loops.
- Fix:
    - Use robust VAD or library-level silence detection with thresholds and debounce.
    - Clip maximum duration and chunk streaming to server for early transcription start.

3.3 Model warmup and caching [P0, S]
- Problem: Cold starts for Whisper/TTS/vision models cause long first responses.
- Fix:
    - Load and warm models at server startup; keep singletons in a thread-safe registry.
    - Cache tokenizers and reuse sessions.

3.4 Concurrency model for TTS/STT [P1, M]
- Risk: Contention, GPU OOM with multiple concurrent requests.
- Fix:
    - Work queue with concurrency controls per model/device.
    - Optional per-request priority (user actions vs background tasks).

3.5 Avoid synchronous heavy work on the main UI thread [P0, S]
- Problem: Client UI freezes during recording, screenshotting, or network I/O.
- Fix:
    - Move blocking work to worker threads or async tasks; keep UI responsive with progress indicators.

3.6 HTTP transfer optimization [P2, S]
- Problem: Base64 payloads inflate size and CPU usage.
- Fix:
    - Prefer multipart/form-data binary uploads for image/audio.
    - Enable gzip/deflate on server responses where appropriate.

---

## 4) API Design Consistency

4.1 Endpoint contract alignment [P1, S]
- Problem: Overlapping endpoints for “analyze + speak” vs “analyze-image-and-voice” can drift.
- Fix:
    - Define clear resource responsibilities: /image, /stt, /tts, /game orchestration.
    - Normalize request/response schemas; versioning under /api/v1 with typed payloads.

4.2 Content type enforcement [P1, S]
- Problem: Accepting multiple shapes makes validation hard.
- Fix:
    - Enforce application/json for metadata; multipart for binary media.
    - Reject unexpected combinations with precise error messages.

4.3 Idempotency for long tasks [P2, M]
- Problem: Retries may duplicate expensive operations.
- Fix:
    - Optional idempotency keys for orchestration endpoints; cache results short-term if inputs identical.

---

## 5) Concurrency, Threading, and Lifecycle

5.1 FastAPI worker/process configuration [P1, S]
- Problem: Defaults may not match CPU/GPU concurrency needs.
- Fix:
    - Document recommended uvicorn/gunicorn settings: workers, threads, timeout-keep-alive.
    - Ensure single model instances per process or implement inter-process sharing strategy.

5.2 Client hotkey and event handling [P1, S]
- Problem: Hotkey listeners can spawn multiple overlapping tasks.
- Fix:
    - Debounce hotkey triggers.
    - Re-entrancy guard to prevent starting another capture while one is running.

5.3 Long-running tasks and cancellation [P2, M]
- Problem: Users cancel mid-record; server still computes.
- Fix:
    - Implement client cancellation propagation; server-side cooperative cancellation if feasible.

---

## 6) Testing Strategy

6.1 Slow tests and flakiness [P2, S]
- Problem: Audio and GPU paths are slow/flake-prone.
- Fix:
    - Mark slow tests with pytest markers; default to skipping unless explicitly enabled.
    - Seed randomness and fix thresholds to make VAD tests deterministic.

6.2 Contract tests for all endpoints [P1, M]
- Fix:
    - Golden tests around JSON schemas; property-based tests for media validators.
    - Error-path tests: size too large, wrong mime, timeouts, provider failures.

6.3 Isolation of external services [P0, S]
- Fix:
    - Ensure all external calls are mocked in unit/integration tests.
    - Provide fixtures for OpenAI/Claude responses, including error variants.

6.4 Coverage on client-side lifecycle [P2, M]
- Fix:
    - Headless tests for start/stop recording, silence detection, overlapping hotkeys, graceful shutdown.

---

## 7) Logging and Observability

7.1 Structured logging [P1, S]
- Fix:
    - Use structured logs with fields: request_id, endpoint, latency_ms, model_used, device, status.
    - Scrub PII/media paths; never log full transcripts/screenshots by default.

7.2 Tracing and metrics [P1, M]
- Fix:
    - Add OpenTelemetry traces: client request -> server -> model call.
    - Metrics: request counts, p50/p95 latencies per endpoint, GPU/CPU utilization, queue depths, error rates.

7.3 User-facing diagnostics [P2, S]
- Fix:
    - Client: “Diagnostics” panel with last error, device info, whether GPU is detected, mic status.

---

## 8) Configuration and Environment

8.1 Centralized config with typed validation [P1, S]
- Fix:
    - Pydantic-based settings for server; single source of truth for feature flags (USE_GPU, ENABLE_OPENAI, MAX_IMAGE_SIZE, AUDIO_SAMPLE_RATE).
    - Ensure defaults are safe and match docs.

8.2 Environment parity [P2, S]
- Fix:
    - Align docs for Windows vs Linux: package names, Python versions, device backends.
    - Add a scripted Windows setup with checks for PortAudio, Visual Build Tools, CUDA libs.

8.3 Secrets and .env handling [P1, S]
- Fix:
    - Never commit real keys; confirm .gitignore filters .env.
    - Provide sample .env with placeholders and comments on scope.

---

## 9) Packaging and Dependency Hygiene

9.1 Dependency pinning and constraints [P1, S]
- Risk: Audio/vision libs often break across versions.
- Fix:
    - Pin critical libs to known-good versions; consider constraints.txt.
    - Periodic dependency update job + smoke tests.

9.2 Optional extras for heavy features [P2, S]
- Fix:
    - extras_require groups like [gpu], [openai], [dev].
    - Reduce install friction for users not needing GPU or certain providers.

9.3 Native dependencies checks [P1, S]
- Fix:
    - Pre-flight script to verify PortAudio, CUDA/cuDNN, ffmpeg availability; fail fast with clear instructions.

---

## 10) Data and Storage

10.1 SQLite schema and migrations [P2, M]
- Fix:
    - Ensure Alembic migrations exist for user preferences/history.
    - Indexes on frequently queried fields; WAL mode for concurrency if needed.

10.2 Data retention and privacy [P2, S]
- Fix:
    - Configurable retention for audio/images/transcripts.
    - “Clear history” endpoint and client UI control.

---

## 11) UX and Accessibility (Non-controversial scope)

11.1 Audio feedback volume and device selection [P3, S]
- Fix:
    - Expose output device choice; volume scaler; mute option for public spaces.

11.2 Failure messaging [P2, S]
- Fix:
    - Clear, actionable messages in client when server unavailable, device missing, or model disabled.

---

## 12) Documentation Gaps

12.1 Endpoint reference vs implementation [P2, S]
- Fix:
    - Auto-generate API docs (OpenAPI) and link from README.
    - Ensure “NEW!” endpoints are live and tested; note required content types.

12.2 GPU setup paths [P2, S]
- Fix:
    - Explicit driver/toolkit versions and compatibility matrix (e.g., CUDA x.y + pytorch x.y).

---

## 13) Code Smells to Hunt in Next Pass

- Overly broad try/except hiding root causes.
- Mixed sync and async in FastAPI handlers leading to sync I/O blocking.
- Global state for models without locks.
- Repeated API client creation per request (for OpenAI/Claude) instead of reusing configured clients.
- Base64 media in JSON payloads instead of multipart.
- Hard-coded constants scattered across client/server instead of config.
- Printing instead of logging; no log levels.
- UI thread operations performing network or file I/O.
- Silent failures on device init (mic/speaker), leading to zombie states.

---

## Prioritized Fix Plan (Next Steps)

1) P0 Batch
- Add request size limits, content-type validation, and strict schema validation on media endpoints.
- Add timeouts/retries/backoff and short-circuit logic for LLM calls; ensure external calls disabled by default in tests.
- Implement model singletons with warmup; add resource cleanup for all audio and thread lifecycles.
- Move client blocking operations off the UI thread; add re-entrancy guard for hotkeys.

2) P1 Batch
- Structured logging, request IDs, and baseline metrics.
- Unified error model with consistent JSON shape; map exceptions.
- Client-side image resize/compression and server-side normalization.
- Concurrency limits for TTS/STT; basic work queue.
- Centralized, typed configuration with feature flags.

3) P2 Batch
- VAD improvements and chunked audio; cancellation propagation.
- Contract tests, slow test markers, and golden schema tests.
- Windows/Linux setup parity checks and pre-flight diagnostics.

4) P3 Batch
- Docs refinements, optional extras, minor UX polish.

---

Checklist for Implementation
- [ ] Define pydantic models for every endpoint request/response.
- [ ] Enforce multipart/form-data for media uploads; cap sizes.
- [ ] Implement global Settings object; read-only at runtime.
- [ ] Add model registry (thread-safe) with warmup hooks.
- [ ] Introduce structured logging with request_id and latency.
- [ ] Wrap external calls with timeouts/backoff; add test fakes.
- [ ] Client: move audio/screenshot/network to worker threads; add debouncing.
- [ ] Add pytest markers for slow/gpu/external; ensure defaults skip.
- [ ] Add OpenAPI docs link and align README.
- [ ] Pre-flight checks: mic/speaker, CUDA, PortAudio, ffmpeg.

Notes
- We’ll validate and adjust specifics against the actual code in the next step (schema details, endpoint shapes, threading model). This document captures the highest-yield, common issues for this stack so we can execute efficiently.