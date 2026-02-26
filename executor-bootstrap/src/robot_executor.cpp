#include "executor/robot_executor.h"

namespace executor {

Executor::Executor()
    : x_(0)
    , y_(0)
    , heading_(HEADING_NORTH)
    , initialized_(false) {
}

void Executor::init(int x, int y, Heading heading) {
    x_ = x;
    y_ = y;
    heading_ = heading;
    initialized_ = true;
}

void Executor::turnRight() {
    // 右转 90 度：顺时针方向变化
    heading_ = static_cast<Heading>((static_cast<int>(heading_) + 1) % 4);
}

void Executor::turnLeft() {
    // 左转 90 度：逆时针方向变化
    heading_ = static_cast<Heading>((static_cast<int>(heading_) + 3) % 4);
}

void Executor::getStatus(int& x, int& y, Heading& heading) const {
    if (!initialized_) {
        x = 0;
        y = 0;
        heading = HEADING_NORTH;
        return;
    }

    x = x_;
    y = y_;
    heading = heading_;
}

} // namespace executor

