#include "interpolation.h"

#include <math.h>
#include <stdlib.h>

/* Popuni preostale NAN vrijednosti: prvo forward, zatim backward fill. */
static void fill_remaining_gaps(double *out, size_t n) {
    double last = NAN;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(out[i])) {
            last = out[i];
        } else if (!isnan(last)) {
            out[i] = last;
        }
    }
    /* Backward fill za eventualne pocetne NAN vrijednosti. */
    double next = NAN;
    for (size_t i = n; i-- > 0;) {
        if (!isnan(out[i])) {
            next = out[i];
        } else if (!isnan(next)) {
            out[i] = next;
        }
    }
}

void forward_fill(const double *temp, size_t n, double *out) {
    for (size_t i = 0; i < n; i++) {
        out[i] = temp[i];
    }
    fill_remaining_gaps(out, n);
}

/* Linearna interpolacija s proizvoljnom x-osi (pozicije ili vrijeme). */
static void linear_on_axis(const double *temp, size_t n, const double *x, double *out) {
    for (size_t i = 0; i < n; i++) {
        out[i] = temp[i];
    }

    for (size_t i = 0; i < n; i++) {
        if (!isnan(out[i])) {
            continue;
        }

        /* Najblizi poznati susjed lijevo. */
        long long left = -1;
        for (long long j = (long long)i - 1; j >= 0; j--) {
            if (!isnan(temp[j])) {
                left = j;
                break;
            }
        }

        /* Najblizi poznati susjed desno. */
        long long right = -1;
        for (size_t j = i + 1; j < n; j++) {
            if (!isnan(temp[j])) {
                right = (long long)j;
                break;
            }
        }

        if (left >= 0 && right >= 0) {
            double xl = x[left], xr = x[right];
            double yl = temp[left], yr = temp[right];
            double span = xr - xl;
            if (span != 0.0) {
                out[i] = yl + (yr - yl) * (x[i] - xl) / span;
            }
        }
    }

    fill_remaining_gaps(out, n);
}

void linear_interpolation(const double *temp, size_t n, double *out) {
    double *x = (double *)malloc(n * sizeof(double));
    if (!x) {
        forward_fill(temp, n, out);
        return;
    }
    for (size_t i = 0; i < n; i++) {
        x[i] = (double)i;
    }
    linear_on_axis(temp, n, x, out);
    free(x);
}

void time_interpolation(const double *temp, size_t n, const long long *epoch, double *out) {
    double *x = (double *)malloc(n * sizeof(double));
    if (!x) {
        forward_fill(temp, n, out);
        return;
    }
    for (size_t i = 0; i < n; i++) {
        x[i] = (double)epoch[i];
    }
    linear_on_axis(temp, n, x, out);
    free(x);
}

/*
 * Prirodni kubicni spline kroz poznate tocke.
 * Os x su pozicije (0..n-1); query su pozicije nedostajucih vrijednosti.
 */
static int cubic_spline_impl(const double *temp, size_t n, double *out) {
    size_t m = 0;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            m++;
        }
    }
    if (m < 4) {
        return 1;
    }

    double *kx = (double *)malloc(m * sizeof(double));
    double *ky = (double *)malloc(m * sizeof(double));
    double *y2 = (double *)malloc(m * sizeof(double));
    double *u = (double *)malloc(m * sizeof(double));
    if (!kx || !ky || !y2 || !u) {
        free(kx); free(ky); free(y2); free(u);
        return 1;
    }

    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            kx[k] = (double)i;
            ky[k] = temp[i];
            k++;
        }
    }

    /* Prirodni rubni uvjeti: druga derivacija = 0 na krajevima. */
    y2[0] = 0.0;
    u[0] = 0.0;
    for (size_t i = 1; i < m - 1; i++) {
        double sig = (kx[i] - kx[i - 1]) / (kx[i + 1] - kx[i - 1]);
        double p = sig * y2[i - 1] + 2.0;
        y2[i] = (sig - 1.0) / p;
        double d = (ky[i + 1] - ky[i]) / (kx[i + 1] - kx[i])
                 - (ky[i] - ky[i - 1]) / (kx[i] - kx[i - 1]);
        u[i] = (6.0 * d / (kx[i + 1] - kx[i - 1]) - sig * u[i - 1]) / p;
    }
    y2[m - 1] = 0.0;
    for (size_t i = m - 1; i-- > 0;) {
        y2[i] = y2[i] * y2[i + 1] + u[i];
    }

    for (size_t i = 0; i < n; i++) {
        if (!isnan(temp[i])) {
            out[i] = temp[i];
            continue;
        }

        double xq = (double)i;
        /* Pronadi interval [kx[lo], kx[hi]] binarnim trazenjem. */
        size_t lo = 0, hi = m - 1;
        while (hi - lo > 1) {
            size_t mid = (lo + hi) / 2;
            if (kx[mid] > xq) {
                hi = mid;
            } else {
                lo = mid;
            }
        }

        double h = kx[hi] - kx[lo];
        double a = (kx[hi] - xq) / h;
        double b = (xq - kx[lo]) / h;
        out[i] = a * ky[lo] + b * ky[hi]
               + ((a * a * a - a) * y2[lo] + (b * b * b - b) * y2[hi]) * (h * h) / 6.0;
    }

    free(kx); free(ky); free(y2); free(u);
    fill_remaining_gaps(out, n);
    return 0;
}

int cubic_interpolation(const double *temp, size_t n, double *out) {
    return cubic_spline_impl(temp, n, out);
}

int spline_interpolation(const double *temp, size_t n, double *out) {
    return cubic_spline_impl(temp, n, out);
}
