#ifndef EXECUTOR_EXECUTOR_INTERFACE_H
#define EXECUTOR_EXECUTOR_INTERFACE_H

#include <stdint.h>
#include "direction.h"
#include "executor_status.h"

namespace executor {

class IExecutor {
public:
    virtual ~IExecutor() = default;

    IExecutor(const IExecutor&) = delete;
    IExecutor& operator=(const IExecutor&) = delete;
    IExecutor(IExecutor&&) = delete;
    IExecutor& operator=(IExecutor&&) = delete;

    virtual void Init(int32_t x, int32_t y, Heading heading) = 0;

    virtual void TurnRight() = 0;
    virtual void TurnLeft() = 0;

    virtual void Forward() = 0;
    virtual void Backward() = 0;

    virtual ExecutorStatus GetStatus() const = 0;
};

} // namespace executor

#endif // EXECUTOR_EXECUTOR_INTERFACE_H

