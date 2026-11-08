---
id: cpp.mod.format
slot: mechanism
domain: generic-cpp
title: format 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/format.h:1
module: format
header: include/fmt/format.h
links:
- to: cpp.tst.color_test.format_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.from_constexpr_fixed_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.custom_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.visit_invalid_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.construct
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.compare
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.add_compare
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.shift_left
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.multiply
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.square
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.divmod_assign_zero_divisor
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.divmod_assign_self
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.divmod_assign_unaligned
  type: verified_by
  weight: 0.5
- to: cpp.tst.bigint_test.divmod_assign
  type: verified_by
  weight: 0.5
- to: cpp.tst.fp_test.double_tests
  type: verified_by
  weight: 0.5
- to: cpp.tst.fp_test.normalize
  type: verified_by
  weight: 0.5
- to: cpp.tst.fp_test.multiply
  type: verified_by
  weight: 0.5
- to: cpp.tst.fp_test.dragonbox_max_k
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.format_error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.count_digits
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.count_digits_uint128
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.divmod_pow10_19
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.countl_zero
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.write_console_signature
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.utf8_decode_decode_all
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.utf8_decode_out_of_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.utf8_decode_surrogate_halves
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.utf8_decode_non_canonical_encodings
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.utf8_decode_bogus_byte_sequences
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.to_utf8
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.shift
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.minus
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.bitwise_not
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.plus_assign
  type: verified_by
  weight: 0.5
- to: cpp.tst.uint128_test.multiply
  type: verified_by
  weight: 0.5
- to: cpp.tst.float_test.isfinite
  type: verified_by
  weight: 0.5
- to: cpp.tst.float_test.isnan
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.bit_cast
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.increment
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.allocator_ref
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
- to: cpp.tst.memory_buffer_test.ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_assignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.grow
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.allocator
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.exception_in_deallocate
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.max_size_allocator
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.max_size_allocator_overflow
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.default_allocator_overflow
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.digits2_alignment
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
- to: cpp.tst.format_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_enum_class
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.big_print
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.bytes
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.group_digits_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_message_example
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.formatter_not_specialized
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.to_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.fill_via_appender
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_to_memory_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.char_traits_not_ambiguous
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_as_to_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.test_formatters_enabled
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_int_test.data
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_int_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.writer
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.print_to_broken_pipe
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_system_error_no_unreachable_code_warning
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.to_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.memory_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.ptr
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.format_windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.format_long_windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.report_windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.to_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.closed_ofstream
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.open_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.to_string_vector
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
- to: cpp.tst.scan_test.read_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code_truncated_alignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.exception
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_reference_wrapper
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_reference_wrapper_with_format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_reference_wrapper_with_format_as_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.int_formatter
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/format.h:1
  note: 公共头文件
---

## 模块
`format`，头文件 `include/fmt/format.h`。

由 cpp_static 按头文件粒度抽取，验证用例 103 个。
