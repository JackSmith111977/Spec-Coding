# 3. Root Cause Confirmation & Correction Routing｜根因确认与纠正路由

## 3.1 目标

基于 Fault Localization Result（故障定位结果），确认能够解释关键异常的 Root Cause（根因），识别最早失效的事实源，并确定最小必要的纠正与重新验证范围。

本步骤重点回答：

> **异常为什么发生，真正应该从哪里纠正。**

只负责根因确认与纠正路由，不在证据不足时强行归因，也不直接替代对应主流程阶段完成正式纠正。

---

## 3.2 根因候选收敛

基于 Fault Boundary、Hypothesis 与 Evidence，区分：

- **Symptom｜症状**：异常表现，不作为最终原因。
- **Contributing Factor｜促成因素**：影响故障发生，但不足以单独解释问题。
- **Root Cause Candidate｜根因候选**：能够解释关键故障链的候选原因。

根因候选应能够解释 First Divergence 及其后的主要异常，而不是只解释某个 Error Message 或局部现象。

```text
Symptom
   ↓
Divergence
   ↓
Candidate Cause
```

> **Cause over Symptom｜确认原因，不停留在症状。**

---

## 3.3 根因证据确认

对 Root Cause Candidate 进行因果确认，重点判断：

- 能否解释关键 Failure、Observed Trace 与 Divergence。
- 是否具有足够 Evidence 支撑。
- 主要竞争性解释是否已被排除。
- 条件允许时，是否可通过干预、对照或重复实验进一步验证。

优先使用：

```text
Cause Present
    ↓
Failure

Cause Controlled
    ↓
Failure Removed
```

无法安全复现或直接干预时，可通过多个相互一致的 Evidence 收敛结论，不机械要求固定证据数量。

根因状态保持轻量：

| 状态 | 含义 |
|---|---|
| `Confirmed` | 证据足以解释故障并排除主要替代原因。 |
| `Probable` | 高度支持，但受环境、历史现场、竞态等限制无法完成强确认。 |
| `Unconfirmed` | 仍只是猜测或证据不足。 |

`Unconfirmed` 应返回前一阶段继续调查；`Probable` 只有在风险可接受且保留不确定性的情况下才可进入后续纠正。

修复后暂时通过不能单独证明原假设就是根因。

> **Evidence before Root Cause｜根因结论必须建立在充分证据上。**

---

## 3.4 最早失效事实源判定

根因确认后，沿现有 Trace 判断哪一个最早的权威事实已经失效：

```text
Root Cause
    ↓
Requirement / AC ?
Design ?
Task ?
Implementation ?
Verification Asset ?
Environment / Dependency ?
```

典型路由：

| 问题来源 | 返回位置 |
|---|---|
| Requirement / AC Problem | Requirement Clarification |
| Design Defect | Technical Design |
| Task Contract Problem | Implementation Planning |
| Implementation Defect | Development Execution |
| Verification Asset Problem | Verification Convergence |
| Environment / Dependency Issue | 对应环境、依赖或运行治理位置 |

若代码实现符合 Design，但 Design 本身错误，应回到 Design；若 Design 又忠实实现了错误的 Requirement / AC，则继续向上找到真正失效的事实源。

不通过下游补丁掩盖上游错误。

> **Correct the Earliest Invalid Source｜修正最早失效的事实源。**

---

## 3.5 纠正范围与路由确定

基于 Invalid Source（失效事实源）沿追溯链确定受影响范围：

```text
Invalid Source
      ↓
Affected Trace
      ↓
Correction Route
      ↓
Reverification Scope
```

重点确认：

- 应返回哪个既有阶段纠正。
- 哪些 Requirement / AC / Design / Task / Change 已受影响。
- 哪些既有 Evidence 因上游事实变化而失效。
- 修正后需要重新执行哪些 Verification。

只重新处理真正受影响的链路，不默认重新执行完整 Spec Coding 流程。

```text
Requirement
    ↓
Design
    ↓
Task
    ↓
Change
    ↓
Verification
```

上游越早发生变化，下游需要重新对齐的范围通常越大；实际范围仍由 Trace 与影响证据确定。

> **Affected Trace Only｜只重新处理受影响链路。**

---

## 3.6 根因确认门禁

只有满足必要 Evidence Threshold（证据门槛）的结论才能进入正式纠正：

```text
Root Cause Candidate
        ↓
解释关键故障？
        ↓
证据充分？
        ↓
主要替代原因已排除？
        ↓
Confirmed / Probable / Unconfirmed
        ↓
   ┌────┴────┐
   ↓         ↓
Enough     Not Enough
   ↓         ↓
Correction  返回故障定位
Routing
```

Evidence Threshold 按风险裁剪：普通确定性缺陷可由强确定性证据快速确认；间歇性、并发、高风险生产问题应采用更强的重复验证或多源证据。

---

## 3.7 产物

形成 **Root Cause Resolution｜根因处置结果**：

| 字段 | 内容 |
|---|---|
| `Failure` | Failure Baseline 引用。 |
| `Root Cause` | 已确认或 Probable 的根因及状态。 |
| `Evidence` | 支撑当前根因结论的关键证据。 |
| `Invalid Source` | 最早失效的事实源。 |
| `Affected Trace` | 受影响的 Requirement / Design / Task / Change / Verification。 |
| `Correction Route` | 应返回的主流程阶段或对应治理位置。 |
| `Reverification Scope` | 修正后需要重新验证的范围。 |
| `Open Items` | 尚需承接的问题；无则省略。 |

只保存根因、证据与纠正决策需要的事实，不复制完整调查过程或中间推理。

---

## 3.8 完成标准

Root Cause 已达到与当前风险相匹配的证据门槛，能够解释关键异常并排除主要替代原因；最早失效事实源已经明确，Affected Trace、Correction Route 与 Reverification Scope 均可确定。

证据不足的 Root Cause Candidate 不应强行收敛，应返回 Evidence Collection & Fault Localization 继续调查。

---

## 3.9 下游使用约定

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

> **以充分证据将根因候选收敛为可信因果结论，找到最早失效的事实源，并沿既有追溯链确定最小必要的纠正与重新验证范围。**
