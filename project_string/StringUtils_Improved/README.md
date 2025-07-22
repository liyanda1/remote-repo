
# 📘 README: StringUtils 改进版

## 📝 项目简介
这是改进版的 StringUtils，修复了原实现中的编码缺陷。适合新员工在完成 UT 编写后作为“参考答案”。

## 🚀 改进点
| 函数                     | 改进内容                                       |
|--------------------------|-----------------------------------------------|
| `EndsWith`               | 检查后缀长度，防止 out_of_range                |
| `Split`                  | 空字符串返回空 vector                         |
| `ReplaceSubstring`       | 检查起始位置有效性，限制替换长度               |
| `IsValidPassword`        | 检查空指针输入                                 |
| `copyToBuffer`           | 检查 null buffer 和缓冲区大小                  |

## 📦 工程结构
```
.
├── string_utils.h
├── string_utils.cpp      # 改进后的实现
├── string_utils_test.cpp # 单元测试
├── CMakeLists.txt
└── README.md
```

## 💻 编译与运行
```bash
mkdir build && cd build
cmake ..
make
./string_utils_test
```
