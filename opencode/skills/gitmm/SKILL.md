---
name: gitmm
description: 华为内部多仓管理工具 git mm 的使用帮助。当你需要拉取代码、创建分支、同步代码、管理多仓库项目时使用此 skill。触发场景包括：用户提到"拉取代码"、"克隆代码"、"创建分支"、"同步代码"、"多仓管理"等与 git mm 相关的操作。
---

# Git MM Skill

华为内部多仓管理工具，用于管理包含多个 Git 子仓库的大型项目。

## 核心命令流程

当用户请求"拉取某个分支的代码"时，按以下流程执行：

### 步骤 1: 确认关键信息

先向用户确认以下信息（如果用户没有提供）：

1. **manifest 仓库地址** (`-u`)：manifest 仓库的 URL
2. **分支名** (`-b`)：manifest 仓库的分支
3. **xml 文件** (`-m`)：清单文件路径，如 `ChargeONE/dependency.xml`
4. **本地存放路径**：代码拉取到哪个目录，默认 `~/workspace/<分支名>/`
5. **要创建的分支名** (`git mm start`)：用户想要基于哪个分支创建新分支

### 步骤 2: 初始化工作区

```bash
git mm init -u <manifest仓库URL> -b <分支> -m <xml文件> -g all
```

**命令参数说明**：
- `-u`：manifest 仓库 URL
- `-b`：分支名（可使用简称，会自动匹配）
- `-m`：清单 xml 文件
- `-g all`：同步所有子仓库

#### 分支名匹配逻辑

1. **先尝试匹配硬编码的分支名**：
   - `master`
   - `develop`
   
2. 如果硬编码列表中没有匹配，用户可提供完整分支名，或后续通过 POST 请求到 codehub API 获取分支列表进行匹配（当前功能待实现）

#### 硬编码分支列表（可自定义）

```
master, main, develop, release, br_V8R10C10B010
```

### 步骤 3: 同步代码

```bash
git mm sync
```

或同步单个子仓库：
```bash
git mm sync <子仓路径>
```

### 步骤 4: 创建分支

```bash
# 为所有子仓创建分支
git mm start <分支名> --all

# 为特定子仓创建分支
git mm start <分支名> <子仓路径>
```

## 常用命令参考

| 操作 | 命令 |
|------|------|
| 初始化 | `git mm init -u <url> -b <branch> -m <xml> -g all` |
| 同步所有 | `git mm sync` |
| 同步单个 | `git mm sync <子仓>` |
| 查看仓库列表 | `git mm list` |
| 创建分支 | `git mm start <分支名> --all` |
| 删除分支 | `git mm abandon <分支名> --all` |
| 查看分支信息 | `git mm info` |
| 查看修改状态 | `git mm status` |
| 提交代码 | `git mm upload` |
| 强制提交 | `git mm upload -f` |
| 批量执行命令 | `git mm forall -c "<git命令>"` |
| 拉取 MR/CR | `git mm cherry-pick -s <编号>` |

## 执行流程

1. **先确认方案**：告知用户将要执行的命令，等待用户确认
2. **用户确认后执行**：使用 Bash 工具执行命令
3. **处理结果**：如果执行过程中出现错误，帮助排查解决

## 注意事项

1. 首次使用需要配置凭证：`git mm credential install` 和 `git mm credential --store`
2. `git mm` 是华为内部多仓管理工具，区别于 NPM 上的同名包
3. 如果用户只是需要单个仓库操作，不需要使用 git mm
