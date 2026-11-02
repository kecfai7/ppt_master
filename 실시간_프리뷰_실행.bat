@echo off
title PPT Master Live Studio Server
cd /d "%~dp0"

set "PY_BIN=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

echo ================================================================
echo   PPT Master 실시간 통합 웹 스튜디오를 시작합니다...
echo   접속 주소: http://localhost:5050
echo ================================================================

start http://localhost:5050
"%PY_BIN%" scripts\live_preview_server.py
pause
