# {{SR_NUMBER}}-{{FEATURE_NAME}} - 测试用例设计文档

## 文档信息

| 项目 | 内容 |
|------|------|
| SR单号 | {{SR_NUMBER}} |
| 需求名称 | {{FEATURE_NAME}} |
| 版本 | {{VERSION}} |
| 作者 | {{AUTHOR}} |
| 日期 | {{DATE}} |

---

## 1. 测试范围

### 1.1 测试目标
<!-- 描述本次测试的目标和范围 -->

### 1.2 测试对象
| 模块/类 | 功能描述 | 测试重点 |
|---------|----------|----------|
| | | |

### 1.3 测试类型
- [ ] 单元测试（UT）
- [ ] 集成测试（IT）
- [ ] 系统测试（ST）
- [ ] 性能测试
- [ ] 可靠性测试

---

## 2. 测试环境

### 2.1 硬件环境
| 项目 | 配置 |
|------|------|
| 目标平台 | x86_64 / ARM / 车载ECU |
| 内存 | |
| 存储 | |

### 2.2 软件环境
| 项目 | 版本 |
|------|------|
| 操作系统 | Linux/QNX/其他 |
| 编译器 | GCC/Clang |
| 测试框架 | Google Test |
| 覆盖率工具 | gcov/lcov |

### 2.3 依赖组件
| 组件 | 版本 | 说明 |
|------|------|------|
| | | |

---

## 3. 测试用例设计

### 3.1 正常场景测试

#### TC001 - 正常升级流程
| 项目 | 内容 |
|------|------|
| 用例ID | TC001 |
| 用例名称 | 正常升级流程 |
| 前置条件 | 系统处于空闲状态，升级包已准备就绪 |
| 测试步骤 | 1. 调用 StartUpgrade() 发起升级<br>2. 等待升级完成<br>3. 验证版本号已更新 |
| 预期结果 | 1. 返回 OK<br>2. 状态从 Idle → Downloading → Verifying → Installing → Activated<br>3. 进度回调正常触发<br>4. 最终状态为 Completed |
| 优先级 | 高 |
| 自动化 | 是 |

#### TC002 - 断点续传
| 项目 | 内容 |
|------|------|
| 用例ID | TC002 |
| 用例名称 | 断点续传功能 |
| 前置条件 | 下载过程中已下载50% |
| 测试步骤 | 1. 开始下载<br>2. 模拟网络中断<br>3. 恢复网络<br>4. 重新发起升级 |
| 预期结果 | 从50%处继续下载，而非从头开始 |
| 优先级 | 高 |
| 自动化 | 是 |

#### TC003 - 取消升级
| 项目 | 内容 |
|------|------|
| 用例ID | TC003 |
| 用例名称 | 取消升级操作 |
| 前置条件 | 升级正在进行中 |
| 测试步骤 | 1. 发起升级<br>2. 在下载/安装过程中调用 CancelUpgrade() |
| 预期结果 | 1. 升级安全终止<br>2. 状态回到 Idle<br>3. 资源正确释放 |
| 优先级 | 高 |
| 自动化 | 是 |

### 3.2 异常场景测试

#### TC101 - 下载超时
| 项目 | 内容 |
|------|------|
| 用例ID | TC101 |
| 用例名称 | 下载超时处理 |
| 前置条件 | 网络延迟极高或断开 |
| 测试步骤 | 1. 发起升级<br>2. 模拟网络超时 |
| 预期结果 | 1. 重试3次<br>2. 最终返回 ERROR_TIMEOUT<br>3. 状态回到 Idle |
| 优先级 | 高 |
| 自动化 | 是 |

#### TC102 - 升级包校验失败
| 项目 | 内容 |
|------|------|
| 用例ID | TC102 |
| 用例名称 | 升级包校验失败 |
| 前置条件 | 升级包被篡改或损坏 |
| 测试步骤 | 1. 准备损坏的升级包<br>2. 发起升级 |
| 预期结果 | 1. 校验阶段失败<br>2. 返回 ERROR_VERIFY_FAILED<br>3. 不进入安装阶段 |
| 优先级 | 高 |
| 自动化 | 是 |

#### TC103 - 安装失败触发回滚
| 项目 | 内容 |
|------|------|
| 用例ID | TC103 |
| 用例名称 | 安装失败触发回滚 |
| 前置条件 | ECU在安装过程中返回错误 |
| 测试步骤 | 1. 正常下载和校验<br>2. 模拟安装失败 |
| 预期结果 | 1. 自动触发回滚<br>2. 恢复到旧版本<br>3. 返回 ERROR_INSTALL_FAILED |
| 优先级 | 高 |
| 自动化 | 是 |

