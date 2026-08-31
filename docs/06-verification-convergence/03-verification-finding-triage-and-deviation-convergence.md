# 3. Verification Finding Triage & Deviation Convergence｜验证发现判定与偏差收敛

## 3.1 目标

基于 Verification Results、Evidence 与 Findings，对未通过、未验证或存在争议的结果进行判定，并将需要处理的问题路由到正确层级完成纠正与重新验证。

本步骤回答：

> **这个 Finding 是否成立、最早失效在哪里、应该回到哪里纠正，以及怎样证明已经重新收敛。**

本步骤不直接修改 Requirement、Design、Task 或业务实现；所有修正返回对应阶段执行。

---

## 3.2 判定 Finding

以 Evidence 为主要依据：

- **Invalid Finding**：误报、证据不足或验证资产本身存在问题。
- **Verification Issue**：测试、环境、Harness 或验证执行存在问题。
- **Implementation Defect**：实现未满足既定 Requirement / Design / Task。
- **Upstream Deviation**：Requirement、Design 或 Task 等上游基线已经失效。
- **Accepted Deviation**：偏差客观存在，但经 Human 明确接受并保留风险记录。
- **Unresolved**：证据不足，暂时无法可靠判定。

权限遵循全局 Human / Agent Authority Contract（人机决策权限契约）：

- 对证据明确、不会改变既定语义契约的 Invalid Finding、Verification Issue 或 Implementation Defect，Agent 可 Autonomous（自主）完成分类、路由与重验。
- Agent 可以对 Upstream Deviation 提出 Suspected Origin（疑似来源）、Affected Trace（受影响追溯链）和建议回流点，但只要判定会导致 Requirement / AC / 固定 Design 等事实源失效或变化，应进入相应 Confirm / Human Decision。
- **Accepted Deviation（接受偏差）始终属于 Human Decision（Human 决策）**；Agent 不得自行降低标准、跳过强制 Gate 或把已知偏差标记为 Pass。
- 证据相互冲突、置信度不足或影响高风险 / 安全边界时，Agent 应先补证据，再按权限升级，而不是强行自动分类。

进入 Upstream Deviation 的 Confirm / Human Decision 或 Accepted Deviation 判断前，同时遵循 [`Human-Agent Collaboration Rules`](../rules/human-agent-collaboration.md)。Human 至少应理解 Expected / Actual、关键 Evidence、影响与风险、Affected Trace 以及 Agent Recommendation；如果 Debug 或 Verification 已使既有共享模型失效，应先完成 Shared Model Repair，再请求偏差判断。

Finding（验证发现）与 Open Item（开放项）不是同一对象：Finding 记录验证阶段观察到的事实及判定；只有其处置需要跨阶段继续等待决策、补充信息或后续承接时，才创建或关联稳定 `OI-xxx`。已有 Open Item 被验证命中时，继续引用原 ID，不创建副本。

Risk（风险）同样独立于二者：风险可以由 Finding 或 Open Item 暴露，但只有存在具体未决问题时才需要 `OI-xxx`。

Verifier 的 `Suspected Origin` 只作定位线索，不自动改变上游事实源。

当 Finding 为 `Unresolved` 且问题本身仍可可靠观察，但当前证据不足以判断故障边界、根因或最早失效层时，应进入 [`Debug & Defect Resolution`](../exception-flows/debug-and-defect-resolution/README.md) 补充定位与根因证据。Debug 形成的 Root Cause / Failure Closure Evidence 回到本步骤继续 Finding 判定与状态收敛；异常流程不直接替代 Finding 的权威状态。

> **Evidence before Decision｜先看证据，再做判定。**

---

## 3.3 定位最早失效层

```text
Finding
   ↓
Implementation
   ↓
Task
   ↓
Design
   ↓
Requirement
```

| 失效层 | 回流位置 |
|---|---|
| Verification Asset / Environment | 多维验证执行 |
| Implementation | 开发实施 |
| Task | 实施规划 |
| Design | 技术方案设计 |
| Requirement | 需求澄清 |

> **Correct the Earliest Invalid Source｜修正最早失效的事实源。**

这里只用于当前变更纠偏，不替代流程复盘阶段 Root Cause Analysis。

---

## 3.4 路由纠正路径

- **Verification Issue**：修正验证资产或环境后重新执行相关验证。
- **Implementation Defect**：返回开发实施，在既定 Requirement / Design / Task 内修复。
- **Upstream Deviation**：从最早失效层开始自上而下重新对齐；涉及事实源变化时执行对应 Confirm / Human Decision。
- **Accepted Deviation**：仅在 Human Decision 后记录接受理由、影响与后续动作，不伪装为 `Pass`。
- **Unresolved**：若只是缺失决策或外部信息，保留 Finding 与所需决策；若需要进一步诊断故障边界 / 根因，则进入 Debug & Defect Resolution。需要跨阶段持续承接时创建或关联 `OI-xxx`。

本阶段只负责判定、路由与跟踪，不在当前上下文隐式完成上游修改。

---

## 3.5 重新验证并收敛

```text
Corrected Source
      ↓
Affected Trace
      ↓
Refresh Verification Baseline
      ↓
Affected Verification
+ Necessary Regression
      ↓
Pass / Fail
```

若仍失败，带新 Evidence 重新进入 Finding 判定；通过则关闭对应 Finding。若 Finding 关联 `OI-xxx`，只有对应未决问题也已形成明确结论时才同步将 Open Item 更新为 `resolved`。

Debug 返回的 Failure Closure 仅作为当前 Finding 的 Resolution Evidence 输入；Finding 是否 `Resolved / Accepted / Blocked / Open` 仍由本步骤依据完整 Verification Evidence 判定。

> **Affected Trace Only｜只重新对齐并验证受影响链路。**

---

## 3.6 产物

形成 **Finding Resolution｜验证发现处置结果**：

| 字段 | 内容 |
|---|---|
| `Finding` | 原始 Finding 引用。 |
| `Decision` | Invalid / Verification Issue / Implementation Defect / Upstream Deviation / Accepted / Unresolved。 |
| `Authority` | 本次判定实际使用的 Autonomous / Confirm / Human Decision。 |
| `Evidence` | 支撑当前判定的关键证据。 |
| `Invalid Source` | 最早失效层；无需纠正时省略。 |
| `Affected Trace` | 受影响 Requirement / Design / Task / Verification 链路。 |
| `Route` | 返回验证、开发实施、实施规划、技术设计、需求澄清或 Debug 异常流程。 |
| `Reverification Scope` | 纠正后需要重新验证的范围。 |
| `Open Item` | 需要跨阶段继续承接时关联的 `OI-xxx`；无则省略。 |
| `Status` | Resolved / Accepted / Blocked / Open。 |

只保存当前收敛真正需要的事实，不复制纠正过程与中间推理。

---

## 3.7 完成标准

所有有效 Finding 已按照 Authority Contract 完成必要判定；可自动处理的问题没有无意义等待 Human，需要改变事实源或接受偏差的问题完成相应 Confirm / Human Decision；需要进一步诊断的问题已由 Debug 提供必要 Root Cause / Failure Closure Evidence；Affected Trace 已重新对齐并必要重验 / 回归，需要跨阶段继续承接的问题均关联稳定 `OI-xxx`，无未处理关键 Finding；无法继续的问题明确 `Blocked`。

最终：**Verification Converged** 或 **Verification Blocked**。

> **基于验证证据按影响与权限完成 Finding 判定；可可靠归因的问题直接路由到最早失效层，需要进一步诊断的问题交由 Debug 异常流程补充证据，再回到本阶段完成纠正与验证收敛。**