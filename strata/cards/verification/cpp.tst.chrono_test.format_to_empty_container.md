---
id: cpp.tst.chrono_test.format_to_empty_container
slot: verification
domain: generic-cpp
title: chrono_test.format_to_empty_container
status: confirmed
confidence: likely
source: extractor
source_ref: test/chrono-test.cc:232
suite: chrono_test
case: format_to_empty_container
file: test/chrono-test.cc
line: 232
links:
- to: cpp.sym.back_inserter
  type: exercises
  weight: 1.0
- to: cpp.sym.format_to
  type: exercises
  weight: 1.0
evidence:
- ref: test/chrono-test.cc:232
  note: gtest 用例
---

## 用例
`chrono_test.format_to_empty_container`

文件 `test/chrono-test.cc:232`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
