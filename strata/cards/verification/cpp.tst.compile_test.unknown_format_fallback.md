---
id: cpp.tst.compile_test.unknown_format_fallback
slot: verification
domain: generic-cpp
title: compile_test.unknown_format_fallback
status: confirmed
confidence: likely
source: extractor
source_ref: test/compile-test.cc:321
suite: compile_test
case: unknown_format_fallback
file: test/compile-test.cc
line: 321
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
- to: cpp.sym.format_to_n
  type: exercises
  weight: 1.0
- to: cpp.sym.string_view
  type: exercises
  weight: 1.0
evidence:
- ref: test/compile-test.cc:321
  note: gtest 用例
---

## 用例
`compile_test.unknown_format_fallback`

文件 `test/compile-test.cc:321`，覆盖符号 5 个。

边来自静态调用匹配，置信度 likely。
