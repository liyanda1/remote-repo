---
id: cpp.mod.core
slot: mechanism
domain: generic-cpp
title: core 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/core.h:1
module: core
header: include/fmt/core.h
links:
- to: cpp.tst.assert_test.fail
  type: verified_by
  weight: 0.5
- to: cpp.tst.assert_test.dangling_else
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_tm
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.grow_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.local_time
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.tm
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.format_precision_q
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_width_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.invalid_colons
  type: verified_by
  weight: 0.5
- to: cpp.tst.chrono_test.glibc_extensions
  type: verified_by
  weight: 0.5
- to: cpp.tst.string_view_test.value_type
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.noncopyable
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.nonmoveable
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.indestructible
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.access
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.try_resize
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.try_resize_partial
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.clear
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.append
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.append_partial
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffer_test.append_allocates_enough_storage
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.is_locking
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.is_output_iterator
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.is_back_insert_iterator
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.char_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.pointer_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.arg_test.volatile_pointer_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.constexpr_parse_format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.constexpr_parse_format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.formattable_concept
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.no_implicit_conversion_to_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_explicitly_convertible_to_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.no_implicit_conversion_to_std_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_explicitly_convertible_to_std_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.has_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.is_contiguous
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.format_context_accessors
  type: verified_by
  weight: 0.5
- to: cpp.tst.util_test.parse_nonnegative_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.constexpr_grow
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_ctor_inline_buffer
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.move_ctor_dynamic_buffer
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
- to: cpp.tst.memory_buffer_test.grow
  type: verified_by
  weight: 0.5
- to: cpp.tst.memory_buffer_test.exception_in_deallocate
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.exception_from_lib
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.unmatched_braces
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.arg_errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.named_arg
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.auto_arg_index
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
- to: cpp.tst.format_test.runtime_precision
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_bool
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_int
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_char
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_pointer
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_custom
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.format_examples
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.formatted_size
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
- to: cpp.tst.module_test.format_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat_to
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vformat_to_n
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.vprint
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.locale
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.no_builtin_types_test.double_is_custom_type
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.format_specs
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.thread_id
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code_truncated_alignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.exception_align
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.format_unique_ptr
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format
  type: verified_by
  weight: 0.5
- to: cpp.tst.format_test.wide_format_to_n_runtime
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.sign_not_truncated
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
- to: cpp.tst.locale_test.int_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.locale_test.sign
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/core.h:1
  note: 公共头文件
---

## 模块
`core`，头文件 `include/fmt/core.h`。

由 cpp_static 按头文件粒度抽取，验证用例 104 个。
