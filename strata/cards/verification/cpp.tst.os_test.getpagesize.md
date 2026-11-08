---
id: cpp.tst.os_test.getpagesize
slot: verification
domain: generic-cpp
title: os_test.getpagesize
status: confirmed
confidence: likely
source: extractor
source_ref: test/posix-mock-test.cc:202
suite: os_test
case: getpagesize
file: test/posix-mock-test.cc
line: 202
links:
- to: cpp.sym.getpagesize
  type: exercises
  weight: 1.0
evidence:
- ref: test/posix-mock-test.cc:202
  note: gtest 用例
---

## 用例
`os_test.getpagesize`

文件 `test/posix-mock-test.cc:202`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
