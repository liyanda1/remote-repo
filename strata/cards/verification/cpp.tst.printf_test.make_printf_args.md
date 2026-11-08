---
id: cpp.tst.printf_test.make_printf_args
slot: verification
domain: generic-cpp
title: printf_test.make_printf_args
status: confirmed
confidence: likely
source: extractor
source_ref: test/printf-test.cc:614
suite: printf_test
case: make_printf_args
file: test/printf-test.cc
line: 614
links:
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
- to: cpp.sym.vsprintf
  type: exercises
  weight: 1.0
evidence:
- ref: test/printf-test.cc:614
  note: gtest 用例
---

## 用例
`printf_test.make_printf_args`

文件 `test/printf-test.cc:614`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
