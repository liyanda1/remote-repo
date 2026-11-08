---
id: cpp.tst.module_test.output_file
slot: verification
domain: generic-cpp
title: module_test.output_file
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:341
suite: module_test
case: output_file
file: test/module-test.cc
line: 341
links:
- to: cpp.sym.output_file
  type: exercises
  weight: 1.0
- to: cpp.sym.println
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:341
  note: gtest 用例
---

## 用例
`module_test.output_file`

文件 `test/module-test.cc:341`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
