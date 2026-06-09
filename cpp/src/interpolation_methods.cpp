#include "interpolation_methods.hpp"

#include <algorithm>
#include <cstdio>
#include <stdexcept>

namespace thesis {

const std::vector<std::string>& classical_method_names() {
    static const std::vector<std::string> names = {
        "forward_fill",      "linear_interpolation", "time_interpolation",
        "cubic_interpolation", "spline_interpolation",
    };
    return names;
}

namespace {

// Popuni preostale rubne NaN: prvo forward, zatim backward.
void fill_remaining_gaps(std::vector<double>& v) {
    double last = quiet_nan();
    for (double& x : v) {
        if (!is_missing(x)) last = x;
        else if (!is_missing(last)) x = last;
    }
    double next = quiet_nan();
    for (auto it = v.rbegin(); it != v.rend(); ++it) {
        if (!is_missing(*it)) next = *it;
        else if (!is_missing(next)) *it = next;
    }
}

// Indeksi i vrijednosti poznatih (ne-NaN) tocaka.
void collect_known(const TimeSeries& s, std::vector<double>& xs,
                   std::vector<double>& ys, bool use_time) {
    for (std::size_t i = 0; i < s.size(); ++i) {
        if (is_missing(s.values[i])) continue;
        xs.push_back(use_time ? static_cast<double>(s.timestamps[i])
                              : static_cast<double>(i));
        ys.push_back(s.values[i]);
    }
}

// Linearna interpolacija nad poznatim (x,y) tockama na zadanoj x koordinati.
double linear_at(const std::vector<double>& xs, const std::vector<double>& ys,
                 double x) {
    if (x <= xs.front()) return ys.front();
    if (x >= xs.back()) return ys.back();
    auto upper = std::lower_bound(xs.begin(), xs.end(), x);
    std::size_t j = static_cast<std::size_t>(upper - xs.begin());
    std::size_t i = j - 1;
    const double t = (x - xs[i]) / (xs[j] - xs[i]);
    return ys[i] + t * (ys[j] - ys[i]);
}

// Koeficijenti drugih derivacija za natural cubic spline (Numerical Recipes).
std::vector<double> natural_spline_second_derivatives(const std::vector<double>& x,
                                                      const std::vector<double>& y) {
    const std::size_t n = x.size();
    std::vector<double> y2(n, 0.0), u(n, 0.0);
    // Prirodni rubni uvjeti: y2[0] = y2[n-1] = 0.
    for (std::size_t i = 1; i + 1 < n; ++i) {
        const double sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1]);
        const double p = sig * y2[i - 1] + 2.0;
        y2[i] = (sig - 1.0) / p;
        double diff = (y[i + 1] - y[i]) / (x[i + 1] - x[i]) -
                      (y[i] - y[i - 1]) / (x[i] - x[i - 1]);
        u[i] = (6.0 * diff / (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p;
    }
    for (std::size_t k = n - 1; k-- > 0;) {
        y2[k] = y2[k] * y2[k + 1] + u[k];
    }
    return y2;
}

double spline_at(const std::vector<double>& xs, const std::vector<double>& ys,
                 const std::vector<double>& y2, double x) {
    if (x <= xs.front()) return ys.front();
    if (x >= xs.back()) return ys.back();
    auto upper = std::lower_bound(xs.begin(), xs.end(), x);
    std::size_t khi = static_cast<std::size_t>(upper - xs.begin());
    std::size_t klo = khi - 1;
    const double h = xs[khi] - xs[klo];
    const double a = (xs[khi] - x) / h;
    const double b = (x - xs[klo]) / h;
    return a * ys[klo] + b * ys[khi] +
           ((a * a * a - a) * y2[klo] + (b * b * b - b) * y2[khi]) * (h * h) / 6.0;
}

TimeSeries interpolate_generic(const TimeSeries& series, bool use_time, bool cubic) {
    TimeSeries result = series;

    std::vector<double> xs, ys;
    collect_known(series, xs, ys, use_time);

    if (!xs.empty()) {
        std::vector<double> y2;
        if (cubic) y2 = natural_spline_second_derivatives(xs, ys);

        for (std::size_t i = 0; i < series.size(); ++i) {
            if (!is_missing(series.values[i])) continue;
            const double x = use_time ? static_cast<double>(series.timestamps[i])
                                      : static_cast<double>(i);
            result.values[i] = cubic ? spline_at(xs, ys, y2, x)
                                     : linear_at(xs, ys, x);
        }
    }

    fill_remaining_gaps(result.values);
    return result;
}

}  // namespace

TimeSeries forward_fill_interpolation(const TimeSeries& series) {
    TimeSeries result = series;
    fill_remaining_gaps(result.values);
    return result;
}

TimeSeries linear_interpolation(const TimeSeries& series) {
    return interpolate_generic(series, /*use_time=*/false, /*cubic=*/false);
}

TimeSeries time_interpolation(const TimeSeries& series) {
    return interpolate_generic(series, /*use_time=*/true, /*cubic=*/false);
}

TimeSeries cubic_interpolation(const TimeSeries& series) {
    if (known_count(series) < 4) {
        throw std::invalid_argument("cubic interpolacija treba barem 4 poznate vrijednosti.");
    }
    return interpolate_generic(series, /*use_time=*/false, /*cubic=*/true);
}

TimeSeries spline_interpolation(const TimeSeries& series) {
    if (known_count(series) < 4) {
        throw std::invalid_argument("spline interpolacija treba barem 4 poznate vrijednosti.");
    }
    return interpolate_generic(series, /*use_time=*/true, /*cubic=*/true);
}

std::map<std::string, TimeSeries> run_classical_interpolations(const TimeSeries& series,
                                                               bool quiet) {
    std::map<std::string, TimeSeries> results;

    struct Entry {
        const char* name;
        TimeSeries (*fn)(const TimeSeries&);
    };
    const Entry entries[] = {
        {"forward_fill", forward_fill_interpolation},
        {"linear_interpolation", linear_interpolation},
        {"time_interpolation", time_interpolation},
        {"cubic_interpolation", cubic_interpolation},
        {"spline_interpolation", spline_interpolation},
    };

    for (const Entry& e : entries) {
        try {
            results[e.name] = e.fn(series);
        } catch (const std::exception& error) {
            if (!quiet) {
                std::printf("  [preskoceno] %s: %s\n", e.name, error.what());
            }
        }
    }
    return results;
}

}  // namespace thesis
