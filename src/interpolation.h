#ifndef INTERPOLATION_H
#define INTERPOLATION_H

#include <stddef.h>

/*
 * Klasicne metode interpolacije/imputacije.
 *
 * Sve funkcije primaju ostecen niz `temp` (NAN na nedostajucim mjestima)
 * i upisuju rekonstrukciju u `out` (velicina n). `out` nikad ne sadrzi NAN
 * (preostale rupe popunjavaju se forward/backward fillom).
 *
 * Funkcije koje vracaju int vracaju 0 kod uspjeha, != 0 ako metoda nije
 * primjenjiva (npr. premalo poznatih tocaka za spline).
 */

void forward_fill(const double *temp, size_t n, double *out);

void linear_interpolation(const double *temp, size_t n, double *out);

/* Linearna interpolacija uz stvarno vrijeme (epoch sekunde) kao os. */
void time_interpolation(const double *temp, size_t n, const long long *epoch, double *out);

/* Kubicni (prirodni) spline. Zahtijeva >= 4 poznate tocke. */
int cubic_interpolation(const double *temp, size_t n, double *out);

/* Spline reda 3 (ista jezgra kao cubic). Zahtijeva >= 4 poznate tocke. */
int spline_interpolation(const double *temp, size_t n, double *out);

#endif /* INTERPOLATION_H */
