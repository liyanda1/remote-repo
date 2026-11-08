---
description: 查看知识库现状：规模、分布、空洞、缺口
---

!`python .opencode/skills/strata/scripts/strata-run.py where`

!`python .opencode/skills/strata/scripts/strata-run.py stat`

!`python .opencode/skills/strata/scripts/strata-run.py holes`

## 汇报要求

1. **规模**：四层各多少节点，和上次比是涨是跌（不知道上次数字就直接说不知道）。
2. **健康度**：三类空洞的数量与占比，重点看 `H3`（用例没映射到代码）的比例。
   超过 30% 说明静态匹配到了召回上限，提示我需要接覆盖率报告。
3. **缺口**：未闭合缺口数量，以及最老的几条挂了多久。
4. **一句话判断**：这个库现在能不能用、最大的短板是什么。

## 收尾

!`python .opencode/skills/strata/scripts/strata-run.py next`

不要罗列所有空洞明细，只要分布和最该补的三条，最后一行给出下一步命令。
