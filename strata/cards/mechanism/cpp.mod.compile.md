---
id: cpp.mod.compile
slot: mechanism
domain: generic-cpp
title: compile 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/compile.h:1
module: compile
header: include/fmt/compile.h
links:
- to: cpp.tst.compile_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.constexpr_formatted_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.static_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.unknown_format_fallback
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.is_compiled_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.bool
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.integer
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.char
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.string
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.combination
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.custom_type
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.multibyte_fill
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_time_formatting_test.floating_point
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.constexpr_parse_arg_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.hash_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.zero_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.width
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.runtime_width
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.high_precision_bounded_output
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.formatted_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_n_output_iterator
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.adl
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.formatted_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.closed_ofstream
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.wide_format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.wide_format_to_n_runtime
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/compile.h:1
  note: 公共头文件
---

## 模块
`compile`，头文件 `include/fmt/compile.h`。

由 cpp_static 按头文件粒度抽取，验证用例 32 个。
