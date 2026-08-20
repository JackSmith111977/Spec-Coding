# 4. State Commit & Continuous Progression｜状态提交与持续推进

## 4.1 目标

基于 Verification Result，将已确认的任务结果、状态与证据写回任务事实源，重新计算 Task Graph 的依赖与可执行条件，并在 Requirement（需求）边界满足时完成需求级集成、AC Gate 与远程同步。

本步骤重点回答：

> **任务结果如何固化、状态如何提交、一个 Requirement 何时可以集成并 Push，以及下一步应继续执行什么。**

本步骤不重复实施与验收，也不维护固定 Wave。

---

## 4.2 固化确认结果

只保留后续推进真正需要的事实：

- **Result｜结果**：Task 最终实现或验收结果。
- **Evidence｜证据**：支持当前结论的正式验证结果。
- **Code Reference｜代码引用**：Task Commit 或其他可追溯实现。
- **Requirement｜需求归属**：当前 Task 的 Primary Requirement。
- **Blocker｜阻塞信息**：阻塞原因、证据与所需动作。
- **Relevant Findings｜有效发现**：会影响后续 Task 或纠偏的事实。

Worker 日志、中间推理、重复调试过程不作为长期事实保存。

> **Persist facts, discard process｜持久化事实，舍弃过程。**

---

## 4.3 提交任务状态

```text
passed
→ Verifying → Done

repair_required
→ Verifying → In Progress

blocked
→ Verifying / In Progress → Blocked
```

需要修复时优先返回原 Worker。

进入 `Blocked` 时至少记录：Reason、Evidence、Affected Contract、Required Action / Decision、Resume From。

`tasks.md` 始终是 Task Definition、Primary Requirement 与 Status 的权威事实源；Worker、Attempt、Workspace 等短生命周期信息由 Harness 独立维护。

---

## 4.4 更新依赖与可执行条件

```text
T01 = Done
   ↓
Depends On(T01) satisfied
   ↓
Recompute Runnable
```

依赖 Task 被阻塞时，不级联修改下游 Task 状态：

```text
T01 = Blocked
T02 Depends On: T01

→ T02 = Ready
→ Runnable(T02) = false
```

只有上游纠偏使下游 Task Contract 本身失效时，才调整下游状态并重新规划 / 校验。

> **Ready 是任务状态，Runnable 是运行时推导结果。**

> **阻塞传播执行条件，不传播虚假的任务状态。**

---

## 4.5 Requirement 级集成与 Push

每次 Task 状态更新后，根据 Primary Requirement 重新计算：

```text
All TasksOf(REQ-xx) = Done ?
          ↓ Yes
Requirement Integration
          ↓
Requirement AC Gate
          ↓ Passed
Requirement Push
```

规则：

- **Requirement Integration（需求级集成）**：汇合该 `REQ-xx` 下已经通过 Task Verification 的代码引用，确认不存在未解决的集成冲突。
- **Requirement AC Gate（需求级验收门禁）**：基于该 Requirement 所属 Acceptance Criteria 验证集成后的需求行为；只补充需求级组合检查，不机械重跑所有 Task Gate。
- **Requirement Push（需求级推送）**：仅表示将已集成且通过 AC Gate 的当前 Requirement 代码同步到远程开发分支。
- Requirement Push **不等于** Merge（合并）、Release（发布）、Deploy（部署）或 Stage 6 的最终 `Verified（已验证）`。
- Integration、AC Gate 或 Push 任一步失败时，保留已确认 Task 事实，记录 Requirement Sync 状态并路由到最短修复 / 纠偏路径；只有 Task Contract 因上游修正失效时才回退其状态。

因此 Git 生命周期为：

```text
Task
→ Local Verification
→ Task Commit
→ Task Verification
→ Done

All TasksOf(REQ-xx) Done
→ Requirement Integration
→ Requirement AC Gate
→ Requirement Push
```

---

## 4.6 触发持续调度

```text
Task / Requirement State Updated
        ↓
Recompute Runnable Set
        ↓
New Runnable Task?
   ┌────┴────┐
  Yes       No
   ↓         ↓
Schedule   判断整体状态
```

存在新的 Runnable Task 时立即下一轮 Ready Task Scheduling，不等待固定 Wave。

若无 Runnable Task：

- 所有 Required Requirement 的 Task 均 `Done`，且 Requirement Integration / AC Gate / Push 均完成 → 开发实施完成，进入 Verification Convergence。
- 存在 Required `Blocked` → 暂停，等待纠偏或外部条件恢复。
- Requirement Sync 未完成 → 继续处理对应集成、AC Gate 或 Push 问题。
- Task Contract 已变化 → 重新经过 Task Set Validation 后再进入开发实施。

> **Event-driven Scheduling｜事件驱动调度。**

---

## 4.7 产物

形成 **Task Graph Update｜任务图更新结果**：

| 字段 | 说明 |
|---|---|
| `task` | 当前 Task 引用。 |
| `requirement` | 当前 Task 的 Primary Requirement。 |
| `status` | `Done`、`In Progress` 或 `Blocked`。 |
| `result` | 已确认并需要下游消费的任务结果。 |
| `evidence` | 支持当前状态的正式验证证据。 |
| `code_ref` | 已正式验收的 Task Commit 或其他代码引用；无则省略。 |
| `blocker` | `Blocked` 时记录原因、证据、受影响契约与所需动作。 |
| `dependency_updates` | 本次状态变化引起的直接依赖变化。 |
| `runnable_updates` | 重算后新增或失去可执行条件的 Task。 |
| `requirement_sync` | 当前 `REQ-xx` 的 task completion、integration、AC gate、push 状态及必要代码引用；尚未触发时可省略。 |
| `next_action` | 下一轮调度、继续修复、Requirement Sync、等待 Blocker 或结束开发实施。 |

只保存已确认事实与必要运行时结论，不复制完整执行过程。

---

## 4.8 完成标准

Verification Result 已映射为正确 Task 状态，必要 Result / Evidence / Code Reference / Blocker 已固化，依赖与 Runnable 条件已重算；达到 Requirement 边界时已完成或明确记录 Integration / AC Gate / Push 状态，并明确下一动作。

---

## 4.9 循环使用约定

```text
Verification Result
        ↓
Commit Facts & Task State
        ↓
Update Task Graph
        ↓
All TasksOf(REQ) Done?
        │
   ┌────┴────┐
   ↓         ↓
  Yes        No
   ↓          ↓
Integration  Recompute Runnable
   ↓
AC Gate
   ↓
Requirement Push
   ↓
Recompute Runnable / Overall State
```

因此，本步骤的最终职责是：

> **将执行结果固化为可信任务事实，以 Task Commit 形成任务级代码边界，以 Requirement Integration + AC Gate + Push 形成需求级 Git 边界，并持续驱动执行直到开发实施整体收敛。**