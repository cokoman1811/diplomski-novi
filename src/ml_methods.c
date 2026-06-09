#include "ml_methods.h"

#include <math.h>
#include <stdlib.h>

/* Kvadrat euklidske udaljenosti u prostoru znacajki (pozicija, sat, dan). */
static double feature_distance_sq(const Series *s, size_t a, size_t b) {
    double dp = (double)a - (double)b;
    double dh = (double)s->hour[a] - (double)s->hour[b];
    double dy = (double)s->yday[a] - (double)s->yday[b];
    return dp * dp + dh * dh + dy * dy;
}

int knn_imputation(const Series *series, const double *temp, int n_neighbors, double *out) {
    size_t n = series->n;

    for (size_t i = 0; i < n; i++) {
        out[i] = temp[i];
    }

    /* Indeksi poznatih vrijednosti. */
    size_t known_count = 0;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            known_count++;
        }
    }
    if (known_count == 0) {
        return 1;
    }

    size_t *known = (size_t *)malloc(known_count * sizeof(size_t));
    if (!known) {
        return 1;
    }
    size_t kc = 0;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            known[kc++] = i;
        }
    }

    int k = n_neighbors;
    if (k < 1) {
        k = 1;
    }
    if ((size_t)k > known_count) {
        k = (int)known_count;
    }

    /* Za svako nedostajuce mjesto: pronadi k najblizih poznatih i prosjek. */
    double *best_dist = (double *)malloc((size_t)k * sizeof(double));
    size_t *best_idx = (size_t *)malloc((size_t)k * sizeof(size_t));
    if (!best_dist || !best_idx) {
        free(known); free(best_dist); free(best_idx);
        return 1;
    }

    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            continue;
        }

        for (int t = 0; t < k; t++) {
            best_dist[t] = INFINITY;
            best_idx[t] = 0;
        }

        for (size_t j = 0; j < known_count; j++) {
            size_t cand = known[j];
            double d = feature_distance_sq(series, i, cand);
            /* Ubaci u sortiranu listu k najboljih. */
            if (d < best_dist[k - 1]) {
                int pos = k - 1;
                while (pos > 0 && best_dist[pos - 1] > d) {
                    best_dist[pos] = best_dist[pos - 1];
                    best_idx[pos] = best_idx[pos - 1];
                    pos--;
                }
                best_dist[pos] = d;
                best_idx[pos] = cand;
            }
        }

        double sum = 0.0;
        for (int t = 0; t < k; t++) {
            sum += temp[best_idx[t]];
        }
        out[i] = sum / (double)k;
    }

    free(known);
    free(best_dist);
    free(best_idx);

    /* Sigurnosna mreza (ne bi smjelo ostati NAN). */
    double last = NAN;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(out[i])) {
            last = out[i];
        } else if (!isnan(last)) {
            out[i] = last;
        }
    }
    double next = NAN;
    for (size_t i = n; i-- > 0;) {
        if (!isnan(out[i])) {
            next = out[i];
        } else if (!isnan(next)) {
            out[i] = next;
        }
    }
    return 0;
}
