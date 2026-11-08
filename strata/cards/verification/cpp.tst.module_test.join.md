---
id: cpp.tst.module_test.join
slot: verification
domain: generic-cpp
title: module_test.join
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:266
suite: module_test
case: join
file: test/module-test.cc
line: 266
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.join
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:266
  note: gtest 用例
---

## 用例
`module_test.join`

文件 `test/module-test.cc:266`，覆盖符号 4 个。

边来自静态调用匹配，置信度 likely。
