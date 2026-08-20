# 3. Verification Finding Triage & Deviation Convergence｜验证发现判定与偏差收敛

## 3.1 目标

基于 Verification Results、Evidence 与 Findings，对未通过、未验证或存在争议的结果进行人工判定，并将需要处理的问题路由到正确层级完成纠正与重新验证。

本步骤回答：

> **这个 Finding 是否成立、最早失效在哪里、应该回到哪里纠正，以及怎样证明已经重新收敛。**

本步骤不直接修改 Requirement、Design、Task 或业务实现；所有修正返回对应阶段执行。

---

## 3.2 人工判定 Finding

以 Evidence 为主要依据：

- **Invalid Finding**：误报、证据不足或验证资产本身存在问题。
- **Verification Issue**：测试、环境、Harness 或验证执行存在问题。
- **Implementation Defect**：实现未满足既定 Requirement / Design / Task。
- **Upstream Deviation**：Requirement、Design 或 Task 等上游基线已经失效。
- **Accepted Deviation**：偏差客观存在，但经 Human 明确接受并保留风险记录。
- **Unresolved**：证据不足，暂时无法可靠判定。

Finding（验证发现）与 Open Item（开放项）不是同一对象：Finding 记录验证阶段观察到的事实及判定；只有其处置需要跨阶段继续等待决策、补充信息或后续承接时，才创建或关联稳定 `OI-xxx`。已有 Open Item 被验证命中时，继续引用原 ID，不创建副本。

Risk（风险）同样独立于二者：风险可以由 Finding 或 Open Item 暴露，但只有存在具体未决问题时才需要 `OI-xxx`。

Verifier 的 `Suspected Origin` 只作定位线索，不替代 Human Decision。

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
- **Upstream Deviation**：从最早失效层开始自上而下重新对齐。
- **Accepted Deviation**：记录接受理由、影响与后续动作，不伪装为 `Pass`。
- **Unresolved**：保留 Finding 与所需决策，阻止无依据收敛；需要跨阶段持续承接时创建或关联 `OI-xxx`。

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

> **Affected Trace Only｜只重新对齐并验证受影响链路。**

---

## 3.6 产物

形成 **Finding Resolution｜验证发现处置结果**：

| 字段 | 内容 |
|---|---|
| `Finding` | 原始 Finding 引用。 |
| `Decision` | Invalid / Verification Issue / Implementation Defect / Upstream Deviation / Accepted / Unresolved。 |
| `Evidence` | 支撑当前判定的关键证据。 |
| `Invalid Source` | 最早失效层；无需纠正时省略。 |
| `Affected Trace` | 受影响 Requirement / Design / Task / Verification 链路。 |
| `Route` | 返回验证、开发实施、实施规划、技术设计或需求澄清。 |
| `Reverification Scope` | 纠正后需要重新验证的范围。 |
| `Open Item` | 需要跨阶段继续承接时关联的 `OI-xxx`；无则省略。 |
| `Status` | Resolved / Accepted / Blocked / Open。 |

只保存当前收敛真正需要的事实，不复制纠正过程与中间推理。

---

## 3.7 完成标准

所有有效 Finding 已 Human Triage，需要纠正的问题已定位最早失效层并回流正确阶段，修正不在验证上下文隐式完成，Affected Trace 已重新对齐并必要重验 / 回归，Accepted Deviation 有理由 / 影响 / 风险记录，需要跨阶段继续承接的问题均关联稳定 `OI-xxx`，无未处理关键 Finding；无法继续的问题明确 `Blocked`。

最终：**Verification Converged** 或 **Verification Blocked**。

> **基于验证证据由 Human 判定真实偏差，将问题路由到最早失效的事实层完成纠正，并仅重新验证受影响链路；需要持续承接的未决问题通过稳定 Open Item 保持追踪，使完整变更重新达到可证明的一致状态。**
