---
id: cpp.tst.memory_buffer_test.grow
slot: verification
domain: generic-cpp
title: memory_buffer_test.grow
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:495
suite: memory_buffer_test
case: grow
file: test/format-test.cc
line: 495
links:
- to: cpp.sym.allocator
  type: exercises
  weight: 1.0
- to: cpp.sym.buffer
  type: exercises
  weight: 1.0
- to: cpp.sym.deallocate
  type: exercises
  weight: 1.0
- to: cpp.sym.to_unsigned
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:495
  note: gtest 用例
---

## 用例
`memory_buffer_test.grow`

文件 `test/format-test.cc:495`，覆盖符号 4 个。

边来自静态调用匹配，置信度 likely。
