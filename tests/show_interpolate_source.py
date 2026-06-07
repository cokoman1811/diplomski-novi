"""Ispis izvornog koda pandas interpolate — pokreni: python tests/show_interpolate_source.py"""

import inspect

import pandas as pd

print(inspect.getsource(pd.Series.interpolate))
