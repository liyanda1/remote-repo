# opencode

待完成的skill

- git mm 
- mr review
- 业务
- hdt 生成

opencode官方文档：https://opencode.ai/docs/zh-cn/

## 常用 Slash 命令

| 命令             | 功能说明                                  | 是否影响上下文   | 是否生成/修改文件 | 典型使用场景              | 备注             |
| ---------------- | ----------------------------------------- | ---------------- | ----------------- | ------------------------- | ---------------- |
| `/init`          | 初始化工程，扫描代码结构并生成 `AGENT.md` | ✅ 重建工程上下文 | ✅ 生成 `AGENT.md` | 第一次接入项目            | 大仓建议分模块   |
| `/compress`      | 压缩当前对话上下文，生成摘要以释放 token  | ✅ 会重写上下文   | ❌                 | 对话过长、接近 token 上限 | 推荐定期执行     |
| `/undo`          | 撤销上一次 AI 操作                        | ❌                | 可能回滚文件      | 生成错误代码              | 支持多级         |
| `/redo`          | 恢复被撤销操作                            | ❌                | 恢复文件修改      | 撤销后恢复                | 与 undo 成对     |
| `/clear`         | 清空当前对话上下文                        | ✅（仅会话）      | ❌                 | 重新开始讨论              | 不删除 AGENT.md  |
| `/context`       | 查看当前加载文件和上下文                  | ❌                | ❌                 | 调试 token 问题           | 查看加载内容     |
| `/remove <path>` | 移除文件或目录                            | ✅                | ❌                 | 精简上下文                | 降低 token 占用  |
| `/share`         | 生成会话分享链接                          | ❌                | ❌                 | 团队协作                  | 企业环境可能禁用 |
| `/export`        | 导出当前对话                              | ❌                | ✅ 导出文件        | 存档/评审                 | 通常 Markdown    |
| `/history`       | 查看历史操作                              | ❌                | ❌                 | 回顾步骤                  | 调试用           |
| `/model`         | 切换模型                                  | ❌                | ❌                 | 切换高性能模型            | 不影响结构       |
| `/help`          | 查看命令帮助                              | ❌                | ❌                 | 查询命令                  |                  |

## Skills

一句话总结：**带目录的说明书**，或者说是 **渐进披露提示词的机制**

```
├── skills/
│   ├── skill-name1/
│   │   ├── SKILL.md	# 元数据 + 指令
│   │   ├── srcipts/	# 资源层（可选）
│   │   │	└── main.py
│   │   ├── references/
│   │   │	└── doc.md
│   │   ├── assets/
│   │   │	└── pic.png
```

创建 `.opencode/skills/git-release/SKILL.md`，内容如下：

```markdown
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do

- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command

## When to use me

Use this when you are preparing a tagged release.
Ask clarifying questions if the target versioning scheme is unclear.
```

配置权限：

在 `opencode.json` 中使用基于模式的权限来控制代理可以访问哪些技能：

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| 权限    | 行为                     |
| :------ | :----------------------- |
| `allow` | 技能立即加载             |
| `deny`  | 对代理隐藏技能，拒绝访问 |
| `ask`   | 加载前提示用户确认       |

模式支持通配符：`internal-*` 可匹配 `internal-docs`、`internal-tools` 等。



## 自定义命令

在 `commands/` 目录中创建 markdown 文件来定义自定义命令。

创建 `~/.config/opencode/commands/test.md`：

```markdown
---
description: Run tests with coverage
agent: build		# 什么模式下可以执行的命令
model: anthropic/claude-3-5-sonnet-20241022	
---
# 描述命令做什么功能
Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```



## 自定义智能体

- 全局：`~/.config/opencode/agents/`
- 项目级：`.opencode/agents/`

创建`~/.config/opencode/agents/review.md`：

```markdown
---
description: Reviews code for quality and best practices
mode: subagent		# 主智能体（可以显式切换）： primary    sub智能体；subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
  bash: false
---

You are in code review mode. Focus on:

- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations

Provide constructive feedback without making direct changes.
```





## oh-my-opencode 插件

https://github.com/code-yeongyu/oh-my-opencode

oh-my-opencode 插件 = 预设工具 + 预设MCP + 预设Agent

**预设tools**

| Tool            | Description                                      |
| --------------- | ------------------------------------------------ |
| lsp高级版       | 通过编程语言的语法和语义，帮助AI快速定位理解代码 |
| ast             | 通过代码语法树进行关联搜索                       |
| look_at         | 借助多模态大模型的视觉，理解图片PDF信息          |
| delegate-task   | Agent任务分配                                    |
| background-task | Agent后台调度                                    |

**预设MCP**

| Tool      | Description                                          |
| --------- | ---------------------------------------------------- |
| websearch | 使用 Exa AI 进行实时网络搜索，返回相关内容。         |
| context7  | 获取代码库或框架的最新官方文档。                     |
| grep_app  | 通过 grep.app 在公共 GitHub 仓库中进行超快代码搜索。 |

**预设Agent**

`.config/opencode/oh-my-opencode.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  "agents": {
    "oracle": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "librarian": {
      "model": "opencode/glm-4.7-free"
    },
    "explore": {
      "model": "opencode/gpt-5-nano"
    },
    "multimodal-looker": {
      "model": "google/gemini-3-flash-preview"
    },
    "prometheus": {
      "model": "google/gemini-3.1-pro-preview"
    },
    "metis": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "momus": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "atlas": {
      "model": "google/gemini-3.1-pro-preview"
    }
  },
  "categories": {
    "visual-engineering": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "ultrabrain": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "artistry": {
      "model": "google/gemini-3.1-pro-preview",
      "variant": "high"
    },
    "quick": {
      "model": "google/gemini-3-flash-preview"
    },
    "unspecified-low": {
      "model": "google/gemini-3-flash-preview"
    },
    "unspecified-high": {
      "model": "google/gemini-3-flash-preview"
    },
    "writing": {
      "model": "google/gemini-3-flash-preview"
    }
  }
}
```



**使用**

安装完成后使用`ulw 设计内容`开始调用，oh-my-opencode会尽可能的调用它的一切潜能，把任务分配给几个智能体，并且并行运行，由主智能体进行居中调度





## FAQ

问题：拷贝粘贴多行时显示`[Pasted ~5 lines]`,
解决办法：只显示一个摘要提示（比如 `[Pasted ~5 lines]`）。你复制的内容其实已经完整地保存在系统剪贴板里了，只是界面为了美观没全显示出来。



问题：如何输入多行。Shift+Enter会直接发送输入内容
解决办法：使用`Ctrl+J`



问题：Linux TUI 选中历史对话内容提示“Copied to clipboard”但粘贴没有内容
解决办法：opencode 依赖xclip软件实现复制，通过`sudo apt install xclip xsel wl-clipboard`安装使用。



问题：.worktrees 合并失败导致代码丢失
问题描述 .worktrees AI合并失败后并没有提示出来，后续操作又会导致.worktrees目录被删除。由于.worktrees目录不会被git跟踪，最终无法找回代码。

解决办法：在将.worktrees合并到主分支之前先备份一次。比如 ! 进入shell模式 cp -r .worktrees .worktrees.bak。