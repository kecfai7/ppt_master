@echo off
chcp 65001 >nul
title PPT Master 다른 PC 자동 환경설치기
cd /d "%~dp0"

echo ====================================================================
echo   PPT Master & Interactive Studio - 새 PC 자동 환경 설치 마법사
echo ====================================================================
echo.

:: 1. Check Python installation
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 시스템에 설치되어 있지 않거나 PATH에 등록되지 않았습니다!
    echo https://www.python.org 에서 Python 3.10 이상을 설치하신 후 다시 실행해 주세요.
    echo (설치 시 반드시 [Add python.exe to PATH] 체크박스를 켜주세요)
    echo ====================================================================
    pause
    exit /b
)

echo [1/4] Python 실행 확인 완료:
python --version
echo.

:: 2. Create Virtual Environment (.venv)
if not exist ".venv\Scripts\python.exe" (
    echo [2/4] 가상환경(.venv) 생성 중... 잠시만 기다려 주세요.
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [경고] 가상환경 생성 실패. 시스템 기본 파이썬으로 계속 진행합니다.
        set "PY_EXEC=python"
        set "PIP_EXEC=pip"
    ) else (
        echo   가상환경(.venv) 생성 완료!
        set "PY_EXEC=.venv\Scripts\python.exe"
        set "PIP_EXEC=.venv\Scripts\pip.exe"
    )
) else (
    echo [2/4] 기존 가상환경(.venv)이 발견되었습니다.
    set "PY_EXEC=.venv\Scripts\python.exe"
    set "PIP_EXEC=.venv\Scripts\pip.exe"
)
echo.

:: 3. Install requirements.txt
echo [3/4] requirements.txt 패키지 설치 및 업데이트 중...
"%PIP_EXEC%" install --upgrade pip
"%PIP_EXEC%" install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [주의] 일부 패키지 설치 중 경고가 발생했을 수 있습니다.
) else (
    echo.
    echo [성공] 필수 라이브러리 설치가 완료되었습니다!
)
echo.

:: 4. Prompt to install Paperlogy fonts
echo [4/4] Paperlogy 글꼴 시스템 설치를 진행합니다...
call "%~dp0Paperlogy_폰트_시스템설치.bat"

echo.
echo ====================================================================
echo   [축하합니다!] 모든 환경 설치가 성공적으로 완료되었습니다.
echo.
echo   실행 가능한 배치 파일 안내:
echo   • 수학_시뮬레이터_실행.bat  : 수학교사용 데스크톱 인터랙티브 GUI 실행
echo   • 실시간_프리뷰_실행.bat    : 웹 프레젠테이션 & 시뮬레이터 프리뷰
echo   • 어린왕자.bat              : 어린왕자 슬라이드쇼 실행
echo ====================================================================
pause
