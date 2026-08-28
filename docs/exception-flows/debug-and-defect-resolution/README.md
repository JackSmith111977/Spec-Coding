# Debug & Defect Resolution｜调试与缺陷解决

本流程用于处理开发、验证、运行时、用户反馈或监控中出现的 Failure（故障）与 Defect（缺陷）。它是 Cross-cutting Exception Workflow（跨阶段异常流程），不作为 Main Workflow 的新增阶段。

核心目标是：**从异常事实出发，以证据定位问题、确认根因、回到最早失效事实源完成纠正，再通过原始故障回归与受影响链路验证关闭异常。**

## 流程

```text
Failure Signal
      ↓
1. Failure Intake & Reproduction
   异常接管与复现
      ↓
Failure Baseline
      ↓
2. Evidence Collection & Fault Localization
   证据采集与故障定位
      ↓
Fault Localization Result
      ↓
3. Root Cause Confirmation & Correction Routing
   根因确认与纠正路由
      ↓
Root Cause Resolution
      ↓
Correct Existing Stage
      ↓
4. Fix Verification & Failure Convergence
   修复验证与异常收敛
      ↓
Failure Closure
      ↓
Owner Stage / Main Workflow Continues
```

## 四个步骤

| 步骤 | 核心问题 | 主要产物 |
|---|---|---|
| [1. 异常接管与复现](01-failure-intake-and-reproduction.md) | 发生了什么，是否具备可靠调查基础？ | `Failure Baseline` |
| [2. 证据采集与故障定位](02-evidence-collection-and-fault-localization.md) | 异常从哪里开始偏离，哪些原因仍然成立？ | `Fault Localization Result` |
| [3. 根因确认与纠正路由](03-root-cause-confirmation-and-correction-routing.md) | 为什么发生，最早失效事实源在哪里？ | `Root Cause Resolution` |
| [4. 修复验证与异常收敛](04-fix-verification-and-failure-convergence.md) | 纠正是否真正解决故障，能否关闭并回接主流程？ | `Failure Closure` |

## 与主流程的关系

普通、边界清晰且可在当前 Task Contract 内直接解决的实现问题仍由原 Worker 局部 `Diagnose → Repair → Recheck`，不必启动完整 Debug Workflow。

当异常无法可靠归因、需要跨层定位、可能涉及上游事实源失效，或 Verification Finding（验证发现）处于 `Unresolved` 且需要进一步诊断时，再进入本流程。

根因确认后，正式纠正仍回到 Requirement Clarification、Technical Design、Implementation Planning、Development Execution、Verification Convergence 或对应环境 / 依赖治理位置完成；Debug 不维护这些阶段的并行状态副本。

最终 `Failure Closure = Resolved` 只表示当前 Failure 已关闭，不等于 Task `Done`、Finding 已收敛或 Requirement 已 `Verified`。这些权威状态继续由各自主流程事实源判定。

## 核心原则

- **Evidence before Fix｜修复前先有证据。**
- **Trace before Guess｜先重建链路，再猜原因。**
- **Hypothesis before Experiment｜先形成可证伪假设，再进行实验。**
- **Correct the Earliest Invalid Source｜修正最早失效的事实源。**
- **Affected Trace Only｜只重新处理受影响链路。**
- **Close the Failure, Restore the Flow｜关闭当前异常，回接既有流程。**
