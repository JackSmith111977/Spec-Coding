# 3. Scope & Rule Confirmation｜范围与规则确认

## 3.1 目标

基于 Requirement Interpretation 与已经确认的 Clarification Results，将需求收敛为**明确的范围边界、业务规则与关键需求决策**，形成后续验收标准与技术方案设计可以直接消费的稳定需求基线。

本步骤回答“**做什么、不做什么、在什么边界下遵循什么规则**”，不展开具体技术实现。

---

## 3.2 确认范围

将需求内容划分为：

- **In Scope**：本次必须实现的行为与结果。
- **Out of Scope**：明确不属于本次需求的内容。
- **Boundary**：容易发生范围扩张、需要显式约束的边界条件。

范围应围绕用户 / 业务结果表达，不直接等同于页面、接口、文件或代码模块。

---

## 3.3 确认业务规则

对会影响目标行为的关键规则进行明确，包括按需确认：

- `Trigger`：什么条件触发行为。
- `Behavior`：触发后应发生什么。
- `State`：不同状态下允许或禁止什么行为。
- `Data`：业务层需要满足的数据语义或约束。
- `Exception`：重要失败、回退或异常行为。

规则保持在 Requirement 层级，不提前设计接口、字段、组件、MQ 或具体代码结构。

---

## 3.4 固化关键决策

将前序澄清得到的关键结论显式保留，包括：

- 对原有歧义的最终解释。
- 范围取舍。
- 核心业务行为和规则决策。
- 仍存在但不阻塞当前推进的 Open Item。

权限遵循全局 Human / Agent Authority Contract（人机决策权限契约）：

- Agent 可自主整理、归纳和结构化**已经明确确认**的需求事实，不需要重复请求 Human 确认。
- 若仍需要决定 Requirement 语义、In Scope / Out of Scope、核心 Business Rule 或关键目标行为，应由 Human Decision（Human 决策）完成；Agent 负责提供证据、候选解释与影响分析。
- 不允许 Agent 通过默认假设把未确认语义写成正式需求事实。

当进入 Human Decision 时，同时遵循 [`Human-Agent Collaboration Rules`](../rules/human-agent-collaboration.md)：如果 Human 尚未掌握当前 Requirement Interpretation、关键歧义 / Delta、相关 Evidence 与主要影响，应先完成必要 Cognitive Sync 并恢复 Decision Readiness，再请求范围或规则判断；已有共享上下文仍有效时不重复同步。

未确认且会阻塞需求正确性的事项不能通过默认假设关闭，应返回澄清。

---

## 3.5 结构化产物

形成 Scope & Rule Definition：

| 章节 | 内容 |
|---|---|
| `In Scope` | 本次明确需要完成的需求行为。 |
| `Out of Scope` | 本次明确不处理的内容。 |
| `Boundaries` | 需要控制的范围边界与限制条件。 |
| `Business Rules` | 已确认的触发、行为、状态、数据与异常规则。 |
| `Decisions` | 已确认的重要需求决策。 |
| `Open Items` | 当前不阻塞但仍需后续承接的问题；无则省略。 |

---

## 3.6 完成标准

当 Human 或 Agent 能清楚说明本次做什么 / 不做什么、关键边界和业务规则、主要需求决策，需要 Human Decision 的业务语义已经完成确认，且不存在仍会阻塞后续验收标准或技术设计的关键未知时，本步骤完成。

若仍存在会改变目标行为、范围或关键规则的 Blocking 问题，应返回 Ambiguity & Gap Identification 继续澄清。

---

## 3.7 下游使用约定

Scope & Rule Definition 是 Acceptance Criteria Confirmation 与后续 Technical Design 的稳定需求边界。

> **将已澄清且完成必要 Human Decision 的需求收敛为明确的范围、业务规则与关键决策，为验收标准与技术方案设计提供稳定边界。**