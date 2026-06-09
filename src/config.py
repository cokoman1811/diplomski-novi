"""Project configuration constants."""

JENA_RAW_FILENAME = "jena_climate_2009_2016.csv"
JENA_ZIP_FILENAME = "jena_climate_2009_2016.csv.zip"
JENA_DATA_URL = (
    "https://storage.googleapis.com/tensorflow/tf-keras-datasets/"
    "jena_climate_2009_2016.csv.zip"
)

DATETIME_COLUMN = "Date Time"
TEMPERATURE_COLUMN = "T (degC)"

COVARIATE_COLUMNS = [
    "p (mbar)",
    "rh (%)",
    "wv (m/s)",
    "max. wv (m/s)",
]

# Jena mjeri svakih 10 minuta → 48 h = 288 uzoraka
QUICK_SAMPLE_HOURS = 48
JENA_INTERVAL_MINUTES = 10
