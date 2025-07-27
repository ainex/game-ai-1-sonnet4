# Debug Guide for AI Gaming Assistant

This guide will help you troubleshoot the audio playback and response issues you're experiencing.

## Issues to Fix

1. **No audio playback** - Audio files are generated but not playing
2. **No text response** - No confirmation of what the AI analyzed
3. **No screenshot confirmation** - No confirmation that screenshots were captured
4. **Missing server response details** - Need to see what the server is actually sending

## Enhanced Logging

I've added comprehensive logging to both client and server:

### Client Logging
- Screenshot capture confirmation with size details
- Server request/response details
- Audio file size and playback attempts
- Detailed error messages

### Server Logging  
- Image analysis results and descriptions
- TTS generation details
- Response content sizes
- Error handling with fallbacks

## Testing Steps

### 1. Test Audio Libraries
First, verify that audio playback works on your system:

```bash
python test_audio.py
```

This will test all available audio libraries (sounddevice, pygame, pyaudio) and create a test audio file.

### 2. Test Server Endpoints
Test if the server is working correctly:

```bash
python test_server.py
```

This will test:
- TTS endpoint with a simple test message
- Image analysis endpoint with a screenshot
- Game analysis endpoint (screenshot + TTS)

### 3. Check Logs
Both client and server now create log files:

- `client.log` - Client-side operations
- `server.log` - Server-side operations

Check these files for detailed information about what's happening.

### 4. Manual Testing

#### Test TTS Only
```bash
curl -X GET "http://localhost:8000/api/v1/tts/test" -o test_audio.wav
```

#### Test Image Analysis Only
```bash
# Use the test_server.py script or manually test with a screenshot
```

## Common Issues and Solutions

### Audio Not Playing
1. **Check audio libraries**: Run `test_audio.py` to see which libraries work
2. **Check audio file size**: Logs will show if audio files are empty or very small
3. **Check system audio**: Ensure your system audio is working and not muted
4. **Try different audio library**: The client tries sounddevice → pygame → pyaudio

### No Server Response
1. **Check server logs**: Look at `server.log` for errors
2. **Check server status**: Ensure server is running on port 8000
3. **Check dependencies**: Ensure TTS and image analysis models are loaded
4. **Check network**: Ensure client can reach localhost:8000

### Empty Audio Files
1. **TTS model issues**: Check if TTS model loaded successfully
2. **Text processing**: Check if image analysis is generating text
3. **Audio generation**: Check if TTS is actually generating audio data

## Debugging Commands

### Check Server Status
```bash
curl http://localhost:8000/docs
```

### Check TTS Service
```bash
curl -X GET "http://localhost:8000/api/v1/tts/test" -v
```

### Check Image Analysis
```bash
# Use test_server.py or manually test with a screenshot
```

## Expected Behavior

### Successful Operation
1. **Screenshot captured**: Log shows "Screenshot captured: (1920, 1080) pixels"
2. **Server request sent**: Log shows request details and response status
3. **Image analyzed**: Server log shows generated description
4. **TTS generated**: Server log shows audio generation details
5. **Audio played**: Client log shows audio playback success

### Log Output Example
```
2024-01-01 12:00:00 - INFO - 📸 Screenshot captured: (1920, 1080) pixels
2024-01-01 12:00:00 - INFO - 📸 Screenshot saved to buffer: 245760 bytes
2024-01-01 12:00:00 - INFO - 📡 Server response status: 200
2024-01-01 12:00:00 - INFO - 📡 Response content length: 123456 bytes
2024-01-01 12:00:00 - INFO - 💾 Audio saved to temporary file: /tmp/audio_123.wav
2024-01-01 12:00:00 - INFO - 🎵 Attempting to play audio: /tmp/audio_123.wav
2024-01-01 12:00:00 - INFO - 📊 Audio file size: 123456 bytes
2024-01-01 12:00:00 - INFO - 🔊 Using sounddevice for audio playback
2024-01-01 12:00:00 - INFO - ✅ Audio playback finished (sounddevice)
```

## Next Steps

1. Run the test scripts to identify where the issue is
2. Check the log files for detailed error messages
3. Verify each component (screenshot, server, TTS, audio) individually
4. Report specific error messages from the logs

The enhanced logging will help pinpoint exactly where the process is failing. 