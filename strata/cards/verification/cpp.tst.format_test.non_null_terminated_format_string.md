---
id: cpp.tst.format_test.non_null_terminated_format_string
slot: verification
domain: generic-cpp
title: format_test.non_null_terminated_format_string
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:2340
suite: format_test
case: non_null_terminated_format_string
file: test/format-test.cc
line: 2340
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:2340
  note: gtest 用例
---

## 用例
`format_test.non_null_terminated_format_string`

文件 `test/format-test.cc:2340`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
