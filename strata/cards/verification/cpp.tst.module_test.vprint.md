---
id: cpp.tst.module_test.vprint
slot: verification
domain: generic-cpp
title: module_test.vprint
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:165
suite: module_test
case: vprint
file: test/module-test.cc
line: 165
links:
- to: cpp.sym.make_format_args
  type: exercises
  weight: 1.0
- to: cpp.sym.vprint
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:165
  note: gtest 用例
---

## 用例
`module_test.vprint`

文件 `test/module-test.cc:165`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
