---
id: cpp.tst.ostream_test.write_to_ostream_max_size
slot: verification
domain: generic-cpp
title: ostream_test.write_to_ostream_max_size
status: confirmed
confidence: likely
source: extractor
source_ref: test/ostream-test.cc:131
suite: ostream_test
case: write_to_ostream_max_size
file: test/ostream-test.cc
line: 131
links:
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
- to: cpp.sym.write_buffer
  type: exercises
  weight: 1.0
- to: cpp.sym.xsputn
  type: exercises
  weight: 1.0
evidence:
- ref: test/ostream-test.cc:131
  note: gtest 用例
---

## 用例
`ostream_test.write_to_ostream_max_size`

文件 `test/ostream-test.cc:131`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
