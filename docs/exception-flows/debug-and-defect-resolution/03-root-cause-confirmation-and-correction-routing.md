# 3. Root Cause Confirmation & Correction Routing｜根因确认与纠正路由

## 3.1 目标

基于 Fault Localization Result（故障定位结果），确认能够解释关键异常的 Root Cause（根因），识别最早失效的事实源，并确定最小必要的纠正与重新验证范围。

本步骤重点回答：

> **异常为什么发生，以及真正应该从哪里纠正。**

只负责根因确认与纠正路由，不在证据不足时强行归因，也不替代对应主流程阶段完成正式纠正。

---

## 3.2 根因候选收敛

基于 Fault Boundary、Hypothesis 与 Evidence，区分：

- **Symptom｜症状**：异常表现。
- **Contributing Factor｜促成因素**：影响故障发生，但不足以单独解释问题。
- **Root Cause Candidate｜根因候选**：能够解释关键故障链的候选原因。

根因候选应能够解释 First Divergence 及其后的主要异常，而不是停留在 Error Message 或局部现象。

> **Cause over Symptom｜确认原因，不停留在症状。**

---

## 3.3 根因证据确认

对 Root Cause Candidate 进行因果确认，重点判断：

- 是否能够解释关键 Failure、Observed Trace 与 Divergence。
- 是否有足够 Evidence 支撑。
- 主要替代原因是否已被排除。
- 条件允许时，是否可通过干预、对照或重复实验进一步验证。

优先形成：

```text
Cause Present
    ↓
Failure

Cause Controlled
    ↓
Failure Removed
```

无法安全复现或直接干预时，可通过相互一致的多源 Evidence 收敛结论，不机械要求固定证据数量。

根因状态：

| 状态 | 含义 |
|---|---|
| `Confirmed` | 证据足以解释故障并排除主要替代原因。 |
| `Probable` | 高度支持，但受环境、竞态或历史现场限制无法完成强确认。 |
| `Unconfirmed` | 证据不足，仍需继续调查。 |

`Unconfirmed` 返回前一阶段；`Probable` 仅在风险可接受且明确保留不确定性时继续纠正。

修复后通过不能单独证明原假设就是根因。

> **Evidence before Root Cause｜根因结论必须建立在充分证据上。**

---

## 3.4 最早失效事实源判定

根因确认后，沿 Trace 判断最早失效的权威事实：

```text
Root Cause
    ↓
Requirement / AC
Design
Task
Implementation
Verification Asset
Environment / Dependency
```

典型路由：

| 问题来源 | 返回位置 |
|---|---|
| Requirement / AC Problem | Requirement Clarification |
| Design Defect | Technical Design |
| Task Contract Problem | Implementation Planning |
| Implementation Defect | Development Execution |
| Verification Asset Problem | Verification Convergence |
| Environment / Dependency Issue | 对应运行或依赖治理位置 |

若下游实现忠实执行了错误的上游定义，应继续向上追溯，而不是通过下游补丁掩盖问题。

> **Correct the Earliest Invalid Source｜修正最早失效的事实源。**

---

## 3.5 纠正范围与路由确定

基于 Invalid Source 沿追溯链确定：

```text
Invalid Source
      ↓
Affected Trace
      ↓
Correction Route
      ↓
Reverification Scope
```

重点明确：

- 返回哪个既有阶段纠正。
- 哪些 Requirement / AC / Design / Task / Change 已受影响。
- 哪些既有 Evidence 已失效。
- 修正后需要重新验证哪些内容。

只重新处理真正受影响的链路，不默认重新执行完整 Spec Coding 流程。

> **Affected Trace Only｜只重新处理受影响链路。**

---

## 3.6 产物

形成 **Root Cause Resolution｜根因处置结果**：

| 字段 | 内容 |
|---|---|
| `Failure` | Failure Baseline 引用。 |
| `Root Cause` | 根因及 Confirmed / Probable 状态。 |
| `Evidence` | 支撑根因结论的关键证据。 |
| `Invalid Source` | 最早失效的事实源。 |
| `Affected Trace` | 受影响的主流程链路。 |
| `Correction Route` | 应返回的阶段或治理位置。 |
| `Reverification Scope` | 修正后需要重新验证的范围。 |
| `Open Items` | 尚需承接的问题；无则省略。 |

只保存根因、证据和纠正决策需要的事实，不复制完整调查过程。

---

## 3.7 完成标准

Root Cause 已达到与当前风险相匹配的证据门槛，能够解释关键异常并排除主要替代原因；最早失效事实源、Affected Trace、Correction Route 与 Reverification Scope 均已明确。

证据不足时返回 Evidence Collection & Fault Localization 继续调查，不强行收敛。

---

## 3.8 下游使用约定

```text
Fault Localization Result
        ↓
根因候选收敛
        ↓
根因证据确认
        ↓
最早失效事实源判定
        ↓
纠正范围与路由确定
        ↓
Root Cause Resolution
        ↓
Correct Existing Stage
        ↓
Fix Verification & Failure Convergence
```

因此，本步骤的最终职责是：

> **以充分证据确认根因，找到最早失效的事实源，并沿既有追溯链确定最小必要的纠正与重新验证范围。**
