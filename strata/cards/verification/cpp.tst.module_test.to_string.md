---
id: cpp.tst.module_test.to_string
slot: verification
domain: generic-cpp
title: module_test.to_string
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:64
suite: module_test
case: to_string
file: test/module-test.cc
line: 64
links:
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
- to: cpp.sym.to_wstring
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:64
  note: gtest 用例
---

## 用例
`module_test.to_string`

文件 `test/module-test.cc:64`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
