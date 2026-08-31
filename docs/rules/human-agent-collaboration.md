# Human-Agent Collaboration Rules｜人机协作规则

本文件定义 Human（人类）与 Agent 在 Spec Coding 正式 Workflow 中如何保持共享认知、何时发生协作、如何发起关键判断，以及 Human 反馈如何重新进入权威事实源。

本规则不要求 Human 跟随 Agent 的全部搜索、推理与执行过程，也不为每个阶段增加人工审批。核心目标是：**让 Agent 保持最大化的契约内自治，同时确保 Human 在真正需要判断时仍具备足够认知。**

---

## 1. Collaboration Principles｜协作原则

- **Agent Owns Exploration｜Agent 负责探索**：能够通过代码、文档、配置、测试、日志、运行环境或其他可用 Evidence 获取的信息，Agent 应优先自主调查，不把未完成的研究直接转交 Human。
- **Human Owns Meaning and Judgment｜Human 负责语义与关键判断**：Requirement 语义、Scope、正确性标准、重要取舍、风险接受等仍按 Human / Agent Authority Contract 判定权限；本规则不扩大 Agent 权限。
- **Shared Baseline, Not Shared Everything｜共享最小充分认知**：Human 不需要复制 Agent 的 Working Context，只需要持续掌握做出后续判断所需的最小共享认知。
- **Evidence before Interaction｜带证据协作**：请求 Human 介入前，Agent 应先缩小问题，说明已有事实、关键不确定性与影响。
- **Sync before Decision｜先同步，再决策**：当 Human 当前认知不足以理解重要决策时，Agent 应先恢复 Decision Readiness（决策就绪），再请求 Confirm 或 Human Decision。
- **Trigger-driven Collaboration｜事件驱动协作**：全局适用不等于全程交互；只有协作 Trigger 成立时才需要同步或介入。

> **Maintain human judgment, not human parity｜维护 Human 的判断能力，而不是要求 Human 与 Agent 掌握同等信息。**

---

## 2. Shared Cognitive Baseline｜共享认知基线

Shared Cognitive Baseline 表示 Human 与 Agent 为继续协作而共同依赖的最小认知状态，按需包含：

| 内容 | 核心问题 |
|---|---|
| `Goal` | 当前正在解决什么问题或推进什么目标？ |
| `Model` | 当前对相关业务、系统、Requirement、Design 或 Failure 的关键理解是什么？ |
| `State` | 当前流程 / 对象推进到哪里？ |
| `Delta` | 相比上一次共享认知，哪些重要事实或判断发生了变化？ |
| `Uncertainty` | 哪些关键未知、冲突或假设仍可能影响后续判断？ |
| `Next` | Agent 接下来准备做什么，以及是否即将进入 Human 决策边界？ |
| `Evidence` | 关键判断需要时可以回到哪里复核？ |

这些内容不要求形成独立长期文档，也不要求每次同步完整重述。已有 Project / Business / System / Requirement / Design / Task / Verification 等 Canonical Artifact 能够承载时，应直接引用或更新既有事实源。

Agent 的搜索结果、临时假设、排除过程、工具输出与中间推理属于 Working Context，默认不进入 Shared Cognitive Baseline。

> **Delta over Replay｜优先同步关键变化，不重复播放全部上下文。**

---

## 3. Sync Triggers｜认知同步触发

Human Interaction（人机交互）按事件触发，而不是按固定时间或每个阶段机械执行。

| Trigger | 何时成立 |
|---|---|
| **Shared Model Established｜共享模型建立** | 首次形成后续会持续依赖的重要项目、业务、系统、需求、设计或其他认知模型。 |
| **Meaningful Model Delta｜关键认知变化** | 新 Evidence 推翻关键假设、改变影响范围 / 边界 / 风险，或使 Human 继续沿用旧模型会影响判断。 |
| **Decision Boundary｜决策边界** | 即将请求 Confirm / Human Decision，且该判断会改变重要事实源、取舍或风险接受。 |
| **Authority Escalation｜权限升级** | Agent 无法在 Autonomous 边界内继续，需要 Human 承接相应权限。 |
| **Shared Model Invalidated｜共享模型失效** | Debug、Verification 或其他 Evidence 证明此前共享认知的重要部分已经错误或失效。 |
| **Major Closure｜重大收敛** | Requirement、Design、Verification、Failure 或规则演进等重要单元完成，Human 后续判断需要知道最终结果或剩余风险。 |

