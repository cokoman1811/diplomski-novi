# Dan 2 — Degradacija, interpolacija i evaluacija

**Datum:** 2026-06-07  
**Autor:** Toni Jakelić

Drugi radni dan: od učitavanja podataka prelazak na **cijeli eksperimentalni tok** — umjetno uklanjanje vrijednosti, klasične metode interpolacije i metrike na obrisanim mjestima.

## Što je napravljeno

- [x] **`src/preprocessing.py`** — `create_missing_values()`
  - nasumično uklanja unutarnje vrijednosti iz niza
  - prvi i zadnji zapis uvijek ostaju (granice za interpolaciju)
  - vraća `damaged_series` + `missing_mask` za evaluaciju
- [x] **`src/interpolation_methods.py`** — tri klasične metode:
  - `forward_fill` — zadnja poznata temperatura
  - `linear_interpolation` — linearna interpolacija između susjeda
  - `time_interpolation` — interpolacija uz obzir vremena (`DatetimeIndex`)
- [x] **`src/evaluation.py`** — `evaluate_reconstruction()`
  - metrike: **MAE**, **RMSE**, **R²**
  - računa se samo na mjestima gdje je `missing_mask == True`
- [x] **Ručni testovi** u `tests/`:
  - `test_preprocessing.py` — provjera rupa i maske
  - `test_interpolation.py` — detaljni ispis po metodi
  - `test_metrics.py` — provjera evaluacije
  - `test_compare_methods.py` — usporedba svih metoda u tablici
- [x] **Pomoćni moduli za testove:** `tests/bootstrap.py`, `tests/output_format.py`
- [x] **`docs/active_context.md`** — zapisano pravilo projekta (metrike samo na uklonjenim vrijednostima)

## Testirano

```powershell
python tests/test_preprocessing.py
python tests/test_interpolation.py
python tests/test_metrics.py
python tests/test_compare_methods.py
```

Testiran je osnovni pipeline na Jena uzorku od **48 sati**, odnosno **288 mjerenja**.

Korišten je `missing_rate = 0.4`, što znači da je umjetno uklonjeno **115 vrijednosti**.

Metrike su izračunate samo na umjetno obrisanim mjestima (`missing_mask == True`).

## Rezultati

| Metoda | MAE | RMSE | R² |
|--------|-----|------|-----|
| forward_fill | 0.1390 | 0.1842 | 0.9910 |
| linear_interpolation | 0.0736 | 0.1066 | 0.9970 |
| time_interpolation | 0.0736 | 0.1066 | 0.9970 |

## Zaključak

Linear interpolation i time interpolation imaju bolje rezultate od forward fill metode.

Budući da su podaci pravilno vremenski uzorkovani, linearna i vremenska interpolacija daju iste rezultate.

## Nove datoteke

| Datoteka | Uloga |
|----------|--------|
| `src/preprocessing.py` | Simulacija nedostajućih vrijednosti |
| `src/interpolation_methods.py` | Klasične metode imputacije |
| `src/evaluation.py` | MAE, RMSE, R² |
| `tests/test_*.py` | Ručni testovi pipelinea |
| `tests/bootstrap.py` | Postavljanje Python puta za testove |
| `tests/output_format.py` | Formatirani ispis u terminalu |

## Eksperimentalni tok (Dan 2)

```
učitaj Jena 48h → create_missing_values() → interpolacija → evaluate_reconstruction()
```

## Sljedeći dan (Dan 3) — obavljeno

Dan 3 je pokrio centralni `load_experiment_series()`, testove i `run.bat`. Vidi [dan3.md](dan3.md).

Plan za Dan 4: cubic/spline metode, integracija u `main.py`, usporedba u terminalu.
