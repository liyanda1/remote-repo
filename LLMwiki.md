# LLM Wiki 

## 背景：知识的困境:为什么我们收藏越多，遗忘越快?

- **信息过载与“收藏即遗忘”**
    论文、文章、截屏散落在各处，信息无法联动，形成一个个信息孤岛，收藏的内容最终沦为“数字垃圾”。

- **传统 RAG的局限**
    将LLM单纯当作“解释器”，每次查询都是“从零开始发现”。查完即焚，无法对历史知识进行有效记忆和积累。

- **核心痛点**：知识无法产生复利
    第100篇笔记不会让第1篇笔记变得更聪明。所有的学习只是线性叠加，而非指数级的增长。



| 对比维度         | 传统 RAG（解释器模式）                                     | LLM Wiki（编译器模式）                                       |
| :--------------- | :--------------------------------------------------------- | :----------------------------------------------------------- |
| **知识状态**     | 静态切片，瞬时记忆，缺乏长期沉淀                           | 结构化产物，持久化存储，形成知识库                           |
| **关联性构建**   | 临时拼凑：查询时即时检索，信息之间缺乏深层逻辑联系         | 网络化链接：预先建立双向链接，形成可漫游的知识网络           |
| **知识积累效应** | 无积累（单次博弈）：每次查询相互独立，无法利用历史结果优化 | 复利增长（持续迭代）：知识随使用不断迭代增值，越用越聪明     |
| **系统可维护性** | 黑盒不可控：内部检索逻辑不透明，难以进行人工干预           | 白盒可追溯：基于 Markdown 文本与 Git 版本控制，可人工审查和回溯 |

## 核心思想

> 基于 Andrej Karpathy llm-wiki 模式的个人知识库系统。 核心理念：**你只负责剪藏，LLM 负责理解和沉淀。**

- **新范式:将LLM视为"编译器”**
    彻底改变传统的运行时检索模式，将原始文档“预先编译”为结构化、高关联度的Wiki产物，构建坚实的知识底座。

- **核心价值:Compounding (复利效应)**
    每一次新的知识输入，都会自动更新旧的关联页面。知识网络在使用中持续迭代生长，实现“越用越聪明”的指数级进化。

解释器"是临时的、一次性的信息拼凑，而“编译器"是长期的、结构化的知识沉淀，LLM Wiki正是构建这种长期价值的最佳实践。

与传统 RAG 的根本区别在于，它将知识「编译一次、持续维护」，而非「每次查询时重新推导」。

```Plain
你（人类）                    LLM（知识库管理员）
     │                                │
     │  剪藏原始来源                    │
     ├───────────────────────────────►│
     │                                │ 读取、理解、提取
     │                                │ 编译到 Wiki 层
     │                                │
     │◄───────────────────────────────┤
     │     浏览 Wiki（只读）            │（维护所有内容）
```

## 核心架构分层

| 层级                            | 归属者         | 核心特性                                            | 核心价值                                             |
| ------------------------------- | -------------- | --------------------------------------------------- | ---------------------------------------------------- |
| Raw 原始层                      | 你（人类）     | 严格的“只读不写”策略，防止原始信息被意外篡改。      | 永远保留未经修改的事实基准，确保知识来源可追溯。     |
| Wiki 编译层                     | LLM 完全拥有   | 由LLM自动生成，包含实体、概念、摘要与双向链接网络。 | 知识的核心载体，实现信息的结构化、网络化呈现与复用。 |
| CLAUDE.md<br />（schema规则层） | LLM 生成并维护 | 一份针对LLM的详细“岗位说明书”与“操作手册”           | 将通用大模型“调教”为懂纪律、懂业务的专属知识管理员。 |

![img](./assets/72ac7f64c41db283051b9e7073d8852f349736137.png)

### 工作流一：摄入

- **动作 · Action**
    将新获取的知识统一放入**raw/文件夹**，触发LLM自动进行内容解析与预处理。

- **联动 · Linkage智能**
    LLM不仅撰写摘要，还会通读现有Wiki主动挖掘交集。一篇新素材通常能触发**10-15个相关概念**页面的自动更新与补充。

- **效果 · Result**
    实现了新知识与旧体系的强行**“缝合”**，让信息流动起来，从根本上避免了知识库中“信息孤岛”的产生。

### 工作流二: 查询与回填

