---
id: cpp.mod.ranges
slot: mechanism
domain: generic-cpp
title: ranges 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/ranges.h:1
module: ranges
header: include/fmt/ranges.h
links:
- to: cpp.tst.compile_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.constexpr_formatted_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.static_format
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
- to: cpp.tst.enum_test.no_reflection
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.annotation_is_required
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.join_fallback_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.closed_ofstream
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.tuple_parse_calls_element_parse
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.disabled_range_formatting_of_path
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.disabled_range_formatting_of_optional
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.unformattable_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.join_tuple
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.join_sentinel
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.join_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_join_adl_begin_end
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.input_range_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.input_range_join_overload
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.std_istream_iterator_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.movable_only_istream_iter_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_explicitly_convertible_to_wstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.join_bytes
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/ranges.h:1
  note: 公共头文件
---

## 模块
`ranges`，头文件 `include/fmt/ranges.h`。

由 cpp_static 按头文件粒度抽取，验证用例 37 个。
