---
id: cpp.tst.std_test.thread_id
slot: verification
domain: generic-cpp
title: std_test.thread_id
status: confirmed
confidence: likely
source: extractor
source_ref: test/std-test.cc:79
suite: std_test
case: thread_id
file: test/std-test.cc
line: 79
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.get_id
  type: exercises
  weight: 1.0
evidence:
- ref: test/std-test.cc:79
  note: gtest 用例
---

## 用例
`std_test.thread_id`

文件 `test/std-test.cc:79`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