#### TC104 - 存储空间不足
| 项目 | 内容 |
|------|------|
| 用例ID | TC104 |
| 用例名称 | 存储空间不足检查 |
| 前置条件 | 存储空间小于升级包大小 |
| 测试步骤 | 1. 填充存储空间<br>2. 发起升级 |
| 预期结果 | 1. 前置检查失败<br>2. 返回 ERROR_NO_SPACE<br>3. 给出清理建议 |
| 优先级 | 中 |
| 自动化 | 是 |

#### TC105 - 并发升级请求
| 项目 | 内容 |
|------|------|
| 用例ID | TC105 |
| 用例名称 | 并发升级请求处理 |
| 前置条件 | 升级正在进行中 |
| 测试步骤 | 1. 发起第一个升级<br>2. 在升级过程中发起第二个升级请求 |
| 预期结果 | 1. 第二个请求返回 ERROR_BUSY<br>2. 第一个升级不受影响 |
| 优先级 | 中 |
| 自动化 | 是 |

### 3.3 边界场景测试

#### TC201 - 最小升级包
| 项目 | 内容 |
|------|------|
| 用例ID | TC201 |
| 用例名称 | 最小升级包处理 |
| 前置条件 | 升级包大小为最小允许值 |
| 测试步骤 | 1. 准备最小升级包<br>2. 执行完整升级流程 |
| 预期结果 | 升级成功，无异常 |
| 优先级 | 中 |
| 自动化 | 是 |

#### TC202 - 最大升级包
| 项目 | 内容 |
|------|------|
| 用例ID | TC202 |
| 用例名称 | 最大升级包处理 |
| 前置条件 | 升级包大小接近存储上限 |
| 测试步骤 | 1. 准备大升级包<br>2. 执行完整升级流程 |
| 预期结果 | 1. 进度更新准确<br>2. 升级成功 |
| 优先级 | 中 |
| 自动化 | 是 |

#### TC203 - 极低电量升级
| 项目 | 内容 |
|------|------|
| 用例ID | TC203 |
| 用例名称 | 低电量禁止升级 |
| 前置条件 | 电池电量低于阈值（如20%） |
| 测试步骤 | 1. 模拟低电量状态<br>2. 发起升级 |
| 预期结果 | 1. 前置检查失败<br>2. 返回 ERROR_LOW_BATTERY<br>3. 提示充电 |
| 优先级 | 高 |
| 自动化 | 是 |

### 3.4 状态转换测试

#### TC301 - 无效状态转换
| 项目 | 内容 |
|------|------|
| 用例ID | TC301 |
| 用例名称 | 无效状态转换处理 |
| 前置条件 | 系统处于 Installing 状态 |
| 测试步骤 | 1. 尝试在 Installing 状态下发起新升级 |
| 预期结果 | 返回 ERROR_INVALID_STATE |
| 优先级 | 中 |
| 自动化 | 是 |

---

## 4. 测试代码框架

### 4.1 Google Test 示例

```cpp
#include <gtest/gtest.h>
#include "upgrade_manager.hpp"

using namespace vehicle::middleware;

class UpgradeManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        manager_ = std::make_unique<UpgradeManager>();
        manager_->Initialize();
    }
    
    void TearDown() override {
        manager_->Deinitialize();
    }
    
    std::unique_ptr<UpgradeManager> manager_;
};

// 正常场景测试
TEST_F(UpgradeManagerTest, NormalUpgradeFlow) {
    // Arrange
    UpgradeRequest request;
    request.ecu_id = "ECU001";
    request.software_version = "2.0.0";
    request.package_path = "/data/upgrade_v2.0.0.pkg";
    
    bool callback_triggered = false;
    auto callback = [&callback_triggered](const UpgradeStatus& status) {
        callback_triggered = true;
        EXPECT_GE(status.progress_percent, 0u);
        EXPECT_LE(status.progress_percent, 100u);
    };
    
    // Act
    auto result = manager_->StartUpgrade(request, callback);
    
    // Assert
    EXPECT_EQ(result, UpgradeResult::kOk);
    
    // 等待升级完成
    WaitForUpgradeComplete();
    
    EXPECT_TRUE(callback_triggered);
    EXPECT_EQ(manager_->GetCurrentState(), UpgradeState::kCompleted);
}

// 异常场景测试 - 并发请求
TEST_F(UpgradeManagerTest, ConcurrentUpgradeRequest) {
    // Arrange - 先发起一个升级
    UpgradeRequest request1;
    request1.ecu_id = "ECU001";
    auto result1 = manager_->StartUpgrade(request1, nullptr);
    ASSERT_EQ(result1, UpgradeResult::kOk);
    
    // Act - 尝试并发发起第二个升级
    UpgradeRequest request2;
    request2.ecu_id = "ECU002";
    auto result2 = manager_->StartUpgrade(request2, nullptr);
    
    // Assert
    EXPECT_EQ(result2, UpgradeResult::kBusy);
}

// 边界测试 - 无效参数
TEST_F(UpgradeManagerTest, InvalidParameters) {
    // Arrange
    UpgradeRequest request;
    // 不设置必填字段
    
    // Act
    auto result = manager_->StartUpgrade(request, nullptr);
    
    // Assert
    EXPECT_EQ(result, UpgradeResult::kInvalidParam);
}

// 负面测试 - 取消升级
TEST_F(UpgradeManagerTest, CancelUpgrade) {
    // Arrange
    UpgradeRequest request;
    request.ecu_id = "ECU001";
    manager_->StartUpgrade(request, nullptr);
    
    // Act
    auto result = manager_->CancelUpgrade();
    
    // Assert
    EXPECT_EQ(result, UpgradeResult::kOk);
    EXPECT_EQ(manager_->GetCurrentState(), UpgradeState::kIdle);
}
```

