@echo off
cd /d "%~dp0"

if not exist diplomski.exe (
    call build.bat
    if errorlevel 1 exit /b 1
)

diplomski.exe %*
