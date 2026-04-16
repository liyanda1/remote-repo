---
name: sdd-task-review
description: "Use when all tasks in tasks.md are passing - run spec and design compliance review before ST acceptance testing"
---

# SDD 规范性 / 合规性检查 — 代码审查

在所有任务完成、进入 ST 之前，运行一次全面的合规性检查，验证代码实现与 srs.md、design.md 的符合程度。

**核心原则：** 审查运行在独立子 Agent 中；主 Agent 只传递文件路径，不读取文件内容。

<HARD-GATE>
任何审查项 FAIL 时，必须先修复再继续 ST。不得跳过审查，不得对「简单」AR 豁免。
</HARD-GATE>

## Checklist

你必须为以下每个步骤创建 TodoWrite 任务，并按顺序完成：

1. **收集路径参数** — 收集所有相关文件路径
2. **构建子 Agent 提示** — 读取审查提示模板，填充路径参数
3. **派发子 Agent** — 启动独立审查 Agent
4. **解析审查结果** — 读取审查结论，处理 PASS / FAIL
5. **修复 + 重审**（如 FAIL）— 修复问题，重新派发子 Agent
6. **记录审查结果** — 在 tasks.md 中记录
7. **移交 ST 阶段** — 调用 `sdd-router:sdd-task-st`

**终态是调用 sdd-task-st。**

---

## Step 1：收集路径参数

收集以下路径（不读取文件内容，只收集路径）：

| 参数 | 路径 | 说明 |
|------|------|------|
| `ar_dir` | `specs/changes/ARxxx-topic/` | AR 工作目录 |
| `srs_file` | `specs/changes/ARxxx-topic/srs.md` | 需求设计说明书 |
| `design_file` | `specs/changes/ARxxx-topic/design.md` | AR 详细设计文档 |
| `tasks_file` | `specs/changes/ARxxx-topic/tasks.md` | 任务状态文件 |
| `spec_file` | `specs/component-detail-design/组件_spec.md` | 组件详细设计 |
| `changed_headers` | `include/xxx.h` 等 | 本次 AR 修改的头文件列表 |
| `changed_sources` | `src/xxx.cpp` 等 | 本次 AR 修改的源文件列表 |
| `changed_tests` | `tests/xxx_test.cpp` 等 | 本次 AR 新增/修改的测试文件列表 |
| `base_sha` | `git rev-parse HEAD~N` | AR 开始前的 git SHA（用于 diff）|

获取 base_sha：
```bash
# 在 tasks.md 进度记录中查找第一个会话的提交，或通过 git log 找到 AR 开始前的 SHA
git log --oneline -20
```

---

## Step 2：构建子 Agent 提示

检查是否存在审查提示模板：
- `skills/sdd-task-review/prompts/review-prompt.md`（优先）
- 不存在则使用本 skill 内嵌的模板（Step 3 中的 inline prompt）

使用文件路径参数填充模板变量。

---

## Step 3：派发子 Agent（OpenCode 方式）

**OpenCode 环境下**，使用 `@mention` 语法或平台原生子 Agent 机制：

```
Agent(
  description = "AR [ARxxx] 合规性审查",
  prompt = """
你是一名代码合规性审查专家，请按以下规则审查。

== 审查目标文件（路径）==
- srs.md: {srs_file}
- design.md: {design_file}
- 修改的头文件: {changed_headers}
- 修改的源文件: {changed_sources}
- 修改的测试文件: {changed_tests}
- 组件详设: {spec_file}

== 使用工具读取上述文件内容，然后执行以下所有审查维度 ==

## 审查维度 S — 需求符合性（Spec Compliance）

| ID | 审查项 | 判断标准 |
|----|-------|---------|
| S1 | srs.md 中所有功能需求均有对应测试 | 每个 §3.x 需求的验收标准（Given/When/Then）都有对应的测试函数 |
| S2 | 测试验证行为，而不是实现细节 | 测试断言基于函数输入/输出，不直接访问私有成员或内部状态（除非设计明确要求）|
| S3 | 无未文档化的副作用 | 实现代码的行为与 srs.md 描述的一致，没有额外改动未提及的系统状态 |
| S4 | 边界条件覆盖 | design.md 边界条件矩阵（§5）中的每一行都有对应测试 |
| S5 | 错误处理覆盖 | design.md 错误处理表（§6）中的每种错误类型都有对应测试 |

## 审查维度 D — 设计符合性（Design Compliance）

| ID | 审查项 | 判断标准 |
|----|-------|---------|
| D1 | 接口签名符合设计 | `include/` 中的函数签名与 design.md §3 的接口设计完全一致（名称、参数类型、返回类型）|
| D2 | 算法逻辑符合设计 | 核心实现逻辑与 design.md §4 的伪代码/流程图一致，关键控制流不偏离设计 |
| D3 | 模块影响范围符合设计 | 修改的文件集合与 design.md §2 的「模块影响分析」表一致，无意外修改其他文件 |
| D4 | 无未授权的设计偏离 | 所有与 design.md 的偏离必须有代码注释记录，说明原因（自适应修改是允许的，但必须有记录）|

## 审查维度 C — 组件规范符合性（Component Compliance）

| ID | 审查项 | 判断标准 |
|----|-------|---------|
| C1 | 不破坏现有对外接口 | `include/` 中已有的公共接口签名未被修改（新增接口不算破坏）|
| C2 | 符合组件架构原则 | 代码组织方式与组件详设（spec.md）的架构原则一致（如分层约束、模块边界）|
| C3 | 代码风格符合规范 | 命名规范、注释风格符合 AGENTS.md 的要求（如有）|

## 输出格式

请以下面的格式输出审查结论：

```markdown
## 审查结论

