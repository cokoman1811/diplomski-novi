"""Classical interpolation methods for temperature time series with missing values."""

import pandas as pd

CLASSICAL_METHOD_NAMES = (
    "forward_fill",
    "linear_interpolation",
    "time_interpolation",
    "cubic_interpolation",
    "spline_interpolation",
)


def _validate_series(series: pd.Series) -> None:
    if not isinstance(series, pd.Series):
        raise ValueError("series must be a pandas Series.")


def _fill_remaining_gaps(result: pd.Series) -> pd.Series:
    """Forward- and back-fill any NaN values left after interpolation."""
    return result.ffill().bfill()


def forward_fill_interpolation(series: pd.Series) -> pd.Series:
    """
    Popuni nedostajuće vrijednosti zadnjom poznatom temperaturom (forward fill).

    Ako na početku niza ostanu NaN vrijednosti, popunjavaju se backward fillom.
    """
    _validate_series(series)

    result = series.copy()
    result = result.ffill()
    return _fill_remaining_gaps(result)


# Kratko ime za starije test skripte.
forward_fill = forward_fill_interpolation


def linear_interpolation(series: pd.Series) -> pd.Series:
    """Popuni nedostajuće vrijednosti linearnom interpolacijom između susjeda."""
    _validate_series(series)

    result = series.copy()
    result = result.interpolate(method="linear")
    return _fill_remaining_gaps(result)


def time_interpolation(series: pd.Series) -> pd.Series:
    """
    Popuni nedostajuće vrijednosti uz obzir vremena između mjerenja.

    Indeks mora biti DatetimeIndex.
    """
    _validate_series(series)

    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("series index must be a DatetimeIndex for time interpolation.")

    result = series.copy()
    result = result.interpolate(method="time")
    return _fill_remaining_gaps(result)


def cubic_interpolation(series: pd.Series) -> pd.Series:
    """
    Popuni nedostajuće vrijednosti kubičnom interpolacijom.

    Zahtijeva dovoljno poznatih točaka (obično barem 4). Koristi scipy preko pandas-a.
    """
    _validate_series(series)

    known_count = int(series.notna().sum())
    if known_count < 4:
        raise ValueError(
            f"cubic interpolation needs at least 4 known values, got {known_count}."
        )

    result = series.copy()
    try:
        result = result.interpolate(method="cubic")
    except (ValueError, ImportError) as error:
        raise ValueError(
            "cubic interpolation failed. Check that scipy is installed and "
            "that the series has enough known values."
        ) from error

    return _fill_remaining_gaps(result)


def spline_interpolation(series: pd.Series) -> pd.Series:
    """
    Popuni nedostajuće vrijednosti spline interpolacijom (red 3).

    Zahtijeva dovoljno poznatih točaka i scipy.
    """
    _validate_series(series)

    known_count = int(series.notna().sum())
    if known_count < 4:
        raise ValueError(
            f"spline interpolation needs at least 4 known values, got {known_count}."
        )

    result = series.copy()
    try:
        result = result.interpolate(method="spline", order=3)
    except (ValueError, ImportError) as error:
        raise ValueError(
            "spline interpolation failed. Check that scipy is installed and "
            "that the series has enough known values."
        ) from error

    return _fill_remaining_gaps(result)


def run_classical_interpolations(series: pd.Series, *, quiet: bool = False) -> dict[str, pd.Series]:
    """
    Pokreni sve klasične metode interpolacije na istom nizu.

    Vraća rječnik s ključevima kao u CLASSICAL_METHOD_NAMES.
    Ako pojedina metoda ne uspije, preskače se i ispisuje se upozorenje.
    """
    _validate_series(series)

    method_functions = {
        "forward_fill": forward_fill_interpolation,
        "linear_interpolation": linear_interpolation,
        "time_interpolation": time_interpolation,
        "cubic_interpolation": cubic_interpolation,
        "spline_interpolation": spline_interpolation,
    }

    results: dict[str, pd.Series] = {}

    for name, method in method_functions.items():
        try:
            results[name] = method(series)
        except ValueError as error:
            if not quiet:
                print(f"  [preskočeno] {name}: {error}")

    return results
