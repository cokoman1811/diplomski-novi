@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Kreiram virtualno okruzenje...
    "C:\Users\ttonjak\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
    if errorlevel 1 (
        echo Python nije pronaden. Instaliraj Python 3.12 pa pokreni ponovo.
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
)

".venv\Scripts\python.exe" main.py %*
