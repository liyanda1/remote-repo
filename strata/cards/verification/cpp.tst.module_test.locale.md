---
id: cpp.tst.module_test.locale
slot: verification
domain: generic-cpp
title: module_test.locale
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:184
suite: module_test
case: locale
file: test/module-test.cc
line: 184
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.make_format_args
  type: exercises
  weight: 1.0
- to: cpp.sym.vformat
  type: exercises
  weight: 1.0
- to: cpp.sym.vformat_to
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:184
  note: gtest 用例
---

## 用例
`module_test.locale`

文件 `test/module-test.cc:184`，覆盖符号 5 个。

边来自静态调用匹配，置信度 likely。
