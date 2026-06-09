#pragma once

#include <cstdint>
#include <string>
#include <vector>

namespace thesis {

// Jednostavan vremenski niz: paralelni vektori vremenskih oznaka i vrijednosti.
// Nedostajuca vrijednost je predstavljena s NaN (vidi is_missing / kNaN).
//
// Ekvivalent pandas `pd.Series` s DatetimeIndex iz Python verzije, ali bez
// vanjskih biblioteka -- samo standardni C++.
struct TimeSeries {
    // Vrijeme mjerenja kao Unix epoch sekunde (UTC).
    std::vector<std::int64_t> timestamps;
    // Temperatura; NaN znaci da vrijednost nedostaje.
    std::vector<double> values;

    std::size_t size() const { return values.size(); }
    bool empty() const { return values.empty(); }
};

// Vrijednost koja oznacava "nedostaje" (ekvivalent np.nan).
double quiet_nan();

// Provjeri je li vrijednost nedostajuca (NaN).
bool is_missing(double value);

// Broj poznatih (ne-NaN) vrijednosti u nizu.
std::size_t known_count(const TimeSeries& series);

// Parsiraj "YYYY-MM-DD HH:MM:SS" u epoch sekunde (UTC). Baca na gresku.
std::int64_t parse_datetime(const std::string& text);

// Formatiraj epoch sekunde natrag u "YYYY-MM-DD HH:MM:SS" (UTC).
std::string format_datetime(std::int64_t epoch_seconds);

// Sat u danu (0-23) za zadanu epoch oznaku.
int hour_of_day(std::int64_t epoch_seconds);

// Dan u godini (1-366) za zadanu epoch oznaku.
int day_of_year(std::int64_t epoch_seconds);

}  // namespace thesis
