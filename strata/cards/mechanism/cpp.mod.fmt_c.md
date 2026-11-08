---
id: cpp.mod.fmt_c
slot: mechanism
domain: generic-cpp
title: fmt-c 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/fmt-c.h:1
module: fmt-c
header: include/fmt/fmt-c.h
links:
- to: cpp.tst.arg_test.format_args
  type: verified_by
  weight: 0.5
- to: cpp.tst.no_builtin_types_test.double_is_custom_type
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/fmt-c.h:1
  note: 公共头文件
---

## 模块
`fmt-c`，头文件 `include/fmt/fmt-c.h`。

由 cpp_static 按头文件粒度抽取，验证用例 2 个。
