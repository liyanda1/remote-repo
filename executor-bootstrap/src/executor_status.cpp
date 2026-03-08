#include "executor_status.h"

namespace executor {

ExecutorStatus::ExecutorStatus(int32_t x, int32_t y, Heading heading)
    : m_x(x)
    , m_y(y)
    , m_heading(heading)
{
}

int32_t ExecutorStatus::GetX() const
{
    return m_x;
}

int32_t ExecutorStatus::GetY() const
{
    return m_y;
}

Heading ExecutorStatus::GetHeading() const
{
    return m_heading;
}

} // namespace executor

