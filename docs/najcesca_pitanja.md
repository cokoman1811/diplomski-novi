# Najčešća pitanja

## Što je pandas?

To je biblioteka u pythonu za rad sa datotekama.

## Što je Series?

```python
series = pd.Series(
    data=temperature.values,
    index=pd.DatetimeIndex(data["timestamp"]),
    name="temperature",
)
```

Series se sastoji od:
- `data` — samo vrijednosti temperatura
- `index` — samo tu da označi vrijeme
- `name="temperature"` — ime temperature

## Što je `_validate_series`?

```python
def _validate_series(series: pd.Series) -> None:
```

Definira funkciju koja uspoređuje `series` s `pd.Series` i ne vraća ništa (`None`).

## Što su `JENA_QUICK_PROCESSED_CSV`, `DEMO_CSV` i `DEFAULT_DEMO_CITY`?

U `src/data_loader.py` ove tri konstante kažu programu **odakle učitati podatke**.

```python
JENA_QUICK_PROCESSED_CSV = PROCESSED_DIR / "jena_temperature_48h.csv"
DEMO_CSV = RAW_DIR / "temperature_demo_cities.csv"
DEFAULT_DEMO_CITY = "Split"
```

### Kako se sklapa putanja do datoteke?

`PROCESSED_DIR` i `RAW_DIR` dolaze iz `src/paths.py`. To su **mape (folderi)** u projektu:

- `RAW_DIR` → `data/raw/` — sirovi ulazni podaci
- `PROCESSED_DIR` → `data/processed/` — obrađeni podaci koje program sam spremi

Znak `/` u Pythonu ovdje **ne znači dijeljenje**, nego **spajanje mape i imena datoteke**.

Primjer za Jena quick mode:

```text
PROCESSED_DIR  +  "jena_temperature_48h.csv"
     ↓                        ↓
data/processed/     jena_temperature_48h.csv
     ↓
data/processed/jena_temperature_48h.csv
```

Dakle:

| Konstanta | Mapa | Datoteka na kraju | Puna putanja |
|-----------|------|-------------------|--------------|
| `JENA_QUICK_PROCESSED_CSV` | `PROCESSED_DIR` (`data/processed/`) | `jena_temperature_48h.csv` | `data/processed/jena_temperature_48h.csv` |
| `DEMO_CSV` | `RAW_DIR` (`data/raw/`) | `temperature_demo_cities.csv` | `data/raw/temperature_demo_cities.csv` |

`jena_temperature_48h.csv` nastaje kad pokreneš:

```powershell
python main.py --quick
```

To je rezani Jena uzorak — prvih 48 sati temperature.

### Što je `DEFAULT_DEMO_CITY`?

To nije putanja, nego **zadani grad** za demo način.

Ako pozoveš `load_experiment_series("demo")` bez `city=...`, program uzme **Split**.

Za drugi grad:

```python
load_experiment_series("demo", city="Zagreb")
```
