---
id: cpp.mod.ostream
slot: mechanism
domain: generic-cpp
title: ostream 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/ostream.h:1
module: ostream
header: include/fmt/ostream.h
links:
- to: cpp.tst.module_test.namespace
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.macros
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.print
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.formatter
  type: verified_by
  weight: 0.5
- to: cpp.tst.module_test.printf
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
- to: cpp.tst.ostream_test.write_to_ostream
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.write_to_ostream_max_size
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.streamed
  type: verified_by
  weight: 0.5
- to: cpp.tst.ostream_test.closed_ofstream
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.format_explicitly_convertible_to_wstring_view
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.is_formattable
  type: verified_by
  weight: 0.5
- to: cpp.tst.xchar_test.streamed
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/ostream.h:1
  note: 公共头文件
---

## 模块
`ostream`，头文件 `include/fmt/ostream.h`。

由 cpp_static 按头文件粒度抽取，验证用例 16 个。
