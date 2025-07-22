#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../include/Scheduler.h"
#include "../include/SimpleTask.h"

using ::testing::_;
using ::testing::Exactly;
using ::testing::AtLeast;

/**
 * @brief MockTaskObserver 用于测试调度器是否正确通知
 */
class MockTaskObserver : public TaskObserver {
public:
    MOCK_METHOD(void, onTaskStart, (const std::string&), (override));
    MOCK_METHOD(void, onTaskComplete, (const std::string&), (override));
    MOCK_METHOD(void, onTaskError, (const std::string&, const std::string&), (override));
};

TEST(SchedulerTest, ExecutesTasksInParallel) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver, onTaskStart(_)).Times(Exactly(3));
    EXPECT_CALL(*mockObserver, onTaskComplete(_)).Times(Exactly(2));
    EXPECT_CALL(*mockObserver, onTaskError(_, _)).Times(Exactly(1));

    scheduler.addObserver(mockObserver);
    scheduler.start();

    scheduler.addTask(std::make_shared<SimpleTask>("Task1", 100, false));
    scheduler.addTask(std::make_shared<SimpleTask>("Task2", 200, true));
    scheduler.addTask(std::make_shared<SimpleTask>("Task3", 150, false));

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    scheduler.stop();
}

TEST(SchedulerTest, HandlesEmptyQueueGracefully) {
    Scheduler scheduler;
    scheduler.start();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    scheduler.stop();
}

TEST(SchedulerTest, MultipleObserversReceiveNotifications) {
    Scheduler scheduler;
    auto mockObserver1 = std::make_shared<MockTaskObserver>();
    auto mockObserver2 = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver1, onTaskStart("TaskX")).Times(1);
    EXPECT_CALL(*mockObserver2, onTaskStart("TaskX")).Times(1);

    scheduler.addObserver(mockObserver1);
    scheduler.addObserver(mockObserver2);
    scheduler.start();

    scheduler.addTask(std::make_shared<SimpleTask>("TaskX", 50, false));
    std::this_thread::sleep_for(std::chrono::milliseconds(200));
    scheduler.stop();
}

TEST(SchedulerTest, StressTestWithManyTasks) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver, onTaskStart(_)).Times(AtLeast(50));
    EXPECT_CALL(*mockObserver, onTaskComplete(_)).Times(AtLeast(45));
    EXPECT_CALL(*mockObserver, onTaskError(_, _)).Times(AtLeast(5));

    scheduler.addObserver(mockObserver);
    scheduler.start();

    for (int i = 0; i < 50; ++i) {
        bool shouldFail = (i % 10 == 0);
        scheduler.addTask(std::make_shared<SimpleTask>("StressTask" + std::to_string(i), 10, shouldFail));
    }

    std::this_thread::sleep_for(std::chrono::seconds(2));
    scheduler.stop();
}