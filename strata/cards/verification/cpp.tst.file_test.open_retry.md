---
id: cpp.tst.file_test.open_retry
slot: verification
domain: generic-cpp
title: file_test.open_retry
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:216
suite: file_test
case: open_retry
file: test/posix-mock-test.cc
line: 216
links:
- to: cpp.sym.file
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:216
  note: gtest 用例
---

## 用例
`file_test.open_retry`

文件 `test/posix-mock-test.cc:216`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
