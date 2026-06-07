import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from src.data_loader import load_processed_series
from src.preprocessing import create_missing_values


series = load_processed_series()

damaged, mask = create_missing_values(
    series,
    missing_rate=0.2,
    random_state=42,
)

print("Original broj zapisa:", len(series))
print("Oštećeni broj zapisa:", len(damaged))
print("Broj umjetno obrisanih vrijednosti:", int(mask.sum()))
print("Broj NaN vrijednosti u damaged:", int(damaged.isna().sum()))

print()
print("Original - prvih 10:")
print(series.head(10))

print()
print("Damaged - prvih 10:")
print(damaged.head(10))

print()
print("Mask - prvih 10:")
print(mask.head(10))
