---
description: 初始化 Strata 知识库（抽取代码 + 编译索引 + 撰写场景卡）
---

先看现状，不要盲目重建：

!`python .opencode/skills/strata/scripts/strata-run.py where`

**如果「节点 / 边」不是 0**：说明库已经建过，直接把上面的自检结果复述给我并停下，
不要重复初始化。要重建请显式说「重新抽取」。

目标仓库：$ARGUMENTS
（留空表示当前目录；也可以写成 `/path/to/repo --home /path/to/strata`，
`--home` 临时指定知识库工程位置，不用改任何配置。）

## 执行步骤

1. 读一眼仓库结构：构建文件（CMakeLists.txt / BUILD / meson.build）、测试目录、
   README 与 doc/ 下的设计文档。**这一步不许跳过**，后面的判断全靠它。

2. 抽取并编译：

!`python .opencode/skills/strata/scripts/strata-run.py extract $ARGUMENTS`

!`python .opencode/skills/strata/scripts/strata-run.py compile`

3. 把编译输出原样贴给我：按槽位、按边类型、按置信度三行，加一行校验结论。
   如果报了校验错误，**先修卡片格式**，不许改校验逻辑绕过。

4. 抽一张生成的用例卡，把它的 `evidence.ref` 拿去和源码核对，确认行号真的对得上。
   核对完告诉我结论（对得上 / 差几行 / 内容不符）。

5. 最后问我：要读哪些文档来写场景卡和概念卡？我会给路径，你一次最多生成 12 张草稿卡，
   正文按 card-format.md 的模板写全（背景/触发/主流程/边界），不许只写结构字段。

## 收尾：把下一步交给用户

!`python .opencode/skills/strata/scripts/strata-run.py next`

回答的最后一行必须照这个格式写：
「接下来跑 `/strata-review`：有 N 张草稿卡等你裁决。」
（具体命令和数字以上面 `next` 的输出为准，不要自己判断。）

## 写卡片之前

必须先读 `.opencode/skills/strata/references/card-format.md`。
最容易犯的三个错：把边写进正文而不是 `links`、`status` 写了 `confirmed`、
引用了不存在的 `to` 导致悬空 link。
