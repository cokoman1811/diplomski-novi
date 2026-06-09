@echo off
REM Izgradnja C++ kopije diplomskog (bez CMake-a).
REM Trazi g++ (MinGW) pa fallback na MSVC cl. Gradi: thesis, app, tests.

set CORE=src\time_series.cpp src\data_loader.cpp src\preprocessing.cpp src\interpolation_methods.cpp src\ml_methods.cpp src\evaluation.cpp

where g++ >nul 2>nul
if %ERRORLEVEL%==0 (
    echo Kompajliram s g++...
    g++ -std=c++17 -O2 -Iinclude src\main.cpp %CORE% -o thesis.exe || goto :err
    g++ -std=c++17 -O2 -Iinclude src\app.cpp -o app.exe || goto :err
    g++ -std=c++17 -O2 -Iinclude tests\run_tests.cpp %CORE% -o tests.exe || goto :err
    goto :ok
)

where cl >nul 2>nul
if %ERRORLEVEL%==0 (
    echo Kompajliram s MSVC cl...
    cl /nologo /std:c++17 /EHsc /O2 /Iinclude src\main.cpp %CORE% /Fe:thesis.exe || goto :err
    cl /nologo /std:c++17 /EHsc /O2 /Iinclude src\app.cpp /Fe:app.exe || goto :err
    cl /nologo /std:c++17 /EHsc /O2 /Iinclude tests\run_tests.cpp %CORE% /Fe:tests.exe || goto :err
    goto :ok
)

echo Nije pronaden ni g++ ni cl. Instaliraj MinGW-w64 ili Visual Studio Build Tools.
goto :eof

:ok
echo.
echo Spremno. Pokreni:
echo   thesis.exe --compare
echo   tests.exe
goto :eof

:err
echo Greska pri kompajliranju.
exit /b 1
