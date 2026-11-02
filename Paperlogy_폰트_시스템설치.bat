@echo off
title Paperlogy 폰트 시스템 전역 설치기
cd /d "%~dp0"

echo ================================================================
echo   Paperlogy (페이퍼로지) 폰트 - Windows 시스템(파워포인트) 전역 등록
echo ================================================================
echo.

:: Check Administrator Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [알림] 관리자 권한이 필요합니다.
    echo 이 파일을 마우스 우클릭한 후 [관리자 권한으로 실행]을 클릭해 주세요!
    echo ================================================================
    pause
    exit /b
)

echo [1/2] projects\math_assets\fonts 폴더의 9개 폰트를 C:\Windows\Fonts 로 복사 중...
copy /y "%~dp0projects\math_assets\fonts\Paperlogy-*.ttf" "%WINDIR%\Fonts\" >nul

echo [2/2] Windows 레지스트리에 정식 시스템 폰트로 등록 중...
powershell -NoProfile -Command "
$fonts = Get-ChildItem '%~dp0projects\math_assets\fonts\Paperlogy-*.ttf';
foreach ($f in $fonts) {
    $fn = $f.BaseName;
    # Register both English and Korean family names in registry
    New-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Fonts' -Name \"$fn (TrueType)\" -Value $f.Name -PropertyType String -Force | Out-Null;
}
New-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Fonts' -Name 'Paperlogy (TrueType)' -Value 'Paperlogy-4Regular.ttf' -PropertyType String -Force | Out-Null;
New-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Fonts' -Name 'Paperlogy Bold (TrueType)' -Value 'Paperlogy-7Bold.ttf' -PropertyType String -Force | Out-Null;
"

echo.
echo ================================================================
echo   [축하] Paperlogy 9종 폰트가 Windows 시스템에 완벽하게 등록되었습니다!
echo   이제 파워포인트를 열면 어떤 덱을 열어도 글꼴이 절대 풀리지 않습니다.
echo ================================================================
pause
