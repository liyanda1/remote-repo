#include "Scheduler.h"
#include <iostream>

Scheduler::Scheduler() : running_(false) {}

Scheduler::~Scheduler() {
    stop();     // 调用stop确保所有线程安全退出
}

void Scheduler::addTask(std::shared_ptr<ITask> task) {
    {
        std::lock_guard<std::mutex> lock(mutex_);   // 加锁保护任务队列
        taskQueue_.push(task);
    }
    cv_.notify_one();   // 通知一个等待中的工作线程
}

void Scheduler::addObserver(std::shared_ptr<TaskObserver> observer) {
    std::lock_guard<std::mutex> lock(mutex_);
    observers_.push_back(observer);
}

void Scheduler::start() {
    running_ = true;
    // 创建4个工作线程（线程池）
    for (int i = 0; i < 4; ++i) {
        threads_.emplace_back(&Scheduler::worker, this);
    }
}
/* 优雅停止机制 */
void Scheduler::stop() {
    {
        std::lock_guard<std::mutex> lock(mutex_);   // 加锁修改运行状态
        running_ = false;
    }
    cv_.notify_all();   // 通知所有等待中的线程
    for (auto& t : threads_) {
        if (t.joinable()) {
            t.join();   // 等待线程结束
        }
    }
    threads_.clear();
}

void Scheduler::worker() {
    while (true) {
        std::shared_ptr<ITask> task;    // 存储待处理任务
        {
            std::unique_lock<std::mutex> lock(mutex_);  // 使用unique_lock配合条件变量
            // 等待条件：有任务或需要停止
            cv_.wait(lock, [this]() { return !taskQueue_.empty() || !running_; });
            if (!running_ && taskQueue_.empty()) {
                return;  // 退出线程
            }
            task = taskQueue_.front();
            taskQueue_.pop();
        }

        try {
            // 通知所有观察者任务开始
            for (auto& obs : observers_) {
                obs->onTaskStart(task->name());
            }
            task->execute();
            // 通知所有观察者任务完成
            for (auto& obs : observers_) {
                obs->onTaskComplete(task->name());
            }
        } catch (const std::exception& ex) {
            // 捕获异常并通知所有观察者
            for (auto& obs : observers_) {
                obs->onTaskError(task->name(), ex.what());
            }
        }
    }
}