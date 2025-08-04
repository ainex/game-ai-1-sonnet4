@echo off
echo Setting up environment and testing Claude 4 models...

REM Load environment variables from .env file
for /f "usebackq tokens=1,2 delims==" %%i in (".env") do (
    if /i "%%i"=="ANTHROPIC_API_KEY" set ANTHROPIC_API_KEY=%%j
    if /i "%%i"=="DEFAULT_MODEL" set DEFAULT_MODEL=%%j
)

echo API Key loaded: %ANTHROPIC_API_KEY:~0,15%...

REM Change to server directory and run test
cd server\src
python ..\..\test_claude4_models.py

pause