#include "time_series.hpp"

#include <cmath>
#include <cstdio>
#include <limits>
#include <stdexcept>

namespace thesis {

double quiet_nan() { return std::numeric_limits<double>::quiet_NaN(); }

bool is_missing(double value) { return std::isnan(value); }

std::size_t known_count(const TimeSeries& series) {
    std::size_t count = 0;
    for (double v : series.values) {
        if (!is_missing(v)) ++count;
    }
    return count;
}

namespace {

// Algoritam "days from civil" (Howard Hinnant) -- pretvara y/m/d u broj dana
// od 1970-01-01. Radi jednako na svim platformama (bez mktime/timegm).
std::int64_t days_from_civil(int y, unsigned m, unsigned d) {
    y -= m <= 2;
    const int era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = static_cast<unsigned>(y - era * 400);
    const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return static_cast<std::int64_t>(era) * 146097 + static_cast<int>(doe) - 719468;
}

// Inverz: broj dana od epohe -> godina/mjesec/dan.
void civil_from_days(std::int64_t z, int& y, unsigned& m, unsigned& d) {
    z += 719468;
    const std::int64_t era = (z >= 0 ? z : z - 146096) / 146097;
    const unsigned doe = static_cast<unsigned>(z - era * 146097);
    const unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    const int yr = static_cast<int>(yoe) + static_cast<int>(era) * 400;
    const unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    const unsigned mp = (5 * doy + 2) / 153;
    d = doy - (153 * mp + 2) / 5 + 1;
    m = mp + (mp < 10 ? 3 : -9);
    y = yr + (m <= 2);
}

}  // namespace

std::int64_t parse_datetime(const std::string& text) {
    int year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0;
    // Podrzi i "YYYY-MM-DD HH:MM:SS" i samo "YYYY-MM-DD".
    int matched = std::sscanf(text.c_str(), "%d-%d-%d %d:%d:%d", &year, &month,
                              &day, &hour, &minute, &second);
    if (matched < 3) {
        throw std::invalid_argument("Neispravan format datuma: " + text);
    }
    std::int64_t days = days_from_civil(year, static_cast<unsigned>(month),
                                        static_cast<unsigned>(day));
    return days * 86400 + hour * 3600 + minute * 60 + second;
}

std::string format_datetime(std::int64_t epoch_seconds) {
    std::int64_t days = epoch_seconds / 86400;
    std::int64_t rem = epoch_seconds % 86400;
    if (rem < 0) {
        rem += 86400;
        --days;
    }
    int year;
    unsigned month, day;
    civil_from_days(days, year, month, day);
    const int hour = static_cast<int>(rem / 3600);
    const int minute = static_cast<int>((rem % 3600) / 60);
    const int second = static_cast<int>(rem % 60);

    char buffer[32];
    std::snprintf(buffer, sizeof(buffer), "%04d-%02u-%02u %02d:%02d:%02d", year,
                  month, day, hour, minute, second);
    return std::string(buffer);
}

int hour_of_day(std::int64_t epoch_seconds) {
    std::int64_t rem = epoch_seconds % 86400;
    if (rem < 0) rem += 86400;
    return static_cast<int>(rem / 3600);
}

int day_of_year(std::int64_t epoch_seconds) {
    std::int64_t days = epoch_seconds / 86400;
    if (epoch_seconds % 86400 < 0) --days;
    int year;
    unsigned month, day;
    civil_from_days(days, year, month, day);
    std::int64_t jan1 = days_from_civil(year, 1, 1);
    return static_cast<int>(days - jan1) + 1;
}

}  // namespace thesis
