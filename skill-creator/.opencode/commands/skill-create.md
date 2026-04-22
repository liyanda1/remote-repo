# /skill-create — 创建新 Skill

引导用户完成 skill 创建流程。

## 执行步骤

### 1. 意图捕获

了解用户想创建什么样的 skill：
- 这个 skill 要让 AI 做什么？
- 什么时候应该触发？（用户会说什么话/什么场景）
- 预期的输出格式是什么？
- 需要测试用例吗？（客观可验证输出的 skill 建议加）

### 2. 撰写 SKILL.md

根据用户意图，创建 skill 目录结构：

```
<skill-name>/
├── SKILL.md          # 必须有，YAML frontmatter + Markdown
├── scripts/          # 可选，确定性任务脚本
├── references/       # 可选，参考文档
└── assets/           # 可选，模板/图标等
```

SKILL.md frontmatter 格式：
```yaml
---
name: skill-name
description: 触发描述，包含做什么 + 何时用。要"pushy"一点。
---
```

Body 部分：imperative 风格，解释 why，< 500 行。

### 3. 编写测试用例

创建 `evals/evals.json`：
```json
{
  "skill_name": "skill-name",
  "evals": [
    {
      "id": 1,
      "prompt": "用户任务提示",
      "expected_output": "预期结果描述",
      "files": [],
      "expectations": []
    }
  ]
}
```

先写 prompt，assertions 后面补。

### 4. 交付

- 告知用户 skill 已创建
- 如果需要，引导用户到 `/skill-eval` 执行测试
