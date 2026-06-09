@echo off
cd /d "%~dp0"

where gcc >nul 2>nul
if errorlevel 1 (
    echo gcc nije pronaden. Instaliraj MinGW-w64 ili dodaj gcc u PATH.
    echo Npr.: winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT
    exit /b 1
)

if not exist build mkdir build

echo Kompajliram...
gcc -std=c99 -O2 -Wall -Wextra src\*.c -o diplomski.exe -lm
if errorlevel 1 (
    echo Greska pri kompajliranju.
    exit /b 1
)

echo Gotovo: diplomski.exe
