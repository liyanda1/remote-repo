---
id: cpp.tst.util_test.parse_nonnegative_int
slot: verification
domain: generic-cpp
title: util_test.parse_nonnegative_int
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:221
suite: util_test
case: parse_nonnegative_int
file: test/format-test.cc
line: 221
links:
- to: cpp.sym.parse_nonnegative_int
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:221
  note: gtest 用例
---

## 用例
`util_test.parse_nonnegative_int`

文件 `test/format-test.cc:221`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
