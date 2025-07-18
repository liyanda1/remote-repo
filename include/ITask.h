#pragma once
#include <string>

class ITask {
public:
    virtual ~ITask() = default;
    virtual std::string name() const = 0;
    virtual void execute() = 0;
};