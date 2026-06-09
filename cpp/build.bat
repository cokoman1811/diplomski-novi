@echo off
REM Jednostavna izgradnja C++ kopije diplomskog (bez CMake-a).
REM Trazi g++ (MinGW) pa fallback na MSVC cl.

where g++ >nul 2>nul
if %ERRORLEVEL%==0 (
    echo Kompajliram s g++...
    g++ -std=c++17 -O2 -Iinclude src\*.cpp -o thesis.exe
    if %ERRORLEVEL%==0 (
        echo Spremno: thesis.exe
        echo Pokreni: thesis.exe --compare
    )
    goto :eof
)

where cl >nul 2>nul
if %ERRORLEVEL%==0 (
    echo Kompajliram s MSVC cl...
    cl /std:c++17 /EHsc /O2 /Iinclude src\*.cpp /Fe:thesis.exe
    if %ERRORLEVEL%==0 (
        echo Spremno: thesis.exe
        echo Pokreni: thesis.exe --compare
    )
    goto :eof
)

echo Nije pronaden ni g++ ni cl. Instaliraj MinGW-w64 ili Visual Studio Build Tools.
