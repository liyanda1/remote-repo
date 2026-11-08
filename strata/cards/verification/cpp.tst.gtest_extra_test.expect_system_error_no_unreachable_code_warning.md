---
id: cpp.tst.gtest_extra_test.expect_system_error_no_unreachable_code_warning
slot: verification
domain: generic-cpp
title: gtest_extra_test.expect_system_error_no_unreachable_code_warning
status: confirmed
confidence: likely
source: extractor
source_ref: test/gtest-extra-test.cc:214
suite: gtest_extra_test
case: expect_system_error_no_unreachable_code_warning
file: test/gtest-extra-test.cc
line: 214
links:
- to: cpp.sym.system_error
  type: exercises
  weight: 1.0
evidence:
- ref: test/gtest-extra-test.cc:214
  note: gtest 用例
---

## 用例
`gtest_extra_test.expect_system_error_no_unreachable_code_warning`

文件 `test/gtest-extra-test.cc:214`，覆盖符号 1 个。

边来自静态调用匹配，置信度 likely。
