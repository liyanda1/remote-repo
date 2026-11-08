---
id: cpp.tst.buffered_file_test.open_retry
slot: verification
domain: generic-cpp
title: buffered_file_test.open_retry
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:382
suite: buffered_file_test
case: open_retry
file: test/posix-mock-test.cc
line: 382
links:
- to: cpp.sym.buffered_file
  type: exercises
  weight: 1.0
- to: cpp.sym.system_error
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:382
  note: gtest 用例
---

## 用例
`buffered_file_test.open_retry`

文件 `test/posix-mock-test.cc:382`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
