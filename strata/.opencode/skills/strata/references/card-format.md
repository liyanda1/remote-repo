# 卡片格式

卡片是事实源。**写错格式就编译不过**，编译器会明确告诉你哪张卡哪个字段有问题。

## 结构

```markdown
---
id: cpp.tst.base_test.format_to     # 必填，全局唯一
slot: verification                  # 必填，四个槽位之一
domain: generic-cpp                 # 必填，所属领域包
title: base_test.format_to          # 必填，显示名
status: confirmed                   # 必填，draft|proposed|confirmed|disputed
confidence: likely                  # 必填，certain|likely|possible
source: extractor                   # 必填，extractor|manual|user-answer|llm-proposal
source_ref: test/core-test.cc:698   # 选填，但强烈建议填
links:                              # 选填，这就是「边」
  - { to: cpp.mod.core, type: verified_by, weight: 1.0 }
evidence:                           # 选填，边的证据
  - { ref: "test/core-test.cc:698", note: "TEST(base_test, format_to)" }
# 下面是领域包声明的业务字段，不同包不一样
suite: base_test
case: format_to
file: test/core-test.cc
line: 698
---

正文：写给人和模型看的说明。这里的 `[[双链]]` 只是路标，编译器不认。
```

## 必填字段

`id`、`slot`、`domain`、`title`、`status`、`confidence`、`source` —— 缺一个就报错。

## 边的合法组合

槽位决定能用哪种边，写错方向会被直接拒绝：

| 起点槽位 | 终点槽位 | 只能用这个边 |
|---|---|---|
| `intent` | `mechanism` | `composed_of` |
| `intent` | `intent` | `fulfills` |
| `mechanism` | `verification` | `verified_by` |
| `verification` | `implementation` | `exercises` |
| `implementation` | `implementation` | `depends_on` |
| `concept` | `intent` / `mechanism` | `explains` |
| `concept` | `concept` | `related_to` |

`weight` 是 0–1 的覆盖强度：1.0 表示确定覆盖，0.5 以下表示只沾到边。

## 正文必须写业务知识（这是知识库的价值所在）

frontmatter 只负责「连得上」，正文负责「看得懂」。
**只有结构字段（type/weight/状态）没有业务内容的卡，编译器会报「正文过薄」警告**——
这样的卡片检索不到任何知识，等于没写。三类卡的正文模板：

**intent（场景卡）正文模板** —— 每节 1–3 句，写完通常 150–400 字：

```markdown
## 背景
谁在什么条件下需要这个能力；为什么要存在这个场景。

## 触发
入口是什么（信号 / 请求 / 命令 / 用户操作），前置条件有哪些。

## 主流程
正常情况下系统做什么，分几步。

## 边界与异常
哪些情况要特殊处理（超时、掉电、并发、参数非法），各自的行为是什么。
```

**mechanism（功能点卡）正文模板**：

```markdown
## 职责
这个功能点负责什么、不负责什么（边界写清楚，防止和相邻功能点混淆）。

## 工作方式
状态转移 / 服务序列 / 算法步骤，按本领域的形态写。

## 输入 / 输出
吃什么、吐什么、和谁交互。

## 上下游
上游依赖谁（含不在本仓的），下游被谁使用。
```

**concept（概念页）正文模板** —— 写给「新人 + 模型」看的背景知识：

```markdown
## 是什么
一句话定义，再加展开。

## 为什么重要
不理解它会在本领域犯什么错。

## 常见误区
容易混淆的点，和正确理解的差别。
```

verification / implementation 由抽取器生成，正文不强制（它们的价值在证据链不在叙述）。

## 五个槽位的卡片该写什么

**intent（场景 / 能力）** —— 少而重，人工维护。正文必须按上面的模板写全。

```markdown
---
id: ota.scn.power-loss-recovery
slot: intent
domain: ota
title: 刷写中断电后恢复
status: proposed
confidence: likely
source: user-answer
links:
  - { to: ota.tr.flashing-power-lost, type: composed_of, weight: 1.0 }
---
## 背景
车辆在 FLASHING 阶段可能意外断电（事故、低压保护、人为拔电）。
## 触发
下次上电自检发现升级标记未清除。
## 主流程
读回滚区标志 → 校验旧镜像完整性 → 走回滚流程 → 上报云端失败原因。
## 边界与异常
回滚区也损坏时进入安全模式；断电发生在校验段则可续刷，不需要回滚。
```

**mechanism（功能点）** —— 领域形态的核心，唯一键由包的 `mechanism_key` 决定。
正文按模板写职责与工作方式。

**concept（概念页）** —— 可选的背景知识层。业务术语多、新人上手难的领域才需要；
一张概念页通过 `explains` 连到它解释的场景/功能点。

```markdown
---
id: ota.cpt.rollback
slot: concept
domain: ota
title: 回滚（Rollback）
status: proposed
confidence: likely
source: manual
links:
  - { to: ota.scn.power-loss-recovery, type: explains }
---
## 是什么
升级失败时把 ECU 恢复到上一个可用版本机制的统称，靠 A/B 分区或备份区实现。
## 为什么重要
车规场景不允许变砖，回滚是所有刷写流程的兜底分支。
## 常见误区
回滚不是「重试升级」，是恢复旧版本；两者状态机路径完全不同。
```

**verification（IT / UT）** —— 可由测试代码批量生成，正文写清这个用例断言什么。

**implementation（代码符号）** —— **不要手写**，由抽取器生成。人工只在需要补
`depends_on` 边时才碰它。

## 五个最常见的错误

| 错误 | 现象 | 正确做法 |
|---|---|---|
| 边写进正文 | 编译通过但图里没有这条边 | 边只能写在 `frontmatter.links` |
| `to` 指向不存在的 id | 报「悬空 link」，整次编译失败 | 先 `grep` 卡片目录确认 id 存在 |
| 模型自己写 `status: confirmed` | 查询会把推测当事实 | 模型上限是 `proposed` |
| 加了包没声明的字段 | 报「未知字段」 | 要么去掉，要么在包里声明 |
| 同名函数当成一个 | 影响面指向错误的文件 | 抽取器已按名字合并 + `locations` 记录多个位置 |

## 校验

```bash
python .opencode/skills/strata/scripts/strata-run.py compile
```

输出三段分布 + 一行结论。**任何 error 都不能跳过**，warning 可以攒着一起看。
