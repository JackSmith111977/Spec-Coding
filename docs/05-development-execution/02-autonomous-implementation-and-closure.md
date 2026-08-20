# 2. Autonomous Implementation & Closure｜自治实施与闭环

## 2.1 目标

基于 Execution Unit，由 Worker Agent 在既定 Task Contract 与 Workspace 内自主完成实现、运行反馈与局部修复，并将结果收敛为可进入正式验证的 Verification-ready Result（待验收结果）。

本步骤重点回答：

> **Worker 如何在不突破既定任务契约的前提下，以最短反馈回路完成实现并形成稳定、可送验的结果。**

只负责单 Task 自治实施与局部闭环，不重新调度任务、不修改 Requirement / Design，也不最终判定 `Done`。

---

## 2.2 接管执行单元

优先确认：

- **Task Contract**：Goal、Boundary、Coverage、Done 是否清晰。
- **Scoped Context**：是否足以开始当前任务。
- **Dependency Result**：依赖结果是否可用。
- **Workspace**：是否处于正确共享 / Worktree / 隔离环境。
- **Verification Contract**：最终需要满足哪些验证要求。

```text
Execution Unit
      ↓
确认目标与边界
      ↓
确认代码入口与依赖
      ↓
开始实施
```

局部信息不足时通过 Search、Read、Runtime Inspect 按需拉取；只有明显大上下文缺口时才请求 Scout / Supervisor。

> **Ready to execute, not fully informed｜具备正确开工条件即可，不追求一次性装载全部上下文。**

---

## 2.3 自治实现与运行探索

Worker 在 Task Contract 内自主选择具体实施路径，可动态搜索 / 阅读代码、选择文件与局部结构、增加辅助代码 / 测试 / 调试脚本，并利用 API、Browser、DB、Logs、Trace 等运行时能力理解真实行为。

```text
Inspect
   ↓
Hypothesize
   ↓
Implement
   ↓
Run / Observe
   ↓
Adjust
   ↺
```

实施过程中优先通过真实代码与运行证据推进。

Worker 可以调整 Implementation Strategy，但不得自行改变 Requirement / Acceptance Criteria、已固定 Design Decision、Task Goal / Boundary / Coverage、Verification Contract。

> **Contract-bound Autonomy｜契约边界内自治。**

---

## 2.4 局部验证与自修闭环

```text
Implement
    ↓
Local Check
    ↓
Passed?
 ┌────┴────┐
 No        Yes
 ↓          ↓
Diagnose   Continue
 ↓
Repair
 └────────↺
```

优先使用 Typecheck / LSP / Compile / Build、Unit / Focused Integration Test、API / Contract、DB / 状态检查、Browser / E2E 局部路径、Logs / Trace / Runtime Observation。

> **Deterministic First｜确定性验证优先。**

能够在当前 Task Contract 内解决的问题，由当前 Worker 直接诊断、修复并重验，不额外交接 Agent。

---

## 2.5 收敛送验结果

局部闭环完成后，Worker 不直接把 Task 标记为 Done，而是形成稳定送验结果并执行：

```text
In Progress → Verifying
```

---

## 2.6 产物

形成 **Verification-ready Result｜待验收结果**：

| 字段 | 说明 |
|---|---|
| `task` | 当前 Task 引用。 |
| `changes` | 实际修改范围。 |
| `result` | Worker 已实际达成的功能或行为结果。 |
| `local_evidence` | 已执行的关键局部检查 / 命令 / 运行反馈及结果。 |
| `notes` | 正式验证需重点关注的信息；无则省略。 |

保持轻量，不生成冗长开发报告。Task 权威定义和状态仍由 `tasks.md` 维护；临时日志、调试过程与中间推理不成为长期事实源。

---

## 2.7 完成标准

Worker 正确消费 Execution Unit，在 Boundary 内实现 Goal，按需获取局部上下文，已知局部问题已通过工具反馈诊断 / 修复，必要 Local Verification 通过，不需要突破上游契约，并形成 Verification-ready Result，完成 `In Progress → Verifying`。

若当前 Task Contract 内无法解决阻塞问题，则以 `Blocked` 退出并交由异常 / 纠偏机制。

---

## 2.8 下游使用约定

```text
Execution Unit
      ↓
Autonomous Implementation
      ↓
Runtime Observation
      ↓
Local Verification / Repair
      ↓
Verification-ready Result
      ↓
In Progress → Verifying
      ↓
Verification & Exception Convergence
```

因此，本步骤的最终职责是：

> **让 Worker 在既定任务契约内自主完成实现、运行反馈与局部修复，并将结果收敛为可由独立 Gate 正式验收的稳定实现。**