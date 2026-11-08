---
id: cpp.tst.memory_buffer_test.allocator
slot: verification
domain: generic-cpp
title: memory_buffer_test.allocator
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:515
suite: memory_buffer_test
case: allocator
file: test/format-test.cc
line: 515
links:
- to: cpp.sym.deallocate
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:515
  note: gtest 用例
---

## 用例
`memory_buffer_test.allocator`

文件 `test/format-test.cc:515`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
