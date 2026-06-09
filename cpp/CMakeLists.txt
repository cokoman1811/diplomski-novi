cmake_minimum_required(VERSION 3.15)
project(thesis_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(thesis
    src/main.cpp
    src/time_series.cpp
    src/data_loader.cpp
    src/preprocessing.cpp
    src/interpolation_methods.cpp
    src/ml_methods.cpp
    src/evaluation.cpp
)

target_include_directories(thesis PRIVATE include)

if(MSVC)
    target_compile_options(thesis PRIVATE /W4)
else()
    target_compile_options(thesis PRIVATE -Wall -Wextra -O2)
endif()
