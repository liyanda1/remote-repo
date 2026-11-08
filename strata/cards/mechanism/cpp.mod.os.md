---
id: cpp.mod.os
slot: mechanism
domain: generic-cpp
title: os 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/os.h:1
module: os
header: include/fmt/os.h
links:
- to: cpp.tst.format_test.locking_formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.failed_expect_throw_msg
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.failed_expect_system_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.exception_tests
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.system_error_tests
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.failed_expect_write
  type: verified_by
  weight: 0.5
- to: cpp.tst.single_evaluation_test.write_tests
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_write_streaming
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_throw_no_unreachable_code_warning
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_throw_behaves_like_single_statement
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_system_error_behaves_like_single_statement
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_write_behaves_like_single_statement
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_throw_msg
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_throw_msg_streaming
  type: verified_by
  weight: 0.5
- to: cpp.tst.gtest_extra_test.expect_system_error_streaming
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.scoped_redirect
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.flush_error_in_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.restore_and_read
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.flush_error_in_restore_and_read
  type: verified_by
  weight: 0.5
- to: cpp.tst.output_redirect_test.error_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.errors
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.error_code
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.output_file
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
- to: cpp.tst.file_test.open_windows_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.default_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_assignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_assignment_closes_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_from_temporary_in_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_from_temporary_in_assignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.move_from_temporary_in_assignment_closes_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close_file_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close_error_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.descriptor
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.move
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.move_while_holding_data
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.buffer_boundary
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.buffer_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.zero_buffer_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.truncate
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.flush
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.default_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.open_buffered_file_in_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.open_buffered_file_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_assignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_assignment_closes_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_from_temporary_in_ctor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_from_temporary_in_assignment
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.move_from_temporary_in_assignment_closes_file
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close_file_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close_error_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.read
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.read_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.write
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.write_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2_noexcept
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2_noexcept_error
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.pipe
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.fdopen
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.line_buffering
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.buffer_boundary
  type: verified_by
  weight: 0.5
- to: cpp.tst.os_test.getpagesize
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.open_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close_no_retry_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.close_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.size
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.max_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.read_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.write_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.convert_read_count
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.convert_write_count
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.dup2_no_except_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.pipe_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.file_test.fdopen_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.open_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close_no_retry_in_dtor
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.close_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.buffered_file_test.fileno_no_retry
  type: verified_by
  weight: 0.5
- to: cpp.tst.scoped_mock.scope
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_text
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_long_long
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_uint
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_ulong_long
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_floats
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_double_whitespace
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_string
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_string_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.separator
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.read_custom
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.invalid_format
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.example
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.end_of_input
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.file
  type: verified_by
  weight: 0.5
- to: cpp.tst.scan_test.lock
  type: verified_by
  weight: 0.5
- to: cpp.tst.std_test.error_code
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/os.h:1
  note: 公共头文件
---

## 模块
`os`，头文件 `include/fmt/os.h`。

由 cpp_static 按头文件粒度抽取，验证用例 108 个。