- **高效检索**
    告别复杂的向量数据库依赖，我们建立了轻量级的检索体系，能够快速响应用户的查询需求，精准定位知识源。
    **核心机制:**通过一个简单的``index.md`索引文件，即可快速建立全局映射，实现毫秒级的信息定位。

- **回填机制**
    这是系统的核心闭环逻辑。每一次与大模型的交互，不再是一次性的对话，而是一次知识的生产与积累过程。
    **价值产出:**每次查询得到的高质量回答，都会被**自动存回Wiki**，让知识资产持续增值，避免信息沉没。

### 工作流三: 健康检查

**自动化“捉虫":LLM驱动的知识库审查**
定期让LLM执行类似代码审查中的`Lint`操作，对整个知识库进行全面的自动化健康检查，及时发现潜在问题。

- 矛盾冲突：智能识别A页面与B页面中逻辑相悖、结论相反的内容，消除歧义。
- 过时内容：基于时间戳或内容特征，自动标记可能已失效、不再适用的历史信息。
- 孤立页面：发现没有任何入链和出链的“孤岛”页面，确保知识网络的连通
- 缺失引用：智能提醒应建立但尚未建立的交叉引用，完善知识间的关联逻辑。

**核心目标:建立有序的知识维护体系**
像维护代码库一样维护知识库，通过持续的自动化检查，主动防止知识熵增，确保知识库长期处于健康、准确、有序的状态。



## 文件目录设计

```Plain
knowledge-base/
├── raw/                        # 人类所有，LLM 只读
│   ├── articles/               # 手动保存的文章（Markdown）
│   ├── clippings/              # Obsidian Web Clipper 剪藏（主要入口）
│   ├── images/                 # 截图和图片
│   ├── pdfs/                   # PDF 文件及配套元数据文件
│   ├── notes/                  # 随手记录
│   └── personal/               # ★ 自己写的文章、分析报告、投资笔记
├── wiki/                       # LLM 完全拥有
│   ├── index.md                # LLM 读取的第一个文件，面向内容的索引
│   ├── log.md                  # 仅追加的操作日志（含 graph-excluded: true）
│   ├── overview.md             # 高层综述 + Health Dashboard
│   ├── QUESTIONS.md            # 开放问题队列
│   ├── sources/                # 每个来源的摘要页
│   ├── concepts/               # 思想、模式、技术（含 aliases 跨语言字段）
│   ├── entities/               # 人物、工具、机构、论文
│   ├── synthesis/              # 跨来源合成分析
│   └── templates/              # 页面模板（LLM 使用）
├── outputs/                    # 查询答案、图表、幻灯片、lint 报告
│   ├── lint.md                 # lint 报告
│   └── query.md                # 查询答案
├── scripts/
│   ├── lint.py                 # Wiki 健康检查脚本（9 项检查）
│   └── qmd-reindex.sh          # qmd 索引重建脚本
├── CLAUDE.md                   # LLM 行为契约（核心文件）
└── README.md                   # 项目说明
```

## 推荐插件

| 插件                 | 用途                                                     | 安装方式          |
| -------------------- | -------------------------------------------------------- | ----------------- |
| Obsidian Web Clipper | 浏览器剪藏到 raw/                                        | 浏览器扩展商店    |
| Dataview             | 查询 frontmatter，显示统计                               | Obsidian 社区插件 |
| Marp for Obsidian    | 预览 LLM 生成的幻灯片                                    | Obsidian 社区插件 |
| Graph View（内置）   | 可视化 Wiki 概念关系，建议开启 Node name: Title 显示中文 | 无需安装          |
| Foam（vscode）       | 可视化图谱                                               |                   |

可选工具

| 工具           | 用途           | 何时需要                   |
| -------------- | -------------- | -------------------------- |
| qmd            | 本地搜索索引   | wiki 规模 > 100篇 source时 |
| open code cron | 定时任务自动化 | 需要自动编译 / 检查时      |

**qmd影响：** 知识库小的时候没区别（30 个概念页手动读完全 OK）。但到 100+ 页时，没有 qmd 意味着：

- QUERY 靠读 index.md 猜相关页面，不够精准
- REFLECT 要逐个读全部文件，context 爆炸
- 没有自动索引同步机制



## 搭建步骤

### **安装环境**

- 已安装 Claude Code （codeagent 3.0）/ open code
- Python 3.8+（用于 lint 脚本）
- Obsidian（用于管理本地化知识库，内网不可用）
- qmd 已安装（`npm install -g @tobilu/qmd`）

### Step 1：Bootstrap（基础搭建）

```Bash
mkdir -p ~/knowledge-base
cd ~/knowledge-base
在终端输入：claude code  或者 opencode
```

将以下提示词完整粘贴给 Claude Code：

```Plain
请帮我从零搭建一个基于 Karpathy LLM Wiki 思路的个人知识库系统。
完整执行以下所有步骤，不要遗漏任何细节。

## 一、创建目录结构

创建以下目录：
raw/articles/
raw/clippings/
raw/images/
raw/pdfs/
raw/notes/
raw/personal/
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/synthesis/
wiki/templates/
outputs/
scripts/

## 二、创建系统文件

### wiki/index.md
frontmatter 包含：type: system-index, graph-excluded: true
正文包含：Sources 列表（按日期倒序）、Concepts 列表、Entities 列表、Recent Synthesis 列表、Outputs 列表

### wiki/log.md
frontmatter 包含：type: system-log, graph-excluded: true
说明：仅追加操作日志，格式为「YYYY-MM-DD | 操作类型 | 说明」

### wiki/overview.md
frontmatter 包含：type: system-overview, graph-excluded: true
包含：Knowledge Base Health Dashboard 表格（总来源数、高置信度概念数、开放问题数、Stale 页面数）

### wiki/QUESTIONS.md
frontmatter 包含：type: system-questions, graph-excluded: true
包含：Open Questions 列表（checkbox 格式）、Resolved Questions 列表

## 三、创建页面模板

