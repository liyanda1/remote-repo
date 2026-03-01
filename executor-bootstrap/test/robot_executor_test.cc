#include <cctest/cctest.h>
#include "executor/robot_executor.h"
#include <thread>
#include <vector>
#include <stdint.h>

using namespace executor;

namespace {

// 避免魔鬼数字：测试中控制并发的关键参数
const int32_t THREAD_COUNT      = 4;
const int32_t LOOP_PER_THREAD   = 100;

} // namespace

FIXTURE(RobotExecutorTest) {
    TEST("should return default status when not initialized") {
        Executor ex;
        int32_t x = -1;
        int32_t y = -1;
        Heading h = HEADING_SOUTH;

        ex.getStatus(x, y, h);

        ASSERT_EQ(0, x);
        ASSERT_EQ(0, y);
        ASSERT_EQ(HEADING_NORTH, h);
    }

    TEST("should initialize position and heading") {
        Executor ex;
        ex.init(3, 5, HEADING_EAST);

        int32_t x = 0;
        int32_t y = 0;
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
        int32_t x = 0;
        int32_t y = 0;
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
        int32_t x = 0;
        int32_t y = 0;
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

    TEST("turnRight/turnLeft when not initialized are no-op") {
        Executor ex;
        ex.turnRight();
        ex.turnLeft();
        int32_t x = -1, y = -1;
        Heading h = HEADING_SOUTH;
        ex.getStatus(x, y, h);
        ASSERT_EQ(0, x);
        ASSERT_EQ(0, y);
        ASSERT_EQ(HEADING_NORTH, h);
    }

    TEST("init normalizes invalid heading") {
        Executor ex;
        // 超出枚举范围时规范到 [0,3]
        ex.init(1, 1, static_cast<Heading>(4));
        int32_t x = 0, y = 0;
        Heading h = HEADING_NORTH;
        ex.getStatus(x, y, h);
        ASSERT_EQ(1, x);
        ASSERT_EQ(1, y);
        ASSERT_EQ(HEADING_NORTH, h);

        ex.init(2, 2, static_cast<Heading>(7));  // 7 % 4 == 3 -> WEST
        ex.getStatus(x, y, h);
        ASSERT_EQ(2, x);
        ASSERT_EQ(2, y);
        ASSERT_EQ(HEADING_WEST, h);
    }

    TEST("concurrent getStatus and turn do not crash") {
        Executor ex;
        ex.init(0, 0, HEADING_NORTH);
        std::vector<std::thread> threads;
        for (int32_t i = 0; i < THREAD_COUNT; ++i) {
            threads.emplace_back([&ex]() {
                for (int32_t j = 0; j < LOOP_PER_THREAD; ++j) {
                    int32_t x, y;
                    Heading h;
                    ex.getStatus(x, y, h);
                    ex.turnRight();
                }
            });
        }
        for (auto& t : threads) {
            t.join();
        }
        int32_t x, y;
        Heading h;
        ex.getStatus(x, y, h);
        ASSERT_EQ(0, x);
        ASSERT_EQ(0, y);
        // 4 线程各转 100 次，共 400 次，400 % 4 == 0，朝向应回到 NORTH
        ASSERT_EQ(HEADING_NORTH, h);
    }
};

