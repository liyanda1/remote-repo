# {{FEATURE_NAME}} - 测试用例设计文档

**AR单号**: {{AR_NUMBER}}  
**需求名称**: {{FEATURE_NAME}}  
**版本**: v1.0  
**日期**: {{DATE}}  
**作者**: {{AUTHOR}}

---

## 1. 测试概述

### 1.1 测试范围

【描述本次测试的范围：覆盖的模块、功能点】

### 1.2 测试策略

【描述测试策略：单元测试、集成测试、系统测试等】

### 1.3 测试环境

| 环境项 | 配置 |
|--------|------|
| 操作系统 | 【如：Linux/Windows】 |
| 编译器 | 【如：GCC 11.0】 |
| 测试框架 | 【如：Google Test 1.12】 |
| 覆盖率工具 | 【如：lcov】 |

---

## 2. 测试用例设计

### 2.1 正常场景（TC001-TC099）

#### TC001: 【用例名称】

| 字段 | 内容 |
|------|------|
| **用例ID** | TC001 |
| **用例名称** | 【简洁描述测试目的】 |
| **前置条件** | 【执行测试前必须满足的条件】 |
| **测试步骤** | 1. 【步骤 1】<br>2. 【步骤 2】<br>3. 【步骤 3】 |
| **预期结果** | 【每个步骤对应的预期结果】 |
| **优先级** | 高/中/低 |
| **自动化** | 是/否 |
| **关联设计** | 【对应的设计文档章节】 |

**测试代码框架：**

```cpp
// TC001: 【用例名称】
TEST_F(ComponentTest, TC001_TestName) {
    // Arrange
    InputData input;
    input.value = 100;
    
    // Act
    auto result = component_->Process(input);
    
    // Assert
    EXPECT_EQ(result.status, Status::kOk);
    EXPECT_EQ(result.output, expected_value);
}
```

#### TC002: 【用例名称】

| 字段 | 内容 |
|------|------|
| **用例ID** | TC002 |
| **用例名称** | 【简洁描述测试目的】 |
| **前置条件** | 【执行测试前必须满足的条件】 |
| **测试步骤** | 1. 【步骤 1】<br>2. 【步骤 2】 |
| **预期结果** | 【每个步骤对应的预期结果】 |
| **优先级** | 高/中/低 |
| **自动化** | 是/否 |
| **关联设计** | 【对应的设计文档章节】 |

---

### 2.2 异常场景（TC101-TC199）

#### TC101: 【用例名称】

| 字段 | 内容 |
|------|------|
| **用例ID** | TC101 |
| **用例名称** | 【简洁描述测试目的】 |
| **前置条件** | 【执行测试前必须满足的条件】 |
| **测试步骤** | 1. 【步骤 1】<br>2. 【步骤 2】 |
| **预期结果** | 【每个步骤对应的预期结果，包含错误处理】 |
| **优先级** | 高/中/低 |
| **自动化** | 是/否 |
| **关联设计** | 【对应的设计文档章节】 |

**测试代码框架：**

```cpp
// TC101: 【用例名称】
TEST_F(ComponentTest, TC101_TestName) {
    // Arrange
    InputData input;
    input.value = INVALID_VALUE;  // 无效值
    
    // Act
    auto result = component_->Process(input);
    
    // Assert
    EXPECT_EQ(result.status, Status::kInvalidParam);
}
```

---

### 2.3 边界场景（TC201-TC299）

#### TC201: 【用例名称 - 边界值测试】

| 字段 | 内容 |
|------|------|
| **用例ID** | TC201 |
| **用例名称** | 【简洁描述测试目的】 |
| **前置条件** | 【执行测试前必须满足的条件】 |
| **测试数据** | 【边界值列表：MIN-1, MIN, MIN+1, NORMAL, MAX-1, MAX, MAX+1】 |
| **测试步骤** | 1. 【步骤 1】<br>2. 【步骤 2】 |
| **预期结果** | 【每个边界值对应的预期结果】 |
| **优先级** | 中 |
| **自动化** | 是 |
| **关联设计** | 【对应的设计文档章节】 |

**参数化测试代码框架：**

```cpp
// TC201: 边界值参数化测试
class BoundaryTest : public ::testing::TestWithParam<int> {};

TEST_P(BoundaryTest, TC201_BoundaryValue) {
    int value = GetParam();
    
    InputData input;
    input.value = value;
    
    auto result = component_->Process(input);
    
    if (value < MIN_VALUE || value > MAX_VALUE) {
        EXPECT_EQ(result.status, Status::kInvalidParam);
    } else {
        EXPECT_EQ(result.status, Status::kOk);
    }
}

INSTANTIATE_TEST_SUITE_P(
    BoundaryValues,
    BoundaryTest,
    ::testing::Values(MIN_VALUE - 1, MIN_VALUE, MIN_VALUE + 1, 
                      NORMAL_VALUE, 
                      MAX_VALUE - 1, MAX_VALUE, MAX_VALUE + 1)
);
```

