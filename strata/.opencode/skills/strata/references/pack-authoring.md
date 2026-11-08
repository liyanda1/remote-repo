# 写一个领域包

领域包决定「这一层在这个领域里叫什么、什么算一个机制」。
**内核不该出现任何业务词**；一旦你把业务词写进 `core/`，这套东西就只对一个部门有用了。

## 第一步永远是定 mechanism_key

不是写抽取器，不是填槽位，是定这个。

`mechanism_key` 是 1–3 个字段，用来唯一指认一个机制：

| 领域 | key | 含义 |
|---|---|---|
| 流程类（升级、刷写） | `(state, event)` | 某状态下收到某事件，只走一条转移 |
| 序列类（UDS、协议交互） | `(sequence_no, service)` | 序列第几步、哪个服务 |
| 命令类（运维、救援） | `(cmd, args)` | 一条命令加一组参数 |
| 代码库（无状态机） | `(module)` | 一个公共头文件算一个模块 |

**自测方法**：能不能用这组字段唯一指认一个机制，并且别人不会给出第二种拆法？
如果同一个东西能被拆成两个（比如「超时重试」算一次转移还是三次），
说明键少了字段，或者粒度没定死。

## 第二步：映射四个槽位

```yaml
id: ota
name: OTA 升级
version: 1
extends: core

slots:
  intent:
    label: 升级场景
    id_prefix: ota.scn
    fields:
      phase: { type: str }
  mechanism:
    label: 状态转移
    id_prefix: ota.tr
    fields:
      state: { type: str, required: true }
      event: { type: str, required: true }
      guard: { type: str }
  verification:
    label: 测试用例
    id_prefix: ota.tst
    fields:
      phase: { type: str }
  implementation:
    label: 符号
    id_prefix: ota.sym
    fields:
      file: { type: path }
      line: { type: int }

mechanism_key: [state, event]
```

字段类型只能是 `str | int | bool | enum | list | path | ref`。
`enum` 必须给 `values`。

## 第三步：抽取器

能复用内核的就别自己写。内核自带四个：

| 抽取器 | 产出 |
|---|---|
| `gtest` | 测试用例 → verification |
| `coverage` | 覆盖率报告 → exercises 边（置信度 certain） |
| `elf` | 构建产物 → 符号与依赖（certain） |
| `git` | 提交与变更 → 变更历史边 |

领域专有的才写 `kind: pack`：

```yaml
extractors:
  - name: ota_state_machine
    kind: pack
    input: ["src/**/*.cpp", "include/**/*.h"]
    rule: |
      找 enum class *State 的枚举值作为 state；
      找 transition 表或 switch(state) 里的 case 分支提取 event；
      if 条件作为 guard 原文保留。
    emits: [mechanism]
    confidence: certain
```

`rule` 用自然语言写清楚判定依据——它不是给机器读的，是给人复核用的。
半年后你要能凭这段话判断这条边还成不成立。

## 第四步：补洞问法

内核只负责扫洞（六类，规则固定），问法由包提供：

```yaml
elicitation:
  - hole: H2-unverified-mechanism
    ask: |
      转移「{state} + {event}」没有任何用例覆盖。
      1) 它由哪个测试触发？
      2) 期望的上报码是什么？
  - hole: H1-orphan-intent
    ask: |
      场景「{title}」没有对应到任何转移。
      1) 它由哪个状态转移实现？
      2) 还是说这只是一个说明性条目，不该建卡？
```

`{字段名}` 会被替换成节点的实际取值。没写模板的空洞走内核默认问法。

## 第五步：验收

```bash
python .opencode/skills/strata/scripts/strata-run.py extract <repo> --pack <你的包>
python .opencode/skills/strata/scripts/strata-run.py compile
python .opencode/skills/strata/scripts/strata-run.py holes
```

三条硬标准：

1. **没有改 `core/` 下任何一行**。需要改，说明抽象错了，回去重想。
2. 编译零错误。
3. 六类空洞能跑出来，且问法是你这个领域的说话方式。

## 什么时候该改内核

问一句：**改这条规则，会影响两个以上的领域吗？**

- 会 → `core/`，需要评审
- 只影响一个 → 包，随便改，不用联调
