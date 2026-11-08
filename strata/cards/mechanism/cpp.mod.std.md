---
id: cpp.mod.std
slot: mechanism
domain: generic-cpp
title: std 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/std.h:1
module: std
header: include/fmt/std.h
links:
- to: cpp.tst.chrono_test.format_to_empty_container
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.output_iterators
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_range
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
- to: cpp.tst.base_test.get_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.adl_check
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_nonconst
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.promiscuous_conversions
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_to_custom_container
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.write_float128
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.write_double_double
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.write_dragon_even
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.copy
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.back_insert_iterator
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.write_uintptr_fallback
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.output_iterators
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_no_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_vector
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_propagates_exceptions
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.vformat_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.memory_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.path
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_std_test.format_vector_path
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code_truncated_alignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_byte
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_explicitly_convertible_to_wstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.compile_time_string_format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.vformat_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.path
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/std.h:1
  note: 公共头文件
---

## 模块
`std`，头文件 `include/fmt/std.h`。

由 cpp_static 按头文件粒度抽取，验证用例 55 个。
