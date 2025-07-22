#include "SimpleTask.h"
#include <iostream>
#include <thread>
#include <chrono>
#include <stdexcept>

SimpleTask::SimpleTask(std::string name, int durationMs, bool shouldFail)
    : name_(std::move(name)), durationMs_(durationMs), shouldFail_(shouldFail) {}

std::string SimpleTask::name() const {
    return name_;
}

void SimpleTask::execute() {
    std::this_thread::sleep_for(std::chrono::milliseconds(durationMs_));
    if (shouldFail_) {
        throw std::runtime_error("Task failed intentionally: " + name_);
    }
    std::cout << "Executed " << name_ << " successfully.\n";
}