#ifndef PREPROCESSING_H
#define PREPROCESSING_H

#include <stddef.h>

/*
 * Umjetno uklanjanje vrijednosti iz niza radi evaluacije.
 *
 * temp        - ulazni temperaturni niz (n vrijednosti)
 * n           - broj vrijednosti
 * missing_rate- udio vrijednosti za uklanjanje (0..1)
 * seed        - sjeme za ponovljiv slucajni odabir
 * damaged     - izlaz: kopija niza s NAN na uklonjenim mjestima (velicina n)
 * mask        - izlaz: 1 gdje je vrijednost uklonjena, inace 0 (velicina n)
 *
 * Prva i zadnja vrijednost se uvijek cuvaju (rubni oslonci za interpolaciju).
 * Vraca broj uklonjenih vrijednosti.
 */
size_t create_missing_values(const double *temp, size_t n, double missing_rate,
                             unsigned long long seed, double *damaged, int *mask);

#endif /* PREPROCESSING_H */
