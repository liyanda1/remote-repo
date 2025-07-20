#pragma once
#include "ITask.h"
#include <string>

/**
 * @brief SimpleTask 是 ITask 的具体实现
 * 模拟任务执行延迟，可选择性抛出异常。
 */
class SimpleTask : public ITask {
public:
    SimpleTask(std::string name, int durationMs, bool shouldFail = false);
    std::string name() const override;
    void execute() override;

private:
    std::string name_;  // 任务名称
    int durationMs_;    // 模拟执行耗时(毫秒)
    bool shouldFail_;   // 是否故意执行失败
};