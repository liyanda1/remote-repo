---
id: cpp.tst.os_test.report_windows_error
slot: verification
domain: generic-cpp
title: os_test.report_windows_error
status: confirmed
confidence: likely
source: extractor
source_ref: test/os-test.cc:96
suite: os_test
case: report_windows_error
file: test/os-test.cc
line: 96
links:
- to: cpp.sym.format_windows_error
  type: exercises
  weight: 1.0
- to: cpp.sym.report_windows_error
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
evidence:
- ref: test/os-test.cc:96
  note: gtest 用例
---

## 用例
`os_test.report_windows_error`

文件 `test/os-test.cc:96`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
