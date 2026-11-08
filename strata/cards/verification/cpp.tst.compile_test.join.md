---
id: cpp.tst.compile_test.join
slot: verification
domain: generic-cpp
title: compile_test.join
status: confirmed
confidence: likely
source: extractor
source_ref: test/compile-test.cc:174
suite: compile_test
case: join
file: test/compile-test.cc
line: 174
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.join
  type: exercises
  weight: 1.0
evidence:
- ref: test/compile-test.cc:174
  note: gtest 用例
---

## 用例
`compile_test.join`

文件 `test/compile-test.cc:174`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
