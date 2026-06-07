import bootstrap  # noqa: F401

from src.data_loader import load_processed_series
from src.evaluation import evaluate_reconstruction
from src.preprocessing import create_missing_values

series = load_processed_series()

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
