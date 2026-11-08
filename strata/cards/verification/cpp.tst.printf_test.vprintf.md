---
id: cpp.tst.printf_test.vprintf
slot: verification
domain: generic-cpp
title: printf_test.vprintf
status: confirmed
confidence: likely
source: extractor
source_ref: test/printf-test.cc:592
suite: printf_test
case: vprintf
file: test/printf-test.cc
line: 592
links:
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
- to: cpp.sym.vfprintf
  type: exercises
  weight: 1.0
- to: cpp.sym.vsprintf
  type: exercises
  weight: 1.0
evidence:
- ref: test/printf-test.cc:592
  note: gtest 用例
---

## 用例
`printf_test.vprintf`

文件 `test/printf-test.cc:592`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
