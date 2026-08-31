# Agent Delegation & Coordination Rules｜Agent 委派与协调规则

本规则定义 Spec Coding 中 Main Agent（主 Agent）与 Subagent（子 Agent）之间的统一协作语义。它适用于正式 Workflow 以及需要 Agent 角色隔离、上下文隔离、独立审查或运行时能力路由的 Applicable Meta Protocol。

本规则不新增 Workflow 阶段，不替代 Task Contract、Verification、Human / Agent Authority 或 Human-Agent Collaboration。核心目标是：**由 Main Agent 持有全局一致性与最终责任，将可独立、可隔离、可验证且权限有界的工作按需委派给合适的 Subagent，并由 Harness 根据当前运行时能力动态选择具体执行方式。**

---

## 1. Roles & Authority｜角色与权限

### Main Agent｜主 Agent

Main Agent 是当前 Workflow 的唯一全局协调与收敛主体，负责：

- 持有当前 Goal、Workflow State、Canonical Context 与关键 Open Item；
- 识别可委派工作并决定串行 / 并行、角色与边界；
- 处理跨任务、跨 Agent 与跨阶段冲突；
- 验证、整合 Subagent 返回结果并更新既有 Canonical Source of Truth；
- 按 [`global-contracts.md`](global-contracts.md) 路由 Authority，并按 [`human-agent-collaboration.md`](human-agent-collaboration.md) 作为默认 Human Interaction Surface；
- 对最终推进结果继续承担责任。

> **Delegate work, not accountability｜委派工作，不转移最终责任。**

### Canonical Subagent Roles｜规范子 Agent 角色

角色按认知职责定义，不按前端、后端、数据库等技术领域固化 Persona：

| Role | 核心职责 | 默认边界 |
|---|---|---|
| `Scout` | 探索项目内部事实，定位入口、链路、依赖与局部上下文。 | Read-oriented；返回压缩 Context / Evidence。 |
| `Researcher` | 获取外部官方资料、标准、当前行为、Benchmark 与技术证据。 | External evidence；不拥有项目决策权。 |
| `Worker` | 在已确认 Contract 内执行具体修改并完成局部验证。 | Scoped write；不得静默改变上游契约。 |
| `Reviewer` | 独立检查候选结果的正确性、完整性、回归与契约一致性。 | 默认只读；形成 Finding / Evidence / Verdict。 |
| `Oracle` | 检查当前方向是否偏离继承决策、约束或已确认事实。 | 只读 Challenge；不成为第二决策主体。 |

`Verifier` 仍表示 Workflow 中的验证职责；`Reviewer` 是需要独立推理型审查时可采用的 Subagent Role。Reviewer 不替代 Deterministic Verification（确定性验证）。

### Authority Boundary｜权限边界

Subagent 在委派边界内自治，但默认不得自行改变：

- Requirement / Acceptance Criteria / Scope；
- 已确认的关键 Design Decision；
- Formal Task 的 Goal / Boundary / Coverage / Verification / Done；
- Workflow State、Accepted Deviation、Risk Acceptance 或其他 Human-owned Decision。

需要突破这些边界时，Subagent 应返回 Evidence、Impact 与 Recommendation，由 Main Agent 按现有 Human / Agent Authority Contract 处理。

> **Subagent may change the delegated result, but not the upstream world that defines the delegation｜Subagent 可以改变被委派工作的结果，但不能自行改变定义该工作的上游契约。**

---

## 2. Delegation & Coordination｜委派与协调

### Delegation Trigger｜委派触发

只有当 Subagent 能带来真实价值时才委派，常见价值包括：

- Context Isolation（上下文隔离）；
- Parallelism（并行）；
- Independent Review（独立审查）；
- Specialized Capability（专门能力）；
- Risk Isolation（风险隔离）；
- Context Refresh / Drift Check（上下文刷新 / 漂移检查）。

