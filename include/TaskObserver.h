#pragma once
#include <string>

class TaskObserver {
public:
    virtual ~TaskObserver() = default;
    virtual void onTaskStart(const std::string& taskName) = 0;
    virtual void onTaskComplete(const std::string& taskName) = 0;
    virtual void onTaskError(const std::string& taskName, const std::string& error) = 0;
};