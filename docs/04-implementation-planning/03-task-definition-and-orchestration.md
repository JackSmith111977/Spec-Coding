# 3. Task Definition & Orchestration｜任务定义与编排

## 3.1 目标

基于 Candidate Task Set（候选任务集），将任务定型为可执行、可验证、依赖清晰并等待整体校验的 Formal Task Set（正式任务集）。

本步骤重点回答：

> **每个 Task 如何定义、如何验证、依赖什么、属于哪个 Requirement、处于什么状态，以及如何组织。**

本步骤不重新拆解任务边界；若发现任务过粗、过细或无法独立验证，应返回 Implementation Task Decomposition 调整。

---

## 3.2 任务定型

直接继承候选任务中的：

```text
Requirement
Goal
Trace
Boundary
Coverage
Open Items（可选）
```

并补齐正式任务定义：

| 字段 | 内容 |
|---|---|
| `ID` | 稳定、唯一的任务标识。 |
| `Requirement` | 当前 Task 的 Primary Requirement，如 `REQ-01`；一个 Task 只设一个主归属。 |
| `Status` | Task 当前生命周期状态；正式定型后初始为 `Draft`。 |
| `Goal` | 当前任务需要完成的单一目标。 |
| `Trace` | 对应的 Requirement / AC / Design 来源，可保留多个关联来源。 |
| `Boundary` | 当前任务覆盖的实施边界。 |
| `Depends On` | 真正存在的阻塞依赖；无则省略。 |
| `Coverage` | 必须覆盖的关键执行路径。 |
| `Verification` | 如何证明 Coverage 与目标已经满足。 |
| `Done` | 什么结果可以判定任务完成。 |

Primary Requirement 用于计算 `TasksOf(REQ-xx)`、Requirement 级 AC Gate 与 Git 同步边界；`Trace` 用于完整追溯，二者职责不同。

Task 描述目标、边界与验证契约，不下沉为具体文件、函数或逐行修改脚本。

---

## 3.3 定义任务生命周期

正式 Task 从本步骤开始进入统一生命周期：

```text
Draft
  ↓
Ready
  ↓
In Progress
  ↓
Verifying
  ↓
Done

In Progress / Verifying
        ↕
     Blocked
```

- `Draft`：Task 已定型，但尚未通过任务集校验。
- `Ready`：已通过任务集校验，可在依赖满足后执行。
- `In Progress`：正在实施。
- `Blocked`：存在阻塞，暂时无法继续。
- `Verifying`：实现与必要 Local Verification 已完成；存在代码变更时，Task Commit 已形成并具有可追溯 `code_ref`，正在执行正式 Verification。
- `Done`：Verification 通过，任务完成。

本步骤只**定义状态模型并初始化 `Draft`**；`Ready` 准入由下一步 Task Set Validation 决定，其余状态由 Development Execution 持续推进。

`tasks.md` 作为任务事实源，应保存 Task 的权威 `Status` 与 Primary Requirement，供 Human、Main Agent、Subagent 与 Harness 统一读取。

---

## 3.4 绑定验证

将 `Coverage` 转换为具体 Verification。

优先使用能够提供确定性反馈的验证方式，例如：

- 逻辑、规则、状态机 → Unit / Property Test。
- API / Contract → API / Contract Test。
- Database / MQ / Async Flow → Integration Test。
- Build / Type / Static Rule → Build / Typecheck / Lint。
- 用户关键交互 → Browser / E2E。
- UI 视觉与体验 → Browser Verification + Human Review。

遵循：

> **Deterministic First｜确定性工具优先。**

`Verification` 回答“怎么证明做对”，`Done` 回答“什么结果算完成”。

所有 Task 都应 Verification-First；适合自动化测试驱动时，可采用 Test-First，但不默认将测试与实现拆成独立 Task。

---

## 3.5 编排必要依赖

只显式记录真正阻塞当前任务执行的 `Depends On`。

常见依赖：

- Data Dependency｜数据依赖。
- Contract Dependency｜契约依赖。
- Capability Dependency｜能力依赖。
- Verification Dependency｜验证依赖。

不因为前后端、目录结构或习惯性开发顺序机械增加依赖。

没有显式依赖的任务是否并行、如何分 Wave，由 Harness / Agent 在执行时根据实际情况推导。

> **Persist constraints, derive strategy｜持久化约束，运行时推导策略。**

---

## 3.6 执行委派

可评估 Task 是否适合独立委派给 Subagent：

- **Independent｜独立**：与其他未完成任务不存在强执行耦合。
- **Context-Isolated｜上下文可隔离**：可以只提供当前 Task 所需 Requirement / Design、直接依赖结果与相关代码。
- **Verifiable｜结果可验证**：完成后能够独立执行 Verification 并判断结果。

满足条件时，可由 Harness 在开发实施阶段动态委派；否则由主 Agent 顺序推进。

Subagent 的主要价值是 **Context Isolation（上下文隔离）**，并行只是额外收益。每个 Subagent 只获得当前 Task 的最小必要上下文，结果统一回到主任务集汇合。

不在 `tasks.md` 中固定 Agent、Model 或 Wave。

> **Persist constraints, derive execution｜持久化约束，运行时推导执行策略。**

---

## 3.7 动态组织任务

默认使用统一 `tasks.md` 维护完整任务集：

```text
tasks.md
├─ T01 [REQ-01]
├─ T02 [REQ-01]
├─ T03 [REQ-02]
└─ T04 [REQ-02]
```

当单个 Task 上下文较大、生命周期较长 / 跨会话恢复、由独立 Agent / Human 并行负责或持续产生较多 Evidence / Notes 时，可按需下钻：

```text
tasks.md
  ↓
T07 → tasks/T07.md
```

即使下钻，`tasks.md` 仍保留任务核心定义、Primary Requirement、依赖、状态与引用。

> **默认集中维护，复杂时按需下钻。**

开发实施时，再从 Task、关联 Requirement / Design、直接依赖和相关代码中动态裁剪执行上下文。

> **Artifact 保持完整，Context 保持最小。**

---

## 3.8 产物

本步骤形成 Formal Task Set，并统一维护在 `tasks.md` 中；所有正式 Task 初始状态为 `Draft`。

每个 Task 至少能回答：

```text
属于哪个 Requirement？
为什么做？
做成什么？
当前处于什么状态？
边界在哪里？
依赖什么？
哪些路径必须覆盖？
怎么验证？
什么算完成？
```

---

## 3.9 完成标准

- 每个 Task 有稳定 ID、Primary Requirement、Goal、Trace 与 Boundary。
- 每个正式 Task 初始 `Status = Draft`。
- Coverage 已绑定明确 Verification。
- Done 描述真实完成结果。
- 必要阻塞依赖已明确，不维护可推导的冗余调度关系。
- 普通 Task 集中维护，复杂 Task 按需下钻。
- 可独立委派 Task 能被 Harness 基于独立性、上下文隔离与可验证性动态识别。
- Task 可通过 Trace 按需获取上游上下文，无需复制完整 Requirement / Design。

---

## 3.10 下游使用约定

Formal Task Set 是 Task Set Validation 的直接输入。

```text
REQ-xx / AC
       ↓
Design
       ↓
Task [Primary REQ]
       ↓
Coverage
       ↓
Verification
```

因此，本步骤的最终职责是：

> **将候选任务定型为具有稳定 Requirement 归属、可执行、可验证、依赖清晰且具有统一生命周期的正式任务集，为后续 `Draft → Ready` 准入和需求级收敛建立基础。**