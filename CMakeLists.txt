cmake_minimum_required(VERSION 3.10)
project(TaskScheduler)

set(CMAKE_CXX_STANDARD 11)
enable_testing()

include_directories(include)

add_library(SchedulerLib src/Scheduler.cpp src/SimpleTask.cpp)
add_executable(SchedulerTest tests/SchedulerTest.cpp)
target_link_libraries(SchedulerTest SchedulerLib gtest gmock pthread)

add_test(NAME SchedulerTest COMMAND SchedulerTest)