---
id: cpp.mod.enum
slot: mechanism
domain: generic-cpp
title: enum 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/enum.h:1
module: enum
header: include/fmt/enum.h
links:
- to: cpp.tst.compile_test.static_format_high_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.unknown_format_fallback
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.length
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.compare
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.from_constexpr_fixed_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.append_partial
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.string_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_to_array
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.no_repeated_format_string_conversions
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.no_reflection
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_hash_collision
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_wrapping_hash_collision
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.annotation_is_required
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.parse_nonnegative_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.utf8_to_utf16
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.constexpr_grow
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_ctor_inline_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_ctor_inline_buffer_non_propagating
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_assignment_unequal_allocators
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_assignment_unequal_allocators_both_dynamic
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.arg_errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.fill
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
- to: cpp.tst.format_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_std_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.compile_time_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.non_null_terminated_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.to_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_vector
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.write_to_ostream_max_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.format_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.vprintf
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.make_printf_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.trailing_percent_non_nul_terminated
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code_truncated_alignment
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/enum.h:1
  note: 公共头文件
---

## 模块
`enum`，头文件 `include/fmt/enum.h`。

由 cpp_static 按头文件粒度抽取，验证用例 48 个。
