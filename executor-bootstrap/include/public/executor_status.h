#ifndef EXECUTOR_EXECUTOR_STATUS_H
#define EXECUTOR_EXECUTOR_STATUS_H

#include <stdint.h>
#include "direction.h"

namespace executor {

class ExecutorStatus {
public:
    ExecutorStatus(int32_t x = 0, int32_t y = 0, Heading heading = HEADING_NORTH);

    int32_t GetX() const;
    int32_t GetY() const;
    Heading GetHeading() const;

private:
    int32_t m_x;
    int32_t m_y;
    Heading m_heading;
};

} // namespace executor

#endif // EXECUTOR_EXECUTOR_STATUS_H

