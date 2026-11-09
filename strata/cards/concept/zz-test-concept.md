---
id: cpp.cpt.format-string
slot: concept
domain: generic-cpp
title: 格式字符串
status: proposed
confidence: likely
source: llm-proposal
tags: [格式化, 语法]
links:
  - { to: cpp.cap.date_and_time_formatting, type: explains }
---
格式字符串描述输出文本的模板：字面字符原样输出，替换域以 { 开头 } 结尾。
最简单的用法是 fmt::format("{}", 42)，运行期按参数类型替换。占位符支持位置索引 {0}、
命名参数 {name}，以及格式规格 {:+.2f}。本库所有能力都围绕「编译期检查 + 运行期替换」展开。
