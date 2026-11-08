---
description: 扫描知识库空洞，逐条提问补全，并把答案写回卡片
---

当前空洞：

!`python .opencode/skills/strata/scripts/strata-run.py holes`

## 补全流程（一次只处理一条）

选**严重度最高、且数量最少**的那一类开始，不要一次铺开。

对选中的空洞：

1. 从输出的清单里取一条，念给我看：哪个节点、缺什么。
2. 按 `references/card-format.md` 里的领域问法提问。
   包里没有模板就用通用问法，**只问一个问题**，别一次问五个。
3. 等我回答后：
   - 改对应卡片（补 `links` / 补正文 / 改 `status` 到 `proposed`）
   - 若答案来自我，标 `source: user-answer`、`confidence: likely`
   - 重新编译：`python .opencode/skills/strata/scripts/strata-run.py compile`
   - 再跑一次 `holes`，确认这一条消失了
4. 告诉我「这一类还剩几条」，然后问我要不要继续。

## 收尾：把下一步交给用户

!`python .opencode/skills/strata/scripts/strata-run.py next`

回答的最后一行按 `next` 的输出写：要么「继续 `/strata-fill`，还剩 N 处」，
要么「空洞已清到可接受范围，改代码前用 `/strata-impact`」。

## 铁律

- **查不到就登记缺口，不许编造**：

!`python .opencode/skills/strata/scripts/strata-run.py gap list`

  需要登记时用 `gap add --hole <id> --question "<问题>" --context "<上下文>"`。

- `H4-unsourced-edge` 不许绕过：缺证据的边要么补 `evidence`，要么删掉。
- 不要为了让空洞消失而删节点。删掉的应该是错的东西，不是难补的东西。
- 一次改完就编译，不要攒着改十几张再编译——出错时定位不到是哪张卡的问题。
