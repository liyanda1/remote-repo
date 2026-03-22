---
name: task-orchestrator
description: "任务编排器 - 用于管理长任务的后台执行。当用户需要执行复杂多步骤任务、长耗时任务、或需要分步确认的任务时，使用此skill。支持调用OpenCode subAgent后台执行、任务拆分、状态监控、失败重试。适用于内网部署模型能力受限场景。"
description_zh: "长任务后台执行与监控编排器"
description_en: "Long-running task orchestrator with subAgent support"
allowed-tools: Bash,Read,Write,Glob,Grep,Task
---

# Task Orchestrator - 任务编排器

## 何时使用我

- 用户要求执行**复杂多步骤任务**（如代码重构、大型文档生成）
- 任务**耗时较长**，需要后台执行不阻塞主会话
- 需要**分步执行**，每步完成后人工确认
- 内网模型能力受限，需要**拆分任务**逐步执行
- 用户提到"分步骤"、"逐步"、"后台执行"、"任务编排"等关键词

## 核心能力

1. **任务拆分** - 将复杂任务拆分为多个小步骤
2. **后台执行** - 调用 @executor subAgent 在后台执行步骤
3. **状态监控** - 实时查看任务执行状态和进度
4. **失败重试** - 单步骤失败可重试，不中断整体流程

## 工作流程

### 1. 创建任务计划

使用脚本创建结构化任务计划：

```bash
python3 .opencode/skills/task-orchestrator/scripts/create-plan.py \
  --task "任务描述" \
  --steps 步骤数量
```

### 2. 执行步骤

调用 executor subAgent 执行指定步骤：

```
@executor 执行步骤1
```

### 3. 监控状态

```bash
python3 .opencode/skills/task-orchestrator/scripts/status.py
```

### 4. 继续执行

步骤完成后，继续下一步：

```
@executor 执行步骤2
```

或使用：

```bash
python3 .opencode/skills/task-orchestrator/scripts/next.py
```

## 任务状态流转

```
[待执行] → [执行中] → [成功] → [完成]
              ↓
           [失败] → [重试]
```

## 最佳实践

1. **任务拆分**：每个步骤控制在5-15分钟内完成
2. **执行顺序**：按步骤顺序执行，不要跳过
3. **状态检查**：长任务期间定期使用 status.py 检查进度
4. **失败处理**：步骤失败时分析原因，可重试或调整计划
5. **结果输出**：执行结果直接写入项目目录，不生成额外文档

## 示例对话

**用户**: 帮我重构这个认证模块，分步骤执行

**Agent**:
```
我来帮你分步骤重构认证模块。

步骤1：创建任务计划
```bash
python3 .opencode/skills/task-orchestrator/scripts/create-plan.py \
  --task "重构认证模块" --steps 4
```

步骤2：执行第1步 - 分析现有代码
@executor 执行步骤1

步骤3：监控执行状态
```bash
python3 .opencode/skills/task-orchestrator/scripts/status.py
```

步骤4：继续执行后续步骤...
```

## 注意事项

- 临时文件自动存储在用户目录（~/.config/opencode/task-orchestrator/），不污染项目
- 任务完成后可运行 cleanup.py 清理临时数据
- 使用 `<Leader>+Right` 可进入subAgent会话查看实时执行详情
