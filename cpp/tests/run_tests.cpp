// Testovi za C++ kopiju diplomskog (preslikano iz tests/*.py).
// Mali vlastiti test harness -- nema vanjskih biblioteka (bez pytest-a).

#include <cmath>
#include <cstdio>
#include <string>
#include <vector>

#include "data_loader.hpp"
#include "evaluation.hpp"
#include "interpolation_methods.hpp"
#include "ml_methods.hpp"
#include "preprocessing.hpp"
#include "time_series.hpp"

using namespace thesis;

namespace {

int g_failures = 0;
int g_checks = 0;

void check(bool condition, const std::string& message) {
    ++g_checks;
    if (!condition) {
        ++g_failures;
        std::printf("  [FAIL] %s\n", message.c_str());
    } else {
        std::printf("  [ok]   %s\n", message.c_str());
    }
}

void check_near(double a, double b, double tol, const std::string& message) {
    check(std::fabs(a - b) <= tol, message);
}

// Mali niz s rupama, ekvivalent SAMPLE_SERIES iz test_ml_methods.py.
// 8 sati, vrijednosti [10,11,NaN,13,NaN,15,16,17].
TimeSeries sample_series() {
    TimeSeries s;
    const std::int64_t start = parse_datetime("2024-01-01 00:00:00");
    const double vals[] = {10.0, 11.0, 0.0, 13.0, 0.0, 15.0, 16.0, 17.0};
    const bool missing[] = {false, false, true, false, true, false, false, false};
    for (int i = 0; i < 8; ++i) {
        s.timestamps.push_back(start + static_cast<std::int64_t>(i) * 3600);
        s.values.push_back(missing[i] ? quiet_nan() : vals[i]);
    }
    return s;
}

void test_knn() {
    std::printf("\n== KNN imputacija ==\n");
    const TimeSeries sample = sample_series();
    const TimeSeries result = knn_imputation(sample, 3);

    check(result.size() == sample.size(), "isti broj zapisa");

    bool no_nan = true;
    for (double v : result.values) no_nan = no_nan && !is_missing(v);
    check(no_nan, "nema NaN nakon imputacije");

    // Poznate vrijednosti ostaju nepromijenjene.
    bool known_unchanged = true;
    for (std::size_t i = 0; i < sample.size(); ++i) {
        if (!is_missing(sample.values[i])) {
            known_unchanged = known_unchanged &&
                              (result.values[i] == sample.values[i]);
        }
    }
    check(known_unchanged, "poznate vrijednosti nepromijenjene");

    check_near(result.values[2], 12.0, 2.0, "rupa na poziciji 2 ~ 12");
    check_near(result.values[4], 14.0, 2.0, "rupa na poziciji 4 ~ 14");

    // Original se ne mijenja.
    check(is_missing(sample.values[2]), "original i dalje ima NaN (kopija, ne mutacija)");
}

void test_preprocessing() {
    std::printf("\n== Preprocessing (create_missing_values) ==\n");
    const TimeSeries series = generate_synthetic_series(48);
    const DamagedSeries damaged = create_missing_values(series, 0.4, 42);

    check(damaged.series.size() == series.size(), "isti broj zapisa nakon ostecenja");

    // Prva i zadnja vrijednost se cuvaju.
    check(!is_missing(damaged.series.values.front()), "prva vrijednost ocuvana");
    check(!is_missing(damaged.series.values.back()), "zadnja vrijednost ocuvana");

    int mask_count = 0, nan_count = 0;
    for (std::size_t i = 0; i < series.size(); ++i) {
        if (damaged.missing_mask[i]) ++mask_count;
        if (is_missing(damaged.series.values[i])) ++nan_count;
    }
    check(mask_count == nan_count, "broj maske == broj NaN");
    check(mask_count > 0, "nesto je obrisano");

    // Original niz nije promijenjen.
    bool original_intact = true;
    for (double v : series.values) original_intact = original_intact && !is_missing(v);
    check(original_intact, "original nije promijenjen (bez NaN)");
}

void test_interpolation() {
    std::printf("\n== Klasicne interpolacije ==\n");
    const TimeSeries series = generate_synthetic_series(48);
    const DamagedSeries damaged = create_missing_values(series, 0.4, 42);

    const auto results = run_classical_interpolations(damaged.series, /*quiet=*/true);

    for (const std::string& name : classical_method_names()) {
        auto it = results.find(name);
        if (it == results.end()) {
            check(false, name + " je proizvela rezultat");
            continue;
        }
        bool no_nan = true;
        for (double v : it->second.values) no_nan = no_nan && !is_missing(v);
        check(no_nan, name + ": nema NaN");
        check(it->second.size() == series.size(), name + ": isti broj zapisa");
    }

    // forward_fill: rupa dobiva zadnju poznatu vrijednost.
    TimeSeries tiny;
    tiny.timestamps = {0, 3600, 7200};
    tiny.values = {5.0, quiet_nan(), 9.0};
    const TimeSeries ff = forward_fill_interpolation(tiny);
    check_near(ff.values[1], 5.0, 1e-9, "forward_fill kopira zadnju poznatu");

    // linear: sredina izmedu 5 i 9 je 7.
    const TimeSeries lin = linear_interpolation(tiny);
    check_near(lin.values[1], 7.0, 1e-9, "linear: sredina 5 i 9 = 7");
}

void test_metrics() {
    std::printf("\n== Evaluacija (MAE/RMSE/R2) ==\n");
    TimeSeries original;
    original.timestamps = {0, 1, 2, 3};
    original.values = {1.0, 2.0, 3.0, 4.0};

    // Savrsena rekonstrukcija.
    const Metrics perfect = evaluate_reconstruction(original, original);
    check_near(perfect.mae, 0.0, 1e-9, "savrsena: MAE = 0");
    check_near(perfect.rmse, 0.0, 1e-9, "savrsena: RMSE = 0");
    check_near(perfect.r2, 1.0, 1e-9, "savrsena: R2 = 1");

    // Konstantna pogreska od 2 na svakoj tocki.
    TimeSeries off = original;
    for (double& v : off.values) v += 2.0;
    const Metrics m = evaluate_reconstruction(original, off);
    check_near(m.mae, 2.0, 1e-9, "pomak 2: MAE = 2");
    check_near(m.rmse, 2.0, 1e-9, "pomak 2: RMSE = 2");
}

}  // namespace

int main() {
    std::printf("======================================================================\n");
    std::printf("TESTOVI -- C++ kopija diplomskog\n");
    std::printf("======================================================================\n");

    test_knn();
    test_preprocessing();
    test_interpolation();
    test_metrics();

    std::printf("\n----------------------------------------------------------------------\n");
    std::printf("Provjera: %d  |  Pala: %d\n", g_checks, g_failures);
    std::printf("Rezultat: %s\n", g_failures == 0 ? "SVE PROLAZI" : "IMA GRESAKA");
    return g_failures == 0 ? 0 : 1;
}
