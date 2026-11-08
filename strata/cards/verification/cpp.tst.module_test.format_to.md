---
id: cpp.tst.module_test.format_to
slot: verification
domain: generic-cpp
title: module_test.format_to
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:80
suite: module_test
case: format_to
file: test/module-test.cc
line: 80
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.format_to
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:80
  note: gtest 用例
---

## 用例
`module_test.format_to`

文件 `test/module-test.cc:80`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
