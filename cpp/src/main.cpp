// Ulazna tocka -- C++ kopija diplomskog projekta (imputacija nedostajucih
// vrijednosti u temperaturnim vremenskim nizovima).
//
// Preslikava `python main.py --compare`: ucita niz, umjetno obrise dio
// vrijednosti, pokrene klasicne metode + KNN i ispise tablicu metrika.

#include <cstdio>
#include <cstring>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "config.hpp"
#include "data_loader.hpp"
#include "evaluation.hpp"
#include "interpolation_methods.hpp"
#include "ml_methods.hpp"
#include "preprocessing.hpp"
#include "time_series.hpp"

namespace {

using namespace thesis;

struct Options {
    bool compare = false;
    std::string source = "synthetic";
    std::string csv_path;
    std::string city;
    double missing_rate = 0.4;
    int n_neighbors = 5;
};

void print_help() {
    std::cout << "Diplomski projekt (C++ kopija) -- imputacija temperatura\n\n";
    std::cout << "Naredbe:\n";
    std::cout << "  --compare                  usporedi metode na umjetno ostecenom nizu\n";
    std::cout << "  --source <synthetic|demo>  izvor podataka (zadano: synthetic)\n";
    std::cout << "  --csv <putanja>            CSV za demo izvor (timestamp,city,temperature)\n";
    std::cout << "  --city <grad>              grad za demo izvor\n";
    std::cout << "  --missing-rate <0..1>      udio obrisanih vrijednosti (zadano: 0.4)\n";
    std::cout << "  --neighbors <n>            broj susjeda za KNN (zadano: 5)\n";
    std::cout << "\nPrimjer:\n";
    std::cout << "  ./thesis --compare --missing-rate 0.3\n";
    std::cout << "  ./thesis --compare --source demo --csv data/raw/temperature_demo_cities.csv --city Split\n";
}

bool parse_args(int argc, char** argv, Options& opts) {
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        auto next = [&](const char* name) -> std::string {
            if (i + 1 >= argc) {
                std::cerr << "Nedostaje vrijednost za " << name << "\n";
                return std::string();
            }
            return argv[++i];
        };

        if (arg == "--compare") opts.compare = true;
        else if (arg == "--source") opts.source = next("--source");
        else if (arg == "--csv") opts.csv_path = next("--csv");
        else if (arg == "--city") opts.city = next("--city");
        else if (arg == "--missing-rate") opts.missing_rate = std::stod(next("--missing-rate"));
        else if (arg == "--neighbors") opts.n_neighbors = std::stoi(next("--neighbors"));
        else if (arg == "--help" || arg == "-h") { print_help(); return false; }
        else {
            std::cerr << "Nepoznat argument: " << arg << "\n";
            return false;
        }
    }
    return true;
}

void print_comparison(const Options& opts) {
    const ExperimentSource source = parse_source(opts.source);
    const TimeSeries series = load_experiment_series(source, opts.csv_path, opts.city);

    const DamagedSeries damaged =
        create_missing_values(series, opts.missing_rate, /*random_state=*/42);

    int removed = 0;
    for (bool b : damaged.missing_mask) removed += b ? 1 : 0;

    std::printf("\n");
    std::printf("======================================================================\n");
    std::printf("USPOREDBA METODA IMPUTACIJE (C++ kopija)\n");
    std::printf("======================================================================\n");
    std::printf("Izvor:           %s\n", opts.source.c_str());
    if (source == ExperimentSource::Demo && !opts.city.empty()) {
        std::printf("Grad:            %s\n", opts.city.c_str());
    }
    std::printf("Zapisa:          %zu\n", series.size());
    std::printf("Obrisano (mask): %d (%.0f%%)\n", removed, opts.missing_rate * 100.0);
    std::printf("Raspon:          %s -> %s\n",
                format_datetime(series.timestamps.front()).c_str(),
                format_datetime(series.timestamps.back()).c_str());
    std::printf("\n");

    // Skupi sve rekonstrukcije: klasicne + KNN.
    std::map<std::string, TimeSeries> reconstructed =
        run_classical_interpolations(damaged.series);
    try {
        reconstructed["knn_imputation"] = knn_imputation(damaged.series, opts.n_neighbors);
    } catch (const std::exception& error) {
        std::printf("  [preskoceno] knn_imputation: %s\n", error.what());
    }

    std::vector<std::string> order = classical_method_names();
    order.push_back("knn_imputation");

    std::printf("%-22s %10s %10s %10s\n", "method", "mae", "rmse", "r2");
    std::printf("%-22s %10s %10s %10s\n", "----------------------", "--------",
                "--------", "--------");

    bool any = false;
    for (const std::string& name : order) {
        auto it = reconstructed.find(name);
        if (it == reconstructed.end()) continue;
        const Metrics m =
            evaluate_reconstruction(series, it->second, damaged.missing_mask);
        std::printf("%-22s %10.4f %10.4f %10.4f\n", name.c_str(), m.mae, m.rmse, m.r2);
        any = true;
    }

    if (!any) {
        std::printf("Nijedna metoda nije uspjela.\n");
    }
    std::printf("\n");
}

}  // namespace

int main(int argc, char** argv) {
    Options opts;
    if (!parse_args(argc, argv, opts)) return 0;

    try {
        if (opts.compare) {
            print_comparison(opts);
        } else {
            print_help();
        }
    } catch (const std::exception& error) {
        std::cerr << "Greska: " << error.what() << "\n";
        return 1;
    }
    return 0;
}
