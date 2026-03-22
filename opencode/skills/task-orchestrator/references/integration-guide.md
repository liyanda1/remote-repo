# Task Orchestrator 集成指南

## 概述

本文档说明如何将 task-orchestrator skill 集成到内网部署的 OpenCode 中。

## 核心问题

OpenCode 本身不直接提供 "subAgent" 机制，但可以通过以下方式模拟：

### 方案A：文件系统通信（推荐）

利用文件系统作为主Agent和"subAgent"之间的通信桥梁：

```
主Agent (监控)          文件系统              "subAgent" (执行)
    │                      │                       │
    │──写入任务计划──────>│                       │
    │                      │                       │
    │                      │<──读取任务计划────────│
    │                      │                       │
    │                      │<──写入执行结果────────│
    │                      │                       │
    │──读取状态──────────>│                       │
```

**实现方式：**
1. 主Agent创建任务计划文件
2. 主Agent生成一个独立的执行脚本（包含完整任务指令）
3. 使用 `nohup` 或后台进程启动执行脚本
4. 执行脚本独立运行，通过文件系统报告进度
5. 主Agent轮询状态文件获取进度

### 方案B：多进程模拟

在OpenCode环境中启动独立的Python进程作为"subAgent"：

```python
import subprocess
import os

# 生成subAgent的执行脚本
subagent_script = generate_subagent_script(task_prompt)

# 后台启动
process = subprocess.Popen(
    ['python3', subagent_script],
    stdout=open('output.log', 'w'),
    stderr=open('error.log', 'w'),
    stdin=subprocess.DEVNULL,
    start_new_session=True  # 脱离终端
)

# 保存进程ID供后续监控
save_pid(process.pid)
```

### 方案C：OpenCode Task 工具

如果OpenCode支持类似 WorkBuddy 的 `Task` 工具，可以直接使用：

```
主Agent调用 Task 工具启动 subAgent
subAgent独立执行
主Agent通过某种机制获取结果
```

需要确认内网OpenCode是否支持此类功能。

## 与内网OpenCode的集成步骤

### 1. 部署Skill

将 `task-orchestrator` 目录复制到OpenCode的skills目录：

```bash
# 项目本地
mkdir -p .opencode/skills/
cp -r task-orchestrator .opencode/skills/

# 或全局
cp -r task-orchestrator ~/.config/opencode/skills/
```

### 2. 适配OpenCode调用方式

根据OpenCode的实际能力，修改 `run-background.py` 中的 `run_subagent` 函数：

```python
def run_subagent(plan_path, step_id, task_description, step_description):
    """
    根据OpenCode实际能力选择实现方式
    """
    
    # 方式1: 如果OpenCode支持subAgent API
    if opencode_supports_subagent():
        return run_via_opencode_api(plan_path, step_id, task_description, step_description)
    
    # 方式2: 使用后台进程
    return run_via_background_process(plan_path, step_id, task_description, step_description)
    
    # 方式3: 使用外部脚本
    return run_via_external_script(plan_path, step_id, task_description, step_description)
```

### 3. 创建OpenCode配置

在项目根目录创建 `.opencode/opencode.json`：

```json
{
  "skills": {
    "task-orchestrator": {
      "enabled": true,
      "auto_advance": false,
      "check_interval_seconds": 30
    }
  }
}
```

## 使用示例

### 场景：重构大型代码库

```bash
# 1. 创建5步骤重构计划
python3 .opencode/skills/task-orchestrator/scripts/create-plan.py \
  --task "重构用户认证模块：1)提取接口 2)实现新类 3)迁移调用 4)删除旧代码 5)测试验证" \
  --steps 5

# 2. 启动第1步（后台执行）
python3 .opencode/skills/task-orchestrator/scripts/run-background.py --step 1

# 3. 主Agent检查状态（可以每30秒检查一次）
python3 .opencode/skills/task-orchestrator/scripts/status.py

# 4. 第1步完成后，确认并执行下一步
python3 .opencode/skills/task-orchestrator/scripts/next.py
```

### 场景：分点执行（人工确认每步）

```bash
# 创建计划
python3 scripts/create-plan.py --task "生成项目文档" --steps 3

# 循环执行每一步
while true; do
  python3 scripts/status.py
  read -p "执行下一步? (y/n): " confirm
  if [ "$confirm" = "y" ]; then
    python3 scripts/next.py --yes
  else
    break
  fi
done
```

## 监控与调试

### 查看实时日志

```bash
# 查看当前步骤的实时日志
tail -f .orchestrator/logs/step-{n}.log

# 查看所有日志
ls -la .orchestrator/logs/
```

### 手动标记步骤状态

如果subAgent未能正确更新状态，可以手动修复：

```bash
python3 scripts/complete-step.py \
  --plan .orchestrator/plans/task-xxx.json \
  --step 2 \
  --status success \
  --result "手动标记完成"
```

## 注意事项

1. **文件权限**：确保OpenCode有读写 `.orchestrator/` 目录的权限
2. **进程管理**：后台进程需要妥善管理，避免僵尸进程
3. **超时处理**：设置合理的超时时间，避免无限等待
4. **错误恢复**：设计重试机制，单步骤失败不应导致整任务失败
5. **资源限制**：内网环境可能资源有限，控制并发任务数

## 扩展建议

1. **Web界面**：可以开发一个简单的Web界面展示任务状态
2. **通知集成**：步骤完成时发送邮件/企业微信通知
3. **历史记录**：保存任务历史，支持查看过往执行记录
4. **模板库**：预置常见任务的模板（代码重构、文档生成等）
