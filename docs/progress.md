# Progress — po danima

Dnevni log napretka. Svaki dan ima svoju datoteku.

| Dan | Datum | Tema | Datoteka |
|-----|-------|------|----------|
| 0 | 2026-06-05 | Priprema projekta, git, struktura | [dan0.md](dan0.md) |
| 1 | 2026-06-06 | Učitavanje podataka (Jena Climate) | [dan1.md](dan1.md) |
| 2 | 2026-06-07 | Degradacija, interpolacija, evaluacija | [dan2.md](dan2.md) |
| 3 | 2026-06-08 | Centralni data loader, testovi, run.bat | [dan3.md](dan3.md) |
| 4 | 2026-06-08 | Klasične interpolacijske metode | [dan4.md](dan4.md) |
| 5 | 2026-06-09 | KNN imputacija (`src/ml_methods.py`) | [dan5.md](dan5.md) |

## Trenutni status

**Zadnji završeni dan: Dan 5** — KNN imputacija u `src/ml_methods.py`, testovi u `tests/test_ml_methods.py`. Random Forest i `--compare` integracija — sljedeće.

### Dan 4 — sažetak

- [x] Proširen **`src/interpolation_methods.py`**
- [x] Klasične metode: forward fill, linear, time, cubic, spline
- [x] Metode rade nad `pd.Series` i **ne mijenjaju** originalni niz
- [x] Pomoćna funkcija **`run_classical_interpolations()`**
- [x] Testovi u **`tests/test_interpolation_methods.py`**
- [x] **`main.py --compare`** ispisuje usporedbu metoda (MAE, RMSE, R²)
- [x] Popravljen **`src/evaluation.py`** (sklearn importi)
- [x] **`docs/najcesca_pitanja.md`** — FAQ, tutorial izvora (`demo`, `jena_quick`, …), scipy, run.bat
- [x] **Testirano:** pytest 11/11 passed, `--compare` radi na demo i jena_quick
- [x] **ML metode još nisu dodane** — ostaju za Dan 5

### Rezultati testiranja (2026-06-09)

```
pytest: 11 passed in ~1.5s
main.py --compare --source demo --city Split: OK (5 metoda u tablici)
```

### Pokretanje

```powershell
.\.venv\Scripts\python.exe -m pytest -v
python main.py --compare
python main.py --compare --source jena_quick
python main.py --compare --source demo --city Split
.\run.bat --compare
```

---

## Plan — Dan 5: Machine learning metode

**Cilj:** dodati KNN i Random Forest imputaciju te usporediti s klasičnim metodama.

### Koraci (plan)

1. Novi modul ili proširenje za ML metode (npr. `src/ml_methods.py`)
2. `knn_imputation(series)` — KNN imputacija
3. `random_forest_imputation(series)` — Random Forest pristup
4. Integrirati u `--compare` ili novu naredbu
5. Ista evaluacija: MAE, RMSE, R² samo na `missing_mask`
6. Grafovi usporedbe (opcionalno)

### Izvan opsega (za sada)

- Neural networks / MLP
- Veliki refactor projekta
