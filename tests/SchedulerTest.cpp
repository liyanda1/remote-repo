#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "../include/Scheduler.h"
#include "../include/SimpleTask.h"

using ::testing::_;
using ::testing::Exactly;
using ::testing::AtLeast;
using ::testing::AnyNumber;

class MockTaskObserver : public TaskObserver {
public:
    MOCK_METHOD(void, onTaskStart, (const std::string&), (override));
    MOCK_METHOD(void, onTaskComplete, (const std::string&), (override));
    MOCK_METHOD(void, onTaskError, (const std::string&, const std::string&), (override));
};

TEST(SchedulerTest, ExecutesTasksInParallel) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    // Expect notifications for 3 tasks
    EXPECT_CALL(*mockObserver, onTaskStart(_)).Times(Exactly(3));
    EXPECT_CALL(*mockObserver, onTaskComplete(_)).Times(Exactly(2));
    EXPECT_CALL(*mockObserver, onTaskError(_, _)).Times(Exactly(1));

    scheduler.addObserver(mockObserver);
    scheduler.start();

    // Add tasks (two succeed, one fails)
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