---

### 2.4 状态转换场景（TC301-TC399）

#### TC301: 【用例名称 - 状态转换测试】

| 字段 | 内容 |
|------|------|
| **用例ID** | TC301 |
| **用例名称** | 【简洁描述测试目的】 |
| **前置条件** | 【初始状态】 |
| **测试步骤** | 1. 【触发状态转换的操作】<br>2. 【验证新状态】 |
| **预期结果** | 【状态转换成功，新状态符合预期】 |
| **优先级** | 高 |
| **自动化** | 是 |
| **关联设计** | 【对应的设计文档章节】 |

**测试代码框架：**

```cpp
// TC301: 状态转换测试
TEST_F(ComponentTest, TC301_StateTransition) {
    // 验证初始状态
    EXPECT_EQ(component_->GetState(), State::kIdle);
    
    // 触发状态转换
    component_->Initialize(config);
    
    // 验证新状态
    EXPECT_EQ(component_->GetState(), State::kReady);
}
```

---

## 3. Mock 对象定义

### 3.1 【服务接口名称】Mock

```cpp
// Mock 外部服务
class MockService : public IService {
public:
    MOCK_METHOD(Result, Connect, (const std::string& endpoint), (override));
    MOCK_METHOD(Result, Send, (const std::vector<uint8_t>& data), (override));
    MOCK_METHOD(Result, Receive, (std::vector<uint8_t>& data), (override));
    MOCK_METHOD(void, Disconnect, (), (override));
};
```

### 3.2 Mock 使用示例

```cpp
TEST_F(ComponentTest, ProcessWithServiceError) {
    auto mock_service = std::make_unique<MockService>();
    
    // 设置 Mock 期望
    EXPECT_CALL(*mock_service, Connect(_))
        .WillOnce(Return(Result::kOk));
    EXPECT_CALL(*mock_service, Send(_))
        .WillOnce(Return(Result::kNetworkError));
    
    // 注入 Mock
    component_->SetService(std::move(mock_service));
    
    // 执行测试
    InputData input;
    input.value = 100;
    
    auto result = component_->Process(input);
    
    // 验证结果
    EXPECT_EQ(result.status, Status::kNetworkError);
}
```

---

## 4. 测试夹具定义

```cpp
// 测试夹具类
class ComponentTest : public ::testing::Test {
protected:
    void SetUp() override {
        // 每个测试用例执行前的初始化
        component_ = std::make_unique<Component>();
        component_->Initialize(default_config_);
    }
    
    void TearDown() override {
        // 每个测试用例执行后的清理
        component_->Shutdown();
    }
    
    std::unique_ptr<Component> component_;
    Config default_config_;
};
```

---

## 5. 构建配置

### 5.1 CMakeLists.txt 示例

```cmake
cmake_minimum_required(VERSION 3.14)
project({{FEATURE_NAME}}_tests)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 Google Test
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# 测试可执行文件
add_executable({{FEATURE_NAME}}_tests
    test_component.cpp
)

# 链接库
target_link_libraries({{FEATURE_NAME}}_tests
    ${GTEST_LIBRARIES}
    ${GTEST_MAIN_LIBRARIES}
    pthread
)

# 启用测试
enable_testing()
add_test(NAME {{FEATURE_NAME}}_tests COMMAND {{FEATURE_NAME}}_tests)
```

---

## 6. 测试数据

### 6.1 测试数据文件

| 数据文件 | 路径 | 说明 |
|----------|------|------|
| 【数据文件 1】 | 【路径】 | 【说明】 |
| 【数据文件 2】 | 【路径】 | 【说明】 |

### 6.2 数据格式说明

【描述测试数据的格式、字段含义】

---

## 7. 质量门禁

| 指标 | 阈值 | 当前状态 |
|------|------|----------|
| 用例总数 | ≥ 设计场景数 × 1.5 | 【数量】 |
| 负面测试比例 | ≥ 40% | 【比例】 |
| 正常场景覆盖 | 100% | 【状态】 |
| 边界值覆盖 | 100% | 【状态】 |
| 状态转换覆盖 | 100% | 【状态】 |
| 可自动化率 | ≥ 80% | 【比例】 |

---

## 8. 附录

### 8.1 测试执行命令

```bash
# 构建测试
mkdir build && cd build
cmake ..
make -j

# 运行测试
./{{FEATURE_NAME}}_tests

# 运行指定测试
./{{FEATURE_NAME}}_tests --gtest_filter=ComponentTest.TC001*

# 生成覆盖率报告
cmake -DCOVERAGE=ON ..
make -j
ctest --output-on-failure
lcov --capture --directory . --output-file coverage.info
lcov --remove coverage.info '/usr/*' '*/tests/*' --output-file coverage_filtered.info
genhtml coverage_filtered.info --output-directory coverage_report
```

### 8.2 变更记录

| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|----------|
| v1.0 | {{DATE}} | {{AUTHOR}} | 初始版本 |
