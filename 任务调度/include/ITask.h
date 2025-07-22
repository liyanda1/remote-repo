#pragma once
#include <string>

/**
 * @brief ITask 定义了任务接口，所有具体任务必须实现。
 */
class ITask {
public:
    virtual ~ITask() = default;
    virtual std::string name() const = 0;
    virtual void execute() = 0;
};