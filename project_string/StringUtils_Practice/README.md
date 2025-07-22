
# 📘 README: StringUtils UT 编程练习（练习版）

## 📝 项目简介
本项目是为新入职开发工程师设计的 **单元测试练习**。通过分析和测试 `StringUtils` 类，提升以下能力：

- 发现常见编码问题（如未做校验、空指针、越界等）
- 独立编写单元测试用例验证代码健壮性
- 掌握 GTest 和 GMock 的基本用法

## 📦 工程结构
```
.
├── string_utils.h          # 被测类声明
├── string_utils.cpp        # 被测类实现（已知多个编码问题）
├── string_utils_test.cpp   # 单元测试（练习版：留空部分待补充）
├── CMakeLists.txt          # 编译配置
└── README.md               # 本文档
```

## 🎯 练习任务
1. 阅读 `string_utils.cpp`，找出潜在的编码缺陷。
2. 在 `string_utils_test.cpp` 中补充缺失的测试用例，覆盖：
   - 正常路径（normal case）
   - 边界条件（edge case）
   - 错误输入（invalid input）
3. 使用 **EXPECT_THROW** / **EXPECT_DEATH** 检验异常处理。
4. 尝试引入 **GMock**，模拟外部依赖。

## 💻 编译与运行
```bash
mkdir build && cd build
cmake ..
make
./string_utils_test
```

## 🏆 挑战
- 编写全覆盖测试
- 重构存在缺陷的函数
