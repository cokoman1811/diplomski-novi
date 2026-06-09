#pragma once

#include "time_series.hpp"

namespace thesis {

// Popuni nedostajuce vrijednosti K-najblizih-susjeda regresijom.
// Model se uci samo na poznatim vrijednostima, predvida na nedostajucim.
// Znacajke: [redni broj, sat u danu, dan u godini] -- kao u Python verziji.
TimeSeries knn_imputation(const TimeSeries& series, int n_neighbors = 5);

}  // namespace thesis
