---
id: cpp.tst.file_test.close_no_retry_in_dtor
slot: verification
domain: generic-cpp
title: file_test.close_no_retry_in_dtor
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:227
suite: file_test
case: close_no_retry_in_dtor
file: test/posix-mock-test.cc
line: 227
links:
- to: cpp.sym.file
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:227
  note: gtest 用例
---

## 用例
`file_test.close_no_retry_in_dtor`

文件 `test/posix-mock-test.cc:227`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
