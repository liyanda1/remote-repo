# Skill Creator — OpenCode 使用指南

> 本文档面向 OpenCode 用户，介绍如何使用 skill-creator 创建 skill、编写测试用例、执行测试评估和迭代改进。

---

## 目录

1. [前置准备](#1-前置准备)
2. [创建 Skill](#2-创建-skill)
3. [编写测试用例](#3-编写测试用例)
4. [执行测试评估](#4-执行测试评估)
5. [审阅测试结果](#5-审阅测试结果)
6. [迭代改进](#6-迭代改进)
7. [触发准确率优化](#7-触发准确率优化)
8. [附录：文件结构速查](#附录文件结构速查)

---

## 1. 前置准备

### 1.1 OpenCode 配置目录机制

OpenCode 的 agents、commands 等文件支持**两级放置**：

| 级别 | 目录路径 | 作用范围 | 适用场景 |
|------|---------|---------|---------|
| **全局** | `~/.config/opencode/` | 所有项目通用 | 个人常用工具，如 skill-creator |
| **项目级** | 项目根目录 `.opencode/` | 仅当前项目 | 项目专属的 agent/command |

> Windows 下 `~` 即 `C:\Users\<用户名>\`，所以全局目录是 `C:\Users\<用户名>\.config\opencode\`。
>
> OpenCode 会**合并**两级配置，项目级覆盖全局同名项，非冲突项全部保留。

**推荐做法**：skill-creator 是通用工具，放在**全局目录**，这样任何项目都能用。如果你只在某个项目用，也可以放项目级。

### 1.2 部署步骤

#### 方案 A：全局部署（推荐，所有项目可用）

skill-creator 的文件分两组部署：

```
C:\Users\<用户名>\.config\opencode\
├── agents\                        ← 组 1：代理（复制 .opencode\agents\ 下的文件）
│   ├── skill-executor.md
│   └── skill-grader.md
├── commands\                      ← 组 1：命令（复制 .opencode\commands\ 下的文件）
│   ├── skill-create.md
│   ├── skill-eval.md
│   └── skill-improve.md
└── skills\
    └── skill-creator\             ← 组 2：skill 本体（复制整个 skill 目录内容）
        ├── SKILL.md
        ├── agents\                # Prompt 模板（grader.md, comparator.md, analyzer.md）
        ├── scripts\               # Python 脚本（aggregate_benchmark.py 等）
        ├── eval-viewer\           # HTML 审阅报告生成器
        ├── references\            # JSON Schema 定义
        └── docs\                  # 本使用指南
```

> **关键**：SKILL.md、scripts/、eval-viewer/、references/、agents/ 模板全部放在 `skills/skill-creator/` 下。
> OpenCode 会自动扫描 `skills/*/SKILL.md` 发现 skill。
> SKILL.md 中所有内部引用（脚本路径、模板路径）都使用相对于自身目录的路径，因此无论放在哪里都能正确找到文件。

#### 方案 B：项目级部署

把同样的结构放到项目的 `.opencode\` 下：

```
your-project\
└── .opencode\
    ├── agents\
    │   ├── skill-executor.md
    │   └── skill-grader.md
    ├── commands\
    │   ├── skill-create.md
    │   ├── skill-eval.md
    │   └── skill-improve.md
    └── skills\
        └── skill-creator\
            ├── SKILL.md
            ├── agents\
            ├── scripts\
            ├── eval-viewer\
            └── references\
```

#### 一键部署

修改下方脚本中的 `SRC` 变量为你的 skill-creator 源码路径，然后执行。

**Linux / macOS（bash）：**

```bash
# ===== 修改此处 =====
SRC=~/tools/skill-creator
# ===================

CFG="$HOME/.config/opencode"

# 组 1：agents + commands
mkdir -p "$CFG/agents" "$CFG/commands"
cp "$SRC/.opencode/agents/"*.md "$CFG/agents/"
cp "$SRC/.opencode/commands/"*.md "$CFG/commands/"

# 组 2：skill 本体
DEST="$CFG/skills/skill-creator"
mkdir -p "$DEST"
cp "$SRC/SKILL.md" "$DEST/"
cp -r "$SRC/agents" "$SRC/scripts" "$SRC/eval-viewer" "$SRC/references" "$DEST/"
[ -d "$SRC/docs" ] && cp -r "$SRC/docs" "$DEST/"

# 验证
echo "=== agents ==="  && ls "$CFG/agents/"
echo "=== commands ===" && ls "$CFG/commands/"
echo "=== skills/skill-creator ===" && ls "$DEST/"
```

**Windows（PowerShell）：**

```powershell
# ===== 修改此处 =====
$SRC = "D:\tools\skill-creator"
# ===================

$globalCfg = "$env:USERPROFILE\.config\opencode"

# 组 1：agents + commands
New-Item -ItemType Directory -Force -Path "$globalCfg\agents", "$globalCfg\commands" | Out-Null
Copy-Item "$SRC\.opencode\agents\*" "$globalCfg\agents\" -Force
Copy-Item "$SRC\.opencode\commands\*" "$globalCfg\commands\" -Force

# 组 2：skill 本体
$skillDest = "$globalCfg\skills\skill-creator"
New-Item -ItemType Directory -Force -Path $skillDest | Out-Null
Copy-Item "$SRC\SKILL.md" "$skillDest\" -Force
Copy-Item "$SRC\agents", "$SRC\scripts", "$SRC\eval-viewer", "$SRC\references" "$skillDest\" -Recurse -Force
if (Test-Path "$SRC\docs") { Copy-Item "$SRC\docs" "$skillDest\" -Recurse -Force }

# 验证
Write-Host "=== agents ===" ; Get-ChildItem "$globalCfg\agents\"
Write-Host "=== commands ===" ; Get-ChildItem "$globalCfg\commands\"
Write-Host "=== skills/skill-creator ===" ; Get-ChildItem "$skillDest\"
```

> **注意**：`opencode.json` 不需要复制到全局目录。全局配置只需放 `.md` 文件，OpenCode 自动扫描发现。

### 1.3 Python 环境

测试评估的聚合和报告生成依赖 Python。确认 Python 可用：

```bash
python3 --version
```

如果只有 `python`，后续命令中替换即可。

> **版本要求**：所有脚本已兼容 **Python 3.7+**。如果 Python 版本 ≥ 3.9 则原生支持，无特殊要求。

### 1.4 可用的命令

| 命令 | 用途 | 参数 |
|------|------|------|
| `/skill-create` | 创建新 skill | 无 |
| `/skill-eval` | 对 skill 运行测试评估 | `SKILL_PATH`（skill 目录路径） |
| `/skill-improve` | 基于 eval 结果改进 skill | `SKILL_PATH`（skill 目录路径） |

---

## 2. 创建 Skill

### 2.1 开始创建

在 OpenCode 中输入：

```
/skill-create
```

代理会引导你完成以下步骤。

### 2.2 意图澄清

代理会问你几个关键问题：

| 问题 | 示例回答 |
|------|---------|
| 这个 skill 要让 AI 做什么？ | "从 PDF 表单中提取字段并填入 Excel" |
| 什么时候应该触发？ | "用户说'提取表单'、'填写 PDF'、'PDF 转 Excel'" |
| 预期输出格式？ | "一个 Excel 文件，每行一个字段" |
| 需要测试用例吗？ | "需要"（建议有客观可验证输出时加） |

### 2.3 Skill 目录结构

创建完成后，你的 skill 目录长这样：

```
my-skill/
├── SKILL.md              # 必须，主文件
├── evals/                # 测试用例
│   ├── evals.json        # 测试用例定义
│   └── files/            # 测试输入文件（可选）
├── scripts/              # 辅助脚本（可选）
├── references/           # 参考文档（可选）
└── assets/               # 模板/资源（可选）
```

### 2.4 SKILL.md 格式

```markdown
---
name: my-skill
description: >
  触发描述。包含两件事：做什么 + 何时用。
  要写得"强势"一点——宁愿多触发也不要漏触发。
  例如：当用户要求提取 PDF 表单、填写 PDF 字段、
  将 PDF 表单导出为 Excel 时，使用此 skill。
---

# My Skill

## 核心流程
...（具体指令，用祈使句风格）

## 输出格式
...（明确格式要求）

## 注意事项
...（解释为什么重要，而不是写大写的 MUST/NEVER）
```

**编写要点：**
- body 部分控制在 **500 行以内**
- 用祈使句（"读取文件"、"检查格式"），不用"你应该"
- 解释 **为什么** 这么做，让模型理解意图而非机械遵守
- 如果内容很多，拆到 `references/` 目录，SKILL.md 中引用

---

## 3. 编写测试用例

### 3.1 测试用例是什么

测试用例（eval case）就是一组**真实用户会提出的任务**。skill-creator 会分别用"加载 skill"和"不加载 skill"两种方式执行这些任务，对比结果来衡量 skill 的价值。

### 3.2 测试用例文件

测试用例保存在 `evals/evals.json`：

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "帮我提取这个 PDF 表单里的所有字段，保存到 Excel",
      "expected_output": "一个 Excel 文件，包含所有 PDF 表单字段名和对应的值",
      "files": ["evals/files/sample-form.pdf"],
      "expectations": []
    },
    {
      "id": 2,
      "prompt": "把这份报名表的 PDF 转成结构化的 Excel 表格",
      "expected_output": "Excel 文件，每行一个报名人，列包含姓名、电话、邮箱等字段",
      "files": ["evals/files/registration.pdf"],
      "expectations": []
    }
  ]
}
```

### 3.3 字段说明

| 字段 | 必需 | 说明 |
|------|:----:|------|
| `id` | ✅ | 唯一整数编号 |
| `prompt` | ✅ | 用户任务描述——写**真实用户会说的话**，不是技术规格 |
| `expected_output` | ✅ | 预期结果的自然语言描述，人能看懂就行 |
| `files` | ❌ | 输入文件路径列表（相对于 skill 根目录）。没有就留空数组 `[]` |
| `expectations` | ❌ | 断言列表。**先留空**，跑完测试后再补 |

### 3.4 怎么写好的测试用例

**prompt 写法：**

❌ 不好的写法：
```json
"prompt": "提取 PDF"
```
太笼统，无法验证。

✅ 好的写法：
```json
"prompt": "帮我提取 D 盘合同文件夹里这份租赁合同的签署日期、甲方乙方名称和月租金，保存到 Excel"
```
具体、有细节、像真实用户说的话。

**测试用例数量建议：**
- 最少 **2-3 个**覆盖核心场景
- 理想 **5-8 个**覆盖正常/边界/异常场景
- 最多不建议超过 15 个（执行耗时太长）

**关键原则：expectations 先不写！**

> 不要在跑测试之前写断言。原因：你可能不知道 skill 实际会产出什么格式。先跑一轮，看到真实产出后，再基于实际输出写客观可验证的断言。

---

## 4. 执行测试评估

### 4.1 启动评估

在 OpenCode 中输入：

```
/skill-eval D:/path/to/my-skill
```

### 4.2 评估的完整流程

评估是一个**连续的五步流程**，不要中途停下来：

```
┌─────────────────────────────────────────────────────┐
│ Step 1: 执行测试用例                                   │
│   对每个 eval 串行执行：                                │
│   ├── with_skill：加载 skill 执行 prompt                │
│   └── baseline：不加载 skill 执行同一 prompt             │
│                                                       │
│ Step 2: 起草断言（expectations）                         │
│   基于实际输出，为每个测试用例编写可验证的断言              │
│                                                       │
│ Step 3: 记录执行时间                                    │
│   为每次运行生成 timing.json                            │
│                                                       │
│ Step 4: 评分 + 聚合 + 生成报告                           │
│   ├── 逐条判定断言 → grading.json                      │
│   ├── 聚合统计 → benchmark.json + benchmark.md         │
│   └── 生成审阅页面 → review.html                       │
│                                                       │
│ Step 5: 用户审阅                                      │
│   用户在浏览器中查看结果并提交反馈                        │
└─────────────────────────────────────────────────────┘
```

### 4.3 Step 1 详解：执行测试用例

#### 目录结构

评估结果存放在 skill 同级的 workspace 目录中：

```
my-skill/
my-skill-workspace/              # 与 skill 同级
└── iteration-1/                 # 第 1 轮评估
    ├── eval-0/                  # 第 1 个测试用例
    │   ├── eval_metadata.json
    │   ├── with_skill/
    │   │   └── outputs/
    │   │       ├── result.xlsx       # 实际产出
    │   │       ├── transcript.md     # 执行日志
    │   │       ├── grading.json      # 评分结果
    │   │       ├── timing.json       # 耗时数据
    │   │       └── metrics.json      # 工具调用统计（可选）
    │   └── without_skill/
    │       └── outputs/
    │           └── result.xlsx
    ├── eval-1/
    │   └── ...
    ├── benchmark.json            # 聚合统计
    ├── benchmark.md              # 可读报告
    └── review.html               # 审阅页面
```

#### 执行方式

由于 OpenCode 不支持并行子代理，测试用例**串行执行**：

1. 代理读取 SKILL.md 的指示
2. 对 evals.json 中的每个测试用例：
   - **with_skill**：按 skill 指示执行 prompt，产出保存到 `with_skill/outputs/`
   - **without_skill**（对照）：不加载 skill，直接执行同一 prompt，产出保存到 `without_skill/outputs/`
3. 为每次运行记录 `eval_metadata.json`

#### eval_metadata.json 格式

```json
{
  "eval_id": 0,
  "eval_name": "租赁合同字段提取",
  "prompt": "帮我提取这份租赁合同的签署日期、甲方乙方名称和月租金",
  "assertions": [
    "输出文件是 .xlsx 格式",
    "包含签署日期字段",
    "包含甲方名称和乙方名称",
    "包含月租金字段"
  ]
}
```

> 注意：第一轮执行时 `assertions` 可以为空数组 `[]`，在 Step 2 补充。

### 4.4 Step 2 详解：起草断言

跑完测试用例后，根据**实际看到的输出**编写断言。

**好断言的标准：**

| 特征 | 示例 |
|------|------|
| ✅ 客观可验证 | "输出文件扩展名为 .xlsx" |
| ✅ 有明确证据 | "Excel 包含名为'签署日期'的列" |
| ✅ 可程序化检查 | "B10 单元格包含 SUM 公式" |
| ❌ 主观判断 | "输出质量很好" |
| ❌ 太模糊 | "包含了相关信息" |
| ❌ 太强 | "精确匹配模板中的每个空格" |

**断言来源：**
- 检查 `expected_output` 中提到的预期
- 查看 with_skill 和 without_skill 的输出差异
- 关注 skill 特有的行为（如使用了特定脚本、遵循了特定格式）

更新两个地方：
1. 各 `eval_metadata.json` 的 `assertions` 字段
2. `evals/evals.json` 的 `expectations` 字段

### 4.5 Step 3 详解：记录执行时间

为每次运行创建 `timing.json`：

```json
{
  "total_duration_seconds": 23.3,
  "executor_start": "2026-04-22T14:30:00Z",
  "executor_end": "2026-04-22T14:30:23Z"
}
```

如果有 token 统计信息，也一并记录。

### 4.6 Step 4 详解：评分 + 聚合 + 报告

#### 4.6.1 评分

代理读取 `agents/grader.md` 评分模板，对每个测试用例的输出逐条判定断言：

- **PASS**：输出中存在清晰证据，且反映了真实的任务完成
- **FAIL**：无证据、证据矛盾、或仅为表面合规
- **不确定时**：举证责任在断言方（视为 FAIL）

评分结果写入 `grading.json`：

```json
{
  "expectations": [
    {
      "text": "输出文件是 .xlsx 格式",
      "passed": true,
      "evidence": "with_skill/outputs/ 中存在 result.xlsx 文件"
    },
    {
      "text": "Excel 包含名为'签署日期'的列",
      "passed": false,
      "evidence": "Excel 中只有 Date 列，没有中文列名"
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  },
  "claims": [
    {
      "claim": "提取了所有 5 个字段",
      "type": "factual",
      "verified": true,
      "evidence": "Excel 包含 5 列，分别对应 5 个目标字段"
    }
  ],
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "输出文件是 .xlsx 格式",
        "reason": "两种配置下都会生成 .xlsx，这条断言无区分力"
      }
    ],
    "overall": "断言检查了格式但未检查字段名的准确性。"
  }
}
```

#### 4.6.2 聚合 Benchmark

运行聚合脚本：

```bash
python3 ~/.config/opencode/skills/skill-creator/scripts/aggregate_benchmark.py D:/path/to/my-skill-workspace/iteration-1 --skill-name my-skill
```

产出：
- `benchmark.json`：结构化统计数据
- `benchmark.md`：人类可读的 Markdown 报告

#### 4.6.3 分析

代理读取 `agents/analyzer.md` 分析模板，对 benchmark 数据进行深度分析：
- 识别**无区分力**的断言（两种配置都 always pass）
- 识别**高方差**的 eval（可能不稳定）
- 分析**时间/token** 的效率权衡

分析结论写入 `benchmark.json` 的 `notes` 字段。

#### 4.6.4 生成审阅报告

```bash
python3 ~/.config/opencode/skills/skill-creator/eval-viewer/generate_review.py D:/path/to/my-skill-workspace/iteration-1 \
  --skill-name "my-skill" \
  --benchmark D:/path/to/my-skill-workspace/iteration-1/benchmark.json \
  --static D:/path/to/my-skill-workspace/iteration-1/review.html
```

产出一个自包含的 HTML 文件，可在任何浏览器中打开。

---

## 5. 审阅测试结果

### 5.1 打开审阅报告

在 Windows 资源管理器中双击 `review.html`，或用浏览器打开。

审阅页面有**两个标签页**：

#### Outputs 标签

逐个浏览每个测试用例：
- 左侧：测试用例列表
- 右侧上方：prompt 和断言列表
- 右侧中间：实际产出（文本文件内联显示，图片/PDF 渲染显示）
- 右侧下方：grading 结果（每条断言的 PASS/FAIL + 证据）
- 底部：**反馈文本框**——在这里写你对这个测试用例的意见

#### Benchmark 标签

展示聚合统计：
- **with_skill vs without_skill** 的通过率对比
- 平均耗时和 token 消耗（mean ± stddev）
- 差异（delta）

### 5.2 如何审阅

重点关注：
1. **with_skill 表现明显优于 without_skill** → skill 价值已验证 ✅
2. **两者差不多** → 断言可能不够强，或 skill 指示不够明确
3. **without_skill 更好** → skill 可能有误导性指令

在反馈文本框中写具体意见，例如：
- "字段名应该用中文而不是英文"
- "输出格式缺少汇总行"
- "这个断言太弱了，两种方式都能通过"

### 5.3 反馈提交

审阅完成后，回到 OpenCode 对话，告诉代理：

> "我看完了，反馈都在报告里了"

或者直接在对话中说明具体意见。

---

## 6. 迭代改进

### 6.1 启动改进

```
/skill-improve D:/path/to/my-skill
```

### 6.2 改进流程

```
┌────────────────────────────────────────────────┐
│ 1. 读取 feedback + benchmark                   │
│ 2. 分析有反馈的测试用例                          │
│ 3. 修改 SKILL.md                               │
│ 4. 在 iteration-2/ 下重跑所有测试                 │
│ 5. 生成对比审阅报告（--previous-workspace）       │
│ 6. 用户审阅 → 回到步骤 1                        │
└────────────────────────────────────────────────┘
```

### 6.3 改进原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **泛化而非过拟合** | 不要针对单个失败用例修修补补 | ❌ "如果是租赁合同就用中文列名" → ✅ "列名使用与原文一致的语言" |
| **保持精简** | 删掉没用或浪费时间的部分 | 如果 skill 指示让模型多做了 3 步无用功，删掉 |
| **解释 why** | 用理解替代命令 | ❌ "MUST use UTF-8" → ✅ "PDF 可能包含中文，用 UTF-8 确保编码正确" |
| **提取重复模式** | 多个测试都产生相同辅助代码时，打包进 scripts/ | 每次都手写 CSV 解析 → 抽成 `scripts/parse_csv.py` |

### 6.4 对比两轮结果

第 2 轮评估时，生成报告时加上 `--previous-workspace` 参数可以看到上轮对比：

```bash
python3 ~/.config/opencode/skills/skill-creator/eval-viewer/generate_review.py D:/path/to/my-skill-workspace/iteration-2 \
  --skill-name "my-skill" \
  --benchmark D:/path/to/my-skill-workspace/iteration-2/benchmark.json \
  --previous-workspace D:/path/to/my-skill-workspace/iteration-1 \
  --static D:/path/to/my-skill-workspace/iteration-2/review.html
```

### 6.5 什么时候停止迭代

满足以下任一条件即可停止：
- 用户表示满意
- 所有反馈都为空（没有改进意见）
- 连续两轮没有实质性进步

---

## 7. 触发准确率优化

> 本节优化 skill 的 `description` 字段，确保 AI 在正确的时候触发 skill。

### 7.1 为什么需要

skill 写得再好，如果 description 不够准确，AI 可能在该用的时候不用，或者不该用的时候乱用。

### 7.2 创建触发测试集

创建一个 JSON 文件（如 `evals/trigger_evals.json`）：

```json
[
  {"query": "帮我提取这份 PDF 表单里的字段", "should_trigger": true},
  {"query": "把这个 PDF 表单的数据填到 Excel 里", "should_trigger": true},
  {"query": "提取 PDF 表单字段并保存到表格", "should_trigger": true},
  {"query": "我有一份 PDF 需要提取表单内容", "should_trigger": true},

  {"query": "帮我读一下这个 PDF 的内容", "should_trigger": false},
  {"query": "把这个 PDF 转成 Word", "should_trigger": false},
  {"query": "合并这几个 PDF 文件", "should_trigger": false},
  {"query": "PDF 加个密码", "should_trigger": false}
]
```

**设计要点：**

| 类别 | 数量 | 要求 |
|------|------|------|
| 正例（should_trigger=true） | 8-10 条 | 覆盖不同表述方式（正式/口语/间接），包含边界场景 |
| 反例（should_not_trigger=false） | 8-10 条 | 重点是**近 miss**——看起来相关但实际不是该 skill 的场景 |

**近 miss 示例：**
- skill 是"提取 PDF 表单" → 反例应该包含"读 PDF"、"合并 PDF"等带 PDF 关键词但不是表单提取的场景

### 7.3 手动触发测试

由于 OpenCode 没有 headless CLI，采用手动测试方式：

1. 展示每条 query 和当前 skill 的 description
2. 判断："AI 看到这个 query 时，会加载这个 skill 吗？"
3. 记录结果

```
query: "帮我提取这份 PDF 表单里的字段"
description: "当用户要求提取 PDF 表单、填写 PDF 字段、将 PDF 表单导出为 Excel 时，使用此 skill。"
判断: 会触发 ✅  (匹配)

query: "帮我读一下这个 PDF"
description: "当用户要求提取 PDF 表单、填写 PDF 字段、将 PDF 表单导出为 Excel 时，使用此 skill。"
判断: 不触发 ✅  (正确拒绝)
```

### 7.4 改进 Description

对于判断错误的 case，修改 description：

**常见问题和对策：**

| 问题 | 对策 |
|------|------|
| 漏触发（该触发没触发） | 在 description 中补充这种表述方式或意图类别 |
| 误触发（不该触发但触发了） | 在 description 中增加排除条件或缩小适用范围 |
| description 太长（>1024 字符） | 删除冗余表述，合并同类项 |
| 描述太笼统 | 增加具体的触发场景和关键词 |

**Description 编写技巧：**
- 用祈使句："使用此 skill 当……"
- 明确边界："此 skill 不适用于……"
- 包含同义词和不同表述方式
- 保持 1024 字符以内

### 7.5 循环优化

```
测试 → 发现问题 → 改 description → 重测 → 直到全部正确
```

---

## 附录：文件结构速查

### OpenCode 配置目录（部署位置）

```
# 全局部署（推荐，所有项目可用）
C:\Users\<用户名>\.config\opencode\
├── agents\
│   ├── skill-executor.md     # 测试执行代理（@skill-executor）
│   └── skill-grader.md       # 评分代理（@skill-grader，只读）
├── commands\
│   ├── skill-create.md       # /skill-create 命令
│   ├── skill-eval.md         # /skill-eval 命令
│   └── skill-improve.md      # /skill-improve 命令
└── skills\
    └── skill-creator\        ← Skill 本体（自包含目录，内部路径全部相对）
        ├── SKILL.md          # 主文件（OpenCode 自动发现）
        ├── agents\           # Prompt 模板（grader.md, comparator.md, analyzer.md）
        ├── scripts\          # Python 工具脚本
        │   ├── aggregate_benchmark.py   # 聚合评分 → benchmark.json + benchmark.md
        │   ├── generate_report.py       # 从 run_loop 输出生成 HTML 报告
        │   ├── improve_description.py   # 基于 eval 结果改进 description（需 claude CLI）
        │   ├── package_skill.py         # 打包 skill 为 .skill 文件
        │   ├── quick_validate.py        # 验证 SKILL.md 格式
        │   ├── run_eval.py              # 触发评估脚本（需 claude CLI）
        │   ├── run_loop.py              # eval + improve 循环（需 claude CLI）
        │   └── utils.py                 # 共享工具函数
        ├── eval-viewer\      # HTML 审阅报告生成器
        │   ├── generate_review.py       # 生成审阅报告（带反馈提交、对比等）
        │   └── viewer.html              # 报告前端模板
        ├── references\       # JSON Schema 定义
        │   └── schemas.md
        └── docs\             # 文档
            └── OpenCode使用指南.md
```

### 评估产出

```
my-skill-workspace/
└── iteration-1/
    ├── eval-0/
    │   ├── eval_metadata.json     # prompt + assertions
    │   ├── with_skill/
    │   │   └── outputs/
    │   │       ├── <产出文件>
    │   │       ├── transcript.md
    │   │       ├── grading.json   # 评分结果
    │   │       ├── timing.json    # 耗时
    │   │       └── metrics.json   # 工具统计（可选）
    │   └── without_skill/
    │       └── outputs/
    │           └── <产出文件>
    ├── eval-1/
    │   └── ...
    ├── benchmark.json             # 聚合统计
    ├── benchmark.md               # 可读报告
    └── review.html                # 审阅页面
```

---

## 快速上手清单

- [ ] 复制 `.opencode/` 和 `opencode.json` 到项目根目录
- [ ] `/skill-create` 创建 skill
- [ ] 编写 2-3 个测试用例到 `evals/evals.json`（expectations 先留空）
- [ ] `/skill-eval <path>` 执行评估
- [ ] 跑完后补充 expectations
- [ ] 代理自动生成 grading + benchmark + review.html
- [ ] 浏览器打开 review.html，填写反馈
- [ ] `/skill-improve <path>` 改进 skill
- [ ] 重复直到满意

