---
id: cpp.tst.module_test.time
slot: verification
domain: generic-cpp
title: module_test.time
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:280
suite: module_test
case: time
file: test/module-test.cc
line: 280
links:
- to: cpp.sym.gmtime
  type: exercises
  weight: 1.0
- to: cpp.sym.time_2
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:280
  note: gtest 用例
---

## 用例
`module_test.time`

文件 `test/module-test.cc:280`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
