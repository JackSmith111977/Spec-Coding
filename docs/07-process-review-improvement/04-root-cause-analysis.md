# 4. Root Cause Analysis｜分析根因

## 4.1 目标

基于上一阶段确认的 `ISS-xxx` 问题，分析问题为什么能够发生并逃逸到后续阶段，最终定位到 SDD 流程中缺失、失效或未被正确执行的机制。

本阶段重点回答：

> **为什么现有 SDD 没有更早阻止、发现或纠正这个问题？**

根因分析不应停留在“代码为什么写错”“Agent 为什么漏做”等表层原因，而应继续追溯到 SDD 的发现、闭环、传递、执行、验证或 Harness 机制本身。

---

## 4.2 分析归因

### 1. 前置阶段是否漏掉本该发现的信息

需求、边界、影响或技术约束在更早阶段已有发现条件但未被识别，可能对应 `discovery-gap`。

### 2. 信息是否已经出现，但没有被闭环

Question 已提出但 unresolved、Agent Assumption 后直接继续、待确认事项未持续管理，可能对应 `closure-gap`。

### 3. 信息是否已明确但未正确传到下游

检查 Requirement、Design、Spec、Plan、Task 之间是否信息丢失或消费不完整：

```text
Requirement 已明确
    ↓
Design 已覆盖
    ↓
Spec 遗漏
```

或：

```text
Spec 已明确
    ↓
Plan / Task 未拆解
```

可能对应 `traceability-gap`。

### 4. 下游机制存在，但检查失效

如 Spec 明确但实现错误、测试存在但未覆盖关键路径、Verification 定义检查但执行遗漏。可能对应 `execution-gap` / `verification-gap`。

### 5. Agent 行为或 Harness 约束是否失效

检查上下文、Skill、Rule、工具、Workflow 是否缺失 / 失效 / 未正确执行，以及 Human Intervention 是否暴露系统性薄弱点。可能对应 `workflow-gap`。

### 6. 其他

证据不足时继续追溯，不强行套分类。

---

## 4.3 根因分析原则

- **Evidence First**：每个根因能回溯到 `EV-xxx` 和 `ISS-xxx`。
- **从表象追到机制**：不能停留在“漏做 / 写错 / Agent 没想到”。
- **寻找最早可拦截点**。
- **区分发现与逃逸**。
- **允许一个根因解释多个 Issue**。
- **允许一个 Issue 有多个根因**。
- **避免强行归因**：证据不足时降低 `confidence`。

---

## 4.4 根因类型

| 类型 | 说明 |
|---|---|
| `discovery-gap` | 前置阶段未识别本可提前发现的需求、边界、影响或约束。 |
| `closure-gap` | 关键问题已出现，但没有形成明确结论或持续管理。 |
| `traceability-gap` | Requirement → Design → Spec → Plan → Task 间信息丢失或消费不完整。 |
| `execution-gap` | Spec / Task 已明确，但实施没有正确执行。 |
| `verification-gap` | 问题存在，但测试、Verification 或 Review 未及时发现。 |
| `workflow-gap` | Agent Workflow、Skill、Rule、Context、Tooling 或其他 Harness 机制缺失 / 失效。 |
| `other` | 有充分证据但无法归入以上类型。 |

---

## 4.5 根因分析产物

统一维护：

```text
root-causes.md
```

| 字段 | 说明 |
|---|---|
| `id` | 唯一 `RC-xxx`。 |
| `title` | SDD 层面的根因短名称。 |
| `type` | 根因类型。 |
| `description` | 缺失 / 失效 / 未正确执行的机制。 |
| `issues` | 一个或多个 `ISS-xxx`。 |
| `earliest_stage` | 最早可拦截阶段。 |
| `escape_reason` | 为什么问题未在最早阶段被拦截。 |
| `failed_mechanism` | SDD 中具体失效机制。 |
| `evidence` | 一个或多个 `EV-xxx`。 |
| `confidence` | high / medium / low，可选。 |

---

## 4.6 示例

```yaml
id: RC-001
title: 需求澄清缺少未决事项闭环
type: closure-gap
description: >
  需求澄清过程中已经提出合同来源是否支持搜索这一问题，
  但未确认事项没有被显式保留，也没有要求在进入后续阶段前完成闭环。
issues:
  - ISS-003
earliest_stage: requirement-clarification
escape_reason: >
  未确认的问题没有阻止 Design 和 Spec 继续推进，后续实现因此基于不完整需求信息完成。
failed_mechanism: >
  Requirement Clarification 缺少 unresolved item 的显式管理与 closure 机制。
evidence:
  - EV-007
  - EV-018
  - EV-052
  - EV-054
confidence: high
```

---

## 4.7 下游使用约定

```text
EV-xxx
  ↓
Process Timeline
  ↓
ISS-xxx
  ↓
RC-xxx
  ↓
IMP-xxx
```

因此，Root Cause Analysis 的最终职责是：

> **从具体问题出发，追溯问题为什么发生、为什么能够逃逸，并定位到 SDD 中真正缺失或失效的机制，为后续设计最小、有效、可验证的流程改进提供依据。**