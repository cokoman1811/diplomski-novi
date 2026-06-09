#include "evaluation.h"

#include <math.h>

Metrics evaluate_reconstruction(const double *original, const double *reconstructed,
                                const int *mask, size_t n) {
    Metrics m = {NAN, NAN, NAN, 0};

    double sum_abs = 0.0;
    double sum_sq = 0.0;
    double sum_true = 0.0;
    size_t count = 0;

    for (size_t i = 0; i < n; i++) {
        if (mask[i]) {
            double diff = original[i] - reconstructed[i];
            sum_abs += fabs(diff);
            sum_sq += diff * diff;
            sum_true += original[i];
            count++;
        }
    }

    if (count == 0) {
        return m;
    }

    m.count = count;
    m.mae = sum_abs / (double)count;
    m.rmse = sqrt(sum_sq / (double)count);

    double mean_true = sum_true / (double)count;
    double ss_tot = 0.0;
    for (size_t i = 0; i < n; i++) {
        if (mask[i]) {
            double dt = original[i] - mean_true;
            ss_tot += dt * dt;
        }
    }

    /* R^2 = 1 - SS_res / SS_tot (kao sklearn). */
    if (ss_tot > 0.0) {
        m.r2 = 1.0 - sum_sq / ss_tot;
    } else {
        m.r2 = (sum_sq == 0.0) ? 1.0 : 0.0;
    }

    return m;
}