### wiki/templates/source-template.md
frontmatter 字段：type, title, date, source_url, domain, author, tags, processed, raw_file, raw_sha256, last_verified, possibly_outdated, language, canonical_source
正文结构：## Summary、## Key Points、## Concepts Extracted、## Entities Extracted、## Contradictions（与其他来源的分歧）、## My Notes

### wiki/templates/personal-writing-template.md
frontmatter 字段：type: personal-writing, title, date, status(draft/published/deprecated), topic_tags, confidence_at_writing(low/medium/high), superseded_by, raw_file, raw_sha256, last_verified, tags, processed
正文结构：## Core Argument、## Key Claims、## Evidence Referenced、## Limitations

### wiki/templates/concept-template.md
frontmatter 字段：type: concept, title（中文主名称）, date, updated, tags, source_count, confidence(low/medium/high), domain_volatility(low/medium/high), last_reviewed, aliases（数组，存储中英文所有叫法）
正文结构：## Definition（首行用「中文名（English Name）」格式）、## Key Points、## My Position、## Contradictions、## Sources（仅 wikilinks 列表）、## Evolution Log（每次更新追加一条）

### wiki/templates/entity-template.md
frontmatter 字段：type: entity, title, date, tags, entity_type(person/tool/institution/paper), aliases
正文结构：## Description、## Key Contributions、## Related Concepts、## Sources

### wiki/templates/synthesis-template.md
frontmatter 字段：type: synthesis, title, date, tags, source_count, confidence
正文结构：## Thesis、## Evidence、## Counter-evidence（Stage 0 反向检验结果）、## Synthesis、## Confidence Notes、## Limitations、## Sources

## 四、创建 scripts/lint.py

lint.py 执行以下 9 项检查，完成后将报告写入 wiki/outputs/lint-YYYY-MM-DD.md（frontmatter 含 graph-excluded: true）：

1. YAML frontmatter 合法性：所有 wiki/ 下的 .md 文件是否有合法 YAML frontmatter（含 type 和 date）
2. Broken Wikilinks：[[xxx]] 引用了不存在的页面
3. Index 一致性：wiki/index.md 中标记的文件是否都实际存在
4. Stub 页面：正文少于 100 字的空壳页面
5. 近重复概念名称：slug 名称 Jaccard 相似度 > 0.7 的 concept 页对
6. SHA-256 完整性：raw 文件哈希与 source 页 raw_sha256 字段比对（⚠ SOURCE MODIFIED）
7. Stale 页面：超过 domain_volatility 时效阈值（high=90天, medium=180天, low=365天）
8. 跨语言重复：source URL 相似度检测 + 不同 concept 页的 aliases 字段重叠检测
9. Wikilink 格式规范：检测非英文小写连字符格式的 wikilink（如中文词汇 [[价值投资]]）及别名断链

## 五、创建 CLAUDE.md（行为契约）

CLAUDE.md 是 LLM 的核心行为规范，必须包含以下所有章节：

### 系统概述
- 三层架构说明（Raw/Wiki/Outputs）
- 核心原则：你完全拥有 wiki/ 目录的读取和写入权限，raw/ 目录由我（人类）拥有，你只能读取，绝不修改。

### INGEST 操作规范
触发词：ingest、摄入、处理这个

来源类型判断（优先级由高到低）：
1. frontmatter 含 type: personal-writing → 走「个人写作」流程
2. 文件路径包含 raw/personal/ → 走「个人写作」流程
3. frontmatter 含 type: pdf-reference → 走「PDF 参考」流程
4. 其他 → 走「外部来源」标准流程

缺少 frontmatter 时的处理规则：
- 从文件第一个 # 标题提取 title；若无标题则从文件名推断
- source 字段留空，在 wiki/sources/<slug>.md 中标注「来源未知」
- date 使用文件系统修改时间
- 不中断 INGEST，但在 log.md 记录「警告：来源文件缺少标准 frontmatter」

**外部来源标准流程（11 步）**：
1. 读取目标原始来源（raw/ 中的文件，只读）
2. 计算原始文件的 SHA-256 哈希（Python hashlib）
3. 与用户确认核心要点（逐一摄入，保持参与感）
4. 生成 slug（小写英文，用连字符，例如 `attention-is-all-you-need`）
5. 创建 wiki/sources/<slug>.md（使用 source-template.md），frontmatter 中写入：
   - `raw_file`: 相对路径（如 `raw/articles/filename.md`）
   - `raw_sha256`: SHA-256 哈希值
   - `last_verified`: 摄入日期（YYYY-MM-DD）
   - 若来源发表日期超过 2 年前：标注 `possibly_outdated: true`，并在摘要末尾添加提示
