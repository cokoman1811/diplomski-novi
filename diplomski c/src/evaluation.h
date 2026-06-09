#ifndef EVALUATION_H
#define EVALUATION_H

#include <stddef.h>

typedef struct {
    double mae;
    double rmse;
    double r2;
    size_t count; /* broj tocaka koristenih u evaluaciji */
} Metrics;

/*
 * Usporedi rekonstruirane vrijednosti s originalom samo na mjestima gdje
 * je mask[i] != 0 (umjetno uklonjene vrijednosti).
 *
 * Vraca metrike; ako nema tocaka, count = 0 i ostale vrijednosti su NAN.
 */
Metrics evaluate_reconstruction(const double *original, const double *reconstructed,
                                const int *mask, size_t n);

#endif /* EVALUATION_H */
