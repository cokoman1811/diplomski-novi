#include "preprocessing.hpp"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <random>
#include <stdexcept>

namespace thesis {

DamagedSeries create_missing_values(const TimeSeries& series, double missing_rate,
                                    unsigned int random_state) {
    if (series.size() < 2) {
        throw std::invalid_argument("series mora imati barem 2 vrijednosti.");
    }
    if (missing_rate < 0.0 || missing_rate > 1.0) {
        throw std::invalid_argument("missing_rate mora biti izmedu 0 i 1.");
    }

    DamagedSeries out;
    out.series = series;
    out.missing_mask.assign(series.size(), false);

    // Kandidati za brisanje su sve osim prve i zadnje tocke (rubni sidra).
    std::vector<std::size_t> eligible;
    for (std::size_t i = 1; i + 1 < series.size(); ++i) eligible.push_back(i);
    if (eligible.empty()) return out;

    const std::size_t n_to_remove =
        std::min(static_cast<std::size_t>(std::llround(missing_rate * series.size())),
                 eligible.size());
    if (n_to_remove == 0) return out;

    std::mt19937 rng(random_state);
    std::shuffle(eligible.begin(), eligible.end(), rng);

    for (std::size_t k = 0; k < n_to_remove; ++k) {
        const std::size_t pos = eligible[k];
        out.series.values[pos] = quiet_nan();
        out.missing_mask[pos] = true;
    }
    return out;
}

}  // namespace thesis
