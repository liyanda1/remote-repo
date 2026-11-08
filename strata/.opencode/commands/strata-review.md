---
description: 列出待确认的草稿卡片，逐条让我裁决
---

列出所有由模型生成、还没被确认的卡片：

!`python .opencode/skills/strata/scripts/strata-run.py drafts`

!`python .opencode/skills/strata/scripts/strata-run.py stat`

## 怎么做

1. 按 `source` 分组：`llm-proposal` 一组、`extractor` 一组。
   `extractor` 那组是从代码/测试抽出来的，一般直接确认就行，不用逐张念。

2. 对 `llm-proposal` 逐条汇报，每条给三样东西：
   - 一句话说这张卡讲什么
   - 它连到了哪些已有节点（`links` 里的 `to`）
   - **你有多确定**：支撑证据是文档原文、代码调用，还是纯推测

3. 每条我给出「确认 / 改 / 删」之后：
   - 确认 → 改 `status: confirmed`；若依据是代码证据，同时把 `confidence` 升到 `certain`
   - 改 → 按我说的改，保持 `proposed`，下次再review
   - 删 → 删掉卡片文件，并检查有没有别的卡片指向它（否则会产生悬空 link）

4. 全部处理完，重新编译：

!`python .opencode/skills/strata/scripts/strata-run.py compile`

编译失败说明删卡时留下了悬空 link，按报错逐个修。

## 收尾：把下一步交给用户

!`python .opencode/skills/strata/scripts/strata-run.py next`

回答的最后一行必须写清楚下一条命令，例如：
「接下来跑 `/strata-fill`：还剩 N 处结构空洞，最该补的是 H3。」
命令和数字以上面 `next` 的输出为准。

## 注意

一次别超过 15 张。超过就先问我要不要分批。
**你自己不能把任何卡片改成 `confirmed`**——这个状态只能由我给。
