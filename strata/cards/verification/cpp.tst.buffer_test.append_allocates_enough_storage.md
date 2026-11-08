---
id: cpp.tst.buffer_test.append_allocates_enough_storage
slot: verification
domain: generic-cpp
title: buffer_test.append_allocates_enough_storage
status: confirmed
confidence: likely
source: extractor
source_ref: test/core-test.cc:254
suite: buffer_test
case: append_allocates_enough_storage
file: test/core-test.cc
line: 254
links:
- to: cpp.sym.buffer
  type: exercises
  weight: 1.0
evidence:
- ref: test/core-test.cc:254
  note: gtest 用例
---

## 用例
`buffer_test.append_allocates_enough_storage`

文件 `test/core-test.cc:254`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
