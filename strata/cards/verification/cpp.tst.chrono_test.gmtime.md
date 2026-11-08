---
id: cpp.tst.chrono_test.gmtime
slot: verification
domain: generic-cpp
title: chrono_test.gmtime
status: confirmed
confidence: likely
source: extractor
source_ref: test/chrono-test.cc:240
suite: chrono_test
case: gmtime
file: test/chrono-test.cc
line: 240
links:
- to: cpp.sym.gmtime
  type: exercises
  weight: 1.0
- to: cpp.sym.time_2
  type: exercises
  weight: 1.0
evidence:
- ref: test/chrono-test.cc:240
  note: gtest 用例
---

## 用例
`chrono_test.gmtime`

文件 `test/chrono-test.cc:240`，覆盖符号 2 个。

边来自静态调用匹配，置信度 likely。
