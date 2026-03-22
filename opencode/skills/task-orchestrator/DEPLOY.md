# Task Orchestrator 部署与使用指南

## 功能介绍

Task Orchestrator 是一个专为内网OpenCode环境设计的任务编排工具，解决模型能力受限时长任务执行困难的问题。

### 核心能力

1. **长任务后台执行** - 主Agent调用OpenCode subAgent在后台执行任务，不阻塞主会话
2. **任务分点执行** - 将复杂任务拆分为多个小步骤，逐步执行，每步可人工确认
3. **实时监控** - 主Agent可随时查看subAgent执行状态和进度
4. **失败重试** - 单步骤失败可单独重试，避免整任务重来
5. **临时文件管理** - 支持自动/手动/保留三种清理策略，不污染项目目录

### 适用场景

- 代码重构涉及多个文件
- 生成大型文档或报告
- 批量数据处理
- 复杂多步骤开发任务
- 内网模型能力受限，需要拆分任务逐步执行

---

## 快速部署（推荐）

### 方式一：项目级部署（仅当前项目使用）

```bash
# 1. 进入你的项目根目录
cd your-project/

# 2. 创建OpenCode配置目录
mkdir -p .opencode/agents/
mkdir -p .opencode/skills/

# 3. 复制skill文件
cp -r /path/to/task-orchestrator .opencode/skills/

# 4. 复制subAgent配置
cp .opencode/skills/task-orchestrator/agents/executor.md .opencode/agents/

# 5. 完成！重启OpenCode生效
```

### 方式二：全局部署（所有项目可用）

```bash
# 1. 创建全局配置目录
mkdir -p ~/.config/opencode/agents/
mkdir -p ~/.config/opencode/skills/

# 2. 复制skill文件
cp -r /path/to/task-orchestrator ~/.config/opencode/skills/

# 3. 复制subAgent配置
cp ~/.config/opencode/skills/task-orchestrator/agents/executor.md ~/.config/opencode/agents/

# 4. 完成！重启OpenCode生效
```

---

## 验证部署

### 1. 检查subAgent是否加载

在OpenCode中输入 `@` 应该能看到 `executor` 选项。

### 2. 检查skill是否可用

在OpenCode中提问关于任务编排的问题，应该能触发task-orchestrator skill。

### 3. 测试执行

```bash
# 创建测试计划
python3 .opencode/skills/task-orchestrator/scripts/create-plan.py \
  --task "测试任务" --steps 2

# 检查状态
python3 .opencode/skills/task-orchestrator/scripts/status.py
```

---

## 使用教程

### 第一步：创建任务计划

```bash
python3 .opencode/skills/task-orchestrator/scripts/create-plan.py \
  --task "重构用户认证模块" \
  --steps 5
```

输出示例：
```
✅ 任务计划已创建
   任务ID: a1b2c3d4
   步骤数: 5

使用方式:
   1. 调用 @executor 执行步骤
   2. 检查状态: python3 scripts/status.py
```

### 第二步：执行步骤

在OpenCode对话中调用subAgent：

```
@executor 执行步骤1，计划文件: ./.orchestrator/plans/task-a1b2c3d4.json
```

或使用快捷键 `<Leader>+Right` 进入subAgent会话直接执行。

### 第三步：监控状态

```bash
# 查看任务状态
python3 .opencode/skills/task-orchestrator/scripts/status.py
```

输出示例：
```
============================================================
📋 任务: 重构用户认证模块
🆔 任务ID: a1b2c3d4
📅 创建时间: 2026-03-22T10:00:00
============================================================

📊 整体进度: 1/5 (20.0%)
📌 整体状态: 🔄 running

📋 步骤详情:
  ✅ 步骤 1: 分析现有代码 - success (耗时 5分30秒)
  ⏳ 步骤 2: 设计策略接口 - pending
  ⏳ 步骤 3: 迁移调用 - pending
  ⏳ 步骤 4: 删除旧代码 - pending
  ⏳ 步骤 5: 测试验证 - pending

💡 下一步:
------------------------------------------------------------
   ⏭️  执行下一步 (步骤 2):
      @executor 执行步骤2
============================================================
```

### 第四步：继续执行

步骤1完成后，继续执行步骤2：

```
@executor 执行步骤2
```

或使用脚本：
```bash
python3 .opencode/skills/task-orchestrator/scripts/next.py
```

### 第五步：清理临时文件（可选）

任务全部完成后，清理临时文件（存储在 `~/.config/opencode/task-orchestrator/`）：

```bash
# 清理已完成的任务
python3 .opencode/skills/task-orchestrator/scripts/cleanup.py

# 清理所有任务数据
python3 .opencode/skills/task-orchestrator/scripts/cleanup.py --all
```

**注意**：临时文件存储在用户目录下，不会污染项目目录。

---

## 完整示例：代码重构

### 场景
需要将单体AuthService重构为策略模式。

### 执行流程

