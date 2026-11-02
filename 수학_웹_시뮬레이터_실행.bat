@echo off
title 수학 웹 인터랙티브 시뮬레이터
cd /d "%~dp0"

set "PY_BIN=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

echo ================================================================
echo   [수학] 웹 실시간 인터랙티브 시뮬레이터
echo   접속 주소: http://localhost:5050/?deck=math
echo ================================================================

start http://localhost:5050/?deck=math
"%PY_BIN%" scripts\live_preview_server.py
pause
