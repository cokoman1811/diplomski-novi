# Dan 5 — KNN imputacija

**Datum:** 2026-06-09  
**Autor:** Toni Jakelić

Prvi korak ML metoda: KNN imputacija temperaturnog niza.

## Što je napravljeno

- [x] Novi modul **`src/ml_methods.py`**
- [x] Funkcija **`knn_imputation(series, n_neighbors=5)`**
  - značajke: redni broj mjerenja, sat u danu, dan u godini
  - model (`KNeighborsRegressor`) trenira se samo na poznatim vrijednostima
  - predikcija samo na `NaN` mjestima
  - preostale rupe: `ffill()` + `bfill()`
- [x] Testovi u **`tests/test_ml_methods.py`**

## Izvan opsega (za sada)

- Random Forest
- integracija u `main.py --compare`

## Testirano

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```