**1. 创建5步骤计划**
```bash
python3 scripts/create-plan.py \
  --task "重构认证模块：1)分析代码 2)设计接口 3)迁移调用 4)删除旧代码 5)测试验证" \
  --steps 5
```

**2. 执行步骤1（分析代码）**
```
用户: @executor 执行步骤1，分析AuthService现有代码，识别可提取的策略

subAgent: 正在分析 src/services/AuthService.java...
          识别出以下责任：
          - 用户登录验证
          - Token生成
          - 权限检查
          - 密码加密
          分析完成，结果已输出到代码注释中
```

**3. 检查状态并继续**
```bash
python3 scripts/status.py
# 显示步骤1完成，提示执行步骤2
```

**4. 执行步骤2-5**
逐个执行剩余步骤，每步完成后检查状态。

**5. 完成清理**
```bash
python3 scripts/cleanup.py --force
```

---

## 临时文件管理（用户无感知）

### 存储位置

所有临时文件自动存储在 `~/.config/opencode/task-orchestrator/` 目录下：

```
~/.config/opencode/task-orchestrator/
├── plans/                  # 任务计划文件
│   └── task-{id}.json
├── logs/                   # 执行日志（调试用）
│   └── step-{n}.log
└── state/                  # 状态文件
    └── current.json
```

**用户完全无感知**，不会污染项目目录。

### 清理策略

创建计划时可指定清理策略：

```bash
# 自动清理（默认）- 任务完成后自动删除临时文件
python3 scripts/create-plan.py --task "xxx" --steps 3 --cleanup auto

# 手动清理 - 任务完成后用户手动删除
python3 scripts/create-plan.py --task "xxx" --steps 3 --cleanup manual

# 保留模式 - 保留所有文件供审计
python3 scripts/create-plan.py --task "xxx" --steps 3 --cleanup keep
```

### 清理命令

```bash
# 清理已完成的任务（保留进行中的任务）
python3 scripts/cleanup.py

# 清理所有任务数据
python3 scripts/cleanup.py --all

# 强制清理（不提示确认）
python3 scripts/cleanup.py --all --force
```

**注意**：执行结果（代码、文档等）直接输出到项目目录，不存放在临时目录中。

---

## 配置说明

### 可选：配置主Agent权限

在项目根目录创建 `.opencode/opencode.json`：

```json
{
  "agent": {
    "build": {
      "permission": {
        "task": {
          "executor": "allow"
        }
      }
    }
  }
}
```

### 可选：自定义executor配置

编辑 `.opencode/agents/executor.md`：

```yaml
---
description: "任务执行子代理"
mode: subagent
model: default
temperature: 0.3
tools:
  write: true
  edit: true
  bash: true
---

# 自定义系统提示词...
```

---

## 目录结构验证

部署完成后，项目结构应该是：

```
your-project/
├── .opencode/
│   ├── agents/
│   │   └── executor.md          # subAgent配置
│   └── skills/
│       └── task-orchestrator/   # skill目录
│           ├── SKILL.md
│           ├── scripts/
│           └── ...
└── ...
```

---

## 快捷键参考

| 快捷键 | 功能 |
|--------|------|
| `<Leader>+Right` | 进入子Agent会话 |
| `<Leader>+Left` | 返回父会话 |
| `<Leader>+Down` | 进入第一个子会话 |
| `Tab` | 在Primary Agents间切换 |
| `@` | 显示subAgent列表 |

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `create-plan` | 创建任务计划（`--cleanup auto/manual/keep`） |
| `status` | 查看任务状态 |
| `next` | 执行下一步（分点模式） |
| `cleanup` | 清理临时文件（`--force` 强制清理） |

---

## 卸载

```bash
# 项目级卸载
rm -rf .opencode/skills/task-orchestrator
rm .opencode/agents/executor.md

# 全局卸载
rm -rf ~/.config/opencode/skills/task-orchestrator
rm ~/.config/opencode/agents/executor.md
```

---

## 常见问题

### Q: subAgent没有显示
A: 检查executor.md是否在agents目录，重启OpenCode

### Q: skill没有触发
A: 确保SKILL.md在skills/task-orchestrator/目录下

### Q: 权限错误
A: 检查.orchestrator目录是否有写权限

### Q: 任务执行卡住
A: 使用 `<Leader>+Right` 切换到subAgent会话查看实时进度

### Q: 如何查看subAgent执行详情
A: 使用快捷键进入subAgent会话，或查看 `.orchestrator/logs/step-{n}.log`

---

## 最佳实践

1. **任务拆分粒度**：每个步骤控制在5-15分钟内完成
2. **及时清理**：任务完成后及时清理临时文件，避免积累
3. **分点确认**：复杂任务建议使用分点模式，每步完成后人工确认
4. **状态检查**：长任务执行期间定期使用status.py检查进度
5. **日志调试**：遇到问题时查看 `.orchestrator/logs/` 中的日志
