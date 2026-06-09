# Najčešća pitanja

Kratki vodič kroz pojmove i naredbe u diplomskom projektu — od pokretanja programa do interpolacije.

---

## Sadržaj

1. [Pokretanje projekta](#1-pokretanje-projekta)
   - [Što je `.venv`?](#što-je-venv)
   - [Što je `run.bat`?](#što-je-runbat)
   - [Kako pokrenuti stvari ispravno](#kako-pokrenuti-stvari-ispravno)
2. [Pandas i podaci](#2-pandas-i-podaci)
   - [Što je pandas?](#što-je-pandas)
   - [Što je `Series`?](#što-je-series)
   - [Što je `DataFrame`?](#što-je-dataframe)
   - [Što je `iloc`?](#što-je-iloc)
   - [Što je `_validate_series`?](#što-je-_validate_series)
3. [Učitavanje podataka](#3-učitavanje-podataka)
   - [Tutorial: izvori podataka](#tutorial-izvori-podataka)
   - [Konstante u `data_loader.py`](#konstante-u-data_loaderpy)
   - [Zašto mali uzorak prije cijelog dataseta?](#zašto-mali-uzorak-prije-cijelog-dataseta)
4. [Interpolacija](#4-interpolacija)
   - [Što je interpolacija?](#što-je-interpolacija)
   - [Razlika između metoda](#razlika-između-metoda)
   - [Što je scipy?](#što-je-scipy)
   - [Zašto prvo klasične metode?](#zašto-prvo-klasične-metode)

---

## 1. Pokretanje projekta

### Što je `.venv`?

**venv** = **virtualno okruženje** — posebna „kutija“ Pythona samo za ovaj projekt.

Na računalu možeš imati više Python instalacija i puno paketa (`pandas`, `pytest`, `sklearn`…). Bez venv-a svi projekti dijele isti Python i lako dođe do konflikta:

- jedan projekt traži `pandas 2.2`, drugi stariju verziju
- `pytest` je instaliran u jednom env-u, a ti pokreneš drugi Python → `No module named pytest`

Virtualno okruženje rješava to: **ovaj diplomski projekt ima svoje pakete u mapi `.venv`**, odvojeno od ostatka sustava.

**Gdje je u projektu?**

```
novi diplomski/
├── .venv/              ← virtualno okruženje (Python + paketi)
│   └── Scripts/
│       └── python.exe  ← Python samo za ovaj projekt
├── requirements.txt    ← popis paketa koje venv treba imati
├── main.py             ← pri pokretanju sam koristi .venv
└── run.bat             ← isto — aktivira .venv
```

Prvi put kad pokreneš `python main.py` ili `run.bat`, projekt **sam kreira** `.venv` i instalira pakete iz `requirements.txt`.

**Analogija**

| Pojam | Značenje |
|-------|----------|
| Sistemski Python | zajednička kuhinja u zgradi — svi je koriste, nered često |
| `.venv` | tvoja privatna kuhinja / garaža s alatom i motorom — znaš točno što je unutra |
| `run.bat` | ključ koji upali auto — jedan klik i program krene s motorom iz garaže |

### Što je `run.bat`?

`run.bat` je Windows skripta u korijenu projekta. Pokreće diplomski jednim klikom ili iz terminala (`.\run.bat`).

**Što radi korak po korak:**

```
run.bat
   ↓
provjeri postoji li .venv
   ↓
ako nema .venv, napravi ga
   ↓
instalira pakete iz requirements.txt
   ↓
pokrene main.py
```

**Razlika između `.venv` i `run.bat`**

| | Što je |
|---|--------|
| **`.venv`** | mjesto gdje su Python i paketi |
| **`run.bat`** | skripta koja koristi taj `.venv` i pokreće projekt |

Ne trebaš ručno „ulaziti“ u venv svaki dan — `main.py` i `run.bat` to rade umjesto tebe.

### Kako pokrenuti stvari ispravno

**Dva Pythona — česta zamka**

| Naredba | Koji Python | Ima projektne pakete? |
|---------|-------------|------------------------|
| `python -m pytest` | često Windows Store Python | ❌ obično ne |
| `.\.venv\Scripts\python.exe -m pytest` | projektni `.venv` | ✅ da |

Zato testovi ponekad „ne rade“ iako Python jest instaliran — pokrenuo si **krivi** Python.

**Naredbe**

Testovi (pytest):
```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Glavni program (sam prebaci na venv):
```powershell
python main.py --compare
```
ili:
```powershell
.\run.bat --compare
```

Ručna test skripta (npr. `test_metrics.py`):
```powershell
.\.venv\Scripts\python.exe tests/test_metrics.py
```

> Za `pytest` u terminalu eksplicitno koristi `.\.venv\Scripts\python.exe`.

---

## 2. Pandas i podaci

### Što je pandas?

Biblioteka u Pythonu za rad s tablicama i vremenskim nizovima.

```python
import pandas as pd
```

`pd` je samo **kratko ime** za cijelu pandas biblioteku — kao nadimak da ne moraš svaki put pisati `pandas`.

Znači: **`pd` je alatna kutija.** Kad vidiš `pd.nešto`, znači: *"uzmi alat `nešto` iz pandas kutije"*.

| Alat | Za što služi u projektu |
|------|-------------------------|
| `pd.DataFrame` | tablica s više stupaca |
| `pd.Series` | jedan stupac (niz vrijednosti) |
| `pd.read_csv` | učitavanje CSV datoteke u tablicu |
| `pd.to_numeric` | pretvaranje teksta u broj |
| `pd.to_datetime` | pretvaranje teksta u datum/vrijeme |

### Što je `Series`?

Alat za **jedan stupac** podataka.

```python
series = pd.Series(
    data=temperature.values,
    index=pd.DatetimeIndex(data["timestamp"]),
    name="temperature",
)
```

Series se sastoji od:

- `data` — vrijednosti (npr. temperature)
- `index` — oznake vremena
- `name` — ime stupca (npr. `"temperature"`)

### Što je `DataFrame`?

Alat za **tablicu** s više stupaca odjednom.

```python
data = pd.read_csv("data/raw/temperature_demo_cities.csv")   # učitaj datoteku
# rezultat je pd.DataFrame
```

Kad treba provjeriti brojeve ili datume u tablici:

```python
data["timestamp"] = pd.to_datetime(data["timestamp"])   # tekst → datum/vrijeme
temperature = pd.to_numeric(data["temperature"])        # tekst → broj
```

`data` izgleda kao Excel tablica:

| timestamp | city | temperature |
|-----------|------|-------------|
| 2024-01-01 00:00:00 | Split | 9.2 |
| 2024-01-01 01:00:00 | Split | 9.0 |

**Razlika u projektu**

| Tip | Što predstavlja |
|-----|-----------------|
| `pd.DataFrame` | cijela tablica (svi stupci) |
| `pd.Series` | jedan stupac (npr. samo temperatura s vremenom kao indeksom) |

U `data_loader.py` prvo učitamo `DataFrame` iz CSV-a, zatim iz njega izvučemo jedan `Series` za eksperimente.

### Što je `iloc`?

`iloc` uzima podatke **po broju reda** — ne po datumu ili imenu. Redovi se broje od 0.

| Red (`iloc`) | Vrijeme | Temperatura |
|--------------|---------|-------------|
| 0 | 2009-01-01 00:10 | -8.02 |
| 1 | 2009-01-01 00:20 | -8.41 |
| 2 | 2009-01-01 00:30 | -8.51 |

```python
series.iloc[0]      # prvi red
series.iloc[5]      # šesti red
series.iloc[:288]   # prvih 288 redova (od 0 do 287)
```

U `data_loader.py` quick mode uzima prvih 48 sati ovako:

```python
series.iloc[:samples]
```

Znači: *"daj mi samo prvih `samples` redova od početka niza"*. Radi i na `DataFrame` i na `Series`.

### Što je `_validate_series`?

```python
def _validate_series(series: pd.Series) -> None:
```

Pomoćna funkcija u `data_loader.py` koja provjerava je li proslijeđeni objekt stvarno `pd.Series` (ima li podatke, ispravan je li indeks). Ako nije — baca grešku prije nego što eksperiment krene s krivim tipom podataka.

---

## 3. Učitavanje podataka

### Tutorial: izvori podataka

U projektu postoje **4 izvora** (`source`). Svi se koriste kroz jednu funkciju:

```python
from src.data_loader import load_experiment_series

series = load_experiment_series("jena_quick")           # zadano
series = load_experiment_series("demo", city="Split")
series = load_experiment_series("jena_full")
series = load_experiment_series("processed")
```

Iz terminala isti izvori idu preko `--compare --source ...`.

#### Pregled — što je što?

| `source` | Odakle čita | Koliko podataka | Kada koristiti |
|----------|-------------|-----------------|----------------|
| **`demo`** | `data/raw/temperature_demo_cities.csv` | ~12 h po gradu (Split, Zagreb) | Najbrži test — **ne treba** Jena download |
| **`jena_quick`** | `data/raw/jena_climate_2009_2016.csv` (reže prvih 48 h u memoriji) | 288 mjerenja (10 min interval) | **Zadano** za razvoj i `--compare` |
| **`processed`** | `data/processed/jena_temperature_48h.csv` | 48 h, već spremljeno na disk | Kad želiš fiksnu datoteku koju je program sam napravio |
| **`jena_full`** | `data/raw/jena_climate_2009_2016.csv` (cijeli file) | 400 000+ redova | Finalni / ozbiljni eksperimenti |

**Važna razlika:** `jena_quick` i `processed` daju sličan uzorak (~48 h), ali:
- `jena_quick` — svaki put reže iz **raw** Jena dataseta u memoriji
- `processed` — čita **već spremljenu** CSV iz `data/processed/`

#### Priprema podataka (prvi put)

```
demo          → ništa, CSV je već u projektu
jena_quick    → python main.py --download   (jednom)
jena_full     → python main.py --download   (jednom)
processed     → python main.py --download
              → python main.py --quick      (stvara data/processed/jena_temperature_48h.csv)
```

#### Naredbe iz terminala

**Priprema i pregled podataka** (bez usporedbe metoda):

```powershell
# Preuzmi Jena dataset u data/raw/
python main.py --download

# Spremi prvih 48 h Jene u data/processed/
python main.py --quick

# Pregled demo podataka za grad (sprema u processed/)
python main.py --demo --city Split
python main.py --demo --city Zagreb
```

**Usporedba interpolacijskih metoda** (`--compare`):

```powershell
# Zadano: jena_quick (najčešće za svakodnevni rad)
python main.py --compare

# Eksplicitno isto
python main.py --compare --source jena_quick

# Demo — mali CSV, bez Jene
python main.py --compare --source demo --city Split
python main.py --compare --source demo --city Zagreb

# Iz spremljene 48h datoteke
python main.py --compare --source processed

# Cijeli Jena dataset (sporo!)
python main.py --compare --source jena_full

# Promijeni koliko vrijednosti se briše (zadano 40%)
python main.py --compare --source jena_quick --missing-rate 0.3
```

Isto preko `run.bat`:

```powershell
.\run.bat --compare
.\run.bat --compare --source demo --city Zagreb
```

#### U Python kodu / testovima

```python
from src.data_loader import load_experiment_series

# Brzi test — zadano
series = load_experiment_series("jena_quick")

# Demo grad (bez city → Split)
series = load_experiment_series("demo")
series = load_experiment_series("demo", city="Zagreb")

# Iz processed mape (mora postojati jena_temperature_48h.csv)
series = load_experiment_series("processed")

# Cijeli Jena (sporo, treba download)
series = load_experiment_series("jena_full")
```

#### Koji izvor odabrati? (brzi vodič)

```
Brzo testiram kod ili pokrećem pytest?
  → demo  ili  jena_quick

Radim --compare svaki dan?
  → jena_quick  (zadano, ne moraš pisati --source)

Želim fiksnu datoteku na disku za eksperiment?
  → python main.py --quick
  → zatim --source processed

Pišem diplomski / finalne rezultate?
  → jena_full  (nakon što sve radi na jena_quick)
```

#### Česte greške

| Greška | Uzrok | Rješenje |
|--------|-------|----------|
| `Jena Climate datoteka ne postoji` | Nema raw Jena CSV-a | `python main.py --download` |
| `Obrađena CSV datoteka ne postoji` | Nema `jena_temperature_48h.csv` | `python main.py --quick` |
| `Nema podataka za grad: X` | Krivi naziv grada u demo | Koristi `Split` ili `Zagreb` |
| `--compare --source demo` bez grada | Program uzima **Split** kao zadani grad | Dodaj `--city Zagreb` ako treba |

### Konstante u `data_loader.py`

Tri konstante kažu programu **odakle učitati podatke**:

```python
JENA_QUICK_PROCESSED_CSV = PROCESSED_DIR / "jena_temperature_48h.csv"
DEMO_CSV = RAW_DIR / "temperature_demo_cities.csv"
DEFAULT_DEMO_CITY = "Split"
```

`PROCESSED_DIR` i `RAW_DIR` dolaze iz `src/paths.py`:

| Konstanta | Mapa | Datoteka |
|-----------|------|----------|
| `JENA_QUICK_PROCESSED_CSV` | `data/processed/` | `jena_temperature_48h.csv` |
| `DEMO_CSV` | `data/raw/` | `temperature_demo_cities.csv` |

Znak `/` u Pythonu ovdje **ne znači dijeljenje**, nego **spajanje mape i imena datoteke**:

```text
PROCESSED_DIR  +  "jena_temperature_48h.csv"
     ↓                        ↓
data/processed/     jena_temperature_48h.csv
     ↓
data/processed/jena_temperature_48h.csv
```

`jena_temperature_48h.csv` nastaje kad pokreneš:

```powershell
python main.py --quick
```

To je rezani Jena uzorak — prvih 48 sati temperature.

**`DEFAULT_DEMO_CITY`** nije putanja, nego **zadani grad** za demo način. Ako pozoveš `load_experiment_series("demo")` bez `city=...`, program uzme **Split**. Za drugi grad:

```python
load_experiment_series("demo", city="Zagreb")
```

Vidi [Tutorial: izvori podataka](#tutorial-izvori-podataka) za sve naredbe i primjere.

### Zašto mali uzorak prije cijelog dataseta?

Cijeli Jena dataset ima **preko 400 000 redova**. To je:

- **sporo** za učitavanje i testiranje
- **teško za debug** kad nešto ne radi
- **nepotrebno** dok razvijaš i provjeravaš kod

Zato prvo radimo s `jena_quick` ili `demo`. Kad pipeline radi ispravno, prelazimo na `jena_full` za ozbiljnije eksperimente.

---

## 4. Interpolacija

### Što je interpolacija?

**Interpolacija** (u ovom projektu: **imputacija**) znači **popunjavanje nedostajućih vrijednosti** u vremenskom nizu temperature.

| Vrijeme | Temperatura |
|---------|-------------|
| 10:00 | 5.0 |
| 10:10 | *nedostaje* |
| 10:20 | 7.0 |

Interpolacija procjenjuje što je bilo u 10:10 (npr. 6.0) na temelju susjednih poznatih vrijednosti.

U projektu prvo **umjetno uklonimo** neke vrijednosti (`create_missing_values`), pa metode pokušaju vratiti original i usporedimo koliko su bile točne (MAE, RMSE, R²).

### Razlika između metoda

| Metoda | Ideja | Kada je dobra |
|--------|-------|---------------|
| **forward_fill** | kopira zadnju poznatu vrijednost unaprijed | jednostavno, ali loše kad temperatura brzo pada/raste |
| **linear** | ravna linija između dva susjeda | dobro za kratke praznine, jednostavno |
| **time** | linearno, ali uz obzir **stvarnog vremena** između mjerenja | bolje kad su razmaci u vremenu različiti |
| **cubic** | glatka krivulja (kubični polinom) kroz više točaka | glađi rezultat, može „previše valovati“ |
| **spline** | spline krivulja — glatka, fleksibilnija od linearne | dobro za glatke temperature, treba dovoljno poznatih točaka |

### Što je scipy?

**scipy** je Python biblioteka za napredniju matematiku (naučne i inženjerske proračune).

Ime dolazi od: **Scientific Python**.

U projektu je scipy potreban za **`cubic_interpolation`** i **`spline_interpolation`** — pandas ih koristi u pozadini kad pozoveš `interpolate(method="cubic")` ili `interpolate(method="spline")`. Ako scipy nije instaliran, te dvije metode neće raditi.

U Danu 2 već rade `forward_fill`, `linear` i `time`. U **Danu 4** dodane su i `cubic` i `spline`. Usporedba:

```powershell
python main.py --compare
```

### Zašto prvo klasične metode?

1. **Jednostavnije za razumjeti** — forward fill i linear imaju jasnu logiku.
2. **Brže za testirati** — ne treba trenirati model.
3. **Dobra baza za usporedbu** — ML metode (KNN, Random Forest) uspoređujemo tek kad klasičan dio radi stabilno.
4. **Manje ovisnosti o hiperparametrima** — klasične metode imaju manje postavki koje mogu pokvariti rezultat.

ML metode dolaze u **Danu 5**.
