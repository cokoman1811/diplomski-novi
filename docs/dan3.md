# Dan 3 — Centralni data loader i stabilizacija projekta

**Datum:** 2026-06-08  
**Autor:** Toni Jakelić

Treći radni dan: ujednačeno učitavanje podataka kroz jedan ulaz, validacija temperaturnog niza, testovi i lakše pokretanje projekta.

## Što je napravljeno

- [x] **`src/data_loader.py`** — dovršen i proširen
  - dodana funkcija **`load_experiment_series()`** kao **jedan centralni ulaz** za eksperimentalne podatke
  - podržani izvori:
    - `demo` → učitava demo CSV po gradu (`temperature_demo_cities.csv`)
    - `jena_quick` → brzi Jena uzorak (npr. 48 h) — **ne učitava cijeli dataset**
    - `jena_full` → cijeli Jena dataset (`jena_climate_2009_2016.csv`)
    - `processed` → već obrađeni podaci iz `data/processed/`
- [x] **Validacija temperaturnog niza** (`_validate_temperature_series`)
  - provjera je li niz prazan
  - provjera NaN vrijednosti
  - provjera duplikata u indeksu
  - provjera vremenskog indeksa (`DatetimeIndex`)
  - provjera da je rezultat uredan `pd.Series`
- [x] **`tests/test_data_loader.py`** — automatski testovi za:
  - demo učitavanje (`source="demo"`)
  - jena_quick učitavanje
  - osnovnu provjeru da funkcije vraćaju ispravan temperaturni niz
- [x] **`run.bat`** — olakšano pokretanje projekta
  - automatski koristi `.venv`
  - instalira potrebne pakete
  - pokreće `main.py`
- [x] **Podaci na disku**
  - `data/raw/jena_climate_2009_2016.csv` — glavni dataset
  - `data/raw/temperature_demo_cities.csv` — demo za brze testove
- [x] **Dokumentacija** — ažurirani `docs/progress.md` i `docs/najcesca_pitanja.md`
- [x] **`scripts/git-sync.ps1`** — sigurniji sync (pull prije pusha)
- [x] **`.gitignore`** — sitna dopuna

## Zašto je `jena_quick` koristan?

Cijeli Jena dataset ima preko 400 000 redova. Za svakodnevni rad i testiranje to je sporo i nepotrebno.

`jena_quick` učitava samo **prvih 48 sati** (288 mjerenja) — dovoljno da provjeriš pipeline, a puno brže od `jena_full`.

## Testirano

```powershell
python -m pytest tests/test_data_loader.py -v
```

ili:

```powershell
.\run.bat
```

## Nove / važne datoteke

| Datoteka | Uloga |
|----------|--------|
| `src/data_loader.py` | `load_experiment_series()` — centralni ulaz za podatke |
| `tests/test_data_loader.py` | Testovi učitavanja |
| `run.bat` | Pokretanje projekta jednim klikom |
| `data/raw/jena_climate_2009_2016.csv` | Glavni dataset |
| `data/raw/temperature_demo_cities.csv` | Demo dataset po gradovima |
| `scripts/git-sync.ps1` | Backup na GitHub |

## Status nakon Dana 3

Projekt je **stabilan** za nastavak rada:

- podaci se učitavaju na jedan predvidljiv način
- validacija hvata uobičajene greške u nizu
- testovi potvrđuju da učitavanje radi
- pokretanje je jednostavnije (`run.bat`)

## Sljedeći dan (Dan 4)

Vidi plan u [progress.md](progress.md) — implementacija klasičnih interpolacijskih metoda (`cubic`, `spline`) i povezivanje s `main.py`.