仅仅“Agent 工作了一段时间”“读了很多文件”或“完成一个普通 Task”不自动构成同步 Trigger；只有它们造成 Human 决策所需认知明显滞后时才需要同步。

---

## 4. Cognitive Sync｜认知同步

Trigger 成立后，只同步对当前继续协作有价值的信息。默认采用 Progressive Disclosure（渐进式披露）：

```text
Decision / Situation View
          ↓
Reason / Impact
          ↓
Evidence（按需深入）
```

优先让 Human 快速理解：

1. 当前发生了什么或模型有什么变化；
2. Agent 目前如何判断；
3. 为什么这个变化重要；
4. 哪些部分仍不确定；
5. 接下来需要 Human 做什么，或 Agent 将如何继续。

需要 Human 回答具体问题时，Agent 应尽量形成 Decision-ready Interaction（可决策交互），按需提供：

- `Context`：当前正在推进什么；
- `Finding / Delta`：已经确认的事实或关键变化；
- `Uncertainty / Decision`：真正需要判断的单一问题；
- `Evidence`：支撑当前理解的关键证据入口；
- `Recommendation`：Agent 当前建议及理由；
- `Impact`：主要选项或判断对后续的影响。

这些是信息要求，不是固定表单；简单问题可以压缩表达，复杂问题再按需展开。

> **Human receives a decision-ready question, not an unfinished investigation｜Human 接收可判断问题，而不是未完成调查。**

---

## 5. Decision Readiness｜决策就绪

在进入重要 Confirm、Human Decision 或 Human Acceptance 前，Agent 应判断 Human 是否已经拥有完成本次判断所需的最小认知。

通常至少应能理解：

- 当前 Goal 与相关权威事实；
- 与本次判断直接相关的 Current Model；
- 关键 Delta / Finding；
- 支撑判断的 Evidence；
- 存在真实选择时的主要 Option / Consequence；
- Agent Recommendation，以及仍保留的不确定性。

如果 Human 已通过前序共享上下文掌握这些信息，不重复同步；如果关键模型已经变化或 Human 无法从当前上下文可靠判断，应先执行 Cognitive Sync，再请求决策。

Authority 仍由 [`global-contracts.md`](global-contracts.md) 的 Human / Agent Authority 决定；Decision Readiness 只约束**如何使已需要的 Human 判断具备有效上下文**，不把 Autonomous 动作升级为人工审批。

---

## 6. Feedback Integration & Shared Model Repair｜反馈吸收与共享模型修复

Human 的反馈如果改变后续执行所依赖的事实、语义、决策或风险边界，应进入相应 Canonical Source of Truth，而不是只停留在会话记录中。

```text
Human Feedback / Decision
          ↓
Identify Authoritative Source
          ↓
Update Canonical Artifact
          ↓
Refresh Affected Trace
          ↓
Continue Autonomous Work
```

规则：

- 优先修改最早且最直接承担该事实的权威来源。
- 下游引用更新后的事实源，不复制新的 Human Decision 副本。
- Human 修正既有 Shared Model 时，只重新同步真正受影响的认知与 Trace。
- Human 暂时无法给出结论且问题需要后续承接时，复用稳定 `OI-xxx`；Blocking 问题不得因同步完成而被视为解决。
- Debug / Verification 证明既有共享认知失效时，应先完成 Shared Model Repair，再基于修正后的事实继续需要的决策与执行。

> **Integrate, don’t merely acknowledge｜反馈必须进入权威模型，而不只是被 Agent 口头“知道了”。**

---

## 7. 使用约定

本文件是所有正式 Main Workflow 与 Exception Workflow 默认适用的跨阶段 Rule，不推进新的状态，也不引入独立 Human Review Stage。

实际执行时：

- 认知、需求、技术决策、验证与规则演进阶段通常更容易触发同步；
- Implementation Planning 与 Task Contract 内的 Development Execution 默认保持低干扰自治，只有真实 Trigger 成立时升级协作；
- Workflow 文档只声明局部 Trigger / Authority 边界并引用本规则，不复制本规则正文。

Harness 可以根据目标项目将本规则映射为轻量 Summary、Decision Packet、Checkpoint、UI 提示、结构化会话状态或其他机制，但不得要求 Human 持续跟踪 Agent 全部 Working Context，也不得通过新增无必要 Gate 降低已有 Autonomous 边界。

> **Global applicability does not imply mandatory interaction｜全局适用，不代表全程打扰 Human。**
