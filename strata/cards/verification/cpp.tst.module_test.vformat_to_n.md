---
id: cpp.tst.module_test.vformat_to_n
slot: verification
domain: generic-cpp
title: module_test.vformat_to_n
status: confirmed
confidence: likely
source: extractor
source_ref: test/module-test.cc:146
suite: module_test
case: vformat_to_n
file: test/module-test.cc
line: 146
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.make_format_args
  type: exercises
  weight: 1.0
- to: cpp.sym.vformat_to_n
  type: exercises
  weight: 1.0
evidence:
- ref: test/module-test.cc:146
  note: gtest 用例
---

## 用例
`module_test.vformat_to_n`

文件 `test/module-test.cc:146`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
