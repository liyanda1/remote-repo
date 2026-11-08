---
id: cpp.tst.base_test.throw_in_buffer_dtor
slot: verification
domain: generic-cpp
title: base_test.throw_in_buffer_dtor
status: confirmed
confidence: likely
source: extractor
source_ref: test/core-test.cc:812
suite: base_test
case: throw_in_buffer_dtor
file: test/core-test.cc
line: 812
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.format
  type: exercises
  weight: 1.0
- to: cpp.sym.format_to
  type: exercises
  weight: 1.0
- to: cpp.sym.ignore_unused
  type: exercises
  weight: 1.0
- to: cpp.sym.parse
  type: exercises
  weight: 1.0
- to: cpp.sym.push_back
  type: exercises
  weight: 1.0
- to: cpp.sym.runtime
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/core-test.cc:812
  note: gtest 用例
---

## 用例
`base_test.throw_in_buffer_dtor`

文件 `test/core-test.cc:812`，覆盖符号 8 个。

边来自静态调用匹配，置信度 likely。
