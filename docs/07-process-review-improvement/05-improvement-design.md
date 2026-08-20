# 5. Improvement Design｜形成改进方案

## 5.1 目标

基于已确认的 `RC-xxx` 根因，判断是否需要改进 Spec Coding / SDD 的可复用规则，并形成少量、明确、可验证的改进方案。

> **改进对象是规则与 Harness 机制本身，而不是某个具体项目产生的 Spec、Plan、Task、Design 或代码。**

---

## 5.2 筛选改进

### 1. 判断是否值得改

结合根因的影响、重复性、风险和现有机制效果，判断是否需要调整规则。

允许结论：

```text
No Process Change
```

避免为了复盘而强行增加规则。

### 2. 判断改进落点

例如：

- Requirement Rule
- Design Rule
- Spec Rule
- Plan / Task Rule
- Implementation Rule
- Verification Rule
- Skill / Rule / AGENTS
- Template / Checklist
- Tooling / Automation

改进应落到最直接承担该问题的规则位置。

---

## 5.3 设计改进

```text
Current State
当前规则或行为
    ↓
Expected State
期望规则或行为
    ↓
Candidate Solutions
候选方案
    ↓
Smallest Effective Change
最小有效改动
    ↓
Decision
最终方案
```

改进可以新增、修改、删除、合并或自动化。

> **优先选择能够直接解决根因、同时对现有流程侵入最小的方案。**

---

## 5.4 验证改进

实施前根据 `expected_state` 定义下一轮验证方式：

- 原问题是否减少或消失。
- 问题是否更早被发现或拦截。
- 是否引入新的明显流程成本。

验证标准尽量在实施前确定。

---

## 5.5 改进产物

统一维护：

```text
improvements.md
```

| 字段 | 说明 |
|---|---|
| `id` | 唯一 `IMP-xxx`。 |
| `title` | 改进名称。 |
| `root_causes` | 一个或多个 `RC-xxx`。 |
| `target` | 需要调整的可复用规则 / Harness 组件。 |
| `current_state` | 当前规则或行为。 |
| `expected_state` | 改进后期望行为。 |
| `candidates` | 主要候选方案。 |
| `decision` | 最终方案。 |
| `change` | 实际需要修改的规则 / Harness 内容。 |
| `validation_plan` | 下一轮如何判断改进有效。 |
| `validation_result` | 下一轮运行后填写。 |
| `status` | 当前生命周期状态。 |

---

## 5.6 下游使用约定

```text
RC-xxx
  ↓
筛选是否改进
  ↓
确定改进落点
  ↓
设计最小有效改动
  ↓
IMP-xxx
  ↓
实施与验证
```

因此，Improvement Design 的最终职责是：

> **将确认的 SDD 根因转化为最小、可复用、可验证的规则改进，为后续实施和验证提供明确输入。**