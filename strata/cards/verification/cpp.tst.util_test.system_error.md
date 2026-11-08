---
id: cpp.tst.util_test.system_error
slot: verification
domain: generic-cpp
title: util_test.system_error
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:284
suite: util_test
case: system_error
file: test/format-test.cc
line: 284
links:
- to: cpp.sym.format_system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:284
  note: gtest 用例
---

## 用例
`util_test.system_error`

文件 `test/format-test.cc:284`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
