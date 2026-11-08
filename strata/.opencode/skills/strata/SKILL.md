---
name: Strata 知识库
description: 构建与维护代码知识库：把「场景/能力 → 功能/机制 → IT/UT → 代码」四层用卡片连成可查询的图，支持改代码前查影响面、按能力查覆盖率、扫结构空洞并补全。用户提到建知识库、影响面分析、改代码会影响什么、某功能由哪些用例和代码支撑、补全边界场景时使用。
---

# Strata 知识库

一套 **卡片 → 索引 → 查询** 的工程。你负责读懂语义、写卡片、提问；脚本负责解析、遍历、校验。
每次操作前先跑自检，确认工程在哪、库是什么状态。

所有命令里的 `scripts/strata-run.py` 都指**本 SKILL.md 所在目录**下的脚本。
如果当前工作目录不在 skill 目录内，用绝对路径调用，例如：

```bash
python /path/to/strata/.opencode/skills/strata/scripts/strata-run.py where
```

---

## 建库是一条链，不要让用户记命令

第一次建库只需要一条 `/strata-build`，它会从抽取一路走到补洞。
后面每一步都可以单独跑，但**任何一步做完，你都必须跑一次 `next` 并告诉用户下一条命令**：

```bash
python scripts/strata-run.py next
```

输出形如「下一步：/strata-review，原因：有 31 张草稿没裁决」。照它说，不要自己判断该干嘛。

| 命令 | 在链条里的位置 |
|---|---|
| `/strata-build` | 全流程入口：抽取 → 编译 → 播种 → 裁决 → 补洞 |
| `/strata-init` | 只做抽取 + 编译 + 首播 |
| `/strata-review` | 裁决草稿 |
| `/strata-fill` | 补结构空洞 |
| `/strata-extract` | 代码大改后增量重抽 |
| `/strata-impact` | 日常：改代码前查影响面 |
| `/strata-status` | 日常：看库健康度 |

---

## 开始前必做：自检

```bash
python scripts/strata-run.py where
```

输出会告诉你：工程根、索引是否存在、卡片数、已装领域包、未闭合缺口。

**如果报「还没指定知识库工程在哪」**，按优先级处理，不要自己猜路径：

1. 用户告诉了路径 → 后面所有命令都带 `--home <路径>`（临时生效，不改任何配置）
2. 用户没说 → 让他在代码仓里跑一次
   `python scripts/strata-run.py home set <工程根>`，
   写进 `.opencode/strata.home`，之后不用再带参数
3. 环境变量 `STRATA_HOME` 只在 CI / 容器里用，不要主动推荐给个人用户

---

## 阶段 1 · 初始化（每个仓库只做一次）

1. 确认目标仓库路径，读它的构建文件与测试目录结构。
2. 决定用哪个领域包：
   - 已有 `packs/generic-cpp/`：通用 C++ 库，可直接用。
   - 领域形态特殊（状态机、服务序列、命令集）：需要新写一个包。
     写包前**必须**读 `references/pack-authoring.md`，并按其中「先定 mechanism_key」的顺序来。
3. 跑抽取：

```bash
python scripts/strata-run.py extract <仓库路径>
python scripts/strata-run.py compile
```

4. 把 `compile` 的三个分布念给用户听（槽位、边类型、置信度）。**任何报错都不许跳过**，
   报错意味着卡片格式不合规，按提示改卡片而不是改校验。

---

## 阶段 2 · 播种意图层（模型的主力工作）

抽取器只能从文档标题生成粗糙的「能力」卡片，真正的场景需要你来提议。

1. 读用户指定的文档（需求、设计说明、测试用例名）。
2. 按 `references/card-format.md` 的模板，为每个可辨认的场景写一张 `intent` 卡片：
   - `status: draft`（**不许写 confirmed**）
   - `confidence: possible`（没有代码证据支撑时）
   - `source: llm-proposal`
   - `links` 里指向你判断相关的 `mechanism` 节点，**必须用已存在的 id**
3. 每批不超过 15 张，写完让用户逐条 review。
4. review 后重新 `compile`，把校验错误逐条修掉。

> **不要一次生成几百张。** 一次 10–15 张，用户能看完、能纠错，这才是知识库能长期活下去的原因。

---

## 阶段 3 · 补全（最高频，也是长期成本）

```bash
python scripts/strata-run.py holes
```

六类空洞，处理方式不同：

| 空洞 | 你的动作 |
|---|---|
| `H1-orphan-intent` | 问用户：这个场景由哪个机制实现？还是不该建卡？ |
| `H2-unverified-mechanism` | 问用户：怎么触发、期望什么；有测试就补 links |
| `H3-unmapped-verification` | 先看用例体是否真的没有调用；确认无被测符号则标注说明 |
| `H4-unsourced-edge` | **不许绕过**：这条边缺证据，必须补 `evidence` 或删边 |
| `H5-single-path` | 只提示风险，不强制补 |
| `H6-conflict` | 问用户以哪个为准，改掉其中一条 |

问法的领域差异由包的 `elicitation` 提供；包里没写的空洞用下面的通用问法。
每次提问都**只问一个空洞的一条**，问完立刻写回，再问下一条。

用户回答后：
1. 改对应卡片（补 `links`、补正文、`source: user-answer`、`confidence: likely`）
2. `python scripts/strata-run.py compile`
3. 确认这个空洞消失

**查不到答案时**，登记缺口而不是编造：

```bash
python scripts/strata-run.py gap add --hole H2-unverified-mechanism --question "低电量时收到升级任务应如何处理" --context "state=READY_TO_FLASH"
```

---

## 阶段 4 · 查询（日常最高频）

```bash
# 改了某个符号，会波及哪些用例、机制、能力
python scripts/strata-run.py impact <符号名或卡片 id>

# 直接基于当前 git 改动算影响面（推荐，不用自己找符号）
python scripts/strata-run.py impact-diff
python scripts/strata-run.py impact-diff --staged --limit 20

# 某个能力覆盖了哪些用例和代码
python scripts/strata-run.py coverage "<能力名>"

# 某条边凭什么存在
python scripts/strata-run.py explain_edge <src> <dst> <type>
```

输出按 **确定 / 很可能 / 可能** 三档分组。转述时**必须保留档位**，
不许合并成一个列表，也不许把「很可能」说成「确定」。

`impact-diff` 会先按行范围定位改动点；若改动落在宏、注释、include 上，
会退到「文件级回退」并明确标出——这种情况只能定位到模块，不能定位到函数，要如实转述。

---

## 卡片写入规则（写错就编译不过）

完整字段见 `references/card-format.md`，这里只列最容易错的四条：

1. **边只写在 `frontmatter.links` 里**，正文里的 `[[双链]]` 编译器不认。
2. **`links[].to` 必须是已存在的卡片 id**，写错就是悬空 link，整次编译失败。
3. **`status` 只能写 `draft` 或 `proposed`**；`confirmed` 只能由人或抽取器给。
4. **不许新增 pack 未声明的字段**，编译器会直接报错（这是故意的，防止拼写错误静默失效）。

---

## 停下来问用户的情况

- 自检报找不到工程根 / 索引为空，而用户以为已经有数据
- `compile` 报错且原因不在你刚改的卡片里
- 一个符号名称在库里对应多条记录（重名函数），需要用户指定是哪个文件里的
- 用户要求的场景在现有领域包里没有对应的机制形态（说明要写新包）
- `H4-unsourced-edge`：缺证据的边，只有用户知道该补什么

其余情况自己判断，不要每步都问。
