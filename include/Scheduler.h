#pragma once
#include "ITask.h"
#include "TaskObserver.h"
#include <memory>
#include <queue>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

class Scheduler {
public:
    Scheduler();
    ~Scheduler();

    void addTask(std::shared_ptr<ITask> task);
    void addObserver(std::shared_ptr<TaskObserver> observer);
    void start();
    void stop();

private:
    void worker();

    std::queue<std::shared_ptr<ITask>> taskQueue_;
    std::vector<std::shared_ptr<TaskObserver>> observers_;
    std::vector<std::thread> threads_;
    std::mutex mutex_;
    std::condition_variable cv_;
    bool running_;
};