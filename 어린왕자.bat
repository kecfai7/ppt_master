@echo off
title 어린왕자 AI 교육 프레젠테이션
cd /d "%~dp0"

set "PY_BIN=python"
if exist "%~dp0.venv\Scripts\python.exe" set "PY_BIN=%~dp0.venv\Scripts\python.exe"

:menu
cls
echo ================================================================
echo   [어린왕자] AI 시대, 교육의 문법이 바뀌다 - 원클릭 실행기
echo ================================================================
echo.
echo   [1] 마우스 클릭 진행 및 애니메이션 덱 열기 (.pptx) [추천]
echo   [2] 파워포인트 전체화면 자율재생 쇼 바로 실행 (.ppsx)
echo   [3] 웹 실시간 동적 프리뷰 서버 (브라우저 http://localhost:5050)
echo   [4] 수학교사용 인터랙티브 수학.pptx 열기
echo   [Q] 종료
echo.
echo ================================================================
set choice=
set /p choice=원하는 번호를 선택하세요 [기본값: 1]: 

if "%choice%"=="" set choice=1
if /i "%choice%"=="q" exit /b
if "%choice%"=="1" goto pptx_click
if "%choice%"=="2" goto ppsx_show
if "%choice%"=="3" goto web_preview
if "%choice%"=="4" goto math_deck

echo 잘못된 입력입니다. 1, 2, 3, 4 또는 Q를 입력하세요.
timeout /t 2 > nul
goto menu

:pptx_click
echo.
echo [안내] 마우스 클릭 진행 + 애니메이션 덱을 엽니다...
start "" "presentations\AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx"
goto end

:ppsx_show
echo.
echo [안내] 전체화면 자율재생 쇼(어린왕자-자율재생.ppsx)를 실행합니다...
start "" "presentations\어린왕자-자율재생.ppsx"
goto end

:web_preview
echo.
echo [안내] 웹 프리뷰 서버(http://localhost:5050)를 실행합니다...
start http://localhost:5050
"%PY_BIN%" scripts\live_preview_server.py
goto end

:math_deck
echo.
echo [안내] 수학교사용 인터랙티브 수학.pptx를 엽니다...
start "" "presentations\수학.pptx"
goto end

:end
