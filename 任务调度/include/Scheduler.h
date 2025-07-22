#pragma once
#include "ITask.h"
#include "TaskObserver.h"
#include <memory>
#include <queue>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

/**
 * @brief Scheduler 多线程任务调度器
 * 支持任务并发执行和任务观察者通知
 */
class Scheduler {
public:
    Scheduler();
    ~Scheduler();

    /**
     * @brief 添加任务到调度队列
     */
    void addTask(std::shared_ptr<ITask> task);

    /**
     * @brief 注册任务观察者
     */
    void addObserver(std::shared_ptr<TaskObserver> observer);

    /**
     * @brief 启动调度器工作线程
     */
    void start();

    /**
     * @brief 停止调度器并等待线程退出
     */
    void stop();

private:
    void worker();  // 工作线程执行函数

    std::queue<std::shared_ptr<ITask>> taskQueue_;  // 任务队列（FIFO）
    std::vector<std::shared_ptr<TaskObserver>> observers_;  // 观察者列表
    std::vector<std::thread> threads_;     // 工作线程池
    std::mutex mutex_;                     // 保护共享资源的互斥锁
    std::condition_variable cv_;           // 线程间通信的条件变量
    bool running_;                         // 调度器运行状态标志
};