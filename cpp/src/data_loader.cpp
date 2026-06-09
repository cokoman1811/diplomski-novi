#include "data_loader.hpp"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <random>
#include <sstream>
#include <stdexcept>

#include "config.hpp"

namespace thesis {

ExperimentSource parse_source(const std::string& name) {
    if (name == "synthetic" || name == "jena_quick") return ExperimentSource::Synthetic;
    if (name == "demo") return ExperimentSource::Demo;
    throw std::invalid_argument("Nepoznat izvor podataka: " + name);
}

TimeSeries generate_synthetic_series(int hours, unsigned int seed) {
    const int interval = config::JENA_INTERVAL_MINUTES;  // minute
    const int samples = hours * 60 / interval;

    TimeSeries series;
    series.timestamps.reserve(samples);
    series.values.reserve(samples);

    // Pocetak: 2009-01-01 00:10:00 (kao prvi Jena zapis), UTC.
    const std::int64_t start = parse_datetime("2009-01-01 00:10:00");
    const std::int64_t step = static_cast<std::int64_t>(interval) * 60;

    std::mt19937 rng(seed);
    std::normal_distribution<double> noise(0.0, 0.4);

    const double pi = 3.14159265358979323846;
    for (int i = 0; i < samples; ++i) {
        const std::int64_t ts = start + static_cast<std::int64_t>(i) * step;
        const double hours_elapsed = (i * interval) / 60.0;
        // Dnevni ciklus: minimum oko 5h ujutro, maksimum oko 15h.
        const double daily = 6.0 * std::sin(2.0 * pi * (hours_elapsed - 9.0) / 24.0);
        const double base = 2.0;          // prosjecna zimska temperatura
        const double trend = 0.01 * i;    // lagani porast tijekom uzorka
        const double value = base + daily + trend + noise(rng);
        series.timestamps.push_back(ts);
        series.values.push_back(value);
    }
    return series;
}

namespace {

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> fields;
    std::string field;
    std::stringstream stream(line);
    while (std::getline(stream, field, ',')) {
        // makni eventualni \r (Windows CRLF)
        if (!field.empty() && field.back() == '\r') field.pop_back();
        fields.push_back(field);
    }
    return fields;
}

}  // namespace

TimeSeries load_demo_series(const std::string& csv_path, const std::string& city) {
    std::ifstream file(csv_path);
    if (!file.is_open()) {
        throw std::runtime_error("CSV datoteka ne postoji: " + csv_path);
    }

    std::string header_line;
    if (!std::getline(file, header_line)) {
        throw std::runtime_error("CSV datoteka je prazna: " + csv_path);
    }
    std::vector<std::string> headers = split_csv_line(header_line);

    int ts_col = -1, city_col = -1, temp_col = -1;
    for (std::size_t i = 0; i < headers.size(); ++i) {
        if (headers[i] == "timestamp") ts_col = static_cast<int>(i);
        else if (headers[i] == "city") city_col = static_cast<int>(i);
        else if (headers[i] == "temperature") temp_col = static_cast<int>(i);
    }
    if (ts_col < 0 || temp_col < 0) {
        throw std::runtime_error("Nedostaju stupci 'timestamp'/'temperature' u CSV-u.");
    }

    struct Row {
        std::int64_t ts;
        double temp;
    };
    std::vector<Row> rows;

    std::string line;
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        std::vector<std::string> fields = split_csv_line(line);
        if (static_cast<int>(fields.size()) <= temp_col) continue;
        if (city_col >= 0 && !city.empty() && fields[city_col] != city) continue;

        Row row;
        row.ts = parse_datetime(fields[ts_col]);
        row.temp = std::stod(fields[temp_col]);
        rows.push_back(row);
    }

    if (rows.empty()) {
        throw std::runtime_error("Nema podataka" + (city.empty() ? std::string() : (" za grad: " + city)));
    }

    std::sort(rows.begin(), rows.end(),
              [](const Row& a, const Row& b) { return a.ts < b.ts; });

    TimeSeries series;
    series.timestamps.reserve(rows.size());
    series.values.reserve(rows.size());
    for (const Row& row : rows) {
        series.timestamps.push_back(row.ts);
        series.values.push_back(row.temp);
    }
    return series;
}

TimeSeries load_experiment_series(ExperimentSource source,
                                  const std::string& csv_path,
                                  const std::string& city) {
    switch (source) {
        case ExperimentSource::Synthetic:
            return generate_synthetic_series(config::QUICK_SAMPLE_HOURS);
        case ExperimentSource::Demo:
            return load_demo_series(csv_path, city);
    }
    throw std::invalid_argument("Nepoznat izvor podataka.");
}

}  // namespace thesis
