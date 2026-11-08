---
id: cpp.tst.module_test.memory_buffer
slot: verification
domain: generic-cpp
title: module_test.memory_buffer
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:206
suite: module_test
case: memory_buffer
file: test/module-test.cc
line: 206
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.format_to
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:206
  note: gtest 用例
---

## 用例
`module_test.memory_buffer`

文件 `test/module-test.cc:206`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
