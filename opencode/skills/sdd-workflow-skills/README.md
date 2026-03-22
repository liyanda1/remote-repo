# SDD 开发流程 Skill - 软件设计文档驱动开发

针对软件开发的 SDD（Software Design Document）开发流程 Skill，支持设计驱动开发方法。

---

## 📦 目录结构

```
sdd-workflow-skills/
├── skills/                                  # 4 个 Skill 文件
│   ├── sdd-workflow/SKILL.md                # 主入口，自动路由到各阶段
│   ├── sdd-design/SKILL.md                  # 阶段一：设计（需求级 + 组件级）
│   ├── sdd-test-design/SKILL.md             # 阶段二：用例设计
│   └── sdd-coding/SKILL.md                  # 阶段三：编码实现
├── templates/                               # 模板文件（可自定义）
│   ├── requirement-design-template.md       # 需求级设计模板 ⬅️ 替换为部门模板
│   ├── component-design-template.md         # 组件级设计模板 ⬅️ 替换为部门模板
│   └── test-case-template.md                # 用例模板
└── README.md                                # 本文档
```

---

## 🚀 快速开始

### 1. 安装 Skill

**方式一：用户级别（推荐，所有项目可用）**
```powershell
# Windows
xcopy /E /I "sdd-workflow-skills\skills\*" "%USERPROFILE%\.workbuddy\skills\"
```

**方式二：项目级别（仅当前项目）**
```
在你的项目下创建：
.workbuddy/skills/
  ├── sdd-workflow/
  ├── sdd-design/
  ├── sdd-test-design/
  └── sdd-coding/
```

### 2. 替换部门设计模板

将 `templates/requirement-design-template.md` 和 `templates/component-design-template.md` 替换为你们部门的设计模板，**保留以下占位符**：
- `{{AR_NUMBER}}` - AR单号
- `{{FEATURE_NAME}}` - 需求名称
- `{{COMPONENT_NAME}}` - 组件名称
- `{{AUTHOR}}` - 作者
- `{{DATE}}` - 日期

### 3. 使用

启动 WorkBuddy 后直接说：
```
> 我要开发一个新功能：用户管理系统
> AR单号：AR20250322001
> 请使用 sdd-workflow skill
```

---

## 🔄 开发流程

```
需求输入 → 需求 AR 实现详设（高层）→ 组件详设（低层）→ 用例设计 → 编码实现 → 测试验证
```

| 阶段 | Skill | 输入 | 输出 |
|------|-------|------|------|
| 需求级设计 | `sdd-design` | 需求描述 + AR单号 | `docs/design/AR{单号}-{需求名}-requirement-design.md` |
| 组件级设计 | `sdd-design` | 需求级设计文档 | `docs/design/AR{单号}-{组件名}-component-design.md` |
| 用例设计 | `sdd-test-design` | 设计文档 | `docs/test-cases/AR{单号}-{需求名}-cases.md` |
| 编码实现 | `sdd-coding` | 设计文档 + 用例文档 | `src/` + `tests/` |

---

## 🎯 设计分层

### 需求级设计（高层设计）

**关注点：**
- 系统整体架构
- 模块划分与职责
- 模块间接口契约
- 数据流设计
- 非功能需求

**产出物：**
```
docs/design/AR20250322001-UserManagement-requirement-design.md
```

### 组件级设计（低层设计）

**关注点：**
- 组件内部架构
- 类/结构体设计
- 详细接口定义
- 算法/状态机设计
- 测试场景清单

**产出物：**
```
docs/design/AR20250322001-AuthenticationService-component-design.md
```

---

## 🎯 质量门禁

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 函数覆盖率 | ≥ 90% | 所有公共API必须测试 |
| 行覆盖率 | ≥ 80% | 可执行代码覆盖 |
| 分支覆盖率 | ≥ 70% | 条件分支覆盖 |
| 负面测试比例 | ≥ 40% | 错误/边界场景覆盖 |
| 设计一致性 | 100% | 代码与设计文档一致 |

---

## 📝 文档命名规范

所有文档统一使用 **AR单号-需求名/组件名** 格式：

```
# 需求级设计文档
AR20250322001-UserManagement-requirement-design.md

# 组件级设计文档
AR20250322001-AuthenticationService-component-design.md

# 用例文档  
AR20250322001-UserManagement-cases.md

# 代码文件（保持原有命名）
authentication_service.hpp
authentication_service.cpp
test_authentication_service.cpp
```

---

## 📋 设计驱动开发原则

### 核心原则

```
设计文档是开发的唯一依据
不允许在没有设计文档的情况下开始编码
```

### 开发流程

1. **设计先行**
   - 先完成需求级设计（高层架构）
   - 再完成组件级设计（低层实现）
   - 设计评审通过后再进入编码

2. **测试先行**
   - 基于设计文档编写测试用例
   - 测试用例评审通过后再实现功能

3. **设计一致性**
   - 代码实现必须严格遵循设计文档
   - 如有偏差，需更新设计文档并记录变更

---

## 🔧 自定义配置

### 修改设计模板

编辑 `templates/requirement-design-template.md` 或 `templates/component-design-template.md`，在保留占位符的前提下添加部门要求：

```markdown
# {{FEATURE_NAME}} - SR/AR 需求级设计

**SR/AR单号**: {{REQUIREMENT_NUMBER}}  
**需求名称**: {{FEATURE_NAME}}  
**所属组件**: {{COMPONENT_NAME}}  
**版本**: v1.0  
**日期**: {{DATE}}  
**作者**: {{AUTHOR}}

---

## [你们部门的章节...]
```

### 修改质量门禁

编辑 `skills/sdd-coding/SKILL.md` 中的阈值：

```yaml
# 质量门禁（可根据部门要求调整）
- 函数覆盖率: ≥ 90%
- 行覆盖率: ≥ 80%
- 分支覆盖率: ≥ 70%
```

---

## 🤝 使用建议

1. **组件级设计阶段**
   - 明确组件架构和子模块划分
   - 定义清晰的对外接口契约
   - 考虑非功能需求（性能、可靠性、安全性）

2. **SR/AR 需求级设计阶段**
   - 详细设计类结构和接口
   - 设计状态机和核心算法
   - 输出完整的测试场景清单

3. **用例设计阶段**
   - 优先设计负面测试（异常、边界、并发）
   - 确保测试覆盖所有设计场景
   - 生成可执行的测试代码框架

4. **编码实现阶段**
   - 严格遵循设计文档
   - 先写测试，再实现功能
   - 确保通过所有质量门禁

---

## 📞 问题反馈

如有问题或改进建议，请联系部门技术负责人。
