# Najčešća pitanja

## Što je pandas?

To je biblioteka u pythonu za rad sa datotekama.

## Što je Series?

```python
series = pd.Series(
    data=temperature.values,
    index=pd.DatetimeIndex(data["timestamp"]),
    name="temperature",
)
```

Series se sastoji od:
- `data` — samo vrijednosti temperatura
- `index` — samo tu da označi vrijeme
- `name="temperature"` — ime temperature

## Što je `_validate_series`?

```python
def _validate_series(series: pd.Series) -> None:
```

Definira funkciju koja uspoređuje `series` s `pd.Series` i ne vraća ništa (`None`).
