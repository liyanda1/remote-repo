#ifndef EXECUTOR_ROBOT_EXECUTOR_H
#define EXECUTOR_ROBOT_EXECUTOR_H

namespace executor {

enum Heading {
    HEADING_NORTH = 0,
    HEADING_EAST,
    HEADING_SOUTH,
    HEADING_WEST
};

class Executor {
public:
    Executor();

    // 由 Config 组件调用，用于初始化扫地机位置和朝向
    void init(int x, int y, Heading heading);

    // 由 Controller 组件调用的动作接口：右转/左转 90 度，位置保持不变
    void turnRight();
    void turnLeft();

    // 由 Controller 组件调用，用于获取当前坐标和朝向
    // 如果尚未初始化，则返回 (0, 0, HEADING_NORTH)
    void getStatus(int& x, int& y, Heading& heading) const;

private:
    int x_;
    int y_;
    Heading heading_;
    bool initialized_;
};

} // namespace executor

#endif // EXECUTOR_ROBOT_EXECUTOR_H

