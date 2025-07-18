#include "Scheduler.h"
#include <iostream>

Scheduler::Scheduler() : running_(false) {}

Scheduler::~Scheduler() {
    stop();
}

void Scheduler::addTask(std::shared_ptr<ITask> task) {
    {
        std::lock_guard<std::mutex> lock(mutex_);
        taskQueue_.push(task);
    }
    cv_.notify_one();
}

void Scheduler::addObserver(std::shared_ptr<TaskObserver> observer) {
    std::lock_guard<std::mutex> lock(mutex_);
    observers_.push_back(observer);
}

void Scheduler::start() {
    running_ = true;
    for (int i = 0; i < 4; ++i) { // Start 4 worker threads
        threads_.emplace_back(&Scheduler::worker, this);
    }
}

void Scheduler::stop() {
    {
        std::lock_guard<std::mutex> lock(mutex_);
        running_ = false;
    }
    cv_.notify_all();
    for (auto& t : threads_) {
        if (t.joinable()) {
            t.join();
        }
    }
    threads_.clear();
}

void Scheduler::worker() {
    while (true) {
        std::shared_ptr<ITask> task;
        {
            std::unique_lock<std::mutex> lock(mutex_);
            cv_.wait(lock, [this]() { return !taskQueue_.empty() || !running_; });
            if (!running_ && taskQueue_.empty())
                return;
            task = taskQueue_.front();
            taskQueue_.pop();
        }

        try {
            for (auto& obs : observers_) obs->onTaskStart(task->name());
            task->execute();
            for (auto& obs : observers_) obs->onTaskComplete(task->name());
        } catch (const std::exception& ex) {
            for (auto& obs : observers_) obs->onTaskError(task->name(), ex.what());
        }
    }
}