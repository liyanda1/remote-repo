#include <cctest/cctest.h>
#include "executor/robot_executor.h"

using namespace executor;

FIXTURE(RobotExecutorTest) {
    TEST("should return default status when not initialized") {
        Executor ex;
        int x = -1;
        int y = -1;
        Heading h = HEADING_SOUTH;

        ex.getStatus(x, y, h);

        ASSERT_EQ(0, x);
        ASSERT_EQ(0, y);
        ASSERT_EQ(HEADING_NORTH, h);
    }

    TEST("should initialize position and heading") {
        Executor ex;
        ex.init(3, 5, HEADING_EAST);

        int x = 0;
        int y = 0;
        Heading h = HEADING_NORTH;

        ex.getStatus(x, y, h);

        ASSERT_EQ(3, x);
        ASSERT_EQ(5, y);
        ASSERT_EQ(HEADING_EAST, h);
    }

    TEST("should turn right 90 degrees") {
        Executor ex;
        ex.init(1, 2, HEADING_NORTH);

        ex.turnRight(); // N -> E
        int x = 0;
        int y = 0;
        Heading h = HEADING_NORTH;
        ex.getStatus(x, y, h);
        ASSERT_EQ(1, x);
        ASSERT_EQ(2, y);
        ASSERT_EQ(HEADING_EAST, h);

        ex.turnRight(); // E -> S
        ex.getStatus(x, y, h);
        ASSERT_EQ(1, x);
        ASSERT_EQ(2, y);
        ASSERT_EQ(HEADING_SOUTH, h);

        ex.turnRight(); // S -> W
        ex.getStatus(x, y, h);
        ASSERT_EQ(1, x);
        ASSERT_EQ(2, y);
        ASSERT_EQ(HEADING_WEST, h);

        ex.turnRight(); // W -> N
        ex.getStatus(x, y, h);
        ASSERT_EQ(1, x);
        ASSERT_EQ(2, y);
        ASSERT_EQ(HEADING_NORTH, h);
    }

    TEST("should turn left 90 degrees") {
        Executor ex;
        ex.init(4, 6, HEADING_NORTH);

        ex.turnLeft(); // N -> W
        int x = 0;
        int y = 0;
        Heading h = HEADING_NORTH;
        ex.getStatus(x, y, h);
        ASSERT_EQ(4, x);
        ASSERT_EQ(6, y);
        ASSERT_EQ(HEADING_WEST, h);

        ex.turnLeft(); // W -> S
        ex.getStatus(x, y, h);
        ASSERT_EQ(4, x);
        ASSERT_EQ(6, y);
        ASSERT_EQ(HEADING_SOUTH, h);

        ex.turnLeft(); // S -> E
        ex.getStatus(x, y, h);
        ASSERT_EQ(4, x);
        ASSERT_EQ(6, y);
        ASSERT_EQ(HEADING_EAST, h);

        ex.turnLeft(); // E -> N
        ex.getStatus(x, y, h);
        ASSERT_EQ(4, x);
        ASSERT_EQ(6, y);
        ASSERT_EQ(HEADING_NORTH, h);
    }
};

