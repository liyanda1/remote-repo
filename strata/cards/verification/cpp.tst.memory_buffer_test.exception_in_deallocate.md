---
id: cpp.tst.memory_buffer_test.exception_in_deallocate
slot: verification
domain: generic-cpp
title: memory_buffer_test.exception_in_deallocate
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:532
suite: memory_buffer_test
case: exception_in_deallocate
file: test/format-test.cc
line: 532
links:
- to: cpp.sym.buffer
  type: exercises
  weight: 1.0
- to: cpp.sym.deallocate
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:532
  note: gtest 用例
---

## 用例
`memory_buffer_test.exception_in_deallocate`

文件 `test/format-test.cc:532`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
