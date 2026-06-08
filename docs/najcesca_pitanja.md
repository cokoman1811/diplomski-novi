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

## Što je `iloc`?

`iloc` uzima podatke iz tablice ili niza **po redu** — broj reda, ne po datumu ili imenu.

Redovi se broje od 0:

| Red (`iloc`) | Vrijeme | Temperatura |
|--------------|---------|-------------|
| 0 | 2009-01-01 00:10 | -8.02 |
| 1 | 2009-01-01 00:20 | -8.41 |
| 2 | 2009-01-01 00:30 | -8.51 |

Primjeri:

```python
series.iloc[0]      # prvi red
series.iloc[5]      # šesti red
series.iloc[:288]   # prvih 288 redova (od 0 do 287)
```

U `data_loader.py` quick mode uzima prvih 48 sati ovako:

```python
series.iloc[:samples]
```

Znači: *"daj mi samo prvih `samples` redova od početka niza"*.

`iloc` radi i na `DataFrame` i na `Series` — uvijek gleda **poziciju reda**, ne vrijednost indeksa.

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

## Što znači `source="jena_quick"`?

`load_experiment_series()` prima parametar `source` koji kaže **odakle učitati podatke**.

```python
series = load_experiment_series("jena_quick")
```

`"jena_quick"` znači: *"učitaj samo mali Jena uzorak (npr. prvih 48 sati), ne cijeli dataset"*.

| `source` | Što učitava |
|----------|-------------|
| `"demo"` | demo CSV po gradu |
| `"jena_quick"` | brzi Jena uzorak (~48 h) |
| `"jena_full"` | cijeli Jena dataset |
| `"processed"` | već obrađena datoteka iz `data/processed/` |

## Zašto koristimo mali uzorak prije cijelog dataseta?

Cijeli Jena dataset ima **preko 400 000 redova**. To je:

- **sporo** za učitavanje i testiranje
- **teško za debug** kad nešto ne radi
- **nepotrebno** dok razvijaš i provjeravaš kod

Zato prvo radimo s `jena_quick` ili `demo`. Kad pipeline radi ispravno, prelazimo na `jena_full` za ozbiljnije eksperimente.

## Što je interpolacija?

**Interpolacija** (u ovom projektu: **imputacija**) znači **popunjavanje nedostajućih vrijednosti** u vremenskom nizu temperature.

Primjer — originalni niz ima rupu:

| Vrijeme | Temperatura |
|---------|-------------|
| 10:00 | 5.0 |
| 10:10 | *nedostaje* |
| 10:20 | 7.0 |

Interpolacija procjenjuje što je bilo u 10:10 (npr. 6.0) na temelju susjednih poznatih vrijednosti.

U projektu prvo **umjetno uklonimo** neke vrijednosti (`create_missing_values`), pa metode pokušaju vratiti original i usporedimo koliko su bile točne (MAE, RMSE, R²).

## Razlika između metoda interpolacije (ukratko)

| Metoda | Ideja | Kada je dobra |
|--------|-------|---------------|
| **forward_fill** | kopira zadnju poznatu vrijednost unaprijed | jednostavno, ali loše kad temperatura brzo pada/raste |
| **linear** | ravna linija između dva susjeda | dobro za kratke praznine, jednostavno |
| **time** | linearno, ali uz obzir **stvarnog vremena** između mjerenja | bolje kad su razmaci u vremenu različiti |
| **cubic** | glatka krivulja (kubični polinom) kroz više točaka | glađi rezultat, može „previše valovati“ |
| **spline** | spline krivulja — glatka, fleksibilnija od linearne | dobro za glatke temperature, treba dovoljno poznatih točaka |

U Danu 2 već rade `forward_fill`, `linear` i `time`. U **Danu 4** dodajemo `cubic` i `spline` te sve povezujemo u `main.py`.
