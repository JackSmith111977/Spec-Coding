# 2. Solution Design & Decision｜方案构思与决策

## 2.1 目标

基于已确认的现状、影响范围与约束，提炼需要解决的关键技术问题，形成可行方案并完成必要的技术决策。

本步骤重点回答：

> **要解决什么技术问题、采用什么技术路径，以及为什么这样选择。**

不展开具体接口、字段、类结构等实施细节，这些留给后续「方案详细设计」。

---

## 2.2 问题提炼

重点明确：

- 当前机制为什么无法满足需求。
- 需要改变的核心行为或系统性质是什么。
- 方案必须满足哪些关键约束。

避免从需求描述或表象问题直接跳到具体技术手段。

```text
Requirement
    ↓
Current State & Impact
    ↓
Technical Problem
```

---

## 2.3 方案构思

只有存在真实选择空间时，才需要设计多个候选方案，例如：

- 同步还是异步。
- 复用现有能力还是新增机制。
- 修改现有接口还是新增接口。
- 不同的数据、状态或架构方案。

对于已有明确工程惯例的简单变化，可直接沿用现有模式，无需为了流程强行构造多个方案。

---

## 2.4 评估取舍

| 维度 | 核心问题 |
|---|---|
| `Requirement Fit` | 是否完整满足需求与验收标准。 |
| `Compatibility` | 是否影响现有行为、接口或数据。 |
| `Complexity` | 实现与维护成本是否合理。 |
| `Risk` | 是否引入新的稳定性或迁移风险。 |
| `Evolvability` | 是否符合现有架构并便于后续演进。 |

性能、安全、资源成本等维度仅在实际相关时补充。

关键技术假设若会直接影响方案是否成立，应先通过代码、测试、实验或其他证据验证。

---

## 2.5 决策收敛

关键决策至少说明：

- **Decision｜决定**：最终采用什么技术路径。
- **Rationale｜依据**：为什么选择该方案。
- **Trade-off｜取舍**：为此接受了什么成本或限制。
- **Open Item｜开放项**：仍需后续设计、验证或决策的问题。

权限遵循全局 Human / Agent Authority Contract（人机决策权限契约）：

- 已有明确架构惯例、影响局部、可回退且能够独立验证的技术选择，可由 Agent Autonomous（Agent 自主）决定。
- 涉及架构边界、数据迁移、兼容策略、安全、显著运维影响、长期维护成本或难回滚路径的关键取舍，由 Agent 提供证据与推荐，并进入 Confirm（Agent 提议 + Human 确认）。
- 如果技术方案成立的前提是改变 Requirement / Acceptance Criteria、接受已知偏差或改变风险边界，应回到对应事实源进入 Human Decision（Human 决策），不得在技术方案中隐式完成。
- Human 已确认的技术原则或项目约束可直接作为后续 Agent 自治边界，不重复确认。

进入重要 Confirm / Human Decision 时同时遵循 [`Human-Agent Collaboration Rules`](../rules/human-agent-collaboration.md)：Human 应先具备对 Technical Problem、关键现状 / 影响、主要候选、Trade-off、Evidence 与 Agent Recommendation 的 Decision Readiness；若前序共享模型仍有效则只同步本次关键 Delta。

必要时保留重要备选方案及放弃原因，但无需记录所有曾考虑过的可能性。

---

## 2.6 方案决策产物

形成 **Solution Decision（方案决策）**：

| 内容 | 说明 |
|---|---|
| `Technical Problem` | 本次需要解决的关键技术问题。 |
| `Candidate Options` | 有真实选择空间时记录主要候选方案。 |
| `Decision` | 最终选择的技术路径。 |
| `Rationale` | 决策依据。 |
| `Trade-offs` | 已接受的重要取舍。 |
| `Open Items` | 尚未解决的问题；无则省略。 |

只保留对后续详细设计有价值的关键决策，不展开具体实现细节。

---

## 2.7 完成标准

当 Human 或 Agent 能清楚回答真正的技术问题、是否存在关键选择、已选方案是否满足需求与约束、关键前提是否经过必要验证、为什么这样选，并且需要 Confirm / Human Decision 的高影响决策已完成相应确认时，本步骤完成。

---

## 2.8 下游使用约定

```text
Impact Baseline
      ↓
Technical Problem
      ↓
Candidate Solutions
      ↓
Trade-off
      ↓
Solution Decision
      ↓
Detailed Technical Design
```

因此，本步骤的最终职责是：

> **围绕 Impact Baseline 中已确认的问题与约束，在清晰的人机权限边界内形成 Solution Decision，使后续详细设计建立在明确、可解释、可追溯的决策基础上。**