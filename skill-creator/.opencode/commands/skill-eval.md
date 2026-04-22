# /skill-eval — 执行 Skill 测试评估

对指定 skill 运行测试用例，生成 benchmark 和审阅报告。

## 前提

skill-creator 部署路径（取实际存在的那个）：
- 全局：`~/.config/opencode/skills/skill-creator/`
- 项目级：`<项目根目录>/.opencode/skills/skill-creator/`

> **执行前，必须先确认 skill-creator 的实际部署路径。** 用该路径替换下文所有 `$SKILL_DIR`。

## 参数

- `$SKILL_PATH`：待评估的 skill 目录路径（必需）

## 执行步骤

### 1. 加载 skill 和测试用例

- 读取 `$SKILL_PATH/SKILL.md`
- 读取 `$SKILL_PATH/evals/evals.json`（如果存在）
- 如果没有 evals.json，提示用户先创建测试用例或使用 `/skill-create`

### 2. 创建 workspace

在 skill 同级创建 `<skill-name>-workspace/iteration-N/` 目录。

### 3. 串行执行测试用例

对每个 eval：
1. **with_skill**：按照 skill 指示执行 prompt，保存输出到 `eval-<ID>/with_skill/outputs/`
2. **baseline**：不加载 skill 执行同一 prompt，保存到 `eval-<ID>/without_skill/outputs/`
3. 写入 `eval_metadata.json`（prompt + assertions）
4. 记录执行时间到 `timing.json`

### 4. 评分

读取 `$SKILL_DIR/agents/grader.md` 模板，内联应用：
- 逐条判定 expectation：PASS/FAIL + evidence
- 提取隐性 claims 并验证
- 批判 eval 本身的弱点
- 写入 `grading.json`

### 5. 聚合 benchmark

```bash
python3 $SKILL_DIR/scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
```

### 6. 分析

读取 `$SKILL_DIR/agents/analyzer.md` 模板，内联分析 benchmark 数据：
- 识别无区分力的断言
- 识别高方差 eval
- 分析时间/token 权衡
- 写入 `benchmark.json` 的 `notes` 字段

### 7. 生成审阅报告

```bash
python3 $SKILL_DIR/eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  --static <workspace>/iteration-N/review.html
```

### 8. 交付

告知用户审阅报告路径，请其在浏览器中打开。