没有明显收益时由 Main Agent 直接处理，不为 Multi-Agent 形式本身增加成本。

### Delegability｜委派准入

候选 Work Unit 应按以下维度判断：

- **Independent｜相对独立**：可在有限依赖下独立推进；
- **Context-Isolated｜上下文可隔离**：可提供最小充分局部上下文；
- **Verifiable｜结果可验证**：输出能够由 Evidence、Gate 或独立检查判断；
- **Authority-Bounded｜权限有界**：无需自行重定义上游 Contract；
- **Conflict-Controllable｜冲突可控**：共享写入、依赖与 Ownership 可被 Main Agent / Harness 控制。

明显不满足时，由 Main Agent直接执行、进一步拆分或改为串行。

### Formal Task vs Ephemeral Work｜正式任务与临时工作

Formal Task 不创建第二套 Delegation Artifact。现有 Task Contract 与 Development Execution 中的 Execution Unit 已承担正式执行委派：

```text
Task Contract
+
Scoped Context
+
Agent / Model
+
Tools
+
Workspace
+
Verification Contract
```

Scout / Researcher / Reviewer / Oracle 等非 Formal Task 工作可使用轻量 Runtime Delegation：

```text
Goal
Boundary
Context
Authority
Expected Result
Evidence / Verification
```

这类委派默认不进入 `tasks.md`，不生成独立长期状态；有长期价值的结论应回到原 Canonical Source of Truth。

### Context & Coordination｜上下文与协调

遵循：**Artifact 保持完整，Context 保持最小。**

默认上下文倾向：

- Scout：Fresh + Scoped；
- Researcher：Fresh；
- Worker：Scoped / Forked Contract Context；
- Reviewer：Fresh + Target Artifact；
- Oracle：Decision-rich / Forked Context。

这些属于运行时语义，不要求作为持久字段。

Read-only Work 可在独立时并行；Writing Work 额外遵循：

> **Single Writer Boundary｜单写入者边界：同一可变边界同一时刻只允许一个 Worker Owner。**

Subagent 默认不自行协调共享 Ownership；出现依赖、写冲突或边界重叠时返回 Main Agent，由 Main Agent / Harness 重新划分、串行化或调整 Workspace。

递归委派不是默认模式。即使 Harness 支持 Nested Delegation，也只有显式授权、边界清晰且父级仍承担责任时才允许。

---

## 3. Capability & Model Routing｜能力与模型路由

具体模型、Thinking Effort（思考强度）、Fresh / Fork、Tools、Workspace 与 Fallback 属于运行时策略，不写入 Formal Task 或其他长期 Workflow Artifact。

### Discover First｜先发现运行时能力

模型选择首先基于当前 Coding Agent 实际暴露的 Effective Runtime Capability（有效运行时能力），而不是全局模型排行榜：

```text
Current Coding Agent Runtime
        ↓
Available Models
Supported Thinking Levels
Context Limits
Tool / Modality Support
Per-subagent Routing Capability
Workspace / Isolation Capability
Quota / Availability / Restriction
```

理论 Provider Capability 与当前 Runtime 不一致时，以当前可执行能力为准。

### Evaluate Second｜再补能力证据

只有存在多个有意义候选且选择会实质影响质量、成本或延迟时，才按 `Minimum Sufficient Harness` 原则补充外部证据，例如 Artificial Analysis、OpenRouter、SWE-bench / Hugging Face Benchmark 或其他当前专项评测。

外部 Benchmark 只是 Evidence，不直接成为项目事实源，也不得覆盖 Runtime Fact。必要时同时考虑 Local Execution Evidence（本地实际执行证据）。

### Route Last｜最后完成路由

模型与 Thinking 由以下信息共同决定：

```text
Role Requirement
+
Work Complexity / Risk / Uncertainty / Novelty
+
Context / Tool Requirement
+
Runtime Capability
+
Cost / Latency Constraint
```

目标是：

