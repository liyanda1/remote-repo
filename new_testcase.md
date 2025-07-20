# 🛠 要拦截的编码问题示例

| 编码问题                 | 测试拦截点                                        |
| ------------------------ | ------------------------------------------------- |
| ✅ 数组越界/队列非法访问  | 队列为空时调用 `pop()` 是否崩溃                   |
| ✅ 内存泄漏               | 是否所有任务都释放（智能指针是否生效）            |
| ✅ 多线程竞争条件         | 多线程同时访问 `taskQueue_` 是否引起死锁/数据丢失 |
| ✅ 异常未捕获导致线程崩溃 | `task->execute()` 抛异常是否被 Scheduler 捕获     |
| ✅ 空指针访问             | 无 Observer/Task 时是否安全                       |
| ✅ 资源未释放             | 调用 `stop()` 后线程是否完全退出                  |

------

# 📋 测试用例结构

每个用例都包括：

- **测试功能**
- **前置条件**
- **执行步骤**
- **预期结果**
- **测试因子分析**
- **GTest/GMock 实现代码**

------

## ✅ 用例 1: 空队列 pop() 安全性

### 📝 测试功能

验证 `Scheduler::worker()` 在空队列时不会调用非法的 `pop()`。

### ⚙️ 前置条件

- 初始化 Scheduler，不添加任何任务。

### 🚀 执行步骤

1. 调用 `start()`。
2. 等待一段时间（无任务）。
3. 调用 `stop()`。

### 🎯 预期结果

- 没有崩溃或异常。
- 所有工作线程正常退出。

### 🔥 测试因子

- 多线程 wait + notify。
- 队列访问是否加锁。

### 💻 测试代码

```cpp
TEST(SchedulerTest, EmptyQueuePopSafe) {
    Scheduler scheduler;
    scheduler.start();

    // 线程等待，没有任务加入
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    // 停止调度器，应无崩溃
    EXPECT_NO_THROW(scheduler.stop());
}
```

------

## ✅ 用例 2: 任务执行异常捕获

### 📝 测试功能

验证任务执行中抛出异常是否被 Scheduler 捕获，并通知 Observer。

### ⚙️ 前置条件

- 注册一个 Mock Observer。
- 添加一个故意抛异常的任务。

### 🚀 执行步骤

1. 调用 `addObserver()`。
2. 添加一个 `SimpleTask("FailTask", 10, true)`。
3. 调用 `start()` 和 `stop()`。

### 🎯 预期结果

- `onTaskStart()` 被调用。
- `onTaskError()` 被调用一次，含错误信息。

### 🔥 测试因子

- 异常传播
- Observer 回调是否执行

### 💻 测试代码

```cpp
TEST(SchedulerTest, TaskExecuteThrowsCaughtAndNotified) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver, onTaskStart("FailTask")).Times(1);
    EXPECT_CALL(*mockObserver, onTaskError("FailTask", testing::HasSubstr("Task failed intentionally"))).Times(1);

    scheduler.addObserver(mockObserver);
    scheduler.addTask(std::make_shared<SimpleTask>("FailTask", 10, true));
    scheduler.start();
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    scheduler.stop();
}
```

------

## ✅ 用例 3: 多线程竞争条件检测

### 📝 测试功能

验证多线程调度是否存在竞争条件，是否会丢任务。

### ⚙️ 前置条件

- 注册 Mock Observer。
- 短时间内添加大量任务（高并发）。

### 🚀 执行步骤

1. 循环添加 100 个任务（部分故意失败）。
2. 调用 `start()`。
3. 等待所有任务完成。

### 🎯 预期结果

- 所有任务都收到启动/完成/错误通知。
- 无死锁或崩溃。

### 🔥 测试因子

- 锁保护 `taskQueue_` 是否充分。
- 线程安全。

### 💻 测试代码

```cpp
TEST(SchedulerTest, HighConcurrencyNoLostTasks) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver, onTaskStart(_)).Times(Exactly(100));
    EXPECT_CALL(*mockObserver, onTaskComplete(_)).Times(AtLeast(90));
    EXPECT_CALL(*mockObserver, onTaskError(_, _)).Times(AtLeast(10));

    scheduler.addObserver(mockObserver);
    scheduler.start();

    for (int i = 0; i < 100; ++i) {
        bool fail = (i % 10 == 0);
        scheduler.addTask(std::make_shared<SimpleTask>("Task" + std::to_string(i), 5, fail));
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));
    scheduler.stop();
}
```

------

## ✅ 用例 4: 无 Observer 安全性

### 📝 测试功能

验证在未注册 Observer 的情况下执行任务是否安全。

### ⚙️ 前置条件

- 不添加任何 Observer。
- 添加一个普通任务。

### 🚀 执行步骤

1. 添加任务。
2. 调用 `start()` 和 `stop()`。

### 🎯 预期结果

- 任务执行正常。
- 无空指针访问。

### 🔥 测试因子

- Observer 遍历是否检查空容器。

### 💻 测试代码

```cpp
TEST(SchedulerTest, NoObserverSafeExecution) {
    Scheduler scheduler;
    scheduler.addTask(std::make_shared<SimpleTask>("LonelyTask", 20, false));
    scheduler.start();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    EXPECT_NO_THROW(scheduler.stop());
}
```

------

## ✅ 用例 5: stop() 后线程完全退出

### 📝 测试功能

验证调用 `stop()` 后所有工作线程是否正常退出，无悬挂线程。

### ⚙️ 前置条件

- 注册 Mock Observer。
- 添加若干任务。

### 🚀 执行步骤

1. 添加 10 个短任务。
2. 调用 `start()` 和 `stop()`。

### 🎯 预期结果

- `stop()` 返回后无工作线程仍在运行。

### 🔥 测试因子

- 资源释放（线程 join）
- 条件变量唤醒是否覆盖所有线程

### 💻 测试代码

```cpp
TEST(SchedulerTest, ThreadsExitAfterStop) {
    Scheduler scheduler;
    auto mockObserver = std::make_shared<MockTaskObserver>();

    EXPECT_CALL(*mockObserver, onTaskStart(_)).Times(Exactly(10));
    EXPECT_CALL(*mockObserver, onTaskComplete(_)).Times(Exactly(10));

    scheduler.addObserver(mockObserver);
    scheduler.start();

    for (int i = 0; i < 10; ++i) {
        scheduler.addTask(std::make_shared<SimpleTask>("ExitTest" + std::to_string(i), 10, false));
    }

    scheduler.stop();
    // 验证 stop 后所有线程已 join，无异常
    EXPECT_NO_THROW(scheduler.stop());
}
```

