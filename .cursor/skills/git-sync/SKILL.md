---
name: git-sync
description: Inicijalizira git, kreira GitHub repo i pusha promjene za diplomski rad. Koristi kad korisnik traži upload, sync, backup na git, push na GitHub, ili spominje git-sync agenta.
---

# Git Sync — diplomski rad

## Brzi sync

```powershell
powershell -ExecutionPolicy Bypass -File scripts/git-sync.ps1
```

## Prvi put — kreiraj GitHub repo

**Opcija A** (gh CLI instaliran i prijavljen):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/git-sync.ps1 -SetupRemote
```

**Opcija B** (ručno na github.com):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/git-sync.ps1 -RemoteUrl "https://github.com/KORISNIK/novi-diplomski.git"
```

## Ručni commit s porukom

```powershell
powershell -ExecutionPolicy Bypass -File scripts/git-sync.ps1 -CommitMessage "Korak 2: opis promjene"
```

## Automatski upload

Hook na `stop` pokreće sync nakon što agent završi rad. Ručno: pozovi `@git-sync` agenta ili reci "uploadaj na git".

## Auth problemi

- `gh auth login` — ako koristiš GitHub CLI
- Git Credential Manager — ako push traži login u browseru
