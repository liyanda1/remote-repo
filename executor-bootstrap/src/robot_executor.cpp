#include "robot_executor.h"
#include <map>

namespace executor {

namespace {

struct DirectionDelta {
    int32_t m_dx;
    int32_t m_dy;
};

// 所有内部使用的实现常量集中在匿名命名空间，避免泄露到对外接口
constexpr int32_t kHeadingModulo      = 4;
constexpr int32_t kMoveStep           = 1;
constexpr int32_t kRightDelta         = 1;
constexpr int32_t kLeftDelta          = kHeadingModulo - kRightDelta;
constexpr int32_t kDefaultCoordinate  = 0;
constexpr Heading kDefaultHeading     = HEADING_NORTH;

// NORTH: y + 1, EAST: x + 1, SOUTH: y - 1, WEST: x - 1
const std::map<Heading, DirectionDelta> kHeadingDeltaMap = {
    {HEADING_NORTH, {0, 1}},
    {HEADING_EAST,  {1, 0}},
    {HEADING_SOUTH, {0, -1}},
    {HEADING_WEST,  {-1, 0}},
};

} // unnamed namespace

Executor::Executor()
    : m_x(kDefaultCoordinate)
    , m_y(kDefaultCoordinate)
    , m_heading(kDefaultHeading)
{
}

Heading Executor::NormalizeHeading(int32_t h)
{
    // 将任意值规范到合法范围 [0, kHeadingModulo)
    int32_t n = h % kHeadingModulo;
    if (n < 0) {
        n += kHeadingModulo;
    }
    return static_cast<Heading>(n);
}

void Executor::Init(int32_t x, int32_t y, Heading heading)
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_x = x;
    m_y = y;
    m_heading = NormalizeHeading(static_cast<int32_t>(heading));
}

void Executor::TurnRight()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_heading = static_cast<Heading>(
        (static_cast<int32_t>(m_heading) + kRightDelta) % kHeadingModulo);
}

void Executor::TurnLeft()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_heading = static_cast<Heading>(
        (static_cast<int32_t>(m_heading) + kLeftDelta) % kHeadingModulo);
}

void Executor::Forward()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    MoveAlongHeading(kMoveStep);
}

void Executor::Backward()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    MoveAlongHeading(-kMoveStep);
}

void Executor::GetStatus(int32_t& x, int32_t& y, Heading& heading) const
{
    std::lock_guard<std::mutex> lock(m_mutex);
    x = m_x;
    y = m_y;
    heading = m_heading;
}

ExecutorStatus Executor::GetStatus() const
{
    int32_t x = kDefaultCoordinate;
    int32_t y = kDefaultCoordinate;
    Heading heading = kDefaultHeading;
    GetStatus(x, y, heading);
    return ExecutorStatus(x, y, heading);
}

void Executor::MoveAlongHeading(int32_t step)
{
    if (!IsValidHeading(m_heading)) {
        // 防御性编程：遇到非法朝向时，不移动位置
        return;
    }

    const auto it = kHeadingDeltaMap.find(m_heading);
    if (it == kHeadingDeltaMap.end()) {
        // 安全兜底：找不到映射则不移动
        return;
    }

    const DirectionDelta& delta = it->second;
    m_x += delta.m_dx * step;
    m_y += delta.m_dy * step;
}

} // namespace executor

