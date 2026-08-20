# 1. Verification Baseline Establishment｜验证基线建立

## 1.1 目标

基于已完成的 Implementation Baseline、Task 结果与实际 Change Set，建立面向完整 Requirement 的 **Verification Baseline（验证基线）**。

本步骤回答：

> **当前完整变更还需要证明什么，以及应以什么方式完成最终验证。**

不重复单 Task 已完成的 Verification，而是补齐跨 Task、关键链路、回归、风险、安全及最终人工验收。

---

## 1.2 接管完整变更

优先接管：

- **Implementation Baseline**：Requirement、Design、Constraints、Risk 等基线引用。
- **Completed Tasks**：Task Boundary、Coverage、Verification 与最终状态。
- **Existing Evidence**：Task 级验收结果与已有确定性证据。
- **Actual Change Set**：最终代码、配置、数据及接口变更。
- **Open Issues / Governance**：遗留风险及明确人工审批；无则省略。

只引用既有事实，必要时沿 Trace 回读上游产物，不重复复制。

---

## 1.3 识别最终验证缺口

重点识别：

- 单 Task 已验证，但跨 Task 组合行为尚未证明。
- 核心端到端业务链路尚未完整验证。
- 实际变更可能影响既有能力，需要回归验证。
- 高风险、安全或关键约束需要独立复核。
- 自动化无法充分证明最终用户或业务意图，需要人工验收。

已有 Evidence 仍有效时优先复用，只重验真正存在缺口或风险的部分。

---

## 1.4 建立验证范围

- **Critical Flow**：必须成立的核心端到端链路。
- **Cross-Task Flow**：需要组合验证的跨任务行为。
- **Regression Scope**：可能受影响的既有能力。
- **Risk / Security Focus**：高风险、安全敏感及关键约束。
- **Runtime Boundary**：验证所需环境、依赖与数据。

验证范围由影响与风险驱动，不默认扩大到全系统。

---

## 1.5 推导验证策略

```text
Source
  ↓
Target
  ↓
Verification Type
  ↓
Method / Requirement
  ↓
Pass Condition
  ↓
Evidence
```

### Deterministic Verification

Build / Static Check、Unit / Integration / Regression Test、Contract / Permission / Data Check、Security Scan、可确定判定 Runtime Check。

### Independent Review

- **Writer / Verifier Separation**：实施与验证尽可能分离。
- **Fresh Context by Default**：独立审查优先隔离上下文。
- **Adversarial Review for Risk**：高风险主动寻找反例。
- **Evidence over Claim**：以可复核 Evidence 为准。

是否采用单个或并行 Verifier Subagent，由执行阶段根据风险和复杂度动态决定。

### Human Acceptance

用于核心用户端到端流程、UI / UX / 视觉交互，以及自动化不足以替代业务最终确认的场景。人工验收由本步骤基于完整需求、实际实现与用户路径动态推导。

---

## 1.6 产物

| 字段 | 内容 |
|---|---|
| `Scope` | 最终验证范围与边界。 |
| `Trace` | Requirement / Design / Task / Change 追溯关系。 |
| `Verification Items` | Target、Type、Method、Pass Condition 与 Evidence。 |
| `Review Focus` | 独立审查 correctness、regression、security 等重点；无则省略。 |
| `Human Acceptance` | 需要人工确认的端到端场景；无则省略。 |
| `Gates` | 必须通过的质量、安全、风险或治理门禁。 |
| `Environment` | 验证所需环境、依赖与数据。 |
| `Open Items` | 尚未解决的问题；无则省略。 |

不展开冗长测试计划，也不固化运行时 Agent 编排策略。

---

## 1.7 完成标准

关键 AC 有最终验证落点，已区分可复用 Evidence 与缺口，Cross-Task / Critical Flow / Regression / Risk / Security 无重大遗漏，三类验证边界明确，关键项有 Pass Condition / Evidence，环境可执行且无基线冲突或不可追溯结论。

最终状态：**Verification Ready**。

```text
Implementation Baseline
        +
Completed Tasks / Evidence
        +
Actual Change Set
        ↓
Verification Gap Analysis
        ↓
Verification Scope
        ↓
Deterministic Verification
Independent Review
Human Acceptance
        ↓
Verification Baseline
        ↓
Verification Ready
```

> **将已经完成任务级验收的完整变更提升到 Requirement / Change 级验证视角，识别剩余正确性证明缺口，并形成轻量、可执行、可追溯的最终验证基线。**