**总体判断：** PASS / FAIL

### S — 需求符合性
| S1 | YES/NO | [说明] |
| S2 | YES/NO | [说明] |
| S3 | YES/NO | [说明] |
| S4 | YES/NO | [说明] |
| S5 | YES/NO | [说明] |

### D — 设计符合性
| D1 | YES/NO | [说明] |
| D2 | YES/NO | [说明] |
| D3 | YES/NO | [说明] |
| D4 | YES/NO | [说明] |

### C — 组件规范符合性
| C1 | YES/NO | [说明] |
| C2 | YES/NO | [说明] |
| C3 | YES/NO | [说明] |

### 问题列表（仅 NO 项）
| 严重性 | 维度 | 问题描述 | 修复建议 |
|-------|------|---------|---------|
| Critical/Important/Minor | Sxx/Dxx/Cxx | [描述] | [建议] |
```
  """
)
```

---

## Step 4：解析审查结果

读取子 Agent 的输出：

**PASS（所有 S1-S5、D1-D4、C1-C3 均为 YES）：**
1. 在 tasks.md 末尾追加审查记录：
   ```markdown
   ## Review 记录
   - 日期：YYYY-MM-DD
   - 结果：PASS
   - 审查维度：S1-S5 PASS, D1-D4 PASS, C1-C3 PASS
   ```
2. 进入 Step 6

**FAIL（任何维度为 NO）：**
1. 读取问题列表
2. 对 Critical / Important 问题，进入 Step 5（修复循环）
3. 对 Minor 问题，可选择立即修复或记录为待办（通过 AskUserQuestion 与用户确认）

---

## Step 5：修复 + 重审（最多 3 轮）

### 修复循环

1. 按问题列表，逐一修复 Critical 和 Important 问题：
   - 修复代码偏离 design.md 的问题（D 维度）→ 按设计修改实现
   - 修复测试覆盖缺失（S 维度）→ 补写测试用例
   - 修复规范违规（C 维度）→ 按规范调整代码
2. 如果修复需要修改 design.md（发现设计有误）→ 通过 AskUserQuestion 报告给用户，等待确认后再修复
3. 修复完成后重新运行测试，确认 Green
4. 重新派发子 Agent（只审查修改过的维度）
5. 最多 3 轮修复 + 重审

**超过 3 轮仍有 FAIL：**
通过 AskUserQuestion 向用户上报，列出：
- 失败的审查项
- 已尝试的修复
- 请用户决定：强制通过 / 修改设计 / 调整需求

---

## Step 6：记录审查结果

在 `specs/changes/ARxxx-topic/tasks.md` 中的「进度记录」节追加：

```markdown
### YYYY-MM-DD 审查记录

- 审查结果：PASS（第 N 轮）
- S 维度：全部通过
- D 维度：全部通过
- C 维度：全部通过
- 修复的问题：[如有，列出 D2、S4 等已修复项]
```

---

## Step 7：移交 ST 阶段

审查 PASS 后：

1. 输出审查完成摘要：
   - AR 编号与主题
   - 审查轮次
   - 修复的问题数量
   - 代码质量总评

2. **必须调用：** 调用 `sdd-router:sdd-task-st` 开始 ST 验收测试

---

## 严重性定义

| 严重性 | 定义 | 是否阻塞 |
|-------|------|---------|
| Critical | 接口签名错误、需求未实现、破坏现有接口 | 是，必须修复 |
| Important | 测试覆盖不足、算法偏离、代码规范违规 | 是，修复后可进 ST |
| Minor | 注释缺失、命名不理想、非必要重复 | 否，可记录后处理 |

## 反模式警告

| 反模式 | 正确做法 |
|-------|---------|
| 主 Agent 自己读文件做审查 | 必须派发子 Agent，独立上下文读取文件 |
| 跳过「简单」AR 的审查 | 每个 AR 必须完整审查 |
| 把多个问题合并为一个发现 | 每个问题单独列出 |
| "代码看起来对" | PASS 必须有具体的 YES 证据 |
| 修改 srs.md / design.md 来规避问题 | 先问用户，经批准才能修改 |

## 集成说明

**调用方：** sdd-router（所有任务 passing，review 未完成时）
**链接到：** sdd-task-st（Step 7，审查 PASS 后）
**派发：** 审查子 Agent（独立上下文）
**读取（仅路径）：** srs.md、design.md、tasks.md、组件详设、修改的代码文件
**产出：** 更新后的 tasks.md（含审查记录）；审查报告（子 Agent 输出）
