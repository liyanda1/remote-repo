
cmake_minimum_required(VERSION 3.10)
project(StringUtilsTest)

set(CMAKE_CXX_STANDARD 11)
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

add_executable(string_utils_test string_utils_test.cpp string_utils.cpp)
target_link_libraries(string_utils_test ${GTEST_LIBRARIES} pthread)
