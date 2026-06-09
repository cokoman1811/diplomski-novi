#include "ml_methods.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <stdexcept>
#include <vector>

#include "interpolation_methods.hpp"

namespace thesis {

namespace {

// Tri vremenske znacajke za svako mjerenje: redni broj, sat u danu, dan u godini.
std::vector<std::array<double, 3>> build_features(const TimeSeries& series) {
    std::vector<std::array<double, 3>> features;
    features.reserve(series.size());
    for (std::size_t i = 0; i < series.size(); ++i) {
        features.push_back({static_cast<double>(i),
                            static_cast<double>(hour_of_day(series.timestamps[i])),
                            static_cast<double>(day_of_year(series.timestamps[i]))});
    }
    return features;
}

double squared_distance(const std::array<double, 3>& a,
                        const std::array<double, 3>& b) {
    double sum = 0.0;
    for (int k = 0; k < 3; ++k) {
        const double d = a[k] - b[k];
        sum += d * d;
    }
    return sum;
}

}  // namespace

TimeSeries knn_imputation(const TimeSeries& series, int n_neighbors) {
    if (n_neighbors < 1) {
        throw std::invalid_argument("n_neighbors mora biti barem 1.");
    }

    TimeSeries result = series;

    std::vector<std::size_t> missing, known;
    for (std::size_t i = 0; i < series.size(); ++i) {
        if (is_missing(series.values[i])) missing.push_back(i);
        else known.push_back(i);
    }

    if (missing.empty()) return result;
    if (known.empty()) {
        throw std::invalid_argument("Nije moguce imputirati: nema poznatih vrijednosti.");
    }

    const auto features = build_features(series);
    const int k = std::min<int>(n_neighbors, static_cast<int>(known.size()));

    for (std::size_t m : missing) {
        // Pronadi k najblizih poznatih tocaka po euklidskoj udaljenosti znacajki.
        std::vector<std::pair<double, std::size_t>> dist;
        dist.reserve(known.size());
        for (std::size_t kn : known) {
            dist.emplace_back(squared_distance(features[m], features[kn]), kn);
        }
        std::partial_sort(dist.begin(), dist.begin() + k, dist.end());

        double sum = 0.0;
        for (int j = 0; j < k; ++j) sum += series.values[dist[j].second];
        result.values[m] = sum / k;
    }

    // Sigurnosna mreza za eventualne preostale NaN.
    return forward_fill_interpolation(result);
}

}  // namespace thesis
