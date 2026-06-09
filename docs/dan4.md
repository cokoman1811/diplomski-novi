# Dan 4 — Klasične interpolacijske metode

**Datum:** 2026-06-08  
**Testirano:** 2026-06-09  
**Autor:** Toni Jakelić

Četvrti radni dan: proširene klasične metode interpolacije, testovi, povezivanje s glavnim programom i dokumentacija.

## Što je napravljeno

- [x] **`src/interpolation_methods.py`** — proširen s novim metodama:
  - `forward_fill_interpolation`
  - `linear_interpolation`
  - `time_interpolation`
  - `cubic_interpolation` (scipy)
  - `spline_interpolation` (scipy)
  - `run_classical_interpolations` — pokreće sve metode odjednom
- [x] Sve metode rade na **kopiji** `pd.Series` i ne mijenjaju original
- [x] Rubni NaN-ovi se popunjavaju s `ffill()` + `bfill()` nakon interpolacije
- [x] **`tests/test_interpolation_methods.py`** — pytest testovi
- [x] **`src/main.py`** — naredba `--compare` za usporedbu metoda u terminalu
- [x] **`src/evaluation.py`** — popravljen import sklearn metrika
- [x] **`pytest.ini`** — pokreće samo pytest testove (ne ručne skripte)
- [x] **`docs/najcesca_pitanja.md`** — reorganiziran FAQ, tutorial izvora podataka, scipy, run.bat

## Eksperimentalni tok (Dan 4)

```
load_experiment_series("jena_quick")
  → create_missing_values()
  → run_classical_interpolations()
  → evaluate_reconstruction()
  → ispis tablice u terminalu
```

## Pokretanje

```powershell
.\.venv\Scripts\python.exe -m pytest -v
python main.py --compare
python main.py --compare --source jena_quick
python main.py --compare --source demo --city Split
.\run.bat --compare
```

## Testirano (2026-06-09)

**pytest:** 11/11 passed (1.45 s)

| Test | Status |
|------|--------|
| `test_load_experiment_series_demo` | PASSED |
| `test_load_experiment_series_jena_quick` | PASSED |
| Sve 5 interpolacijskih metoda (original se ne mijenja) | PASSED |
| `test_linear_interpolation_fills_middle_gap` | PASSED |
| `test_time_interpolation_with_datetime_index` | PASSED |
| `test_time_interpolation_requires_datetime_index` | PASSED |
| `test_run_classical_interpolations_returns_expected_keys` | PASSED |

**`--compare` (demo, Split):** tablica s 5 metoda — forward_fill, linear, time, cubic, spline — sve ispisane s MAE, RMSE, R².

## Datoteke Dana 4

| Datoteka | Uloga |
|----------|--------|
| `src/interpolation_methods.py` | 5 klasičnih metoda + `run_classical_interpolations()` |
| `tests/test_interpolation_methods.py` | pytest testovi |
| `src/main.py` | `--compare`, `print_classical_comparison()` |
| `src/evaluation.py` | fix sklearn importa |
| `pytest.ini` | ograničava pytest na službene testove |
| `docs/najcesca_pitanja.md` | FAQ i tutorial za izvore podataka |

## Sljedeći dan (Dan 5)

- ML metode: KNN, Random Forest
- Integracija ML metoda u usporedbu
- Grafovi (opcionalno)
