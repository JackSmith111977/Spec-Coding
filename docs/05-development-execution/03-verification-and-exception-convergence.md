# 3. Verification & Exception Convergence｜验收与异常收敛

## 3.1 目标

基于 Verification-ready Result，独立执行 Task Verification Contract，判断当前实现是否真正满足 Coverage 与 Done，并对失败结果进行归因与分流，使 Task 最终收敛到 `Done`、返回修复或 `Blocked`。

本步骤重点回答：

> **当前实现是否已经被独立证明满足任务契约；若未通过，问题应由谁处理、回到哪里继续推进。**

只负责正式验收、失败归因与异常收敛，不重新实现功能，也不隐式修改 Requirement / Design / Task Contract。

---

## 3.2 准备验收输入

核心输入：

- **Task Contract**：Goal、Boundary、Coverage、Done。
- **Verification Contract**：必须执行和满足的验证要求。
- **Verification-ready Result**：Worker 实际实施结果。
- **Actual Changes**：Patch、Commit 或 Workspace 实际修改。
- **Local Evidence**：Worker 局部证据，仅作参考和定位。
- **Runtime / Environment**：正式 Gate 所需环境。

```text
What to Verify
      +
What Result to Verify
      +
Where to Verify
        ↓
Acceptance Ready
```

Worker Self Verification 不直接视为正式证据，正式验收尽可能对当前实际结果重新执行独立 Gate。

---

## 3.3 执行独立验收与质量门禁

优先使用 Build / Compile / Typecheck / Lint、Unit / Integration、API / Contract、DB / MQ / Async Flow、Browser / E2E / Critical Path、Architecture / Dependency / Schema Rule、Security 等确定性 Gate。

> **Deterministic Gate First｜确定性门禁优先。**

机器难以判定的复杂 UX、语义行为、代码可维护性或高风险改动，可按任务风险补充 Fresh Reviewer。

---

## 3.4 归因失败并分流异常

| 类型 | 典型情况 | 处理方式 |
|---|---|---|
| **Implementation Defect** | 实现 Bug、类型错误、测试失败、行为不符合 Task Contract | 返回原 Worker 修复，`Verifying → In Progress` |
| **Integration / Environment Issue** | 集成顺序、运行环境、临时依赖或验证设施异常 | 处理运行条件后重验；必要时暂时阻塞 |
| **Task Contract Problem** | Boundary、Coverage、Depends On 或 Verification 定义不足 / 失效 | `Verifying → Blocked`，回实施规划纠偏 |
| **Requirement / Design Problem** | Requirement 歧义、固定设计无法成立、上游冲突 | `Verifying → Blocked`，触发上游纠偏 |

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
Verifying
```

> **Attribution before Escalation｜先归因，再升级。**

---

## 3.5 形成验收结论

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

形成 **Verification Result｜验收结果**，至少保留：

- `task`
- `verdict`
- `target_status`
- `evidence`
- `findings`（无则省略）
- `blocker / required_action`（阻塞时）

只保存正式验收和下游状态推进需要的事实。

---

## 3.7 完成标准

正式 Gate 已执行，结果有可复核 Evidence；失败已先归因，能在当前实现内解决的返回原 Worker，超出当前 Task Contract 的问题进入 Blocked / 上游纠偏；最终明确目标状态。

---

## 3.8 下游使用约定

Verification Result 是 State Commit & Continuous Progression 的直接输入。

> **以独立、确定性优先的 Gate 证明 Task 是否满足既定 Coverage 与 Done，并在失败时将问题路由到最短正确反馈路径。**