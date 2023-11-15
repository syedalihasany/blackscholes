cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(torch_wrapper)

list(APPEND CMAKE_PREFIX_PATH "/home/bohan/benchmarks_tester/AxBench/libtorch")
find_package(Torch REQUIRED)

add_executable(blackscholes blackscholes.cpp)
target_link_libraries(blackscholes "${TORCH_LIBRARIES}")
set_property(TARGET blackscholes PROPERTY CXX_STANDARD 17)
#[[the line belowis added to allow Cmake to find the torch installation]]
set(Torch_DIR "/home/bohan/.local/lib/python3.8/site-packages")
