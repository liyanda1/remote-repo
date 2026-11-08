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

`weight` 是 0–1 的覆盖强度：1.0 表示确定覆盖，0.5 以下表示只沾到边。

## 四个槽位的卡片该写什么

**intent（场景 / 能力）** —— 少而重，人工维护。

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
设备在 FLASHING 阶段掉电，下次上电必须走回滚，不能继续刷写。
```

**mechanism（功能 / 机制）** —— 领域形态的核心，唯一键由包的 `mechanism_key` 决定。

```markdown
---
id: ota.tr.flashing-power-lost
slot: mechanism
domain: ota
title: FLASHING + POWER_LOST → 回滚
status: confirmed
confidence: certain
source: extractor
state: FLASHING
event: POWER_LOST
guard: ""
links:
  - { to: ota.tst.power_loss_ut, type: verified_by }
---
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
