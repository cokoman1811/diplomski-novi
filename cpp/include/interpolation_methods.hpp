#pragma once

#include <map>
#include <string>
#include <vector>

#include "time_series.hpp"

namespace thesis {

// Imena klasicnih metoda (preslikano iz CLASSICAL_METHOD_NAMES).
const std::vector<std::string>& classical_method_names();

// Popuni nedostajuce vrijednosti zadnjom poznatom (forward fill), pa rubovi bfill.
TimeSeries forward_fill_interpolation(const TimeSeries& series);

// Linearna interpolacija po rednom broju mjerenja.
TimeSeries linear_interpolation(const TimeSeries& series);

// Linearna interpolacija uz obzir stvarnog vremena izmedu mjerenja.
TimeSeries time_interpolation(const TimeSeries& series);

// Kubicna (natural cubic spline) interpolacija; treba >= 4 poznate tocke.
TimeSeries cubic_interpolation(const TimeSeries& series);

// Spline interpolacija reda 3; treba >= 4 poznate tocke.
TimeSeries spline_interpolation(const TimeSeries& series);

// Pokreni sve klasicne metode na istom nizu. Metode koje ne uspiju se preskacu.
std::map<std::string, TimeSeries> run_classical_interpolations(const TimeSeries& series,
                                                               bool quiet = false);

}  // namespace thesis
