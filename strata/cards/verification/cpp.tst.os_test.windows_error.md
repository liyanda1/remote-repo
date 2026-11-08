---
id: cpp.tst.os_test.windows_error
slot: verification
domain: generic-cpp
title: os_test.windows_error
status: confirmed
confidence: likely
source: extractor
source_ref: test/os-test.cc:83
suite: os_test
case: windows_error
file: test/os-test.cc
line: 83
links:
- to: cpp.sym.format_windows_error
  type: exercises
  weight: 1.0
- to: cpp.sym.system_error
  type: exercises
  weight: 1.0
- to: cpp.sym.to_string
  type: exercises
  weight: 1.0
- to: cpp.sym.windows_error
  type: exercises
  weight: 1.0
evidence:
- ref: test/os-test.cc:83
  note: gtest 用例
---

## 用例
`os_test.windows_error`

文件 `test/os-test.cc:83`，覆盖符号 4 个。

边来自静态调用匹配，置信度 likely。
