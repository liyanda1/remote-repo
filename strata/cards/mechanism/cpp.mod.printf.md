---
id: cpp.mod.printf
slot: mechanism
domain: generic-cpp
title: printf 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/printf.h:1
module: printf
header: include/fmt/printf.h
links:
- to: cpp.tst.module_test.sprintf
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.no_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.trailing_percent
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.escape
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.positional_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.automatic_arg_indexing
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.zero_positional_width_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.default_align_right
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.zero_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.plus_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.minus_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.space_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.dynamic_width
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.int_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.zero_int_with_zero_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.float_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.string_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.ignore_precision_for_non_numeric_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.dynamic_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.positional_width
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.positional_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.positional_width_and_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.bool
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.string
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.vprintf
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.check_format_string_regression
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.fixed_large_exponent
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.make_printf_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.trailing_percent_non_nul_terminated
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/printf.h:1
  note: 公共头文件
---

## 模块
`printf`，头文件 `include/fmt/printf.h`。

由 cpp_static 按头文件粒度抽取，验证用例 31 个。
