# Progress — po danima

Dnevni log napretka. Svaki dan ima svoju datoteku.

| Dan | Datum | Tema | Datoteka |
|-----|-------|------|----------|
| 0 | 2026-06-05 | Priprema projekta, git, struktura | [dan0.md](dan0.md) |
| 1 | 2026-06-06 | Učitavanje podataka (Jena Climate) | [dan1.md](dan1.md) |
| 2 | 2026-06-07 | Degradacija, interpolacija, evaluacija | [dan2.md](dan2.md) |
| 3 | 2026-06-08 | Centralni data loader, testovi, run.bat | [dan3.md](dan3.md) |
| 4 | — | Klasične interpolacijske metode (plan) | *(u implementaciji)* |

## Trenutni status

**Zadnji završeni dan: Dan 3** — projekt je stabilan i spreman za nastavak.

### Dan 3 — sažetak

- [x] Dovršen **`src/data_loader.py`**
- [x] Jedan centralni ulaz za eksperimentalne podatke: **`load_experiment_series()`**
- [x] Podržani izvori: `demo`, `jena_quick`, `jena_full`, `processed`
- [x] **`jena_quick`** — brzo testiranje bez učitavanja cijelog dataseta (npr. 48 h)
- [x] Validacija temperaturnog niza (prazan niz, NaN, duplikati, vremenski indeks)
- [x] Testovi u **`tests/test_data_loader.py`**
- [x] **`run.bat`** — automatski `.venv`, instalacija paketa, pokretanje `main.py`
- [x] Dokumentacija ažurirana
- [x] Glavni dataset na disku: `data/raw/jena_climate_2009_2016.csv`

---

## Plan — Dan 4: Implementacija klasičnih interpolacijskih metoda

**Cilj:** proširiti klasične metode, povezati ih s `main.py` i ispisati usporedbu u terminalu. **ML metode (KNN, Random Forest) — ne raditi u Danu 4** (ostaju za Dan 5 ili kasnije).

### Koraci

1. **Napraviti ili urediti** `src/interpolation_methods.py`

2. **Dodati / uskladiti funkcije** (sve primaju `pd.Series` s nedostajućim vrijednostima, vraćaju novi `pd.Series`):

   | Funkcija | Opis |
   |----------|------|
   | `forward_fill_interpolation(series)` | zadnja poznata vrijednost |
   | `linear_interpolation(series)` | linearna interpolacija |
   | `time_interpolation(series)` | interpolacija uz obzir vremena |
   | `cubic_interpolation(series)` | kubična interpolacija |
   | `spline_interpolation(series)` | spline interpolacija |

3. **Pravila implementacije**
   - funkcije **ne smiju mijenjati** originalni `series` — rade na **kopiji**
   - jednostavni **docstringovi** i komentari (početnički jasno)

4. **Povezati s `src/main.py`**
   - eksperiment se pokreće iz glavnog programa (ne samo ručni testovi)
   - koristiti `load_experiment_series()` za učitavanje podataka

5. **Evaluacija**
   - koristiti postojeće metrike iz `src/evaluation.py` (MAE, RMSE, R²)
   - metrike računati samo na umjetno uklonjenim vrijednostima (`missing_mask`)

6. **Ispis u terminalu**
   - tablica ili pregledna usporedba svih klasičnih metoda

7. **Izvan opsega Dana 4**
   - KNN, Random Forest, MLP → Dan 5+
   - grafovi (opcionalno kasnije)

### Očekivani tok (Dan 4)

```
load_experiment_series("jena_quick")
  → create_missing_values()
  → svaka interpolacijska metoda
  → evaluate_reconstruction()
  → ispis usporedbe u terminalu
```
