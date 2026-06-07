# Progress — novi diplomski

Dnevni log napretka na implementaciji diplomskog projekta.

---

## 2026-06-07 — Dan 2: degradacija, interpolacija i evaluacija

**Autor:** Toni Jakelić

Drugi radni dan: od učitavanja podataka prelazak na **cijeli eksperimentalni tok** — umjetno uklanjanje vrijednosti, klasične metode interpolacije i metrike na obrisanim mjestima.

### Napravljeno

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

### Testirano

```powershell
python tests/test_preprocessing.py
python tests/test_interpolation.py
python tests/test_metrics.py
python tests/test_compare_methods.py
```

**Setup:** Jena Climate, prvih **48 h** (288 zapisa, interval 10 min), `missing_rate=0.4`, `random_state=42`

### Rezultati (usporedba metoda)

| Metoda | MAE | RMSE | R² |
|--------|-----|------|-----|
| forward_fill | 0.1390 | 0.1842 | 0.9910 |
| linear_interpolation | 0.0736 | 0.1066 | 0.9970 |
| time_interpolation | 0.0736 | 0.1066 | 0.9970 |

**Zaključak dana:** na ovom uzorku linearna i time interpolacija jednako nadmašuju forward fill; time i linear daju iste metrike jer je Jena niz ravnomjerno uzorkovan (10 min).

### Novi moduli u `src/`

| Datoteka | Uloga |
|----------|--------|
| `preprocessing.py` | Simulacija nedostajućih vrijednosti |
| `interpolation_methods.py` | Klasične metode imputacije |
| `evaluation.py` | MAE, RMSE, R² |

### Sljedeće

- [ ] Dodati spline / moving average metode
- [ ] ML metode (KNN, Random Forest, MLP)
- [ ] Integrirati eksperiment u `src/main.py` (ne samo ručni testovi)
- [ ] Grafička usporedba original vs. rekonstruirano
- [ ] Početi puniti `rad.md` — metodologija i prvi rezultati

---

## 2026-06-06 — Dan 1: učitavanje podataka

Vidi detalje u [dan1.md](dan1.md).

- Jena Climate download i učitavanje
- CLI: `--download`, `--quick`, `--demo`
- Automatski `.venv` bootstrap u `main.py`

---

## 2026-06-05 — Priprema projekta

- Struktura repozitorija (`src/`, `data/`, `docs/`)
- Git + GitHub (`diplomski-novi`)
- GitHub profile README
- Demo CSV za gradove (Split, Zagreb)
