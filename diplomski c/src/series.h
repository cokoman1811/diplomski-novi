#ifndef SERIES_H
#define SERIES_H

#include <stddef.h>

/*
 * Temperaturni vremenski niz.
 *
 * temp[i]  - vrijednost temperature (moze biti NAN ako je nedostajuca)
 * epoch[i] - vrijeme mjerenja u sekundama od 1970-01-01 (UTC)
 * hour[i]  - sat u danu (0-23), znacajka za KNN
 * yday[i]  - redni dan u godini (1-366), znacajka za KNN
 */
typedef struct {
    size_t n;
    double *temp;
    long long *epoch;
    int *hour;
    int *yday;
} Series;

/* Alokacija niza od n elemenata. Vraca 0 kod neuspjeha. */
int series_alloc(Series *s, size_t n);

/* Oslobadanje memorije niza. */
void series_free(Series *s);

/*
 * Ucitavanje temperaturnog niza iz CSV datoteke.
 *
 * Podrzava dva formata (prepoznaje se iz zaglavlja):
 *   - timestamp,city,temperature  (demo datoteka s vise gradova)
 *   - timestamp,temperature        (obradena datoteka)
 *
 * city != NULL filtrira retke po gradu (samo za demo format).
 *
 * Vraca 0 kod uspjeha, != 0 kod greske (poruka se ispisuje na stderr).
 */
int series_load_csv(Series *s, const char *path, const char *city);

#endif /* SERIES_H */
