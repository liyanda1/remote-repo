---
description: 代码有较大改动后重新抽取并编译（不重建场景层）
---

!`python .opencode/skills/strata/scripts/strata-run.py where`

对 $ARGUMENTS 重新做一次增量抽取（留空表示当前目录）：

!`python .opencode/skills/strata/scripts/strata-run.py extract $ARGUMENTS`

!`python .opencode/skills/strata/scripts/strata-run.py compile`

## 你要做的判断

1. 对比这次和上次的槽位数字（上次的数字看 `git log` 或我告诉你的），指出：
   - 符号数变化 → 是否与这次代码改动规模相符
   - 用例数变化 → 是否有新测试没被识别（可能是不同测试框架）
   - 校验是否通过

2. 如果符号数**下降**，先查原因再下结论：可能是文件被删、也可能是抽取规则漏了
   新的写法（比如新引入的命名空间或宏）。

3. 重编后跑一次空洞扫描，把**新出现**的空洞列出来：

!`python .opencode/skills/strata/scripts/strata-run.py holes`

只报新增或数量变多的那几类，不要把所有空洞重念一遍。

## 收尾

!`python .opencode/skills/strata/scripts/strata-run.py next`

最后一行写明下一步该跑什么（以 `next` 的输出为准）。
如果这次抽取新增了空洞，通常就是 `/strata-fill`。
