# OpenCode subAgent 集成详解

## OpenCode subAgent 机制

OpenCode支持两种Agent模式：

### 1. Primary Agent（主代理）
- 用户直接交互的主要助手
- 内置：`build`（默认，全功能）、`plan`（受限，只规划）
- 使用 `Tab` 键切换

### 2. Subagent（子代理）
- 专注于特定任务的专家助手
- 通过Task工具或 `@` 提及调用
- 可以创建独立的子会话，后台并行执行

## 调用方式

### 方式一：自动调用（主Agent决策）

主Agent分析任务后，自动使用Task工具调用合适的subAgent。

配置权限（在 `opencode.json` 中）：
```json
{
  "agent": {
    "build": {
      "permission": {
        "task": {
          "*": "deny",
          "executor": "allow"
        }
      }
    }
  }
}
```

### 方式二：手动调用（用户@提及）

在对话中直接@调用：
```
@executor 执行plan.json中的步骤1
```

### 方式三：在SKILL.md中调用

```markdown
请 @executor 执行以下任务：
- 计划文件: ./plan.json
- 步骤: 1
- 描述: 分析现有代码
```

## 子Agent配置

### 文件位置

- 项目级：`.opencode/agents/executor.md`
- 全局：`~/.config/opencode/agents/executor.md`

### 配置格式（Markdown）

```yaml
---
description: "任务执行子代理"
mode: subagent          # 必须设置为 subagent
model: default          # 可选：指定模型
temperature: 0.3        # 可选：温度参数
tools:                  # 工具权限
  write: true
  edit: true
  bash: true
permission:             # 细粒度权限
  write: allow
  edit: allow
---

# 系统提示词

你是一个任务执行子代理...
```

## 会话导航

OpenCode支持在主会话和子会话间切换：

| 快捷键 | 功能 |
|--------|------|
| `<Leader>+Right` | 进入子会话 |
| `<Leader>+Left` | 返回父会话 |
| `<Leader>+Down` | 进入第一个子会话 |
| `Tab` | 在Primary Agents间切换 |

## 与task-orchestrator集成

### 数据流

```
用户/主Agent
     │
     ├──1. 创建计划 (create-plan.py)
     │
     ├──2. 调用 @executor ─────┐
     │                         │
     │<──3. 返回结果────────────┘
     │
     ├──4. 检查状态 (status.py)
     │
     └──5. 继续下一步
```

### 实现细节

1. **主Agent创建计划** - 生成JSON格式的任务计划
2. **调用executor subAgent** - 通过Task工具或@提及
3. **subAgent执行任务** - 独立会话中执行
4. **状态同步** - 通过文件系统共享状态
5. **主Agent监控** - 轮询状态文件

### 示例对话流程

**用户**: 帮我重构认证模块

**主Agent**: 
```
我来帮你重构认证模块。首先创建一个5步骤的计划：

1. 分析现有代码
2. 设计策略接口
3. 迁移调用
4. 删除旧代码
5. 测试验证

正在创建计划...
```

**主Agent**（执行脚本后）:
```
计划已创建: .orchestrator/plans/task-abc123.json

现在开始执行第1步：分析现有代码

@executor 请执行步骤1，计划文件: .orchestrator/plans/task-abc123.json
```

**executor subAgent**（独立会话）:
```
正在执行步骤1：分析现有代码...

已读取 src/services/AuthService.java
识别出以下责任：
- 用户登录验证
- Token生成
- 权限检查
- 密码加密

分析完成，结果已保存。
```

**主Agent**:
```
步骤1完成！让我检查状态...

📊 进度: 1/5 (20%)
✅ 步骤1: 分析完成

是否继续执行步骤2？
```

## 注意事项

1. **权限配置** - 确保主Agent有权限调用executor subAgent
2. **状态文件** - subAgent和主Agent通过文件系统同步状态
3. **超时处理** - subAgent执行可能超时，需要设置合理的超时时间
4. **错误恢复** - 单步骤失败不应影响其他步骤
5. **会话管理** - 可以使用快捷键在会话间切换查看进度

## 故障排查

### subAgent不执行

检查：
1. executor.md是否在正确的agents目录
2. opencode.json中task权限是否配置正确
3. 重启OpenCode使配置生效

### 状态不同步

检查：
1. .orchestrator目录权限
2. 状态文件路径是否正确
3. subAgent是否有写权限

### 任务卡住

1. 使用 `<Leader>+Right` 切换到subAgent会话查看
2. 检查subAgent是否还在运行
3. 必要时手动终止并重新执行
