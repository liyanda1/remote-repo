---
id: cpp.tst.format_test.invalid_glibc_buffer
slot: verification
domain: generic-cpp
title: format_test.invalid_glibc_buffer
status: confirmed
confidence: likely
source: extractor
source_ref: test/format-test.cc:2849
suite: format_test
case: invalid_glibc_buffer
file: test/format-test.cc
line: 2849
links:
- to: cpp.sym.fprintf
  type: exercises
  weight: 1.0
evidence:
- ref: test/format-test.cc:2849
  note: gtest 用例
---

## 用例
`format_test.invalid_glibc_buffer`

文件 `test/format-test.cc:2849`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
