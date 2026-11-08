---
id: cpp.tst.file_test.dup_no_retry
slot: verification
domain: generic-cpp
title: file_test.dup_no_retry
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:337
suite: file_test
case: dup_no_retry
file: test/posix-mock-test.cc
line: 337
links:
- to: cpp.sym.format
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:337
  note: gtest 用例
---

## 用例
`file_test.dup_no_retry`

文件 `test/posix-mock-test.cc:337`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
