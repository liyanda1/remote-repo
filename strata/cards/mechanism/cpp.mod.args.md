---
id: cpp.mod.args
slot: mechanism
domain: generic-cpp
title: args 模块
status: confirmed
confidence: certain
source: extractor
source_ref: include/fmt/args.h:1
module: args
header: include/fmt/args.h
links:
- to: cpp.tst.args_test.size
  type: verified_by
  weight: 0.5
- to: cpp.tst.base_test.throw_in_buffer_dtor
  type: verified_by
  weight: 0.5
evidence:
- ref: include/fmt/args.h:1
  note: 公共头文件
---

## 模块
`args`，头文件 `include/fmt/args.h`。

由 cpp_static 按头文件粒度抽取，验证用例 2 个。
