---
id: cpp.tst.file_test.dup2_error
slot: verification
domain: generic-cpp
title: file_test.dup2_error
status: confirmed
confidence: likely
source: extractor
source_ref: test/os-test.cc:496
suite: file_test
case: dup2_error
file: test/os-test.cc
line: 496
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
evidence:
- ref: test/os-test.cc:496
  note: gtest 用例
---

## 用例
`file_test.dup2_error`

文件 `test/os-test.cc:496`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
