from src.data_loader import load_jena_temperature_slice
from src.preprocessing import create_missing_values


series = load_jena_temperature_slice(hours=48)

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
