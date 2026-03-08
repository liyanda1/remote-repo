#ifndef EXECUTOR_ROBOT_EXECUTOR_H
#define EXECUTOR_ROBOT_EXECUTOR_H

#include <stdint.h>
#include <mutex>
#include "executor_interface.h"

namespace executor {

// 线程安全的扫地机执行器默认实现，可被 Config/Controller 等多线程调用
class Executor : public IExecutor {
public:
    Executor();

    // 由 Config 组件调用，用于初始化扫地机位置和朝向
    void Init(int32_t x, int32_t y, Heading heading) override;

    void TurnRight() override;
    void TurnLeft() override;

    void Forward() override;
    void Backward() override;

    ExecutorStatus GetStatus() const override;

private:
    // 内部使用的状态填充函数，不对外暴露
    void GetStatus(int32_t& x, int32_t& y, Heading& heading) const;

    static Heading NormalizeHeading(int32_t h);

    // 按当前朝向移动一步，step 为正表示前进，为负表示后退
    void MoveAlongHeading(int32_t step);

    mutable std::mutex m_mutex;
    int32_t m_x;
    int32_t m_y;
    Heading m_heading;
};

} // namespace executor

#endif // EXECUTOR_ROBOT_EXECUTOR_H

