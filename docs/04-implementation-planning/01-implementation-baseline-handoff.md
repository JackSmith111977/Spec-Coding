# 1. Implementation Baseline Handoff｜实施基线接管

## 1.1 目标

基于已完成并通过验证的需求与技术方案产物，接管后续实施规划所需的最终结论，形成统一、稳定、可追溯的 Implementation Baseline（实施基线）。

本步骤重点回答：

> **后续任务拆解应以哪些已经确认的需求、决策、设计、约束与遗留事项为准。**

本步骤只负责上游结论的接管与对齐，不重新分析需求、系统影响或技术方案，也不提前拆解任务或设计验证用例。

---

## 1.2 确认上游准入

首先确认 Design Acceptance Result（方案验收结果）中：

- `Readiness = Ready`。
- 不存在仍会阻塞任务规划与实施的 Open Item。
- 当前使用的是已经收敛的最终需求与技术方案版本。

若 Readiness 为 `Not Ready`，或发现上游仍存在会直接影响任务拆解的冲突与缺口，应返回对应上游阶段纠正，而不是在本步骤自行补全。

---

## 1.3 接管实施依据

| 来源 | 重点接管内容 | 下游作用 |
|---|---|---|
| `Scope & Rule Definition` | In Scope、Out of Scope、Boundary、Business Rules、关键需求决策 | 明确实施范围与不可越过的需求边界 |
| `Acceptance Criteria` | 核心行为、关键边界与可验证结果 | 保留需求正确性的最终判定依据 |
| `Solution Decision` | Decision、必要的 Trade-offs / Constraints | 固定已经收敛的技术方向 |
| `Detailed Technical Design` | Structure、To-Be Flow、Contracts、Boundary Handling | 提供任务拆解所需的设计基线 |
| `Design Acceptance Result` | Validated Assumptions、Risks、Open Items、Readiness | 接管最终验收结论与仍需后续关注的问题 |

优先消费上游最终结论；只有结论不清、存在冲突或需要确认依据时，才沿追溯链回查原始文档、代码或 Evidence。

---

## 1.4 对齐有效结论

重点处理：

- **Final over Historical｜最终优先**：已被后续决策或设计修正的历史结论不再进入实施基线。
- **Conclusion over Raw Material｜结论优先**：默认使用已确认的结构化结论，不重新从原始需求或代码推测。
- **Reference over Duplication｜引用优先**：能够直接引用上游条目或章节时，不重复复制完整内容。
- **Open stays Open｜开放项保持开放**：仍未关闭的 `OI-xxx` 保持原 ID、状态、阻塞标记和承接阶段，不在实施基线复制成新问题。
- **No Silent Redesign｜禁止隐式重设计**：发现冲突或关键缺失时回到所属阶段纠正。

实施基线是上游事实的下游消费视图，不应成为新的事实源。

---

## 1.5 检查交接完整性

确认需求范围 / 规则 / AC、关键技术决策、Structure / To-Be Flow / Contracts / Boundary Handling、兼容 / 依赖等约束、最终 Risks 与 Open Items 均可稳定读取且可追溯，没有 `blocking = true` 的遗留问题。

这里只检查交接完整性，不重新执行 Design Acceptance & Convergence（方案验收与收敛）。

若发现阻塞问题：

```text
需求 / 规则缺口
    → Requirement Clarification

技术决策冲突
    → Solution Design & Decision

设计细节缺失
    → Detailed Technical Design

验收结论失效
    → Design Acceptance & Convergence
```

修正后重新接管受影响结论即可。

---

## 1.6 实施基线产物

| 章节 | 内容 |
|---|---|
| `Requirement Baseline` | 本次实施必须遵守的 Scope、Rules 与 Acceptance Criteria。 |
| `Fixed Decisions` | 已确认、不应在任务规划中重新发散的关键技术决策。 |
| `Design Baseline` | Structure、To-Be Flow、Contracts 与 Boundary Handling 的有效设计结论。 |
| `Constraints` | 兼容、依赖、架构、发布或其他需要在实施中保持的限制条件。 |
| `Risks` | 仍需实施或验证关注的已知风险；无则省略。 |
| `Open Items` | 需要继续承接的 `OI-xxx` 引用及当前状态 / 阻塞信息；无则省略。 |

Implementation Baseline 应尽量保存上游引用关系，只在需要降低下游理解成本时摘要关键内容，避免复制形成重复事实源。

---

## 1.7 完成标准

当 Human 或 Agent 能清楚回答当前方案是否 Ready、必须完成 / 明确不做什么、哪些决策已固定、任务拆解应依据哪些设计、有哪些约束 / 风险 / Open Item、且基线无过时 / 冲突 / 不可追溯结论时，本步骤完成。

---

## 1.8 下游使用约定

```text
Scope / Rules / Acceptance Criteria
              +
        Solution Decision
              +
   Detailed Technical Design
              +
    Design Acceptance Result
              ↓
 Implementation Baseline Handoff
              ↓
     Implementation Baseline
              ↓
 Implementation Task Decomposition
```

因此，本步骤的最终职责是：

> **以最小重复成本接管并对齐已经收敛的需求与技术方案结论，并通过稳定 `OI-xxx` 引用保留未决事项，为后续任务拆解建立唯一、稳定、可追溯的实施起点。**