### 4.2 Mock 对象示例

```cpp
#include <gmock/gmock.h>

// Mock 诊断服务
class MockDiagnosticService : public IDiagnosticService {
public:
    MOCK_METHOD(Result, Connect, (const std::string& ecu_id), (override));
    MOCK_METHOD(Result, SendData, (const std::vector<uint8_t>& data), (override));
    MOCK_METHOD(Result, ReceiveData, (std::vector<uint8_t>& data), (override));
    MOCK_METHOD(void, Disconnect, (), (override));
};

// 使用 Mock 进行测试
TEST_F(UpgradeManagerTest, UpgradeWithMockDiagnostic) {
    auto mock_diag = std::make_unique<MockDiagnosticService>();
    
    EXPECT_CALL(*mock_diag, Connect("ECU001"))
        .WillOnce(Return(Result::kOk));
    EXPECT_CALL(*mock_diag, SendData(_))
        .Times(AtLeast(1))
        .WillRepeatedly(Return(Result::kOk));
    
    manager_->SetDiagnosticService(std::move(mock_diag));
    
    // 执行测试...
}
```

### 4.3 CMake 配置示例

```cmake
# tests/CMakeLists.txt
enable_testing()
find_package(GTest REQUIRED)

add_executable(upgrade_manager_test
    test_upgrade_manager.cpp
    mock_diagnostic_service.cpp
)

target_link_libraries(upgrade_manager_test
    upgrade_manager
    GTest::gtest
    GTest::gtest_main
    gmock
)

# 覆盖率配置
if(COVERAGE)
    target_compile_options(upgrade_manager_test PRIVATE --coverage)
    target_link_options(upgrade_manager_test PRIVATE --coverage)
endif()

add_test(NAME upgrade_manager_test COMMAND upgrade_manager_test)
```

---

## 5. 测试执行计划

### 5.1 执行顺序
| 阶段 | 用例范围 | 执行环境 | 责任人 |
|------|----------|----------|--------|
| 单元测试 | TC001-TC301 | 开发机 | 开发 |
| 集成测试 | | 仿真环境 | 测试 |
| 系统测试 | | 实车/台架 | 测试 |

### 5.2 回归测试策略
- 每次代码提交后自动执行单元测试
- 每日构建执行全量测试
- 版本发布前执行完整回归

---

## 6. 质量门禁

| 指标 | 阈值 | 说明 |
|------|------|------|
| 函数覆盖率 | ≥ 90% | 所有函数至少被调用一次 |
| 行覆盖率 | ≥ 80% | 可执行代码覆盖 |
| 分支覆盖率 | ≥ 70% | 条件分支覆盖 |
| 负面测试比例 | ≥ 40% | 异常/边界场景占比 |
| 测试通过率 | 100% | 所有用例必须通过 |
| 静态检查 | 0 严重警告 | MISRA C++ / AUTOSAR |

---

## 7. 附录

### 7.1 测试数据
| 数据项 | 值 | 说明 |
|--------|-----|------|
| 有效ECU ID | ECU001, ECU002 | |
| 无效ECU ID | "", "INVALID" | |
| 有效版本号 | "1.0.0", "2.0.0" | |
| 升级包路径 | /data/upgrade.pkg | |

### 7.2 常见问题排查
| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 测试挂起 | 异步操作未等待 | 添加超时机制 |
| Mock 不生效 | 接口未正确注入 | 检查依赖注入 |
| 覆盖率不达标 | 分支未覆盖 | 补充负面测试 |

---

## 变更记录

| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|----------|
| 1.0 | | | 初始版本 |
