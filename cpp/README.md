# Diplomski — C++ kopija

C++17 verzija Python diplomskog projekta (imputacija nedostajućih vrijednosti u
temperaturnim vremenskim nizovima). Bez vanjskih biblioteka — sve je
implementirano u standardnom C++-u (nema pandas / numpy / sklearn / scipy).

## Što odgovara čemu

| Python (`src/`) | C++ (`cpp/`) | Sadržaj |
|-----------------|--------------|---------|
| `config.py` | `include/config.hpp` | konstante (interval, broj sati) |
| `data_loader.py` | `data_loader.{hpp,cpp}` | učitavanje / generiranje niza |
| `preprocessing.py` | `preprocessing.{hpp,cpp}` | umjetno brisanje vrijednosti |
| `interpolation_methods.py` | `interpolation_methods.{hpp,cpp}` | forward fill, linear, time, cubic, spline |
| `ml_methods.py` | `ml_methods.{hpp,cpp}` | KNN imputacija |
| `evaluation.py` | `evaluation.{hpp,cpp}` | MAE, RMSE, R² |
| `pd.Series` | `TimeSeries` | vremenski niz (timestamp + vrijednost, NaN = nedostaje) |
| `main.py` | `src/main.cpp` | CLI `--compare` |
| `app.py` | `src/app.cpp` | stub web aplikacije (nije implementiran) |
| `tests/*.py` | `tests/run_tests.cpp` | testovi (vlastiti mini-harness, bez pytest-a) |

## Razlike u odnosu na Python

- **Podaci:** umjesto preuzimanja Jena dataseta, `synthetic` izvor generira
  realističan 48 h temperaturni niz (dnevni sinusni ciklus + šum). `demo` izvor
  čita CSV (`timestamp,city,temperature`) ako ga imaš.
- **cubic/spline:** implementiran *natural cubic spline* (Numerical Recipes).
  Pandas/scipy koriste malo drukčije rubne uvjete pa brojke neće biti identične,
  ali ponašanje je isto.
- **KNN:** ista logika kao `KNeighborsRegressor` — euklidska udaljenost na
  značajkama `[redni broj, sat, dan u godini]`, prosjek k najbližih.

## Izgradnja

### Opcija A — skripta (Windows)

```powershell
cd cpp
.\build.bat
```

### Opcija B — CMake (svuda)

```powershell
cd cpp
cmake -B build
cmake --build build --config Release
```

### Opcija C — ručno (g++)

```powershell
cd cpp
g++ -std=c++17 -O2 -Iinclude src/*.cpp -o thesis.exe
```

## Pokretanje

```powershell
.\thesis.exe --compare
.\thesis.exe --compare --missing-rate 0.3
.\thesis.exe --compare --neighbors 7
.\thesis.exe --compare --source demo --csv ..\data\raw\temperature_demo_cities.csv --city Split
```

## Testovi

```powershell
.\tests.exe
```

Ispisuje provjere za KNN, preprocessing, interpolacije i metrike te na kraju
sažetak prolaza/padova (ekvivalent `pytest` testovima iz Python verzije).

## Kompajler (jednom)

C++ se ne može pokrenuti samo iz editora — treba kompajler. Bilo koji od:

- **MinGW-w64 (g++)**: `winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT`
- **LLVM (clang)**: `winget install -e --id LLVM.LLVM`
- **MSVC**: Visual Studio Build Tools (C++ workload)

Nakon instalacije otvori novi terminal pa pokreni `.\build.bat`.
