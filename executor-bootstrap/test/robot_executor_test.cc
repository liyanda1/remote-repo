#include <cctest/cctest.h>
#include "robot_executor.h"
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
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(0, status.GetX());
        ASSERT_EQ(0, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());
    }

    TEST("should initialize position and heading") {
        Executor ex;
        ex.Init(3, 5, HEADING_EAST);

        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(3, status.GetX());
        ASSERT_EQ(5, status.GetY());
        ASSERT_EQ(HEADING_EAST, status.GetHeading());
    }

    TEST("should move forward and backward along heading") {
        Executor ex;
        ex.Init(0, 0, HEADING_NORTH);

        ex.Forward();  // (0,0,N) -> (0,1,N)
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(0, status.GetX());
        ASSERT_EQ(1, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());

        ex.Backward(); // (0,1,N) -> (0,0,N)
        status = ex.GetStatus();
        ASSERT_EQ(0, status.GetX());
        ASSERT_EQ(0, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());

        ex.Init(2, 2, HEADING_EAST);
        ex.Forward();  // (2,2,E) -> (3,2,E)
        status = ex.GetStatus();
        ASSERT_EQ(3, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_EAST, status.GetHeading());

        ex.Backward(); // (3,2,E) -> (2,2,E)
        status = ex.GetStatus();
        ASSERT_EQ(2, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_EAST, status.GetHeading());
    }

    TEST("should turn right 90 degrees") {
        Executor ex;
        ex.Init(1, 2, HEADING_NORTH);

        ex.TurnRight(); // N -> E
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(1, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_EAST, status.GetHeading());

        ex.TurnRight(); // E -> S
        status = ex.GetStatus();
        ASSERT_EQ(1, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_SOUTH, status.GetHeading());

        ex.TurnRight(); // S -> W
        status = ex.GetStatus();
        ASSERT_EQ(1, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_WEST, status.GetHeading());

        ex.TurnRight(); // W -> N
        status = ex.GetStatus();
        ASSERT_EQ(1, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());
    }

    TEST("should turn left 90 degrees") {
        Executor ex;
        ex.Init(4, 6, HEADING_NORTH);

        ex.TurnLeft(); // N -> W
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(4, status.GetX());
        ASSERT_EQ(6, status.GetY());
        ASSERT_EQ(HEADING_WEST, status.GetHeading());

        ex.TurnLeft(); // W -> S
        status = ex.GetStatus();
        ASSERT_EQ(4, status.GetX());
        ASSERT_EQ(6, status.GetY());
        ASSERT_EQ(HEADING_SOUTH, status.GetHeading());

        ex.TurnLeft(); // S -> E
        status = ex.GetStatus();
        ASSERT_EQ(4, status.GetX());
        ASSERT_EQ(6, status.GetY());
        ASSERT_EQ(HEADING_EAST, status.GetHeading());

        ex.TurnLeft(); // E -> N
        status = ex.GetStatus();
        ASSERT_EQ(4, status.GetX());
        ASSERT_EQ(6, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());
    }

    TEST("turnRight/turnLeft when default constructed will rotate from NORTH") {
        Executor ex;
        ex.TurnRight();
        ex.TurnLeft();
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(0, status.GetX());
        ASSERT_EQ(0, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());
    }

    TEST("init normalizes invalid heading") {
        Executor ex;
        // 超出枚举范围时规范到 [0,3]
        ex.Init(1, 1, static_cast<Heading>(4));
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(1, status.GetX());
        ASSERT_EQ(1, status.GetY());
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());

        ex.Init(2, 2, static_cast<Heading>(7));  // 7 % 4 == 3 -> WEST
        status = ex.GetStatus();
        ASSERT_EQ(2, status.GetX());
        ASSERT_EQ(2, status.GetY());
        ASSERT_EQ(HEADING_WEST, status.GetHeading());
    }

    TEST("concurrent getStatus and turn do not crash") {
        Executor ex;
        ex.Init(0, 0, HEADING_NORTH);
        std::vector<std::thread> threads;
        for (int32_t i = 0; i < THREAD_COUNT; ++i) {
            threads.emplace_back([&ex]() {
                for (int32_t j = 0; j < LOOP_PER_THREAD; ++j) {
                    ExecutorStatus status = ex.GetStatus();
                    ex.TurnRight();
                }
            });
        }
        for (auto& t : threads) {
            t.join();
        }
        ExecutorStatus status = ex.GetStatus();
        ASSERT_EQ(0, status.GetX());
        ASSERT_EQ(0, status.GetY());
        // 4 线程各转 100 次，共 400 次，400 % 4 == 0，朝向应回到 NORTH
        ASSERT_EQ(HEADING_NORTH, status.GetHeading());
    }
};

