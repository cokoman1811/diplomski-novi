# Diplomski rad — Toni Jakelić

**Radni naslov:** Usporedba klasičnih i neuronskih metoda za imputaciju nedostajućih podataka u vremenskim nizovima

**Autor:** Toni Jakelić  
**Godina:** 2026.  
**Radna mapa:** `Desktop\novi diplomski`

Svježi početak pisanja i eksperimentiranja. Stari projekt (`diplomski rad`) ostaje netaknut — ovdje gradimo novu verziju rada korak po korak.

## O projektu

Cilj rada je usporediti klasične metode interpolacije i metode strojnog učenja u zadatku popunjavanja nedostajućih vrijednosti u vremenskim podacima.

Planirane metode:
- Linearna interpolacija
- Spline interpolacija
- KNN imputacija
- Random Forest regresija
- LSTM neuronska mreža

Metrike evaluacije: MAE, RMSE, MAPE i grafička usporedba.

## Struktura

```
novi diplomski/
├── src/              # Izvorni kod (metode, eksperimenti)
├── data/             # Dataseti i ulazni podaci
├── docs/             # Projektna dokumentacija
├── main.py           # Ulazna točka za eksperimente
├── app.py            # Web UI za vizualizaciju (kasnije)
├── requirements.txt  # Python ovisnosti
├── rad.md            # Tekst diplomskog rada
├── KORACI.md         # Log napretka
└── scripts/          # Git sync skripte
```

## Status

- [x] Korak 0 — mapa projekta kreirana
- [x] Korak 1 — skeleton rada u `rad.md`
- [x] Korak 2 — Git repozitorij + auto-upload (`@git-sync`)
- [x] Korak 3 — struktura projekta (`src/`, `data/`, `docs/`, `main.py`, `app.py`)
- [ ] Korak 4 — čeka sljedeću uputu

Detalji u [KORACI.md](KORACI.md).

## Kako radimo

1. Ti kažeš što želiš u sljedećem koraku.
2. Agent to napravi (tekst, kod, struktura — što zatreba).
3. Napredak se zapisuje u `KORACI.md`.
4. Sljedeći korak.

## Git i backup

Repozitorij je inicijaliziran na grani `main`. Za upload na GitHub:

```powershell
# Jednom — GitHub CLI (preporučeno)
winget install GitHub.cli
gh auth login
.\scripts\git-sync.ps1 -SetupRemote
```

Ili ručno na [github.com/new](https://github.com/new) (ime: `novi-diplomski`), pa:

```powershell
.\scripts\git-sync.ps1 -RemoteUrl "https://github.com/TVOJ_USERNAME/novi-diplomski.git"
```

U chatu možeš i: `@git-sync uploadaj sve na git`

## Bilješke

Mentor i studij upisuju se u `rad.md` kad budu dogovoreni. Tema i detalji eksperimenta razvijaju se kako rad napreduje.
