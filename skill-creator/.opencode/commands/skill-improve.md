# /skill-improve — 基于 Eval 结果改进 Skill

根据用户反馈和 benchmark 数据改进 skill。

## 前提

skill-creator 部署路径（取实际存在的那个）：
- 全局：`~/.config/opencode/skills/skill-creator/`
- 项目级：`<项目根目录>/.opencode/skills/skill-creator/`

> **执行前，必须先确认 skill-creator 的实际部署路径。** 用该路径替换下文所有 `$SKILL_DIR`。

## 参数

- `$SKILL_PATH`：skill 目录路径（必需）
- `$FEEDBACK`：用户反馈内容（可选，从对话中获取）

## 执行步骤

### 1. 读取当前状态

- 读取最新 `iteration-N/` 下的 `benchmark.json` 和 `feedback.json`
- 如果用户在对话中直接提供了反馈，优先使用对话中的反馈

### 2. 分析反馈

聚焦有具体反馈的测试用例。空反馈 = 用户满意，忽略。

### 3. 改进 Skill

按照改进原则修改 SKILL.md：
1. **从反馈中泛化**：不针对单个用例修修补补，理解根本原因
2. **保持精简**：删掉没用的部分，读 transcript 看是否有浪费
3. **解释 why**：用理论心智替代大写 MUST/NEVER
4. **提取重复模式**：如果多个测试用例都写了相同的辅助脚本，把它放进 `scripts/`

### 4. 重新评估

在 `iteration-N+1/` 下重跑所有测试用例（参考 `/skill-eval` 流程）。

### 5. 对比

用 `--previous-workspace` 生成对比审阅报告：
```bash
python3 $SKILL_DIR/eval-viewer/generate_review.py <workspace>/iteration-N+1 \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N+1/benchmark.json \
  --previous-workspace <workspace>/iteration-N \
  --static <workspace>/iteration-N+1/review.html
```

### 6. 循环

告知用户新的审阅报告路径，等待反馈。
重复直到用户满意或无实质性进展。
