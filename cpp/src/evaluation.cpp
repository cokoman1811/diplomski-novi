#include "evaluation.hpp"

#include <cmath>
#include <stdexcept>

namespace thesis {

Metrics evaluate_reconstruction(const TimeSeries& original,
                                const TimeSeries& reconstructed,
                                const std::vector<bool>& missing_mask) {
    std::vector<double> y_true, y_pred;
    const bool use_mask = !missing_mask.empty();

    for (std::size_t i = 0; i < original.size(); ++i) {
        if (use_mask && !missing_mask[i]) continue;
        y_true.push_back(original.values[i]);
        y_pred.push_back(reconstructed.values[i]);
    }

    if (y_true.empty()) {
        throw std::invalid_argument("Nema tocaka za evaluaciju.");
    }

    const std::size_t n = y_true.size();
    double sum_abs = 0.0, sum_sq = 0.0, mean_true = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        const double err = y_pred[i] - y_true[i];
        sum_abs += std::fabs(err);
        sum_sq += err * err;
        mean_true += y_true[i];
    }
    mean_true /= n;

    double ss_tot = 0.0;
    for (std::size_t i = 0; i < n; ++i) {
        const double d = y_true[i] - mean_true;
        ss_tot += d * d;
    }

    Metrics metrics;
    metrics.mae = sum_abs / n;
    metrics.rmse = std::sqrt(sum_sq / n);
    metrics.r2 = (ss_tot > 0.0) ? (1.0 - sum_sq / ss_tot) : 0.0;
    return metrics;
}

}  // namespace thesis
