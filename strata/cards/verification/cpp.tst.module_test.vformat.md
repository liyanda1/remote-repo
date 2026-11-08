---
id: cpp.tst.module_test.vformat
slot: verification
domain: generic-cpp
title: module_test.vformat
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:133
suite: module_test
case: vformat
file: test/module-test.cc
line: 133
links:
- to: cpp.sym.make_format_args
  type: exercises
  weight: 1.0
- to: cpp.sym.vformat
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:133
  note: gtest 用例
---

## 用例
`module_test.vformat`

文件 `test/module-test.cc:133`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
