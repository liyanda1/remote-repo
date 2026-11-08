---
id: cpp.tst.file_test.close_error_in_dtor
slot: verification
domain: generic-cpp
title: file_test.close_error_in_dtor
status: confirmed
confidence: likely
source: extractor
source_ref: test/os-test.cc:416
suite: file_test
case: close_error_in_dtor
file: test/os-test.cc
line: 416
links:
- to: cpp.sym.file
  type: exercises
  weight: 1.0
evidence:
- ref: test/os-test.cc:416
  note: gtest 用例
---

## 用例
`file_test.close_error_in_dtor`

文件 `test/os-test.cc:416`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
