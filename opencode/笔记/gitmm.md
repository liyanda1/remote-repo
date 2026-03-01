

---

## 1. 工具概述

-   **核心用途**：多仓库管理工具，解决包含多个Git子仓库的大型项目的协同开发问题。
-   **工作模式**：通过一个 **manifest仓库**（清单仓库）来统一管理所有子仓库的地址、分支和版本依赖关系。
-   **适用场景**：适用于华为内部及使用华为CodeArts Repo服务的大型项目，特别是需要同时修改多个组件（子仓）的场景。

## 2. 核心概念

在使用 `git mm` 之前，需要理解两个核心概念：

-   **manifest仓库**：这是一个特殊的仓库，它不存放项目业务代码，而是存放一个或多个 **XML文件**。这些XML文件定义了该项目包含哪些子仓库、每个子仓库的远程路径、以及默认分支等信息。
-   **子仓库**：实际存放业务代码的多个Git仓库。`git mm` 命令的工作对象就是这些子仓库。
-   **MR开发模式 vs CR开发模式**：`git mm` 通常对应华为内部的 **CR（变更请求）开发模式**，这是一种自研的多仓协同工作流，区别于开源的MR（合并请求）模式。

## 详细用法指南

以下是基于华为内部实践整理的 `git mm` 常用命令及操作流程。

### 4.1 初始化工作区

这是在新电脑上拉取项目代码的第一步。

```bash
git mm init -u <manifest仓库URL> -b <分支> -m <xml文件>
```
-   **`-u`**：指定manifest仓库的地址（例如：`ssh://git@source.huawei.com:2222/.../manifest.git`）。
-   **`-b`**：指定manifest仓库的分支（例如：`master` 或 `br_V8R10C10B010`）。
-   **`-m`**：指定使用哪个XML文件作为清单（例如：`ChargeONE/dependency.xml`）。

### 4.2 同步代码

初始化后，或日常更新代码时使用。

-   **同步所有仓库**：
    ```bash
    git mm sync
    ```
    这个命令会根据manifest文件拉取所有子仓库的最新代码。

-   **同步单个子仓库**：如果只想更新特定的子仓，可以在命令后加上仓库名。
    
    ```bash
    git mm sync product/bras
    ```

### 4.3 分支管理

在进行新特性开发或修复Bug时，通常需要创建本地分支。

-   **查看所有子仓库列表**：
    ```bash
    git mm list
    ```

-   **创建并切换分支**：
    -   为所有子仓创建分支：`git mm start <新分支名> --all` 。
    -   为特定子仓创建分支：`git mm start <新分支名> <子仓路径>` 。
    ```bash
    # 示例：为所有子仓创建名为 feature/new-function 的分支
    git mm start feature/new-function --all
    ```

-   **删除分支**：
    
    ```bash
    git mm abandon <分支名> --all
    ```
    
-   **查询分支信息**：
    
    ```bash
    git mm info
    ```
    该命令可以查看各个子仓库当前所在的分支和提交记录。

### 4.4 代码开发与提交

修改完代码后，进行提交。

1.  **查看修改状态**：在主仓目录下粗略查看哪些子仓有修改。
    ```bash
    git mm status
    ```
    > **提示**：如果需要查看具体的修改内容，仍然需要进入对应的子仓目录执行 `git status` 或 `git diff`。

2.  **提交代码**：`git mm` 的提交流程通常是将本地的多个仓库的修改一起推送到远端并生成变更请求（CR）。
    ```bash
    # 普通提交
    git mm upload
    
    # 强制提交（覆盖远端）
    git mm upload -f
    ```

3.  **批量执行命令**：如果需要在所有子仓中执行同一条Git命令，可以使用 `forall`。
    ```bash
    git mm forall -c "<git命令>"
    
    # 示例：在所有子仓中执行 git pull
    git mm forall -c "git pull origin master"
    ```

### 4.5 特殊场景处理

-   **拉取特定的合并请求（MR/CR）**：
    ```bash
    git mm cherry-pick -s <MR编号>
    ```
    例如：`git mm cherry-pick -s 21469` 。

-   **解决冲突**：
    当 `cherry-pick` 或 `rebase` 失败时，需要手动解决冲突。
    
    1.  进入有冲突的子仓，手动编辑文件解决冲突。
    2.  执行 `git add <解决冲突的文件>`。
    3.  执行 `git rebase --continue` 继续操作。
    
-   **撤销提交**：
    如果需要撤销最近一次的commit（例如合并commit），可以使用：
    
    ```bash
    # 撤回最近一次提交，但保留修改内容在工作区
    git reset --soft HEAD~1
    ```

## 5. 注意事项

1.  **区分同名工具**：需要注意的是，NPM上有一个同名的 `gitmm` 包，它的功能是在提交时自动为commit信息添加分支前缀，**并非**本文介绍的多仓管理工具，使用时请根据上下文区分。
2.  **认证配置**：首次使用时，通常需要安装并配置凭证插件，如 `git mm credential install` 和 `git mm credential --store`，以便工具可以自动处理认证信息。
3.  **子模块 vs 子仓库**：`git mm` 管理的子仓库在原理上类似于Git的`submodule`，但提供了更强大和便捷的批量操作能力。

