cmake_minimum_required(VERSION 3.15)
project(thesis_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Zajednicki moduli (sve osim ulaznih tocaka main/app/test).
set(THESIS_CORE
    src/time_series.cpp
    src/data_loader.cpp
    src/preprocessing.cpp
    src/interpolation_methods.cpp
    src/ml_methods.cpp
    src/evaluation.cpp
)

add_executable(thesis src/main.cpp ${THESIS_CORE})
add_executable(app src/app.cpp)
add_executable(tests tests/run_tests.cpp ${THESIS_CORE})

foreach(target thesis app tests)
    target_include_directories(${target} PRIVATE include)
    if(MSVC)
        target_compile_options(${target} PRIVATE /W4)
    else()
        target_compile_options(${target} PRIVATE -Wall -Wextra -O2)
    endif()
endforeach()

enable_testing()
add_test(NAME unit_tests COMMAND tests)
