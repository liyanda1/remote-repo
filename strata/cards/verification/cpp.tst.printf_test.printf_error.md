---
id: cpp.tst.printf_test.printf_error
slot: verification
domain: generic-cpp
title: printf_test.printf_error
status: confirmed
confidence: likely
source: extractor
source_ref: test/printf-test.cc:585
suite: printf_test
case: printf_error
file: test/printf-test.cc
line: 585
links:
- to: cpp.sym.fprintf
  type: exercises
  weight: 1.0
evidence:
- ref: test/printf-test.cc:585
  note: gtest 用例
---

## 用例
`printf_test.printf_error`

文件 `test/printf-test.cc:585`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
