# 3. Verification & Exception Convergence｜验证与异常收敛

## 3.1 目标

基于 Verification-ready Result，独立执行 Task Verification Contract，判断当前实现是否真正满足 Coverage 与 Done，并对失败结果进行归因与分流，使 Task 最终收敛到 `Done`、返回修复或 `Blocked`。

本步骤重点回答：

> **当前实现是否已经被独立证明满足任务契约；若未通过，问题应由谁处理、回到哪里继续推进。**

只负责正式验证、失败归因与异常收敛，不重新实现功能，也不隐式修改 Requirement / Design / Task Contract。

---

## 3.2 准备验证输入

核心输入：

- **Task Contract**：Requirement、Goal、Boundary、Coverage、Done。
- **Verification Contract**：必须执行和满足的验证要求。
- **Verification-ready Result**：Worker 实际实施结果。
- **Code Reference｜代码引用**：存在代码变更时，以 `code_ref` 指向的 Task Commit 为正式验证对象。
- **Actual Changes**：由 `code_ref` 对应 Commit、Patch 或无代码任务的实际结果确定。
- **Local Evidence**：Worker 局部证据，仅作参考和定位。
- **Applicable Rules｜适用规则**：存在代码变更时，包括 [`Code Quality Rules`](../../../rules/code-quality.md)、[`Agent Delegation & Coordination Rules`](../../../rules/agent-delegation-and-coordination.md) 及项目自身规则。
- **Runtime / Environment**：正式 Gate 所需环境。

```text
What to Verify
      +
What Result to Verify
      +
Exact Code Reference
      +
Applicable Rules
      +
Where to Verify
        ↓
Verification Ready
```

Worker Self Verification 不直接视为正式证据，正式验证尽可能对当前实际结果重新执行独立 Gate。

---

## 3.3 执行独立验证与质量门禁

优先使用 Build / Compile / Typecheck / Lint、Unit / Integration、API / Contract、DB / MQ / Async Flow、Browser / E2E / Critical Path、Architecture / Dependency / Schema Rule、Security 等确定性 Gate。

> **Deterministic Gate First｜确定性门禁优先。**

存在 `code_ref` 时，Gate 必须针对该代码引用对应的实际变更执行，避免验证对象与 Worker 后续工作区状态漂移。

机器难以稳定判定的复杂 UX、语义行为、代码可理解性 / 信息质量 / 变更清晰度 / 一致性或高风险改动，可按任务风险补充 Fresh Reviewer。`Reviewer` 是 Agent Delegation & Coordination Rules 中的独立审查 Subagent Role，`Verifier` 则表示本步骤承担的正式 Verification 职责；Reviewer 只补充独立推理和 Finding，不替代 Deterministic Gate，也不默认直接修复被审查实现。

Reviewer 的 Context 应尽量与原 Worker 实施过程隔离；复杂 Review 的有效能力不应明显低于被审查结果所需的推理能力。具体 Model / Thinking 由 Harness 基于当前 Runtime 动态路由，不写回 Task Contract。

---

## 3.4 归因失败并分流异常

失败应先基于现有 Evidence 尝试归因；只有能够可靠判断所属层级时，才直接进入对应修复 / 纠偏路径。

| 类型 | 典型情况 | 处理方式 |
|---|---|---|
| **Implementation Defect** | 实现 Bug、类型错误、测试失败、行为不符合 Task Contract，或明显违反适用代码质量规则 | 返回原 Worker 修复，`Verifying → In Progress`；修复后重新 Local Verification 与 Task Commit |
| **Integration / Environment Issue** | 集成顺序、运行环境、临时依赖或验证设施异常 | 处理运行条件后重验；必要时暂时阻塞 |
| **Task Contract Problem** | Boundary、Coverage、Depends On 或 Verification 定义不足 / 失效 | `Verifying → Blocked`，回实施规划纠偏 |
| **Requirement / Design Problem** | Requirement 歧义、固定设计无法成立、上游冲突 | `Verifying → Blocked`，触发上游纠偏 |

```text
Gate Failed
    ↓
Can attribute reliably?
   ┌────┴────┐
  Yes        No
   ↓          ↓
Existing     Debug & Defect Resolution
Routing      Exception Workflow
```

若异常无法可靠归因、需要跨层定位或现有证据不足以判断最早失效位置，应进入 [`Debug & Defect Resolution`](../../exceptions/debug-and-defect-resolution/README.md)。Debug 负责形成 Root Cause / Correction / Failure Closure Evidence，正式 Task 状态仍由当前 Development Execution 流程写回，不由异常流程维护并行状态。

对于可明确归因的 Implementation Defect，仍优先保持最短局部修复路径：

```text
Verifying
    ↓
Gate Failed
    ↓
Implementation Defect
    ↓
In Progress
    ↓
Original Worker Repair
    ↓
Local Verification
    ↓
New Task Commit
    ↓
Verifying
```

如果失败主要来自当前验证 Agent / Model / Tool 的 Capability Problem，而不是被验证实现本身，不应形成 Implementation Defect 或 Human Authority Escalation；优先由 Harness 调整 Context、Thinking、Model、Tool 或 Fallback 后重新执行同一 Verification Contract。

> **Attribution before Escalation｜先归因，再升级。**

---

## 3.5 形成验证结论

### 通过

```text
verdict = passed
→ target_status = Done
```

### 需要实现修复

```text
verdict = repair_required
→ target_status = In Progress
```

### 当前任务无法继续

```text
verdict = blocked
→ target_status = Blocked
```

本步骤负责判定目标状态，下一阶段正式写回 `tasks.md`。

---

## 3.6 产物

形成 **Verification Result｜验证结果**，至少保留：

- `task`
- `requirement`
- `verdict`
- `target_status`
- `evidence`
- `code_ref`（存在代码变更时保留本次实际验证的 Task Commit）
- `findings`（无则省略）
- `blocker / required_action`（阻塞时）

只保存正式验证和下游状态推进需要的事实。Reviewer Role、Model、Thinking、Attempt 等只属于运行时执行信息，不进入 Verification Result 的长期契约，除非其差异本身影响 Evidence 解释。

---

## 3.7 完成标准

正式 Gate 已针对正确验证对象执行，结果有可复核 Evidence；存在代码变更时已按风险检查适用 Code Quality Rules；必要 Fresh Reviewer 已作为独立审查补充而非替代 Gate；Verification Result 保留实际验证的 `code_ref`；失败已先归因，能在当前实现内解决的返回原 Worker，超出当前 Task Contract 的问题进入 Blocked / 上游纠偏，无法可靠归因的问题进入 Debug & Defect Resolution；最终明确目标状态或异常承接路径。

---

## 3.8 下游使用约定

Verification Result 是 State Commit & Continuous Progression 的直接输入；进入 Debug 的异常在形成可信 Resolution Evidence 后回到对应 Owner Stage，再由主流程继续状态收敛。

> **以独立、确定性优先的 Gate 对可追溯实现结果进行正式验证，并在失败时先完成可靠归因；Reviewer 仅在需要独立推理时补充审查，明确问题走最短修复路径，无法可靠归因的问题交由 Debug 异常流程定位，再回到既有事实源继续推进。**
