# Active Context — Diplomski rad

## Tema

Tema diplomskog rada je usporedba klasičnih i strojno-učenih metoda za interpolaciju/imputaciju nedostajućih vrijednosti u vremenskim nizovima temperature.

Glavni cilj nije izrada web aplikacije, nego izgradnja eksperimentalnog sustava koji može:
- učitati temperaturni vremenski niz
- umjetno ukloniti dio vrijednosti
- rekonstruirati uklonjene vrijednosti različitim metodama
- usporediti rekonstrukciju s originalom
- izračunati MAE, RMSE i R2 metrike

## Glavni znanstveni tok

Projekt treba raditi ovim redom:

1. učitati originalni vremenski niz temperature
2. umjetno ukloniti dio vrijednosti
3. zapamtiti gdje su vrijednosti uklonjene pomoću `missing_mask`
4. primijeniti metodu interpolacije/imputacije
5. usporediti rekonstruirane vrijednosti s originalnima
6. izračunati metrike samo na umjetno uklonjenim mjestima

Važno pravilo:

Ako postoji `missing_mask`, metrike se računaju samo tamo gdje je:

```python
missing_mask == True