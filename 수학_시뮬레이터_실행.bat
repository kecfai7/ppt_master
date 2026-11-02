@echo off
title 수학 인터랙티브 시뮬레이터 (Math Dynamic Graph GUI)
cd /d "%~dp0"

set "PY_BIN=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

set "MPLCONFIGDIR=%TEMP%\mpl_cache"

echo ================================================================
echo   [수학교사용] 인터랙티브 그래프 + 실시간 시뮬레이터
echo ================================================================
echo.
echo   * 마우스 조작: 슬라이더를 마우스로 드래그하거나 [-] [+] 클릭
echo   * 키보드 조작: [1~4] 모드 전환 ^| [위/아래] 변수 선택 ^| [좌/우] 수치 조절
echo.
echo   시뮬레이터 창을 엽니다...
echo ================================================================

"%PY_BIN%" scripts\math_interactive_gui.py
