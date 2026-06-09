#pragma once

// Projektne konstante (preslikano iz src/config.py).
namespace config {

// Jena mjeri svakih 10 minuta -> 48 h = 288 uzoraka.
inline constexpr int QUICK_SAMPLE_HOURS = 48;
inline constexpr int JENA_INTERVAL_MINUTES = 10;

inline constexpr const char* TEMPERATURE_NAME = "temperature";

}  // namespace config
