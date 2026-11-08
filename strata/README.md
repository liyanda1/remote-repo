# Strata

> strata /ˈstrɑːtə/ — 地层。一层层沉积下来的东西，按顺序读，就能还原它怎么形成的。

把散落的文档、测试和代码，按层沉积成能查、能问、能反查影响面的知识库。
四层结构：**场景 → 功能 → IT/UT → 代码**。

> 📐 完整设计说明与使用手册见 [docs/architecture.html](docs/architecture.html)（含 7 张架构图，浏览器直接打开）

## 三条原则

1. **卡片是事实源，索引是派生物。** 删掉 `index.sqlite` 能一键重建；删掉卡片就真没了。
2. **模型写内容，工具保一致。** 模型负责读懂、提议、提问；工具负责解析、遍历、校验。两者不许越界。
3. **未确认的知识不算知识。** 模型产出只能到 `proposed`，`confirmed` 必须由人或代码证据给出。

## 目录

```
strata.py        命令行入口（python strata.py <cmd>）

core/            内核，零领域内容，不随业务变化
├── schema.yaml      四槽位元模型、边类型、证据字段、空洞规则
├── pack.schema.yaml 写领域包的规范（想接新领域只读这个）
├── base.py          SQLite 存储与路径
├── compiler.py      卡片 -> 索引（单事务重建，失败整体回滚）
├── analyze.py       空洞扫描 / 影响面 / 覆盖查询
├── mcp_server.py    MCP 查询服务（stdio 本机 / HTTP 全组远端共用）
└── viz.py           全景图导出（单文件 HTML，数据内嵌，零前端依赖）

extractors/      抽取器，可插拔
packs/           领域包安装位，默认空
cards/           知识卡片（事实源，进 Git）
├── intent/          场景层
├── mechanism/       功能层
└── verification/    验证层（IT / UT）

.opencode/       skill + 七条命令，复制进你的代码仓即可用
templates/       OpenCode 接入模板（AGENTS 片段 / command / opencode.json）
```

## 快速开始

在 OpenCode 里（推荐）：

```bash
pip install pyyaml                                    # 唯一依赖
cp -r <strata>/.opencode/skills/strata <你的仓>/.opencode/skills/
cp -r <strata>/.opencode/commands    <你的仓>/.opencode/commands/

# 告诉 skill 知识库工程在哪（写一次，之后所有命令都不用带路径）
python <你的仓>/.opencode/skills/strata/scripts/strata-run.py home set <strata 路径>
```

然后敲一条命令走完整条链：**`/strata-build <你的代码仓>`**。
它依次做抽取 → 编译 → 播种场景 → 逐张裁决 → 补空洞，
只在需要你拍板时停下；每步收尾都会告诉你下一条命令是什么。

只查库的人什么都不用装，连服务端就行（见下）。

纯命令行（CI / 调试用）：

```bash
python strata.py extract <repo>        # 从代码仓抽取卡片（C++）
python strata.py compile               # cards/ -> index.sqlite
python strata.py stat                  # 节点 / 边 / 各层规模
python strata.py impact <symbol>       # 改这个符号会波及什么
python strata.py holes                 # 列出六类空洞
python strata.py serve                 # 本机 MCP（stdio）
python strata.py serve --http --host 0.0.0.0 --port 8760 --token <口令>
                                       # 远端 MCP：全组连同一个 URL 共用一份库
python strata.py viz                   # 导出全景图 docs/graph.html（单文件，可直接浏览全部节点）
```

## 全景图

不想对话、想自己逛这张网的时候：

```bash
python strata.py viz                   # 离线导出，生成 docs/graph.html，发给人 / 挂 Git 均可
# 或者服务端起了 HTTP 后，浏览器直接开 http://<主机>:8760/?token=<口令>
```

四列分层浏览全部节点（场景 → 功能点 → 用例 → 代码），点节点看详情和上下游，
搜索支持 `slot:` / `conf:` / `file:` 前缀；文件胶囊上的橙色数字 = 该文件没被
任何用例覆盖的符号数，「只看孤儿」一键筛出全部断连节点。链接即状态：
`#<节点id>` 分享某个节点，`#q=关键词` 分享一次搜索。

## 多人共用

一份索引 + 一个服务端，全组连同一个 URL——不要每人拷一份 `index.sqlite`。

```json
{
  "mcp": {
    "strata": {
      "type": "remote",
      "url": "http://<服务机>:8760/mcp",
      "headers": { "Authorization": "Bearer <口令>" },
      "enabled": true
    }
  }
}
```

服务端只读打开索引：查询请求不可能写坏数据；重建索引是单事务，
读者要么看到旧库要么看到新库，不会看到空库；重编后不用重启服务。

## 接一个新领域

1. 读 `core/pack.schema.yaml`
2. 定 `mechanism_key`（最重要的一步，决定「什么算一个功能点」）
3. 填四个槽位的 label 与 fields
4. 写 1 个 pack 抽取器（core 自带的四个直接复用）
5. 写几条引述模板，把空洞翻译成本领域的问法
6. 放到 `packs/<你的领域>/domain.yaml`

**验收标准：接入新领域不需要改 `core/` 下任何一行。** 需要改，说明抽象错了。

## 卡片的最小结构

```markdown
---
id: <slot_prefix>.<slug>
slot: intent | mechanism | verification | implementation
domain: <pack id>
title: <一句话>
status: draft | proposed | confirmed | disputed
confidence: certain | likely | possible
source: extractor | manual | user-answer | llm-proposal
links:
  - { to: <卡片 id>, type: <edge type>, weight: 0~1 }
evidence:
  - { ref: "<file>:<line> 或 <doc>#<anchor>", note: <说明> }
---

正文：给人看，也给模型当检索上下文。
```

边只认 `frontmatter.links`，正文里的 `[[双链]]` 是给模型看的路标，编译器忽略。
