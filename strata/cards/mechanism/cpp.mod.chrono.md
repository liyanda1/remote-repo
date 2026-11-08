---
id: cpp.mod.chrono
slot: mechanism
domain: generic-cpp
title: chrono 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/chrono.h:1
module: chrono
header: include/fmt/chrono.h
links:
- to: cpp.tst.chrono_test.format_tm
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_tm_future
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_tm_past
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.grow_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.gmtime
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.sys_time
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.local_time
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.local_time_before_epoch
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.local_time_narrow_duration
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.tm
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.daylight_savings_time_end
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_default
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.duration_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.tm_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.tp_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_default_fp
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_full_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_simple_q
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_precision_q
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_full_specs_q
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_width_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_colons
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.negative_durations
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.special_durations
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.floating_duration_sign
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.unsigned_duration
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.weekday
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.cpp20_duration_subsecond_support
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.utc_clock
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.timestamp_ratios
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.timestamp_sub_seconds
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.glibc_extensions
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.out_of_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.float_to_integral_duration_cast
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.custom_rep_duration_cast
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.calendar_padding
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.year_month_day
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.year_month_day_weekday_and_day_of_year
  type: verified_by
  weight: 0.5
- to: cpp.tst.color_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.compile_fallback
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.compile_type_with_get
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_default
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_escape
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.dynamic_format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.manual_ordering
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.named
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.static_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.text_and_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.unknown_format_fallback
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.empty
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.to_string_and_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.compile_format_string_literal
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
- to: cpp.tst.compile_test.constexpr_string_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.compile_test.format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_unscoped_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_underlying_type
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_dense_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_holey_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_sparse_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_negative_values
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_scattered_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_hash_collision
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_wrapping_hash_collision
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_sparse_enum_alias
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_with_extreme_values
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_alias
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_unknown_value
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_unknown_char_value
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_enum_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_underlying
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_underlying_is_mapped
  type: verified_by
  weight: 0.5
- to: cpp.tst.enum_test.format_underlying_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_impl_test.format_error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.escape
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.unmatched_braces
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.no_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.args_in_different_positions
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.arg_errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_emoji
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_issue_4851
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_multiple_emoji
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_mixed_content
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_precision_multiple_emoji
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_emoji_alignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_new_emoji_ranges
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.display_width_regional_indicator_pair
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.many_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.named_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.auto_arg_index
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.empty_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.left_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.right_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.center_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.fill
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.plus_sign
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.minus_sign
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.space_sign
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.hash_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.zero_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.zero_flag_and_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.width
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.debug_presentation
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.runtime_width
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.exponent_range
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.high_precision_trailing_zeros
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.high_precision_long_double
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.large_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.utf8_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.runtime_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_bool
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_short
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_bin
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_dec
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_hex
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_oct
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_int_locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_float
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_double
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.precision_rounding
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.prettify_float
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_nan
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_infinity
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_long_double
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_volatile_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_unsigned_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_cstring
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_pointer
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_enum_class
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_std_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_explicitly_convertible_to_std_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_implicitly_convertible_and_inherits_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_custom
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_string_from_speed_test
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.variadic
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.bytes
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.group_digits_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.nested_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.unpacked_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.compile_time_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.custom_format_compile_time_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.named_arg_udl
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.strong_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.non_null_terminated_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.back_insert_slicing
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_facet
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_facet_separator
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_facet_grouping
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_named_arg_with_locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_int_locale_zero_padding
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.formatter_nonconst_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.adl
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.formatter_overrides_implicit_conversion
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.ustring
  type: verified_by
  weight: 0.5
- to: cpp.tst.incomplete_type_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_system_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.dup_error_in_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.header_only_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.namespace
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.macros
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.named_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.literals
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.time
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.time_point
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.time_duration
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.weekday
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.printf
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.color
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.cstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.buffered_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.custom_context
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.compile_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.format_enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.no_builtin_types_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.no_builtin_types_test.format_pointer_compiled
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.format_windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.format_long_windows_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.io_putting
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.empty_custom_output
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.write_to_ostream_max_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.join_fallback_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.constexpr_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.template
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.copyfmt
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.range
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.streamed
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.unlocalized
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.number_is_too_big_in_arg_index
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.switch_arg_indexing
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.invalid_arg_index
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.hash_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.width
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.length
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.int
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.long_long
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.float
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.inf
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.char
  type: verified_by
  weight: 0.5
- to: cpp.tst.printf_test.pointer
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_odr_test.format_vector
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_array
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_2d_array
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_array_of_literals
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_vector
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_nested_vector
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_map
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_map_custom_pair
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_set
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_flat_set
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_adl_begin_end
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_width
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_pair
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_tuple
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_struct
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.range_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.range_format_debug_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.range
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.enum_range
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
- to: cpp.tst.ranges_test.nested_ranges
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.escape
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.range_of_range_of_mixed_const
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.vector_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.container_adaptor
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_as_tie
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_as_tuple_like
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.lvalue_qualified_begin_end
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.input_range_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.input_range_join_overload
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.format_as_with_ranges_mutable_begin_end
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.std_istream_iterator_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.movable_only_istream_iter_join
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.movable_only_istream_iter_join2
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_test.container_adaptor_opt_out
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_hex
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.path
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_std_test.format_vector_path
  type: verified_by
  weight: 0.5
- to: cpp.tst.ranges_std_test.format_quote_path
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.thread_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.complex
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.source_location
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.optional
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.expected
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.expected_format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.optional_format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.variant
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.variant_format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code_truncated_alignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.exception
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.exception_ptr
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.exception_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.type_info
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.bitint
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_bit_reference
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_const_bit_reference
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_bitset
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_atomic
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_atomic_flag
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_unique_ptr
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_shared_ptr
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
- to: cpp.tst.unicode_test.use_utf8
  type: verified_by
  weight: 0.5
- to: cpp.tst.unicode_test.legacy_locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_explicitly_convertible_to_wstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.compile_time_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_as
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.named_arg_udl
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.join
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.join_bytes
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.enum
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.streamed
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.sign_not_truncated
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.chrono
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.color
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_map
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.escape_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.localized_double
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.format_default_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.format_plus
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.wformat
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.chrono_weekday
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.sign
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.format_bitset
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.complex
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.optional
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.variant
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.expected
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test_xchar.path
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/chrono.h:1
  note: 公共头文件
---

## 模块
`chrono`，头文件 `include/fmt/chrono.h`。

由 cpp_static 按头文件粒度抽取，验证用例 340 个。
