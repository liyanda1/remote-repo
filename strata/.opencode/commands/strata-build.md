---
description: 第一次建库用这一条——抽取、编译、播种、裁决、补洞，从头走到尾
---

这是一条贯穿全流程的命令。你不需要让用户记住其它命令，只要按下面的顺序推进，
每完成一步就说清楚「做完了什么」和「下一步正在做什么」。

知识库位置（没配过就别带参数，先看自检结果）：

!`python .opencode/skills/strata/scripts/strata-run.py where`

!`python .opencode/skills/strata/scripts/strata-run.py home`

目标仓库：$ARGUMENTS（留空表示当前目录）

## 第 1 步 · 确认位置

- 如果「最终生效」是空的：让用户选一条路——要么把工程根路径告诉我（我用 `--home` 带上），
  要么跑一次 `home set <路径>` 写进本仓配置。**不要猜路径**。
- 如果索引已经存在且节点数不为 0：告诉用户库已建过，问是「继续治理」还是「重新抽取」。
  重新抽取必须由用户明确说出这四个字。

## 第 2 步 · 抽取与编译

!`python .opencode/skills/strata/scripts/strata-run.py extract $ARGUMENTS`

如果这条报「还没指定知识库工程在哪」，说明位置没配：用 bash 工具跑
`python .opencode/skills/strata/scripts/strata-run.py home set <用户给的工程根>`，
然后用同样的参数重跑这一条。**不要自己编路径。**

!`python .opencode/skills/strata/scripts/strata-run.py compile`

把三行分布（按槽位 / 按边类型 / 按置信度）和校验结论原样贴给用户。
校验报错就修卡片格式，**不许改校验逻辑绕过**。

## 第 3 步 · 抽一张卡核对证据

从 `cards/verification/` 随便挑一张，把 `evidence.ref` 里的文件和行号拿去源码里核对，
告诉用户「对得上 / 差几行 / 内容不符」。这一步是强制的：证据链不能复核，整个库就不可信。

## 第 4 步 · 播种场景层

问用户要播哪些文档（设计文档、需求、测试计划都行），然后：
- 先读 `.opencode/skills/strata/references/card-format.md`
- 一次最多 12 张，`status: draft`，`source: llm-proposal`，`confidence: possible`
- 每张卡的 `links` 必须至少连到一个已存在的 mechanism/verification 节点
- 写完跑一次 `compile`，确认没有悬空 link

## 第 5 步 · 逐张裁决（必须等用户）

把刚播的卡逐张念给用户，每条给三样：讲什么、连到哪些已有节点、你有多确定。
用户说「确认 / 改 / 删」之后改卡片，然后 `compile`。
**你自己不能把 status 改成 confirmed。**

## 第 6 步 · 交接

跑一次状态判断，把结果告诉用户，并明确写出下一条命令是什么：

!`python .opencode/skills/strata/scripts/strata-run.py next`

最后一行必须是这样一句：
「接下来跑 `/strata-fill`，因为还有 N 处空洞」或「库已经可以用，改代码前跑 `/strata-impact`」。

## 贯穿全程的三条线

- 每个 shell 块的真实输出才是依据，不许用「应该是」「一般来说」替代。
- 一次只做一步，做完就报告，不要闷头跑十步再一次性汇报。
- 任何一步拿不到确定结果，就 `gap add` 登记并问用户，不许编造。
