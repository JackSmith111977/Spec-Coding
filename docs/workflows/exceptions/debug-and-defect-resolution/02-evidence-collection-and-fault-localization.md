# 2. Evidence Collection & Fault Localization｜证据采集与故障定位

## 2.1 目标

基于 Failure Baseline（故障基线）与已有主流程产物，对照预期行为与实际运行结果，通过 Evidence（证据）和可验证 Hypothesis（假设）持续缩小问题范围，形成明确的 Fault Boundary（故障边界）与 Root Cause Candidate（根因候选）。

本步骤重点回答：

> **异常从哪里开始偏离预期，以及当前证据支持哪些可能原因。**

只负责调查与定位，不提前确认最终 Root Cause，也不直接修改 Requirement、Design、Task 等事实源。

---

## 2.2 故障链路重建

优先复用已有有效基线，例如：

- System Context
- Acceptance Criteria
- Impact Baseline
- Detailed Technical Design
- Task Contract
- `code_ref` / Existing Evidence

据此形成 Expected Trace（预期链路），再结合 Runtime Evidence 重建 Observed Trace（实际链路）：

```text
Expected Trace
      ↓
Observed Trace
      ↓
First Divergence
```

重点标记关键节点：

```text
✓ Confirmed
? Unknown
✗ Diverged
```

已有基线不足时，再沿代码、配置与运行时定向下钻，不默认重新扫描整个项目。

> **Trace before Guess｜先重建链路，再猜原因。**

---

## 2.3 区分性证据采集

围绕 Divergence（偏离点）采集能够区分不同可能原因的 Evidence。

优先关注：

- **Boundary Evidence**：判断异常位于边界哪一侧。
- **Differential Evidence**：对比 Failing Case 与 Known-good Case。
- **Change Evidence**：检查异常前后的代码、配置、依赖、数据或环境变化。

Recent Change 只作为线索，不直接视为 Cause。

证据来源按需选择 Code、Logs、Trace、Metrics、DB、MQ、Runtime、Test、Git、Config 等。

> **Discriminating Evidence First｜优先采集能区分可能性的证据。**

---

## 2.4 假设驱动调查

基于 Observation（观察）提出可被证据支持或证伪的 Hypothesis：

```text
Observation
    ↓
Hypothesis
    ↓
Predicted Evidence
    ↓
Inspect / Experiment
    ↓
Support / Reject
    ↺
```

有效假设应回答：

> **如果这个原因成立，还应该观察到什么？**

可按需增加 Debug Log、Test、Script 或 Instrumentation（观测增强），但调查性修改应服务于取证与验证假设，而不是无依据修复。

关键反证同样需要保留；已可靠排除的方向，不应在没有新证据时重复调查。

> **Hypothesis before Experiment｜先形成可证伪假设，再进行实验。**

---

## 2.5 故障边界收敛

综合 Trace、Evidence 与 Hypothesis Result，逐步缩小搜索范围：

```text
System
  ↓
Subsystem
  ↓
Service
  ↓
Component
  ↓
Execution Path
  ↓
Fault Boundary
```

本步骤不要求已经证明最终 Root Cause，只需要将模糊异常收敛到足以进入下一阶段因果确认的范围。

Regression（回归问题）可按需利用 Last Known Good / First Known Bad 与 Git Bisect 等方式进一步缩小候选 Change。

> **Narrow before Explain｜先缩小故障边界，再解释最终原因。**

---

## 2.6 主流程产物复用原则

Debug 优先消费主流程已有事实：

```text
System Context
      ↓
Impact Baseline
      ↓
Acceptance Criteria
      ↓
To-Be Flow / Contracts
      ↓
Task Coverage / Verification
      ↓
code_ref / Evidence
```

这些产物用于建立 Expected Trace 与调查索引；Debug 主要新增：

```text
Observed Trace
+
Runtime Evidence
+
Fault Boundary
```

已有基线不可用时，可直接基于 Failure Baseline、System Context 与 Runtime Evidence 调查。

> **Reuse Existing Baseline when Available｜已有有效基线优先复用。**

---

## 2.7 产物

形成 **Fault Localization Result｜故障定位结果**：

| 字段 | 内容 |
|---|---|
| `Failure` | Failure Baseline 引用。 |
| `Expected Trace` | 关键预期行为链路。 |
| `Observed Trace` | 实际链路及关键偏离点。 |
| `Evidence` | 支撑当前定位的关键证据。 |
| `Hypotheses` | 关键假设及 Supported / Rejected / Open 状态。 |
| `Fault Boundary` | 已收敛的故障范围。 |
| `Candidate Cause` | Root Cause Candidate；无则省略。 |
| `Open Items` | 仍需承接的问题；无则省略。 |

只保留后续根因确认需要的事实，不复制完整日志、实验过程或中间推理。

---

## 2.8 完成标准

Expected Trace 与 Observed Trace 已形成必要对照，关键偏离点已明确；调查由具有区分力的 Evidence 驱动，关键 Hypothesis 已被支持、排除或明确待验证；故障范围已收敛到可继续确认的具体边界。

若仍无法推进，应明确缺失的 Evidence 或阻塞条件。

本步骤结束时**不要求已经证明最终根因**。

---

## 2.9 下游使用约定

```text
Failure Baseline
      +
Available Main-flow Baseline
      ↓
Expected / Observed Trace
      ↓
Discriminating Evidence
      ↓
Hypothesis Loop
      ↓
Fault Boundary
      ↓
Root Cause Candidate
      ↓
Root Cause Confirmation & Correction Routing
```

因此，本步骤的最终职责是：

> **复用已有基线建立预期行为，以运行证据重建实际行为，通过区分性证据和可证伪假设持续缩小搜索空间，将模糊异常收敛为明确故障边界与可验证根因候选。**
