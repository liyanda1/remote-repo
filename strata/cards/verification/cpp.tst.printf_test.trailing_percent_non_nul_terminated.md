---
id: cpp.tst.printf_test.trailing_percent_non_nul_terminated
slot: verification
domain: generic-cpp
title: printf_test.trailing_percent_non_nul_terminated
status: confirmed
confidence: likely
source: extractor
source_ref: test/printf-test.cc:624
suite: printf_test
case: trailing_percent_non_nul_terminated
file: test/printf-test.cc
line: 624
links:
- to: cpp.sym.sprintf
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/printf-test.cc:624
  note: gtest 用例
---

## 用例
`printf_test.trailing_percent_non_nul_terminated`

文件 `test/printf-test.cc:624`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
