# TDD 开发流程 Skill - 车载中间件专用版

针对车载中间件开发（如升级软件管理、诊断通信等）的 TDD 开发流程 Skill，支持 C++ 语言和 AUTOSAR 标准。

---

## 📦 目录结构

```
tdd-workflow-skills/
├── skills/                              # 4 个 Skill 文件
│   ├── tdd-workflow/SKILL.md            # 主入口，自动路由到各阶段
│   ├── tdd-design/SKILL.md              # 阶段一：详设（SR单号-需求名-design.md）
│   ├── tdd-test-design/SKILL.md         # 阶段二：用例设计（SR单号-需求名-cases.md）
│   └── tdd-coding/SKILL.md              # 阶段三：TDD 编码
├── templates/                           # 模板文件（可自定义）
│   ├── detail-design-template.md        # 详设模板 ⬅️ 替换为部门模板
│   └── test-case-template.md            # 用例模板
└── README.md                            # 本文档
```

---

## 🚀 快速开始

### 1. 安装 Skill

**方式一：用户级别（推荐，所有项目可用）**
```powershell
# Windows
xcopy /E /I "tdd-workflow-skills\skills\*" "%USERPROFILE%\.workbuddy\skills\"
```

**方式二：项目级别（仅当前项目）**
```
在你的项目下创建：
.workbuddy/skills/
  ├── tdd-workflow/
  ├── tdd-design/
  ├── tdd-test-design/
  └── tdd-coding/
```

### 2. 替换部门详设模板

将 `templates/detail-design-template.md` 替换为你们部门的详设模板，**保留以下占位符**：
- `{{SR_NUMBER}}` - SR单号
- `{{FEATURE_NAME}}` - 需求名称
- `{{AUTHOR}}` - 作者

### 3. 使用

启动 WorkBuddy 后直接说：
```
> 我要开发一个新功能：软件升级管理模块
> SR单号：SR20250322001
> 请使用 tdd-workflow skill
```

---

## 🔄 开发流程

```
需求输入 → 详设文档 → 用例设计 → TDD 编码（红-绿-重构）
```

| 阶段 | Skill | 输入 | 输出 |
|------|-------|------|------|
| 详设 | `tdd-design` | 需求描述 + SR单号 | `docs/design/SR{单号}-{需求名}-design.md` |
| 用例 | `tdd-test-design` | 详设文档 | `docs/test-cases/SR{单号}-{需求名}-cases.md` |
| 编码 | `tdd-coding` | 用例文档 | `src/` + `tests/` |

---

## 🎯 质量门禁（车载中间件）

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 函数覆盖率 | 100% | 所有公共API必须测试 |
| 行覆盖率 | ≥ 85% | 可执行代码覆盖 |
| 分支覆盖率 | ≥ 80% | 重点关注错误处理分支 |
| MC/DC 覆盖 | ≥ 100% | ASIL-B/C/D 要求 |
| 负面测试比例 | ≥ 45% | 中间件需更高容错要求 |
| 静态检查 | 0 严重警告 | MISRA C++ / AUTOSAR |

---

## 📝 文档命名规范

所有文档统一使用 **SR单号-需求名** 格式：

```
# 详设文档
SR20250322001-SoftwareUpgrade-design.md

# 用例文档  
SR20250322001-SoftwareUpgrade-cases.md

# 代码文件（保持原有命名）
upgrade_manager.hpp
upgrade_manager.cpp
test_upgrade_manager.cpp
```

---

## 📋 中间件开发特殊考虑

### 1. 状态机设计
- 使用状态模式管理复杂状态转换
- 所有状态转换必须可追踪、可测试
- 支持状态持久化（断电恢复）

### 2. 资源管理
- 使用 RAII 模式
- 内存分配必须有失败处理
- 避免动态内存（AUTOSAR 要求）

### 3. 并发安全
- 状态访问必须线程安全
- 使用互斥锁保护共享状态
- 避免死锁

### 4. 错误处理
- 所有错误码必须明确定义
- 错误信息必须可查询
- 支持错误恢复

---

## 🔧 自定义配置

### 修改详设模板

编辑 `templates/detail-design-template.md`，在保留占位符的前提下添加部门要求：

```markdown
# {{FEATURE_NAME}} - 详细设计文档

**SR单号**: {{SR_NUMBER}}  
**需求名称**: {{FEATURE_NAME}}  
**版本**: v1.0  
**日期**: {{DATE}}  
**作者**: {{AUTHOR}}

---

## [你们部门的章节...]
```

### 修改质量门禁

编辑 `skills/tdd-coding/SKILL.md` 中的阈值：

```yaml
# 质量门禁（可根据部门要求调整）
- 函数覆盖率: ≥ 100%
- 行覆盖率: ≥ 85%
- 分支覆盖率: ≥ 80%
```

---

## 📖 相关标准

- **AUTOSAR Classic Platform** 4.4
- **AUTOSAR Adaptive Platform** 19-03
- **MISRA C++:2008**
- **ISO 26262** 功能安全

---

## 🤝 使用建议

1. **详设阶段**：明确状态机、接口契约、资源需求
2. **用例阶段**：优先设计负面测试（异常、边界、并发）
3. **编码阶段**：严格遵循红-绿-重构循环
4. **审查阶段**：确保满足质量门禁要求

---

## 📞 问题反馈

如有问题或改进建议，请联系部门技术负责人。
