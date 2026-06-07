# Log koraka — novi diplomski

## Korak 0 — Priprema

**Datum:** 2026-06-03  

**Što je napravljeno:**
- Kreirana mapa `novi diplomski` na Desktopu
- Dogovor: radimo ispočetka, korak po korak, prema tvojim uputama

**Sljedeće:** čeka se Korak 1 od tebe

---

## Korak 1 — Pisanje u novoj mapi

**Datum:** 2026-06-03  

**Što je napravljeno:**
- Kreirana glavna datoteka za pisanje: `rad.md` (skeleton poglavlja)
- Radna mapa: `Desktop\novi diplomski`

**Sljedeće:** otvori mapu u Cursoru i počni pisati u `rad.md` (ili reci što prvo popuniti)

---

## Korak 2 — Git + auto-upload

**Datum:** 2026-06-05  

**Što je napravljeno:**
- Git repozitorij inicijaliziran (`main` branch)
- Cursor agent `@git-sync` — upload na GitHub
- Skripta `scripts/git-sync.ps1` — commit + push
- Hook na kraju agent sesije — automatski sync

**Sljedeće:** kreirati GitHub repo i povezati remote (vidi upute ispod)

### Kako povezati GitHub (jednom)

**A)** Instaliraj GitHub CLI: `winget install GitHub.cli`, zatim `gh auth login`, pa:
```powershell
.\scripts\git-sync.ps1 -SetupRemote
```

**B)** Ručno na https://github.com/new (ime: `novi-diplomski`), pa:
```powershell
.\scripts\git-sync.ps1 -RemoteUrl "https://github.com/TVOJ_USERNAME/novi-diplomski.git"
```

---

## Korak 3 — Struktura projekta

**Datum:** 2026-06-05  

**Što je napravljeno:**
- Kreirana mapa `src/` s ulaznom točkom (`src/main.py`)
- Kreirana mapa `data/` za datasete
- Kreirana mapa `docs/` za projektnu dokumentaciju
- Dodani `main.py`, `app.py`, `requirements.txt`
- Ažurirani `README.md` i `.gitignore`

**Sljedeće:** postaviti virtualno okruženje i početi implementaciju modula u `src/`

---

## Korak 4 — Učitavanje podataka (Dan 1)

**Datum:** 2026-06-06  

**Što je napravljeno:**
- Moduli `config.py`, `paths.py`, `download_data.py`, `data_loader.py`
- CLI u `src/main.py` (`--download`, `--quick`, `--demo`)
- Automatsko `.venv` u korijenskom `main.py`
- Uspješno testirano: `python main.py --quick` → `jena_temperature_48h.csv` (288 zapisa)

**Detalji:** vidi [docs/dan1.md](docs/dan1.md)

**Sljedeće:** simulacija nedostajućih vrijednosti i prva metoda imputacije

---

## Korak 5 — Degradacija, interpolacija, evaluacija (Dan 2)

**Datum:** 2026-06-07  

**Što je napravljeno:**
- `preprocessing.py`, `interpolation_methods.py`, `evaluation.py`
- Ručni testovi i usporedba 3 klasične metode na Jena 48h uzorku
- Progress zapis u `docs/progress.md`

**Detalji:** vidi [docs/dan2.md](docs/dan2.md) i [docs/progress.md](docs/progress.md)

**Sljedeće:** Dan 3 — spline / ML metode, integracija u `main.py`, grafovi