6. **概念名称对齐检查**（提取概念之前必须执行）：
   - 将每个提取到的概念名称统一映射为英文小写连字符 slug（例如「第一性原理」→「first-principles-thinking」）
   - 在 wiki/concepts/ 中查找该 slug 是否已存在对应文件
   - **同时检查所有已有 concept 页的 `aliases` 字段**：遍历 wiki/concepts/*.md，解析每页 frontmatter 的 aliases 列表，检查是否包含当前概念名称（支持中英文别名匹配）
   - 若通过 slug 匹配或通过 aliases 匹配到已有页面：更新已有页面，不创建新页面
   - 若找不到任何匹配：才创建新页面，并在 frontmatter 的 `aliases` 中同时填入中文名和英文名（如果有的话）
7. 为每个提取到的概念：
   - 如果 wiki/concepts/<concept>.md 已存在：更新它，追加新来源引用，在 Evolution Log 追加记录，更新 source_count 和 confidence，**同时更新 last_reviewed 字段**
   - 如果不存在：创建新文件（使用 concept-template.md），**同时在 aliases 字段填入该概念的中英文名称**
   - **Evolution Log 追加规则**：
     - 若本次来源与当前 Definition 一致：写「强化」
     - 若有修正：写「修正：[具体变化]」
     - 若相互矛盾：写「新增分歧：[分歧内容]，见 Contradictions 节」
     - 格式：`- YYYY-MM-DD（N sources）：[本次认知变化的一句话描述]`
8. 为每个提取到的实体：同上逻辑
9. 更新 wiki/index.md：将来源从 Unprocessed 移动到 Processed
10. 读取 wiki/QUESTIONS.md，检查本次来源是否能回答开放问题：
   - 若能：提示用户「此来源可能回答了开放问题：[问题描述]，是否立即执行 QUERY？」
   - 用户确认后，执行 QUERY 并将结果写入 wiki/synthesis/，同时在 QUESTIONS.md 中将该问题移入 Answered
11. 在 wiki/log.md 末尾追加：`YYYY-MM-DD HH:MM | ingest | [来源标题]`

**个人写作流程（不同于标准流程）**：
- 不生成 Summary 节，跳过客观摘要
- 核心论点写入相关 concept 页的 ## My Position 节（标注「个人认知」）
- 不参与 confidence 的 source_count 计数（避免用自己的文章给自己背书）
- 若文章中引用了外部来源，提取这些引用并尝试与已有 wiki/sources/ 页面建立 wikilinks
- raw_sha256 哈希机制同样适用
- Evolution Log 记录：「YYYY-MM-DD 个人写作 [[slug]] 确立了对此概念的明确立场」

### QUERY 操作规范
触发词：直接提问，或「根据我的知识库」

执行步骤：
Step Q1：执行 qmd query "<用户问题>" --json，获取 top 5 相关页面（若 qmd 报错则降级读取 wiki/index.md）
Step Q2：逐一完整读取 top 5 文件
Step Q3：合成答案，每个核心结论必须溯源到具体 wiki/sources/<slug>.md（不允许只引用 concept 页）；注明各来源 confidence 级别；来源相互矛盾时显式标注分歧
Step Q4：若答案具有复用价值，写入 wiki/outputs/YYYY-MM-DD-<topic>.md，文件 frontmatter 含 graph-excluded: true；在输出末尾包含「⚠ Confidence Notes」节；更新 wiki/index.md 的 Recent Synthesis 列表；追加 wiki/log.md

输出格式按问题类型：
- 普通问题 → Markdown 正文
- 比较类 → Markdown 表格
- 演示类 → Marp 幻灯片（frontmatter 加 marp: true）
- 趋势类 → Python matplotlib 代码块
- 清单类 → 结构化 bullet list

### LINT 操作规范
触发词：lint、检查、健康检查

执行步骤：
1. 运行 scripts/lint.py（包含 9 项检查）
2. 将报告写入 wiki/outputs/lint-YYYY-MM-DD.md（frontmatter 含 graph-excluded: true）
3. 执行 qmd status，对比索引文件数与 wiki/ 实际 .md 文件数（排除系统文件）；若索引落后则执行 qmd add wiki/，在报告中记录
4. 向用户展示摘要并询问是否修复

### REFLECT 操作规范
触发词：reflect、综合分析、发现规律

四阶段执行：
Stage 0（反向检验）：在生成任何合成结论之前，主动搜索反驳证据。若无反对来源，在 Limitations 节标注「⚠ 回音室风险：未找到反驳来源，结论可能存在确认偏差」
Stage 1（模式扫描）：使用 qmd 批量扫描
  qmd multi-get "wiki/concepts/*.md" -l 40
  qmd multi-get "wiki/entities/*.md" -l 40
  qmd multi-get "wiki/synthesis/*.md" -l 60
  识别跨来源模式、隐性关联、内容空白、矛盾对
Stage 2（深度合成）：对有证据支撑的候选项，完整读取相关页面，写入 wiki/synthesis/<topic>-synthesis.md
Stage 3（Gap Analysis）：
  - source_count = 1 且创建超过 30 天的孤立概念
  - 多处提及但无独立页面的概念/实体（隐性盲区）
  - 覆盖明显稀薄的主题领域
  - 输出到 wiki/outputs/gap-report-YYYY-MM-DD.md（frontmatter 含 graph-excluded: true）

完成后更新 wiki/overview.md 的 Health Dashboard，更新 wiki/index.md，追加 wiki/log.md

### MERGE 操作规范
触发词：merge、去重

同语言合并流程：
1. 与用户确认合并方案（绝不自动合并）
2. 主 slug 保留，被合并页面的 wikilinks 全部更新
3. 被合并文件替换为重定向文件（内容：redirect: [[wiki/concepts/主slug]]）
4. log.md 记录：YYYY-MM-DD | merge | [旧slug] → [主slug]

跨语言合并专项流程（区别于同语言 MERGE）：
1. 主 slug 保留英文
2. aliases 取两个页面的并集
3. Key Points / Sources / Evolution Log 按并集+去重合并
4. My Position 若两页都有，先向用户展示对比后再合并
5. 被合并的旧 slug 文件保留为 redirect 文件（确保旧 wikilinks 不 broken）
6. log.md 记录：YYYY-MM-DD | merge | [旧slug] → [主slug]（跨语言合并）

### ADD-QUESTION 操作规范
触发词：我想搞清楚、add question、记录一个问题

执行步骤：
1. 将问题规范化（提取核心疑问）
2. 追加到 wiki/QUESTIONS.md（checkbox 格式：- [ ] 问题内容（opened YYYY-MM-DD））
3. 追加 wiki/log.md

### Wikilink 使用规范

**格式铁律（不可违反）**：
所有 wikilink 目标必须使用英文小写连字符格式
✅ [[value-investing]]  ✅ [[attention-mechanism]]  ✅ [[warren-buffett]]
❌ [[价值投资]]（中文词汇）❌ [[ValueInvesting]]（驼峰）❌ [[value_investing]]（下划线）

中文名称的正确处理方式：
- 写入 concept 页 frontmatter 的 aliases 字段
- concept 页正文第一行使用括号标注：「价值投资（Value Investing）」
- wikilink 始终用英文 slug

**允许使用 wikilinks 的场景**：
- concept 页引用其他 concept/entity 页
- source 页引用 concept/entity 页
- synthesis 页引用 concept/source/entity 页

**禁止使用 wikilinks 的场景**：
- 任何页面不得引用系统文件：[[log]] [[index]] [[overview]] [[QUESTIONS]]
- 任何页面不得引用 lint 报告：[[outputs/lint-xxx]]
- 任何页面不得以操作名称作为 wikilink：[[ingest]] [[query]] [[reflect]]
- log.md 内部记录使用纯文本路径（如 wiki/sources/xxx.md），不使用 wikilinks

### Wiki 语言规范
- Wiki 层（concept/entity/synthesis 页）统一用中文写作
- concept 页 title 字段使用中文主名称（图谱节点显示）
- 英文术语在 concept 页首次出现时括号标注：「注意力机制（Attention Mechanism）」
- 所有 slug（文件名）统一用英文小写连字符，不使用中文文件名
- aliases 字段覆盖中英文所有叫法

### Confidence 更新规则
| 来源数量 | Confidence | 处理方式 |
|---|---|---|
| 1 个来源 | low | 自动设置 |
| 3+ 个来源 | medium | 自动设置 |
| 5+ 个来源且无重大矛盾 | 候选 high | 向用户展示 Definition 和 Sources 列表，等待确认 |
| 用户明确回复「确认」或「ok」| high | 才可设置 |

注意：个人写作（raw/personal/）不参与 source_count 计数

### Source Integrity Rules
- re-ingest 规则：若 lint 报告 ⚠ SOURCE MODIFIED，需重新摄入该文件并更新所有受影响的 concept/entity 页面，Evolution Log 记录「YYYY-MM-DD 来源更新：[[slug]] 哈希变更，内容已重新提取」
- 来源超过 2 年标注 possibly_outdated: true
- 矛盾来源必须在 source 页和 concept 页的 Contradictions 节显式记录，不得静默覆盖

### 系统文件隔离规则
以下文件的 frontmatter 必须含 graph-excluded: true，不参与 Obsidian 图谱：
- wiki/log.md
- wiki/index.md
- wiki/overview.md
- wiki/QUESTIONS.md
- wiki/outputs/ 下所有文件

### 文档维护规则
当 CLAUDE.md 规则更新时，同步更新 USER_GUIDE.md 对应章节，确保两份文档一致。

## 六、初始化 qmd 索引

执行：
qmd add wiki/
qmd status

## 八、执行完成后的验证

输出以下验证报告：
1. 目录结构树（tree -L 3 或 find）
2. CLAUDE.md 包含的章节列表
3. wiki/templates/ 下的模板文件列表
4. qmd status 输出（索引文件数量）
5. scripts/lint.py 包含的检查项列表
```

### Step 2：标定（首次使用前必做）

> Karpathy 原文特别强调：在正式批量处理前，先交互式标定 2-3 篇最典型的来源，审查输出质量后再调整 CLAUDE.md。

```Bash
# 先放入 1 篇测试文章
cp ~/你的文章.md ~/knowledge-base/raw/articles/

# 告诉 Claude Code
你：ingest raw/articles/你的文章.md
# 仔细审查：摘要质量、概念提取是否准确、wikilinks 格式是否正确
# 若不满意，告诉 LLM：请更新 CLAUDE.md，以后处理 [情况] 时要 [规范]
```

**标定后再处理剩余文章，避免大量文章风格不一致。**

### Step 3：全系统 Audit

搭建完成后，执行一次完整的系统状态核查，确认所有规则已落地：

```Plain
请对当前知识库做一次完整的系统状态核查，逐项验证以下内容，
输出核查报告到 wiki/outputs/system-audit-YYYY-MM-DD.md：

## 一、目录结构完整性
验证 raw/ 和 wiki/ 下所有子目录是否存在

## 二、CLAUDE.md 关键规则覆盖（逐项输出是/否）
- [ ] Raw 层不可变原则
- [ ] INGEST 来源类型判断（personal-writing vs 外部来源）
- [ ] INGEST SHA-256 哈希记录规则
- [ ] INGEST 去重检测（含 canonical_source 译文检测）
- [ ] INGEST 概念名称对齐检查（aliases 匹配）
- [ ] INGEST QUESTIONS.md 匹配检查
- [ ] INGEST 缺少 frontmatter 的处理规则
- [ ] INGEST URL 直接输入的 defuddle 调用规则
- [ ] INGEST 最后一步执行 qmd update
- [ ] QUERY 使用 qmd query 优先（含 fallback）
- [ ] QUERY 来源溯源要求（追溯到 sources 页）
- [ ] QUERY Confidence Notes 输出要求
- [ ] QUERY 高价值答案持久化规则
- [ ] confidence: high 必须用户确认，禁止自动晋升
- [ ] LINT 运行 scripts/lint.py（9 项检查）
- [ ] LINT 执行 qmd 索引同步验证
- [ ] REFLECT Stage 0 反向检验
- [ ] REFLECT Stage 1 使用 qmd multi-get 批量扫描
- [ ] REFLECT Stage 3 Gap Analysis
- [ ] MERGE 跨语言合并专项流程（redirect 文件保留）
- [ ] Wikilink 格式铁律（英文小写连字符）
- [ ] Wikilink 禁止清单（系统文件不得被 wikilink）
- [ ] Wiki 语言规范（中文写作，英文 slug，aliases 跨语言）
- [ ] 系统文件隔离规则（graph-excluded: true）
- [ ] 文档维护规则（CLAUDE.md 更新时同步 USER_GUIDE.md）

## 三、模板文件完整性（逐项验证必需字段）
- [ ] source-template.md 含 language / canonical_source
- [ ] personal-writing-template.md 含 type: personal-writing / confidence_at_writing
- [ ] concept-template.md 含 aliases / domain_volatility / last_reviewed / Evolution Log
- [ ] entity-template.md 含 aliases
- [ ] synthesis-template.md 含 Counter-evidence / Confidence Notes / Limitations

## 四、系统文件隔离状态
- [ ] wiki/log.md 含 graph-excluded: true
- [ ] wiki/index.md 含 graph-excluded: true
- [ ] wiki/overview.md 含 graph-excluded: true
- [ ] wiki/QUESTIONS.md 含 graph-excluded: true

## 五、scripts/lint.py 检查项（验证是否包含全部 9 项）

## 六、qmd 状态
- qmd status 输出（索引文件数量）
- 执行一次测试查询，输出 top 3 结果

输出：✅ 通过 / ❌ 未通过（含缺失内容） / 建议修复优先级
```



## 操作详解

### INGEST — 摄入

**触发词**：`ingest`、`摄入`、`处理这个`

**外部来源流程**（raw/articles/、raw/clippings/、raw/pdfs/）：

```Plain
ingest raw/articles/my-article.md
```

LLM 会按顺序执行：

1. 计算原始文件的 SHA-256 哈希
2. 与你确认核心要点
3. 创建 `wiki/sources/<slug>.md`，frontmatter 中写入 `raw_sha256` 和 `last_verified`
4. 提取概念和实体，创建/更新 `wiki/concepts/` 和 `wiki/entities/` 页面
5. 更新 concept 页的 Evolution Log（强化/修正/分歧）
6. 若来源超过 2 年前，标注 `possibly_outdated: true`
7. 检查 `wiki/QUESTIONS.md`，若有来源能回答的问题则提示你
8. 更新 `wiki/index.md`
9. 在 `wiki/log.md` 追加记录

**个人写作流程**（raw/personal/）：

```Plain
ingest raw/personal/my-investment-analysis.md
```

LLM 会：

- 不生成 Summary 节，跳过客观摘要
- 将核心论点提取后写入相关 concept 页的 `## My Position` 节（标注「第一手认知」）
- 在 Evolution Log 记录：「YYYY-MM-DD 个人写作 slug 确立了对此概念的明确立场」
- **不参与 confidence 的 source_count 计数**（避免用自己的文章给自己背书）
- 若文章引用了外部来源，尝试建立 wikilinks

**预期耗时**：每篇文章 1-3 分钟。建议前 5 篇逐一处理确认质量后再批量。

### QUERY — 查询

**触发词**：直接提问即可，或说「根据我的知识库」

**示例**：

```Plain
根据我的知识库，什么是最重要的开发原则？
帮我对比 A 和 B 这两个概念
```

**LLM 的执行步骤**：

1. 读取 wiki/index.md，识别最相关的 3-5 个页面
2. 读取这些页面
3. **每个核心结论必须追溯到具体的 wiki/sources/slug 页面**（不允许只引用 concept 页）
4. 将答案写入 `wiki/outputs/<slug>-YYYY-MM-DD.md`
5. **在输出文件末尾必须包含「⚠ Confidence Notes」节**，列出所有 low/medium confidence 的引用
6. 更新 `wiki/index.md` 的 Recent Synthesis 列表
7. 在 `wiki/log.md` 追加记录

### LINT — 健康检查

**触发词**：`lint`、`检查`、`健康检查`

```Bash
你：lint
```

**lint.py 检查项**：

| #    | 检查项             | 说明                                                         |
| ---- | ------------------ | ------------------------------------------------------------ |
| 1    | Frontmatter 完整性 | 所有 .md 文件是否有合法 YAML frontmatter（含 type 和 date）  |
| 2    | Broken Wikilinks   | [[xxx]] 引用了不存在的页面                                   |
| 3    | Index 一致性       | index.md 中标记为 processed 的来源是否有对应文件             |
| 4    | Stub 页面          | 正文少于 100 字的空壳页面                                    |
| 5    | SHA-256 完整性     | raw 文件哈希与 source 页记录的哈希是否一致（⚠ SOURCE MODIFIED） |
| 6    | Stale 页面         | 超过时效阈值的 concept 页面（根据 domain_volatility）        |

**Staleness 时效阈值**：

- domain_volatility: high → 90 天
- domain_volatility: medium → 180 天
- domain_volatility: low → 365 天

**输出**：`wiki/outputs/lint-YYYY-MM-DD.md` 报告文件，同时终端打印摘要。

**建议频率**：每两周一次。

### REFLECT —综合分析

**触发词**：`reflect`、`综合分析`、`发现规律`

**四阶段执行**：

**Stage 0（反向检验）**：在生成任何合成结论之前，主动在已有 sources 中搜索与候选结论相矛盾的证据。若找不到反对声音，在 Limitations 节标注：「⚠ 回音室风险：未找到反驳来源，结论可能存在确认偏差」

**Stage 1（模式扫描）**：仅扫描 index.md，识别跨来源的模式、隐性关联、内容空白、可能的矛盾对。

**Stage 2（深度合成）**：对有证据支撑的候选项，写入 `wiki/synthesis/<topic>-synthesis.md`。

**Stage 3（Gap Analysis）**：

- 找出 source_count = 1 且创建超过 30 天的页面（孤立概念）
- 找出多个 sources 提及但尚无独立页面的概念/实体（隐性盲区）
- 找出知识库覆盖明显稀薄的主题领域
- 输出到 `wiki/outputs/gap-report-YYYY-MM-DD.md`

**完成后**：更新 `wiki/overview.md` 的 Health Dashboard，更新 `wiki/index.md` 的 Recent Synthesis，在 `wiki/log.md` 追加记录。

**建议频率**：每月一次，或每积累 10 篇新来源后一次。

### ADD-QUESTION — 记录问题

**触发词**：`我想搞清楚`、`add question`、`记录一个问题`

**示例**：

```Plain
你：我想搞清楚价值投资和成长投资的核心区别是什么
LLM：（规范化问题 → 追加到 wiki/QUESTIONS.md → 记录到 log）
```

**执行步骤**：

1. 将问题规范化（提取核心疑问）
2. 追加到 `wiki/QUESTIONS.md` 的 Open Questions： 

```Plain
- [ ] 价值投资和成长投资的核心区别是什么（opened YYYY-MM-DD）
```

1. 在 `wiki/log.md` 追加记录

**当 ingest 时**，LLM 会检查新来源是否能回答开放问题，若是则提示你。

### MERGE — 去重合并

**触发词**：`merge`、`去重`

**典型场景**：

- `wiki/concepts/attention.md` 和 `wiki/concepts/attention-mechanism.md` 内容重叠
- Lint 报告发现大量指向同一主题的不同名称页面

**执行前 LLM 会先与你确认合并方案**，不会自动合并。合并后更新所有指向被合并页面的 wikilinks。

## Frontmatter 规范

### 所有页面必须包含

```YAML
---
type: <page-type>
title: "页面标题"
date: YYYY-MM-DD
tags: [wiki, wiki/<type>]
---
```

### Source 页（外部来源）额外字段

```YAML
---
type: source-summary
title: "{{title}}"
date: YYYY-MM-DD
source_url: "{{url}}"
domain: "{{domain}}"
author: "{{author}}"
tags: [wiki, wiki/source]
processed: true
raw_file: "raw/articles/filename.md"   # 相对路径
raw_sha256: "<64-char-hex>"            # SHA-256 哈希
last_verified: YYYY-MM-DD              # 最近一次验证哈希的日期
possibly_outdated: false               # 来源是否超过 2 年
---
```

### Source 页（个人写作）额外字段

```YAML
---
type: personal-writing
title: "{{title}}"
date: YYYY-MM-DD                      # 写作日期（非摄入日期）
status: draft                          # draft / published / deprecated
topic_tags: []
confidence_at_writing: medium          # 写作时对内容的把握程度
superseded_by: ""                      # 若有更新的文章，填入新文章路径
raw_file: "raw/personal/filename.md"
raw_sha256: "<hash>"
last_verified: YYYY-MM-DD
tags: [wiki, wiki/source]
processed: true
---
```

### Concept 页额外字段

```YAML
---
type: concept
title: "{{title}}"
date: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [wiki, wiki/concept]
source_count: 0         # 引用此概念的外部来源数量
confidence: low         # low / medium / high
domain_volatility: medium  # low / medium / high
last_reviewed: YYYY-MM-DD  # 最近一次更新此概念的日期
---
```

### Confidence 更新规则

| 来源数量              | Confidence 值 | 说明                             |
| --------------------- | ------------- | -------------------------------- |
| 1 个来源              | low           | 自动                             |
| 3+ 个来源             | medium        | 自动                             |
| 5+ 个来源且无重大矛盾 | 候选 high     | 禁止自动晋升                     |
| 用户确认后            | high          | 必须用户明确回复「确认」或「ok」 |

> **注意**：个人写作（raw/personal/）不参与 source_count 计数。

### Evolution Log 格式

```Plain
## Evolution Log

<!-- 每次更新此概念页时追加一条 -->- 2026-04-06（2 sources）：强化：来自 [[wiki/sources/attention-paper]] 和 [[wiki/sources/transformer-blog]] 的证据一致
- 2026-04-10（3 sources）：修正：新增 [[wiki/sources/new-source]] 显示原定义忽略了 X 维度
```

## Confidence 与来源完整性

### 为什么 confidence: high 不能自动晋升？

系统升级前，5 个来源就能让一个概念自动变成「高置信度」。但这会产生错误复利：错误的概念一旦被标记为 high，后续 query 就会大量引用它，形成自我强化。

升级后的机制：

- 达到 5 个来源 → 进入「候选 high」状态
- LLM 必须向你展示该 concept 页的完整 Definition 和 Sources 列表
- 你明确回复「确认」后，confidence 才变为 high
- high 是你的**主动背书**，不是计数器的输出

### 如何判断是否确认 high？

LLM 会问：「概念 X 现在有 5+ 个来源且无矛盾，是否确认 confidence 为 high？」你需要回顾：

- 这些来源的权威性如何？
- 定义是否经过你的审查和认可？
- 你自己是否认同这个定义？

只有在你真正理解和认可时才能确认。

### SHA-256 完整性守护

每次 ingest 时，LLM 计算原始文件的 SHA-256 哈希并写入 source 页 frontmatter。Lint 时会重新计算并比对。如果 raw 文件在你不知情的情况下被修改（哪怕是一个字符），lint 就会报告 ⚠ SOURCE MODIFIED，提示你重新摄入。

## 常见问题

### Q：我编辑了 raw 文件，LLM 会知道吗？

**不会主动知道**。但下次运行 `lint` 时，lint.py 会检测到 SHA-256 哈希变化，报告 ⚠ SOURCE MODIFIED，并建议你重新摄入。重新摄入后会更新所有受影响的 concept/entity 页面，并在 Evolution Log 记录变更。

### Q：如何处理自己写的旧文章？

将文章放入 `raw/personal/` 目录，然后用 `ingest raw/personal/你的文章.md` 处理。LLM 会识别为 personal-writing 来源：

- 提取核心论点写入相关 concept 页的 `## My Position` 节
- 在 Evolution Log 记录立场确立
- 不参与 confidence 计数（避免用自己的文章给自己背书）

### Q：confidence: high 是怎么产生的？

**不能自动产生**。当一个 concept 达到 5+ 个外部来源且无重大矛盾时，LLM 会暂停并请求你确认。你明确回复「确认」或「ok」后，confidence 才更新为 high。这是你对知识库内容的主动背书，而非系统自动判断。

### Q：如何查看知识库健康状态？

查看 `wiki/overview.md` 的 Knowledge Base Health Dashboard，每次执行 REFLECT 后自动更新。包含：总来源数、高置信度概念数、开放问题数、Stale 页面数、孤立概念数、知识密集/空白领域等指标。

### Q：如何避免错误复利？

1. **Confidence 门控**：high 必须你确认，不能自动晋升
2. **溯源到 source**：每个核心结论必须追溯到具体 source 页，不允许只引用 concept
3. **回音室风险检查**：REFLECT Stage 0 会主动搜索反驳证据
4. **矛盾显式标注**：Evolution Log 记录认知变化，Contradictions 节记录分歧
5. **Staleness 衰减**：长期未更新的概念会被标记，避免过时内容自我强化

### Q：来源超过 2 年会怎样？

LLM 会在 source 页的 frontmatter 标注 `possibly_outdated: true`，并在摘要末尾添加提示。这不是说你不能用它，而是提醒你在基于该来源做决策时要额外谨慎。

### Q：LLM 会不会用旧来源的答案回答新问题？

不会。每次 QUERY 时 LLM 会先读取 index.md 识别相关页面，然后综合多个来源的证据合成答案。系统设计鼓励不断用新来源更新已有概念页（同时更新 last_reviewed 和 Evolution Log），而不是让旧内容持续占据主导。

### Q：CLAUDE.md 需要我自己维护吗？

CLAUDE.md 会随你的使用自然演化。当你发现 LLM 的某类输出不符合期望时，告诉它「请更新 CLAUDE.md，以后处理 [情况] 时要 [规范]」，让 LLM 自己更新行为契约。

