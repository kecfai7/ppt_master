@echo off
title GitHub + Vercel ���� �����
cd /d "%~dp0"

echo ================================================================
echo   PPT Master & Live Math Studio - GitHub + Vercel ���� �����
echo ================================================================
echo.

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [�˸�] �ý��ۿ� Git�� ��ġ�Ǿ� ���� �ʽ��ϴ�.
    echo.
    echo 1. ���� �޴����� PowerShell�� ���� �Ʒ� ���ɾ�� 1�� ���� ��ġ�� �� �ֽ��ϴ�:
    echo    winget install --id Git.Git -e --source winget
    echo.
    echo 2. �Ǵ� Git ���� ����Ʈ���� ��ġ ���� �ٿ�ε�:
    echo    https://git-scm.com/download/win
    echo.
    echo ��ġ�� ��ģ �� �� â�� �ݰ� �ٽ� ������ �ּ���!
    echo ================================================================
    pause
    exit /b
)

echo [1/3] ���� �� ���� ��Ű�� �ֽ�ȭ ��...
call "%~dp0.venv\Scripts\python.exe" scripts\build_static_site.py

echo.
echo [2/3] Git ����� �ʱ�ȭ �� Ŀ�� ���� ��...
if not exist ".git" (
    git init
    git branch -M main
)
git add .
git commit -m "Deploy PPT Master & Live Interactive Math Studio"

echo.
echo [3/3] GitHub �����(https://github.com/kecfai7/ppt_master.git)�� Ǫ�� ��...
git remote remove origin >nul 2>nul
git remote add origin https://github.com/kecfai7/ppt_master.git
git push -u origin main --force

echo.
echo ================================================================
echo   [����] GitHub ���ε尡 �Ϸ�Ǿ����ϴ�!
echo   Ȯ��: https://github.com/kecfai7/ppt_master
echo ================================================================
echo.
echo   [���� �ܰ�: Vercel ����]
echo   1. https://vercel.com/new �� �����մϴ�.
echo   2. kecfai7 / ppt_master ����� ���� [Import]�� Ŭ���մϴ�.
echo   3. Framework Preset�� [Other] �״�� �ΰ� [Deploy]�� Ŭ���մϴ�!
echo.
echo ================================================================
pause
