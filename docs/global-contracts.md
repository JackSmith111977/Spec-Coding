# Global Contracts｜全局执行契约

本文件定义所有正式 Workflow（包括 Main Workflow 与 Exception Workflow）默认继承的通用规则。具体 Workflow 存在更严格规则时，以更严格规则为准。

## Terminology｜术语

核心英文术语及规范中文解释统一见 [`glossary.md`](glossary.md)。

- 非直观术语首次承担关键语义时使用 `English Term（中文解释）`。
- Schema 字段、状态值、ID、代码标识可直接保留英文。
- `Spec Coding` 是流程 / 方法名称，不默认存在独立 `Spec` 产物。

## Tailoring｜流程裁剪

原则：**核心不变量固定，执行深度按风险调整。**

| 深度 | 适用情况 |
|---|---|
| `Reuse` | 已有上下文、设计或证据仍完整有效。 |
| `Light` | 局部、低风险、边界清晰。 |
| `Standard` | 一般 Feature 或常规跨层变化。 |
| `Deep` | 高风险、高不确定、跨系统或难回滚变化。 |

Workflow 责任可以被已有有效证据直接满足，但以下内容不能因裁剪而消失：

- Requirement / Scope / Acceptance Criteria 的正确性。
- Requirement → Design → Task → Change → Verification 的 Traceability（可追溯性）。
- Blocking Open Item 与必要 Gate。
- 与风险匹配的 Verification 与 Evidence。
- Human / Agent Authority 边界。
- 发现偏差后的纠偏链路。
- 有 Git 固化变更时的 Task Commit 与 `code_ref`。

执行中若出现跨系统、Schema / 数据迁移、状态机、权限 / 安全、并发 / 异步、兼容性、难回滚决策或影响范围不明等信号，应提高执行深度。

## Open Item｜开放项

Open Item 表示尚未解决、需要后续阶段或 Workflow 继续承接的具体问题或决策。

最小字段：

| 字段 | 说明 |
|---|---|
| `id` | 稳定 `OI-xxx`，跨阶段持续复用。 |
| `origin` | 最初发现位置。 |
| `description` | 当前未决问题。 |
| `status` | `open` / `resolved` / `deferred`。 |
| `blocking` | 是否阻塞当前 Gate。 |
| `owner_stage` | 当前承接阶段。 |
| `related` | Requirement / AC / Design / Task / Finding / Evidence 等关联。 |
| `resolution` | `resolved` 时记录结论与必要依据。 |

```text
首次发现
  ↓
OI-xxx / open
  ↓
跨阶段引用同一 ID
  ├→ resolved
  └→ deferred
```

- 下游引用同一个 `OI-xxx`，不复制新的事实源。
- `blocking = true` 时不能绕过对应 Gate。
- `deferred` 必须有明确延期理由与承接位置。
- Risk、Finding 与 Open Item 是不同对象，可以关联但不自动互相转换。

## Human / Agent Authority｜人机决策权限

权限按“是否改变已确认事实源”和“错误决策影响”划分，而不是按阶段固定角色。

| 权限 | 边界 |
|---|---|
| `Autonomous` | 不改变既定语义契约，可回退、可验证、边界明确。 |
| `Confirm` | Agent 可提出方案，但技术 / 架构 / 数据 / 安全等影响显著，需要 Human 确认。 |
| `Human Decision` | 直接定义业务意图、正确性标准或风险接受边界。 |

典型 Human Decision 包括 Requirement 语义、In / Out Scope、核心 Business Rule、AC 语义变化、Accepted Deviation，以及对强制 Gate 的豁免。

> **Evidence before Escalation｜先取证，再升级。** Agent 应先缩小问题；Human 已确认的边界不重复请求确认。

## Human-Agent Collaboration｜人机协作

Human / Agent Authority 回答“谁有权决定”；[`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md) 回答“什么时候需要协作、Human 做判断前需要同步什么，以及反馈如何重新进入事实源”。

所有正式 Workflow 默认适用 Human-Agent Collaboration Rules，但**全局适用不代表每个阶段都必须发生 Human Interaction**：Agent 在 Autonomous 边界内继续自主推进，只有 Shared Model 建立 / 变化、Decision Boundary、Authority Escalation、Shared Model Invalidated、Major Closure 等真实 Trigger 成立时才同步。

进入重要 Confirm、Human Decision 或 Human Acceptance 前，应满足与当前风险匹配的 Decision Readiness；如果 Human 已掌握必要上下文则直接复用，不重复汇报。Human 的有效反馈若改变后续依赖的事实或语义，应更新对应 Canonical Source of Truth，并只重新对齐受影响 Trace。
