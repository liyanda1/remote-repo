---
id: cpp.tst.base_test.no_repeated_format_string_conversions
slot: verification
domain: generic-cpp
title: base_test.no_repeated_format_string_conversions
status: confirmed
confidence: likely
source: extractor
source_ref: test/core-test.cc:908
suite: base_test
case: no_repeated_format_string_conversions
file: test/core-test.cc
line: 908
links:
- to: cpp.sym.format_to
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/core-test.cc:908
  note: gtest 用例
---

## 用例
`base_test.no_repeated_format_string_conversions`

文件 `test/core-test.cc:908`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
