#ifndef EXECUTOR_ROBOT_EXECUTOR_H
#define EXECUTOR_ROBOT_EXECUTOR_H

#include <stdint.h>
#include <mutex>

namespace executor {

enum Heading {
    HEADING_NORTH = 0,
    HEADING_EAST,
    HEADING_SOUTH,
    HEADING_WEST
};

// 线程安全的扫地机执行器，可被 Config/Controller 等多线程调用
class Executor {
public:
    Executor();

    // 禁止拷贝与移动，避免多线程下共享同一内部状态
    Executor(const Executor&) = delete;
    Executor& operator=(const Executor&) = delete;
    Executor(Executor&&) = delete;
    Executor& operator=(Executor&&) = delete;

    // 由 Config 组件调用，用于初始化扫地机位置和朝向
    // heading 若超出 [NORTH,WEST] 会被规范到合法范围
    void init(int32_t x, int32_t y, Heading heading);

    // 由 Controller 组件调用的动作接口：右转/左转 90 度，位置保持不变
    // 未初始化时调用为 no-op，不改变状态
    void turnRight();
    void turnLeft();

    // 由 Controller 组件调用，用于获取当前坐标和朝向
    // 如果尚未初始化，则返回 (0, 0, HEADING_NORTH)
    void getStatus(int32_t& x, int32_t& y, Heading& heading) const;

private:
    static Heading normalizeHeading(int32_t h);

    // 避免魔鬼数字：统一管理方向和默认值
    static constexpr int32_t HEADING_MODULO       = 4;
    static constexpr int32_t HEADING_RIGHT_DELTA  = 1;
    static constexpr int32_t HEADING_LEFT_DELTA   = HEADING_MODULO - HEADING_RIGHT_DELTA;
    static constexpr int32_t DEFAULT_COORDINATE   = 0;
    static constexpr Heading DEFAULT_HEADING      = HEADING_NORTH;

    mutable std::mutex m_mutex;
    int32_t m_x;
    int32_t m_y;
    Heading m_heading;
    bool m_initialized;
};

} // namespace executor

#endif // EXECUTOR_ROBOT_EXECUTOR_H

