---
description: 扫描知识库空洞并逐个向用户提问补全
---
1. 调 `find_holes`，拿到按严重度排序的空洞列表。
2. 一次只问一个空洞，按 `packs/<domain>/domain.yaml` 里 `elicitation` 的模板措辞提问。
3. 用户回答后：
   - 按 `cards/` 的 frontmatter 格式新建或修改卡片
   - `source` 填 `user-answer`，`confidence` 填 `likely`，`status` 填 `proposed`
   - `evidence` 里写上 `conversation:<日期>#<轮次>`
4. 改完提示用户执行 `python strata.py compile` 重新编译。

**禁止**：用户没回答的字段留空即可，不许自己填默认值；不许把 `status` 直接写成 `confirmed`。
