---
id: cpp.tst.buffered_file_test.close_no_retry_in_dtor
slot: verification
domain: generic-cpp
title: buffered_file_test.close_no_retry_in_dtor
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:394
suite: buffered_file_test
case: close_no_retry_in_dtor
file: test/posix-mock-test.cc
line: 394
links:
- to: cpp.sym.buffered_file
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:394
  note: gtest 用例
---

## 用例
`buffered_file_test.close_no_retry_in_dtor`

文件 `test/posix-mock-test.cc:394`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