> **Minimum Sufficient Capability｜最低充分能力：使用能够可靠满足当前 Delegation / Execution Contract 的最低充分模型能力与思考强度，而不是统一使用最强或最便宜配置。**

角色只定义相对能力倾向：

- Scout：优先代码导航、工具可靠性、速度与足够推理；
- Researcher：优先检索、来源判断、综合与事实可靠性；
- Worker：优先 Coding、工具使用、契约遵循与长程执行；
- Reviewer：优先推理、错误发现、Evidence 区分与代码 / 设计理解；复杂 Review 的有效能力不应明显低于被审查 Worker；
- Oracle：优先深度推理、长上下文一致性、矛盾发现与 Trade-off 判断。

Role 不绑定固定 Thinking Level；复杂度、风险和失败历史变化时可动态提高 Context、Thinking 或 Model Capability。

---

## 4. Result, Validation & Escalation｜结果、验证与升级

### Result Handoff｜结果回传

非 Formal Task Subagent 默认返回最小充分结果：

```text
Result
Evidence
Uncertainty
Relevant Risk
Recommended Next Action
```

按角色补充：Scout 返回 Relevant Context；Researcher 返回 Sources / Gaps；Reviewer 返回 Findings / Verdict；Oracle 返回 Drift / Contradiction。

Worker 不使用新的通用 Result Schema，继续使用 Development Execution 已定义的 Verification-ready Result 与 Task Commit / `code_ref`。

### Candidate before Canonical｜候选先于事实源

Subagent Result 默认只是 Candidate Result。Main Agent 应根据风险检查 Evidence、必要时调用 Deterministic Verification、Reviewer 或 Oracle，确认后再更新既有 Requirement、Design、Task、Finding、Evidence 或其他 Canonical Source。

不得建立 `scout-state`、`oracle-state`、`reviewer-truth` 等平行事实源。

### Failure Routing｜失败分流

区分三类问题，但不新增持久状态机：

- **Capability Problem｜能力问题**：上下文不足、模型 / Thinking 不足、工具不可用、Repeated Failure。优先补 Context、提高 Thinking / Model、改变执行策略或使用独立 Review；这通常属于 Execution Attempt 问题。
- **Boundary Problem｜边界问题**：继续工作必须越过当前 Delegation / Task Boundary。返回 Main Agent 重新判断 Task、Design 或依赖。
- **Authority Problem｜权限问题**：进一步涉及 Requirement / AC / Scope / 高影响 Design / Accepted Risk 等，由 Main Agent 进入现有 `Autonomous / Confirm / Human Decision` 路由。

> **Capability failure ≠ Boundary failure ≠ Authority escalation｜能力不足、边界失效与权限升级必须分别判断。**

Fallback 只有在候选配置仍满足当前 Capability Requirement 时才可静默使用；否则应显式降级、升级或阻断，不以“API 可用”视为能力等价。

### Validation & Completion｜验证与完成

Reviewer 只能补充独立判断，不替代正式 Verification；Formal Task 仍按现有 Deterministic Gate、Fresh Review（按需）、Verification Result 与 Task State 收敛。

Subagent 完成仅表示当前 Delegated Work 完成，不自动意味着 Task `Done`、Requirement `Verified`、Finding Closed 或 Workflow 完成。

---

## 5. 使用约定

本规则负责稳定的 Main Agent / Subagent 协作语义；Workflow 只声明局部委派条件或验证需要并引用本规则，不复制角色与调度正文。

Harness Compilation 负责将本规则编译到当前 Coding Agent：发现可用 Agent / Model / Thinking / Tools / Workspace，按需补能力证据，并以最低复杂度实现 Role、Context Isolation、Model Routing、Fallback 与 Runtime Coordination。

最终必须保持：

> **Main Agent owns coherence; Subagents execute bounded work; Harness derives runtime strategy｜Main Agent 持有全局一致性，Subagent 执行有界工作，Harness 动态推导具体运行策略。**
