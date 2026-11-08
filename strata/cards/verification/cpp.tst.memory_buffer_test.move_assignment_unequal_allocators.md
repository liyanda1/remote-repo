---
id: cpp.tst.memory_buffer_test.move_assignment_unequal_allocators
slot: verification
domain: generic-cpp
title: memory_buffer_test.move_assignment_unequal_allocators
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:417
suite: memory_buffer_test
case: move_assignment_unequal_allocators
file: test/format-test.cc
line: 417
links:
- to: cpp.sym.buffer
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:417
  note: gtest 用例
---

## 用例
`memory_buffer_test.move_assignment_unequal_allocators`

文件 `test/format-test.cc:417`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
