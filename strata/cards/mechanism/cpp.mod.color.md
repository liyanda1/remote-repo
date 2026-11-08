---
id: cpp.mod.color
slot: mechanism
domain: generic-cpp
title: color 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/color.h:1
module: color
header: include/fmt/color.h
links:
- to: cpp.tst.args_test.basic
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.strings_and_refs
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.custom_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.to_string_and_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.named_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.named_strings
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.named_arg_by_ref
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.named_custom_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.clear
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.reserve
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.throw_on_copy
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.move_constructor
  type: verified_by
  weight: 0.5
- to: cpp.tst.args_test.named_arg_count
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_to_empty_container
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_width_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_colons
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.text_style
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.println
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_variant
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_expected
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.output_iterators
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_range
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
- to: cpp.tst.base_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_to_array
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
- to: cpp.tst.base_test.no_repeated_format_string_conversions
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.format_error_code
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
- to: cpp.tst.format_test.large_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_custom
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.custom_format_compile_time_string
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
- to: cpp.tst.format_test.format_to_memory_buffer
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
- to: cpp.tst.format_test.adl
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vprint
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.memory_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.output_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.compile_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.print_2
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_to
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
- to: cpp.tst.xchar_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.ostream
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.wformat
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/color.h:1
  note: 公共头文件
---

## 模块
`color`，头文件 `include/fmt/color.h`。

由 cpp_static 按头文件粒度抽取，验证用例 87 个。
