#pragma once
#include "ITask.h"
#include <string>

class SimpleTask : public ITask {
public:
    SimpleTask(std::string name, int durationMs, bool shouldFail = false);
    std::string name() const override;
    void execute() override;

private:
    std::string name_;
    int durationMs_;
    bool shouldFail_;
};