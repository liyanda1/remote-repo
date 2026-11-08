---
id: cpp.tst.module_test.errors
slot: verification
domain: generic-cpp
title: module_test.errors
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:224
suite: module_test
case: errors
file: test/module-test.cc
line: 224
links:
- to: cpp.sym.format_system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.make_format_args
  type: exercises
  weight: 1.0
- to: cpp.sym.report_system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.report_windows_error
  type: exercises
  weight: 1.0
- to: cpp.sym.system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
- to: cpp.sym.vsystem_error
  type: exercises
  weight: 1.0
- to: cpp.sym.vwindows_error
  type: exercises
  weight: 1.0
- to: cpp.sym.windows_error
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:224
  note: gtest 用例
---

## 用例
`module_test.errors`

文件 `test/module-test.cc:224`，覆盖符号 9 个。

边来自静态调用匹配，置信度 likely。
