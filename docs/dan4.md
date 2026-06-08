# Dan 4 — Klasične interpolacijske metode

**Datum:** 2026-06-08  
**Autor:** Toni Jakelić

Četvrti radni dan: proširene klasične metode interpolacije, testovi i povezivanje s glavnim programom.

## Što je napravljeno

- [x] **`src/interpolation_methods.py`** — proširen s novim metodama:
  - `forward_fill_interpolation`
  - `linear_interpolation`
  - `time_interpolation`
  - `cubic_interpolation`
  - `spline_interpolation`
  - `run_classical_interpolations` — pokreće sve metode odjednom
- [x] Sve metode rade na **kopiji** `pd.Series` i ne mijenjaju original
- [x] Rubni NaN-ovi se popunjavaju s `ffill()` + `bfill()` nakon interpolacije
- [x] **`tests/test_interpolation_methods.py`** — pytest testovi
- [x] **`src/main.py`** — naredba `--compare` za usporedbu metoda u terminalu
- [x] **`src/evaluation.py`** — popravljen import sklearn metrika
- [x] **`pytest.ini`** — pokreće samo pytest testove (ne ručne skripte)

## Pokretanje

```powershell
python -m pytest
python main.py --compare
python main.py --compare --source demo --city Split
```

## Eksperimentalni tok (Dan 4)

```
load_experiment_series("jena_quick")
  → create_missing_values()
  → run_classical_interpolations()
  → evaluate_reconstruction()
  → ispis tablice u terminalu
```

## Sljedeći dan (Dan 5)

- ML metode: KNN, Random Forest
- Integracija ML metoda u usporedbu
- Grafovi (opcionalno)
