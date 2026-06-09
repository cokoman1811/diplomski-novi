#pragma once

#include <vector>

#include "time_series.hpp"

namespace thesis {

// Metrike rekonstrukcije.
struct Metrics {
    double mae;
    double rmse;
    double r2;
};

// Usporedi rekonstruirane vrijednosti s originalom.
// Ako je `missing_mask` zadan (ne prazan), metrike se racunaju samo na
// pozicijama gdje je maska true (umjetno obrisane vrijednosti).
Metrics evaluate_reconstruction(const TimeSeries& original,
                                const TimeSeries& reconstructed,
                                const std::vector<bool>& missing_mask = {});

}  // namespace thesis
