#pragma once

#include <vector>

#include "time_series.hpp"

namespace thesis {

// Rezultat umjetnog ostecivanja niza.
struct DamagedSeries {
    TimeSeries series;             // kopija s NaN na obrisanim mjestima
    std::vector<bool> missing_mask;  // true ondje gdje je vrijednost obrisana
};

// Nasumicno ukloni unutarnje vrijednosti iz niza za evaluaciju.
// Prva i zadnja vrijednost se uvijek cuvaju (rubne tocke za interpolaciju).
// `missing_rate` je udio izmedu 0 i 1; `random_state` je sjeme za ponovljivost.
DamagedSeries create_missing_values(const TimeSeries& series,
                                    double missing_rate = 0.2,
                                    unsigned int random_state = 42);

}  // namespace thesis
