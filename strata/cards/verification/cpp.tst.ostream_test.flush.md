---
id: cpp.tst.ostream_test.flush
slot: verification
domain: generic-cpp
title: ostream_test.flush
status: confirmed
confidence: likely
source: extractor
source_ref: test/os-test.cc:322
suite: ostream_test
case: flush
file: test/os-test.cc
line: 322
links:
- to: cpp.sym.file
  type: exercises
  weight: 1.0
- to: cpp.sym.output_file
  type: exercises
  weight: 1.0
evidence:
- ref: test/os-test.cc:322
  note: gtest 用例
---

## 用例
`ostream_test.flush`

文件 `test/os-test.cc:322`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
