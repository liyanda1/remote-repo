---
id: cpp.tst.output_redirect_test.restore_and_read
slot: verification
domain: generic-cpp
title: output_redirect_test.restore_and_read
status: confirmed
confidence: likely
source: extractor
source_ref: test/gtest-extra-test.cc:359
suite: output_redirect_test
case: restore_and_read
file: test/gtest-extra-test.cc
line: 359
links:
- to: cpp.sym.buffered_file
  type: exercises
  weight: 1.0
- to: cpp.sym.file
  type: exercises
  weight: 1.0
- to: cpp.sym.fprintf
  type: exercises
  weight: 1.0
evidence:
- ref: test/gtest-extra-test.cc:359
  note: gtest 用例
---

## 用例
`output_redirect_test.restore_and_read`

文件 `test/gtest-extra-test.cc:359`，覆盖符号 3 个。

边来自静态调用匹配，置信度 likely。
