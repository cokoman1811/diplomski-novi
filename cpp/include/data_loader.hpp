#pragma once

#include <string>

#include "time_series.hpp"

namespace thesis {

// Izvori podataka (preslikano iz ExperimentSource u Python verziji).
// - "synthetic": generirani 48 h temperaturni niz (ne treba vanjske datoteke)
// - "demo":      ucitavanje iz CSV-a (timestamp,city,temperature)
enum class ExperimentSource { Synthetic, Demo };

ExperimentSource parse_source(const std::string& name);

// Generiraj sintetski temperaturni niz nalik Jeni:
// `hours` sati mjerenja svakih 10 minuta, s dnevnim sinusnim ciklusom + sum.
// Sluzi kao zamjena za pravi Jena dataset da je program odmah pokretljiv.
TimeSeries generate_synthetic_series(int hours = 48, unsigned int seed = 7);

// Ucitaj temperaturni niz iz demo CSV-a (stupci: timestamp, city, temperature).
// Ako je `city` zadan, filtrira se po gradu. Baca na gresku ako file ne postoji.
TimeSeries load_demo_series(const std::string& csv_path, const std::string& city = "");

// Ucitaj niz za eksperiment iz imenovanog izvora.
TimeSeries load_experiment_series(ExperimentSource source,
                                  const std::string& csv_path = "",
                                  const std::string& city = "");

}  // namespace thesis
