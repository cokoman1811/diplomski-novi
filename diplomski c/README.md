# Diplomski — C verzija

C (C99) implementacija eksperimenta za usporedbu klasičnih i strojno-učenih
metoda imputacije nedostajućih vrijednosti u temperaturnim vremenskim nizovima.

Ovo je C inačica glavnog (Python) diplomskog rada koji se nalazi u korijenskoj mapi.
Sve metode (interpolacija, KNN, metrike) pisane su ručno, bez vanjskih biblioteka.

## Sadržaj

```
diplomski c/
├── src/
│   ├── series.h / dataset.c    # struktura niza, učitavanje CSV-a, parsiranje datuma
│   ├── preprocessing.*         # umjetno uklanjanje vrijednosti (RNG)
│   ├── interpolation.*         # forward fill, linear, time, cubic, spline
│   ├── ml_methods.*            # KNN imputacija
│   ├── evaluation.*            # MAE, RMSE, R²
│   └── main.c                  # CLI
├── data/                       # kopije ulaznih CSV podataka
├── Makefile                    # build (Linux/macOS/MinGW)
├── build.bat                   # build na Windowsu (gcc)
└── run.bat                     # build + pokretanje na Windowsu
```

## Build i pokretanje

Pokretati iz ove mape (`diplomski c`) jer se podaci čitaju relativno (`data/...`).

### Windows (gcc / MinGW-w64)

```powershell
cd "diplomski c"
.\build.bat
.\diplomski.exe --compare
.\diplomski.exe --compare --source demo --city Split
.\diplomski.exe --compare --missing-rate 0.3
```

> Treba `gcc` u PATH-u: `winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT`

### Linux / macOS

```bash
cd "diplomski c"
make
./diplomski --compare
```

## Argumenti

| Argument | Zadano | Opis |
|----------|--------|------|
| `--compare` | — | pokreni usporedbu metoda |
| `--source` | `jena_quick` | `jena_quick` \| `processed` \| `demo` |
| `--city` | `Split` | grad (samo za `demo`) |
| `--missing-rate` | `0.4` | udio umjetno uklonjenih vrijednosti |

## Implementirane metode

`forward_fill`, `linear_interpolation`, `time_interpolation`,
`cubic_interpolation`, `spline_interpolation` (prirodni kubični spline),
`knn_imputation` (značajke: pozicija, sat, dan u godini).
