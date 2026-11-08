---
id: cpp.mod.format_inl
slot: mechanism
domain: generic-cpp
title: format-inl 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/format-inl.h:1
module: format-inl
header: include/fmt/format-inl.h
links:
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.format_error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.utf8_to_utf16
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.utf8_to_utf16_empty_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.format_system_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.system_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.report_system_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_facet
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.invalid_glibc_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_write
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.scoped_redirect
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.restore_and_read
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.fprintf
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.printf_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.is_printable
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/format-inl.h:1
  note: 公共头文件
---

## 模块
`format-inl`，头文件 `include/fmt/format-inl.h`。

由 cpp_static 按头文件粒度抽取，验证用例 16 个。
