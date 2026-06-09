#include "series.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Broj dana od 1970-01-01 za zadani gregorijanski datum (Howard Hinnant). */
static long long days_from_civil(int y, int m, int d) {
    y -= (m <= 2);
    long long era = (y >= 0 ? y : y - 399) / 400;
    unsigned yoe = (unsigned)(y - era * 400);
    unsigned doy = (153u * (unsigned)(m + (m > 2 ? -3 : 9)) + 2u) / 5u + (unsigned)(d - 1);
    unsigned doe = yoe * 365u + yoe / 4u - yoe / 100u + doy;
    return era * 146097LL + (long long)doe - 719468LL;
}

/*
 * Parsiranje vremenske oznake "YYYY-MM-DD HH:MM:SS" (sekunde su opcionalne).
 * Postavlja epoch (UTC), hour i yday. Vraca 0 kod uspjeha.
 */
static int parse_timestamp(const char *text, long long *epoch, int *hour, int *yday) {
    int Y = 0, M = 0, D = 0, h = 0, mi = 0, s = 0;
    int got = sscanf(text, "%d-%d-%d %d:%d:%d", &Y, &M, &D, &h, &mi, &s);
    if (got < 3) {
        return 1;
    }
    if (M < 1 || M > 12 || D < 1 || D > 31) {
        return 1;
    }

    long long days = days_from_civil(Y, M, D);
    *epoch = days * 86400LL + (long long)h * 3600LL + (long long)mi * 60LL + (long long)s;
    *hour = h;
    *yday = (int)(days - days_from_civil(Y, 1, 1)) + 1;
    return 0;
}

int series_alloc(Series *s, size_t n) {
    s->n = n;
    s->temp = (double *)malloc(n * sizeof(double));
    s->epoch = (long long *)malloc(n * sizeof(long long));
    s->hour = (int *)malloc(n * sizeof(int));
    s->yday = (int *)malloc(n * sizeof(int));
    if (!s->temp || !s->epoch || !s->hour || !s->yday) {
        series_free(s);
        return 1;
    }
    return 0;
}

void series_free(Series *s) {
    if (!s) {
        return;
    }
    free(s->temp);
    free(s->epoch);
    free(s->hour);
    free(s->yday);
    s->temp = NULL;
    s->epoch = NULL;
    s->hour = NULL;
    s->yday = NULL;
    s->n = 0;
}

/*
 * Vrati pokazivac na `wanted`-ti stupac u retku CSV-a (0-bazirano).
 * Mijenja `line` ubacujuci '\0' na granicama. Vraca NULL ako stupac ne postoji.
 */
static char *csv_field(char *line, int wanted) {
    int index = 0;
    char *start = line;
    for (char *p = line;; p++) {
        if (*p == ',' || *p == '\0' || *p == '\n' || *p == '\r') {
            int last = (*p == '\0' || *p == '\n' || *p == '\r');
            *p = '\0';
            if (index == wanted) {
                return start;
            }
            if (last) {
                return NULL;
            }
            index++;
            start = p + 1;
        }
    }
}

/* Pronadi indeks stupca po imenu u zaglavlju. Vraca -1 ako ne postoji. */
static int csv_find_column(const char *header, const char *name) {
    char buf[1024];
    strncpy(buf, header, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';

    int index = 0;
    char *start = buf;
    for (char *p = buf;; p++) {
        if (*p == ',' || *p == '\0' || *p == '\n' || *p == '\r') {
            int last = (*p == '\0' || *p == '\n' || *p == '\r');
            *p = '\0';
            if (strcmp(start, name) == 0) {
                return index;
            }
            if (last) {
                return -1;
            }
            index++;
            start = p + 1;
        }
    }
}

int series_load_csv(Series *s, const char *path, const char *city) {
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Greska: ne mogu otvoriti datoteku: %s\n", path);
        return 1;
    }

    char line[1024];
    if (!fgets(line, sizeof(line), f)) {
        fprintf(stderr, "Greska: prazna datoteka: %s\n", path);
        fclose(f);
        return 1;
    }

    int col_time = csv_find_column(line, "timestamp");
    int col_temp = csv_find_column(line, "temperature");
    int col_city = csv_find_column(line, "city");

    if (col_time < 0 || col_temp < 0) {
        fprintf(stderr, "Greska: nedostaje stupac timestamp ili temperature u %s\n", path);
        fclose(f);
        return 1;
    }

    size_t capacity = 512;
    size_t count = 0;
    double *temp = (double *)malloc(capacity * sizeof(double));
    long long *epoch = (long long *)malloc(capacity * sizeof(long long));
    int *hour = (int *)malloc(capacity * sizeof(int));
    int *yday = (int *)malloc(capacity * sizeof(int));
    if (!temp || !epoch || !hour || !yday) {
        free(temp); free(epoch); free(hour); free(yday);
        fclose(f);
        return 1;
    }

    char work[1024];
    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '\n' || line[0] == '\r' || line[0] == '\0') {
            continue;
        }

        /* Filtriranje po gradu (kopija retka jer csv_field mijenja sadrzaj). */
        if (city != NULL && col_city >= 0) {
            strncpy(work, line, sizeof(work) - 1);
            work[sizeof(work) - 1] = '\0';
            char *city_value = csv_field(work, col_city);
            if (city_value == NULL || strcmp(city_value, city) != 0) {
                continue;
            }
        }

        strncpy(work, line, sizeof(work) - 1);
        work[sizeof(work) - 1] = '\0';
        char *ts = csv_field(work, col_time);

        char work2[1024];
        strncpy(work2, line, sizeof(work2) - 1);
        work2[sizeof(work2) - 1] = '\0';
        char *tv = csv_field(work2, col_temp);

        if (ts == NULL || tv == NULL) {
            continue;
        }

        long long e = 0;
        int h = 0, yd = 0;
        if (parse_timestamp(ts, &e, &h, &yd) != 0) {
            continue;
        }

        char *endptr = NULL;
        double value = strtod(tv, &endptr);
        if (endptr == tv) {
            continue;
        }

        if (count == capacity) {
            capacity *= 2;
            double *t2 = (double *)realloc(temp, capacity * sizeof(double));
            long long *e2 = (long long *)realloc(epoch, capacity * sizeof(long long));
            int *h2 = (int *)realloc(hour, capacity * sizeof(int));
            int *y2 = (int *)realloc(yday, capacity * sizeof(int));
            if (!t2 || !e2 || !h2 || !y2) {
                free(t2 ? t2 : temp);
                free(e2 ? e2 : epoch);
                free(h2 ? h2 : hour);
                free(y2 ? y2 : yday);
                fclose(f);
                return 1;
            }
            temp = t2; epoch = e2; hour = h2; yday = y2;
        }

        temp[count] = value;
        epoch[count] = e;
        hour[count] = h;
        yday[count] = yd;
        count++;
    }

    fclose(f);

    if (count < 2) {
        fprintf(stderr, "Greska: premalo zapisa (%zu) u %s\n", count, path);
        free(temp); free(epoch); free(hour); free(yday);
        return 1;
    }

    s->n = count;
    s->temp = temp;
    s->epoch = epoch;
    s->hour = hour;
    s->yday = yday;
    return 0;
}
