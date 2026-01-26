# ThreadSanitizer（TSan）使用与原理说明

本文档用于系统性说明 C/C++ Sanitizer 体系中各类 Sanitizer 的差异，重点介绍 ThreadSanitizer（TSan）的工作原理、工具限制，以及在 **GTest 测试场景** 与 **真实业务场景** 下使用 TSan 的差异和实践方法。

---

## 1. 各类 Sanitizer 的差异说明

### 1.1 Sanitizer 的总体设计目标

Sanitizer 是一类基于 **编译期插桩（Instrumentation）+ 运行期检测** 的动态分析工具，其目标是在程序运行过程中捕获：

- 不一定立即导致崩溃
- 但违反语言规范、并发模型或内存使用规则
- 并可能在生产环境中引发严重问题

不同 Sanitizer 在 **检测对象、插桩粒度、运行时模型** 上存在本质差异。

---

### 1.2 AddressSanitizer（ASan）

**检测目标**：

- 堆 / 栈 / 全局变量越界访问
- Use-After-Free（UAF）
- Double Free
- 部分非法内存访问

**核心机制**：

- Shadow Memory 机制
- 通过地址映射（如 1:8）标记真实内存的可访问性
- 在每一次内存访问前插入校验逻辑

**特点**：

- 内存错误检测精度高
- 性能开销中等（通常 1.5x ~ 2x）
- 不关注并发语义，仅检测内存合法性

---

### 1.3 LeakSanitizer（LSan）

**检测目标**：

- 程序退出时仍然可达的堆内存（内存泄漏）

**核心机制**：

- 在进程退出阶段扫描：
  - 栈
  - 全局变量
  - 寄存器
- 判断 heap 对象是否可达

**特点**：

- 通常作为 ASan 的子能力存在
- 不检测并发或内存越界问题

---

### 1.4 UndefinedBehaviorSanitizer（UBSan）

**检测目标**：

- C/C++ 标准定义的未定义行为（UB），包括：
  - 整型溢出
  - 空指针解引用
  - 非法类型转换
  - 未对齐内存访问

**核心机制**：

- 在可能触发 UB 的表达式处插入运行时检查
- 不依赖 Shadow Memory

**特点**：

- 性能开销低
- 偏向语言语义和规范正确性

---

### 1.5 ThreadSanitizer（TSan）

**检测目标**：

- 数据竞争（Data Race）
- 错误的同步关系
- 违反 happens-before 规则的并发访问

**TSan 的判断视角**：

> 当多个线程并发访问同一内存地址，
> 且至少一个为写操作，
> 并且访问之间不存在明确的同步关系，
> 则认为存在数据竞争。

---

### 1.6 各 Sanitizer 的本质差异总结

| 维度 | ASan | UBSan | TSan |
|----|----|----|----|
| 检测对象 | 内存生命周期 | 语言未定义行为 | 并发内存访问 |
| 是否关注线程 | 否 | 否 | 是（核心） |
| 插桩粒度 | 内存访问 | 表达式级 | 内存访问 + 同步事件 |
| 运行时模型 | Shadow Memory | 直接检查 | 并发事件与时序建模 |

---

## 2. ThreadSanitizer（TSan）的工作原理

### 2.1 设计目标

TSan 的核心目标并非检测死锁或锁使用错误，而是：

> 判断任意两个内存访问之间是否存在合法的 happens-before 关系。

---

### 2.2 编译期插桩内容

TSan 会对以下操作进行插桩：

1. 所有内存读 / 写操作
2. 线程创建与销毁
3. 锁操作（mutex lock / unlock）
4. 原子操作（std::atomic）
5. 条件变量、futex 等同步原语

---

### 2.3 运行时核心机制：Happens-Before 模型

TSan 基于 **向量时钟（Vector Clock）** 建立并发时序模型：

- 每个线程维护逻辑时间戳
- 每个内存地址维护最近访问的时间信息
- 同步操作会合并时间戳，建立 happens-before 关系

**简化判断逻辑**：

- 若两个线程访问同一地址
- 且至少一个为写
- 且访问时间之间不存在 happens-before

则判定为数据竞争。

---

### 2.4 TSan 的严格性说明

即使某些并发访问在实际运行中概率极低，只要缺乏同步语义，TSan 仍会报告问题。这一行为符合 C/C++ 内存模型定义，并非误报。

---

## 3. 为什么 TSan 不能与其他 Sanitizer 同时使用

### 3.1 结论

TSan **不能与 ASan / LSan / MSan 等 Sanitizer 同时启用**。

---

### 3.2 根本原因：插桩与运行时模型冲突

#### 3.2.1 ASan 的假设

- 内存访问路径尽量接近原始 load / store
- Shadow Memory 与真实地址保持固定映射关系

#### 3.2.2 TSan 的假设

- 每一次内存访问都是并发事件
- 访问必须被完整记录（线程、时间、地址）

两者均需要重写内存访问路径，且都假设自身是唯一拦截者。

---

### 3.3 技术层面的不可兼容点

- Shadow Memory 结构冲突
- 插桩顺序与访问语义被破坏
- 并发事件模型无法正确建立

---

### 3.4 官方实践建议

- ASan / UBSan：日常质量保障
- TSan：并发专项验证
- 分开构建、分开运行

---

## 4. GTest 中使用 TSan 与业务中跑 TSan 的差异

### 4.1 结论

在 GTest 中运行 TSan，检测的是 **测试执行模型下的并发问题**，并不完全等价于真实业务进程。

---

### 4.2 生命周期模型差异

**业务进程**：

- 单一 main
- 生命周期完整
- 线程池和单例模型稳定

**GTest**：

- 单进程，多 TestCase 串行执行
- 全局/静态对象跨 TestCase 共享
- 线程可能跨 TestCase 存活

---

### 4.3 隐式共享状态放大竞态

GTest 中的以下结构容易触发 TSan：

- 静态局部变量
- 单例对象
- Lazy initialization 逻辑

这些问题在业务场景中可能不会暴露。

---

### 4.4 测试代码引入的非真实并发

测试中常见的线程控制（sleep、手动并发构造）会人为放大竞态，TSan 对测试代码与业务代码一视同仁。

---

## 5. 在 GTest 中运行 TSan 的方法

### 5.1 编译与链接配置

**编译选项**：

```bash
-fsanitize=thread -g -O1
```

**链接选项**：

```bash
-fsanitize=thread
```

---

### 5.2 CMake 示例

```cmake
add_executable(test_tsan test_xxx.cpp)

target_compile_options(test_tsan PRIVATE -fsanitize=thread -g -O1)
target_link_options(test_tsan PRIVATE -fsanitize=thread)
```

建议为 TSan 单独构建测试目标。

---

### 5.3 运行时参数配置

```bash
export TSAN_OPTIONS="halt_on_error=1 history_size=7 report_signal_unsafe=0"
```

---

### 5.4 使用建议

**推荐做法**：

- 每个 TestCase 内创建的线程必须 join
- 明确测试并发行为或功能逻辑
- 对全局状态显式加锁

**不推荐做法**：

- TestCase 之间共享后台线程
- 依赖进程退出阶段析构
- 在 SetUpTestSuite 中创建长期线程

---

## 6. 总结

TSan 是并发问题定位的核心工具，但其检测模型严格、性能开销大、使用场景特殊。合理区分 Sanitizer 职责、正确理解 GTest 与业务执行模型差异，是高效使用 TSan 的前提。

