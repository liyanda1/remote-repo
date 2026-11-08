---
id: cpp.tst.file_test.dup2_retry
slot: verification
domain: generic-cpp
title: file_test.dup2_retry
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:346
suite: file_test
case: dup2_retry
file: test/posix-mock-test.cc
line: 346
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:346
  note: gtest 用例
---

## 用例
`file_test.dup2_retry`

文件 `test/posix-mock-test.cc:346`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
