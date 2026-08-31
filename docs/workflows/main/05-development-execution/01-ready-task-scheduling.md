# 1. Ready Task Scheduling｜就绪任务调度

## 1.1 目标

基于已经通过 Task Set Validation、处于 `Ready` 状态的任务集，结合依赖、冲突与当前执行环境，动态筛选可执行任务并构造高效、低冲突的 Agent Execution Unit（执行单元）。

本步骤重点回答：

> **当前哪些 Task 可以执行，应如何调度，以及每个 Agent 应在什么上下文和工作空间中启动。**

本步骤只负责运行时调度，不重新拆解 Task、修改 Requirement / Design，也不提前进入代码实现。

---

## 1.2 筛选可执行任务

```text
Status = Ready
+
Depends On 已满足
+
无有效 Blocker
+
所需执行环境可用
        ↓
Runnable Task
```

- `Ready` 是持久化任务状态，表示已通过规划门禁。
- `Runnable` 是运行时视图，表示当前已具备实际执行条件。

不引入 `Queued`、`Runnable`、`Scheduled` 等持久化状态。

---

## 1.3 判定执行策略

重点考虑 Dependency、Boundary、Contention 与 Critical Path。

> **先降低冲突，再提高并行度。**

```text
单个 Writing Task
    → 当前 Workspace

多个 Read-only Task
    → Shared Workspace

多个独立 Writing Task
    → Parallel + Independent Worktree

存在明显依赖或高冲突
    → Sequential
```

Worktree 是并行写任务的隔离机制，不作为 Task 固定属性，由当前 Execution Set 动态决定。

> **Persist constraints, derive execution｜持久化约束，运行时推导执行策略。**

---

## 1.4 构造执行单元

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

Scoped Context 优先包含：

```text
Current Task
+
Referenced Requirement / AC / Design
+
Direct Dependency Result
+
Relevant Code Context
+
Verification Requirement
+
Active Constraints
```

默认只提供当前 Task 所需最小上下文，其余信息由 Agent 按需检索。

> **Artifact 保持完整，Context 保持最小。**

Agent、Model、Fresh / Fork、Scout、Worktree 等属于运行时策略，不写回 Task 核心定义。

---

## 1.5 认领并启动任务

```text
Runnable Task
        +
Execution Unit Ready
        ↓
      Claim
        ↓
Ready → In Progress
        ↓
  Worker Execution
```

任务权威状态写回 `tasks.md`；Worker、Workspace、Attempt 等短生命周期信息可由 Harness 作为 Execution Metadata 独立维护。

Agent、Worktree 或运行环境启动失败，优先作为 Execution Attempt 异常；只有任务本身无法继续时才进入 `Blocked`。

---

## 1.6 产物

形成 **Execution Dispatch｜执行调度结果**：

| 字段 | 说明 |
|---|---|
| `runnable_tasks` | 本轮实际可执行 Task 集合。 |
| `scheduling` | 必要的串行 / 并行、执行顺序和隔离策略，不固化为长期 Wave。 |
| `execution_units` | 本轮启动的执行单元集合。 |

Execution Unit 是单 Worker 的直接输入契约。Execution Dispatch 是短生命周期 Runtime Artifact，不作为新的长期事实源；Task 定义和状态仍由 `tasks.md` 维护。

---

## 1.7 完成标准

当前轮次已识别 Runnable Task、检查依赖 / 冲突 / 环境、动态确定串并行和 Workspace 策略、为待执行 Task 构造最小 Execution Unit，并完成被启动任务 `Ready → In Progress`；未调度 Ready Task 保持原状态。

---

## 1.8 下游使用约定

```text
Ready Task Set
      ↓
Runnable Derivation
      ↓
Execution Strategy
      ↓
Execution Unit
      ↓
Ready → In Progress
      ↓
Autonomous Implementation & Closure
```

因此，本步骤的最终职责是：

> **将规划世界中的 `Ready` Task 动态转换为运行时世界中的高质量执行单元，并以最低冲突成本启动最适合当前条件的 Agent 执行。**