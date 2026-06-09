# Diplomski rad — Toni Jakelić

**Radni naslov:** Usporedba klasičnih i strojno-učenih metoda za imputaciju nedostajućih podataka u vremenskim nizovima

**Autor:** Toni Jakelić  
**Godina:** 2026.

## O projektu

Cilj rada je usporediti klasične metode interpolacije i metode strojnog učenja u zadatku popunjavanja nedostajućih vrijednosti u temperaturnim vremenskim nizovima. Cijeli eksperimentalni sustav implementiran je u **programskom jeziku C** (standard C99), bez vanjskih biblioteka — sve metode (interpolacija, KNN, metrike) pisane su ručno.

Tok eksperimenta:

1. učitaj originalni temperaturni niz iz CSV-a
2. umjetno ukloni dio vrijednosti (pamti se `missing_mask`)
3. rekonstruiraj uklonjene vrijednosti različitim metodama
4. usporedi rekonstrukciju s originalom **samo na uklonjenim mjestima**
5. izračunaj MAE, RMSE i R²

### Implementirane metode

| Metoda | Opis |
|--------|------|
| `forward_fill` | popuna zadnjom poznatom vrijednošću |
| `linear_interpolation` | linearna interpolacija po poziciji |
| `time_interpolation` | linearna interpolacija po stvarnom vremenu |
| `cubic_interpolation` | prirodni kubični spline |
| `spline_interpolation` | spline reda 3 (ista jezgra) |
| `knn_imputation` | K-najbližih susjeda (značajke: pozicija, sat, dan u godini) |

## Struktura

```
diplomski-kopija/
├── src/                    # C izvorni kod
│   ├── series.h / dataset.c    # struktura niza + učitavanje CSV-a, parsiranje datuma
│   ├── preprocessing.*         # umjetno uklanjanje vrijednosti (RNG)
│   ├── interpolation.*         # klasične metode
│   ├── ml_methods.*            # KNN imputacija
│   ├── evaluation.*            # MAE, RMSE, R²
│   └── main.c                  # CLI (--compare, --source, --city, --missing-rate)
├── data/                   # ulazni podaci (CSV)
├── docs/                   # projektna dokumentacija
├── Makefile                # build (Linux/macOS/MinGW)
├── build.bat               # build na Windowsu (gcc)
├── run.bat                 # build + pokretanje na Windowsu
├── rad.md                  # tekst diplomskog rada
└── KORACI.md               # log napretka
```

## Build i pokretanje

### Windows (gcc / MinGW-w64)

```powershell
.\build.bat                       # kompajliraj -> diplomski.exe
.\run.bat --compare               # build (ako treba) + usporedba
.\diplomski.exe --compare --source demo --city Split
.\diplomski.exe --compare --missing-rate 0.3
```

> Treba `gcc` u PATH-u. Instalacija: `winget install -e --id BrechtSanders.WinLibs.POSIX.UCRT`

### Linux / macOS

```bash
make            # kompajliraj
make run        # build + ./diplomski --compare
./diplomski --compare --source jena_quick
```

### Argumenti

| Argument | Zadano | Opis |
|----------|--------|------|
| `--compare` | — | pokreni usporedbu metoda |
| `--source` | `jena_quick` | izvor: `jena_quick` \| `processed` \| `demo` |
| `--city` | `Split` | grad (samo za `demo`) |
| `--missing-rate` | `0.4` | udio umjetno uklonjenih vrijednosti |

## Podaci

- `data/processed/jena_temperature_48h.csv` — prvih 48 h Jena Climate temperature (288 mjerenja svakih 10 min)
- `data/raw/temperature_demo_cities.csv` — mali demo s gradovima Split/Zagreb

## Git i backup

```powershell
.\scripts\git-sync.ps1            # commit + push
```

U chatu: `@git-sync uploadaj sve na git`
