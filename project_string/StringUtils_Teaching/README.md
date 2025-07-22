
# 📘 README: StringUtils UT 编程练习（教学版）

## 📝 项目简介
本项目是为新入职开发工程师设计的 **单元测试练习**。通过阅读和测试 `StringUtils` 类的实现，掌握以下能力：

- 识别 **常见编码缺陷**（如未做校验、空指针、数组越界等）
- 编写 **GTest 单元测试**，验证代码健壮性
- 使用 **GMock** 模拟外部依赖，提高测试隔离性

## 📦 工程结构
```
.
├── string_utils.h          # 被测类声明
├── string_utils.cpp        # 被测类实现（包含多个已知编码问题）
├── string_utils_test.cpp   # 单元测试（教学版：完整示例）
├── CMakeLists.txt          # 编译配置
└── README.md               # 本文档
```

## 🚩 被测类：`StringUtils`
| 函数名                     | 描述                                   | 已知问题                            |
|---------------------------|---------------------------------------|-------------------------------------|
| `EndsWith(str, suffix)`   | 检查字符串是否以指定后缀结尾           | 未检查 `suffix.length > str.length`|
| `Split(str, delimiter)`   | 按分隔符切割字符串                     | 未处理空输入                        |
| `ReplaceSubstring(str, start, len, repl)` | 替换字符串子串                | 未检查 `start` 和 `len` 是否越界    |
| `IsValidPassword(password)`| 检查密码是否符合规则（至少1大写+1数字）| 未检查 `password` 是否为 `nullptr`  |
| `copyToBuffer(src, buf, size)` | 拷贝字符串到缓冲区                | 未检查 `buf` 是否为 `nullptr`；`src.size()>size`时可能越界|

## 🎯 练习目标（教学版）
- 已提供完整测试用例
- 阅读每个测试的 **功能描述、前置条件、预期结果**
- 分析为什么这些输入会暴露编码缺陷
- 修改 `StringUtils` 实现并观察测试是否通过

## 💻 编译与运行
```bash
mkdir build && cd build
cmake ..
make
./string_utils_test
```

## 📖 学习重点
- **编码安全**: 输入校验、指针检查、边界保护
- **单元测试**: GTest 断言（`EXPECT_EQ`, `EXPECT_THROW`, `EXPECT_DEATH`）
- **Mock 技巧**: GMock 的 `EXPECT_CALL` 使用
