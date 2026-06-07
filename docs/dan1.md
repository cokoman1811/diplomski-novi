# Dan 1 — Učitavanje podataka

**Datum:** 2026-06-06  
**Autor:** Toni Jakelić

Prvi radni dan na implementaciji: postavljen je osnovni pipeline za preuzimanje i učitavanje temperaturnih vremenskih nizova.

## Što je napravljeno

- [x] Konfiguracija projekta (`src/config.py`) — URL Jena dataseta, nazivi stupaca, interval mjerenja (10 min), quick sample (48 h)
- [x] Putanje i mape (`src/paths.py`) — `data/raw/`, `data/processed/`
- [x] Preuzimanje dataseta (`src/download_data.py`) — automatski download i raspakiravanje Jena Climate CSV-a
- [x] Učitavanje podataka (`src/data_loader.py`):
  - demo CSV s više gradova (Split, Zagreb)
  - puni Jena temperaturni niz (2009–2016)
  - rezani uzorak za brzi test (prvih 48 h)
- [x] CLI ulazna točka (`src/main.py`) — naredbe `--download`, `--quick`, `--demo`, `--city`
- [x] Interaktivni unos grada u demo načinu
- [x] Automatsko virtualno okruženje (`main.py` u korijenu) — kreira `.venv` i instalira pakete pri prvom pokretanju
- [x] Ažuriran `README.md` s uputama za pokretanje

## Testirano

```powershell
python main.py --download
python main.py --quick
python main.py --demo --city Split
```

**Rezultat (`--quick`):**
- Učitano **288 mjerenja** (48 h × 6 mjerenja/h, interval 10 min)
- Razdoblje: 2009-01-01 00:10 → 2009-01-03 00:00
- Izlaz spremljen u `data/processed/jena_temperature_48h.csv`

## Nove datoteke

| Datoteka | Uloga |
|----------|--------|
| `src/config.py` | Konstante (dataset, stupci, quick mode) |
| `src/paths.py` | Putanje do `data/raw` i `data/processed` |
| `src/download_data.py` | Preuzimanje Jena Climate dataseta |
| `src/data_loader.py` | Učitavanje temperaturnih nizova u `pandas.Series` |
| `src/main.py` | CLI i ispisi (head/tail, spremanje CSV-a) |

## Dataset

**Jena Climate** — meteorološka stanica u Jeni (Njemačka), 2009–2016, mjerenja svakih 10 minuta.

- Raw: `data/raw/jena_climate_2009_2016.csv`
- Processed (quick): `data/processed/jena_temperature_48h.csv`

## Naredbe

```powershell
python main.py --download        # preuzmi Jena dataset (jednom)
python main.py --quick           # brzi test — prvih 48 h temperature
python main.py --demo            # demo s gradovima Split/Zagreb
python main.py --demo --city Split
```

## Sljedeći dan

Na Danu 1 riješeno je **učitavanje**. Sljedeći korak bio je eksperimentalni tok — vidi [Dan 2](dan2.md).
