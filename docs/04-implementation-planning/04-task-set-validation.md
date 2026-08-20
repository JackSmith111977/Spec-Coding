# 4. Task Set Validation｜任务集校验

## 4.1 目标

基于已经定型的 Formal / Executable Task Set，从整体视角确认任务是否完整、对齐、可执行且可验证，并最终达到 Execution Ready。

本步骤重点回答：

> **这些 Task 合在一起，是否足以完整、正确地实现已经确认的需求与技术方案。**

本步骤不重新评审需求或技术方案本身；若发现问题，应定位所属上游阶段并回源修正。

---

## 4.2 覆盖校验

```text
Requirement / AC
       ↓
Design
       ↓
Task
```

重点确认：

- In Scope 的需求是否都有任务承接。
- Acceptance Criteria 是否有对应实施闭环。
- 每个 Task 是否有且只有一个 Primary Requirement，并可稳定计算 `TasksOf(REQ-xx)`。
- Structure、To-Be Flow、Contracts 中的关键变化是否有实施落点。
- Boundary Handling 的重要异常与边界是否进入 Task Coverage。
- Risks / Open Issues 是否已被任务承接或明确保留。

重点发现：`Uncovered Requirement`、`Uncovered Design`、`Uncovered Boundary`、`Unowned Task`、`Unowned Open Item`。

---

## 4.3 一致性校验

重点确认：

- Task 未超出 Scope。
- Task 的 Primary Requirement 与 AC / Trace 不冲突。
- Task 未重新改变 Fixed Decisions。
- 不同 Task 对同一 Contract、状态或规则理解一致。
- Task Boundary 与上游 Design 不冲突。
- 不存在重复、互相矛盾或无来源任务。

```text
Requirement
↕
Design
↕
Task
```

---

## 4.4 可执行性校验

重点确认：

- 不存在循环依赖。
- 必要 Blocking Dependency 已显式记录。
- Task 能获得实施所需上游与依赖上下文。
- 不存在尚未定义但会阻塞实施的中间 Contract 或基础能力。
- Risks / Open Issues 中不存在被遗漏的 Blocking 问题。

没有显式依赖的并行与执行 Wave 仍由 Harness / Agent 在运行时推导。

---

## 4.5 可验证性校验

```text
Goal
  ↓
Coverage
  ↓
Done
  ↓
Verification
```

重点确认 Coverage 足以证明关键行为、Verification 与 Coverage 匹配、Done 可实际验证，以及关键兼容 / 异常 / 边界没有“有实现、无证据”。

同时确认同一 `REQ-xx` 下的 Task 合并后能够覆盖该 Requirement 的 Acceptance Criteria，为后续 Requirement AC Gate（需求级验收门禁）提供可计算边界。

> **验证方式是否真的能够证明目标已经满足。**

---

## 4.6 校验方式

默认采用 **Read-only Validation｜只读校验**。

校验只发现和定位问题，不静默修改 Requirement、Design 或 Task。

```text
Requirement / Rule Gap
    → Requirement Clarification

Design Gap / Conflict
    → Technical Design

Task Boundary Gap
    → Implementation Task Decomposition

Task Definition / Dependency Gap
    → Task Definition & Orchestration
```

修正后只重新校验受影响链路。

简单 Feature 可由单一 Agent 完成；规模较大时，可按覆盖、一致性、依赖、验证维度使用 Subagent 独立检查，再由主 Agent 汇总。

---

## 4.7 产物

```text
Execution Readiness: Ready

Coverage: Pass
Consistency: Pass
Executability: Pass
Verifiability: Pass

Open Risks:
- R02 ...
```

只有存在问题时才输出必要 Findings：

```text
Issue
Source
Impact
Recommended Return Point
```

通过校验的 Task 完成：

```text
Draft → Ready
```

`Ready` 只表示通过规划准入，不代表当前立即 Runnable。

---

## 4.8 完成标准

- 需求、设计、边界与遗留事项有明确任务承接。
- 每个 Task 有明确 Primary Requirement，`TasksOf(REQ-xx)` 可稳定推导。
- Task 与 Scope、Decision、Contract 一致。
- 依赖完整且无明显执行阻塞。
- 每个 Task 的 Verification 能证明 Coverage 与 Done。
- 同一 Requirement 下的任务集合能够支撑需求级 AC Gate。
- 不存在未处理 Blocking 问题。
- 校验问题已完成回源修正并重新对齐。

最终结果：**Execution Ready**。

---

## 4.9 下游使用约定

```text
Formal Task Set
        ↓
Task Set Validation
        ↓
Coverage
Consistency
Executability
Verifiability
        ↓
Draft → Ready
        ↓
Development Execution
```

因此，本步骤的最终职责是：

> **确认任务集能够完整、无冲突且可验证地承接已确认方案，并为开发实施及后续 Requirement 级收敛建立可靠的 Execution Ready 边界。**