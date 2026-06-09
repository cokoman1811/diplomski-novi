#ifndef ML_METHODS_H
#define ML_METHODS_H

#include "series.h"

/*
 * KNN imputacija temperature.
 *
 * Model se "uci" samo na poznatim vrijednostima i predvida samo na
 * nedostajucim mjestima. Znacajke su (pozicija, sat u danu, dan u godini),
 * udaljenost je euklidska. Predikcija je prosjek k najblizih susjeda.
 *
 * series     - niz sa znacajkama (hour, yday, n)
 * temp       - ostecen niz vrijednosti (NAN na nedostajucim mjestima)
 * n_neighbors- broj susjeda (k); efektivno se ogranicava na broj poznatih
 * out        - izlaz (velicina series->n), bez NAN vrijednosti
 *
 * Vraca 0 kod uspjeha, != 0 ako nema poznatih vrijednosti.
 */
int knn_imputation(const Series *series, const double *temp, int n_neighbors, double *out);

#endif /* ML_METHODS_H */
