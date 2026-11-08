---
id: cpp.mod.xchar
slot: mechanism
domain: generic-cpp
title: xchar 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/xchar.h:1
module: xchar
header: include/fmt/xchar.h
links:
- to: cpp.tst.module_test.to_string
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
- to: cpp.tst.printf_test.check_format_string_regression
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_explicitly_convertible_to_wstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.to_wstring
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/xchar.h:1
  note: 公共头文件
---

## 模块
`xchar`，头文件 `include/fmt/xchar.h`。

由 cpp_static 按头文件粒度抽取，验证用例 29 个。
