# Najčešća pitanja

## Što je pandas?

To je biblioteka u Pythonu za rad s tablicama i vremenskim nizovima.

Na početku datoteke obično piše:

```python
import pandas as pd
```

`pd` je samo **kratko ime** za cijelu pandas biblioteku — kao da joj daš nadimak da ne moraš svaki put pisati `pandas`.

Znači: **`pd` je alatna kutija.**

U toj kutiji postoje različiti alati:

| Alat | Za što služi u projektu |
|------|-------------------------|
| `pd.DataFrame` | tablica s više stupaca |
| `pd.Series` | jedan stupac (niz vrijednosti) |
| `pd.read_csv` | učitavanje CSV datoteke u tablicu |
| `pd.to_numeric` | pretvaranje teksta u broj |
| `pd.to_datetime` | pretvaranje teksta u datum/vrijeme |

Kad vidiš `pd.nešto`, znači: *"uzmi alat `nešto` iz pandas kutije"*.

## Što je Series?

Jedan od alata u kutiji je `pd.Series` — koristi se za **jedan stupac** podataka.

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

## Što je DataFrame?

Za **tablicu** (više stupaca odjednom) iz pandas kutije uzimamo alat `pd.DataFrame`.

Primjer — demo CSV s gradovima. Ovdje koristimo dva alata odjednom:

```python
data = pd.read_csv("data/raw/temperature_demo_cities.csv")   # read_csv → učitaj datoteku
# rezultat je pd.DataFrame
```

Kad treba provjeriti brojeve ili datume u tablici, koriste se i ostali alati:

```python
data["timestamp"] = pd.to_datetime(data["timestamp"])   # tekst → datum/vrijeme
temperature = pd.to_numeric(data["temperature"])        # tekst → broj
```

`data` je `DataFrame`. Izgleda kao Excel tablica:

| timestamp | city | temperature |
|-----------|------|-------------|
| 2024-01-01 00:00:00 | Split | 9.2 |
| 2024-01-01 01:00:00 | Split | 9.0 |

Razlika u projektu:

- `pd.DataFrame` — cijela tablica (svi stupci)
- `pd.Series` — jedan stupac (npr. samo temperatura s vremenom kao indeksom)

U `data_loader.py` prvo učitamo `DataFrame` iz CSV-a, a zatim iz njega izvučemo jedan `Series` za eksperimente.

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
