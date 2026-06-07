import sys
from pathlib import Path

from src.data_loader import load_jena_temperature_slice
from src.preprocessing import create_missing_values
from src.evaluation import evaluate_reconstruction


series = load_jena_temperature_slice(hours=48)

damaged, mask = create_missing_values(
    series,
    missing_rate=0.2,
    random_state=42,
)

reconstructed = damaged.interpolate(method="time")

metrics = evaluate_reconstruction(
    original=series,
    reconstructed=reconstructed,
    missing_mask=mask,
)

print("Broj originalnih zapisa:", len(series))
print("Broj obrisanih vrijednosti:", int(mask.sum()))
print()

print("Metrike:")
print(metrics)