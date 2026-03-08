#ifndef EXECUTOR_DIRECTION_H
#define EXECUTOR_DIRECTION_H

#include <stdint.h>

namespace executor {

enum Heading {
    HEADING_NORTH = 0,
    HEADING_EAST,
    HEADING_SOUTH,
    HEADING_WEST
};

inline bool IsValidHeading(Heading heading)
{
    return heading >= HEADING_NORTH && heading <= HEADING_WEST;
}

} // namespace executor

#endif // EXECUTOR_DIRECTION_H

