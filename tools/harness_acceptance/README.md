# Harness Acceptance V3

Harness Acceptance 是 Harness Compilation V3 的第四阶段确定性支持层。它消费已经通过 Stage 3 handoff 的 `Semantic IR + Environment Model + Adoption Baseline + Adaptation Plan + Harness Candidate`，只回答：

> **这份具体 Harness Candidate 是否真的被当前 Runtime 接管，并在独立 Fresh Agent 的真实行为中保持了所需语义？**

它不重新设计 Semantic Clause、Provider 或 Harness Component，也不替代 Main Workflow Stage 6 的 Verification Convergence。

## Flow

```text
Harness Candidate
      ↓
prepare
      ↓
Clause / Artifact / Provider verification worklist
      ↓
Verification Plan
      ↓
Structural + Runtime + Semantic + Mutation execution
      ↓
Verification Report
      ↓
Independent Fresh-Agent Acceptance
      ↓
Acceptance Receipt
      ↓
validate
      ↓
READY / BLOCKED
```

## `prepare`

`prepare` 只建立不可跳过的验证账本：每个 `covered` Clause 一个验证工作项、每个 Candidate Artifact 一个 Runtime visibility 工作项、每个 Selected Provider 一个 active-state 工作项，并给出 `load / process / boundary / gate_lifecycle / exception` 五类 Fresh-Agent Acceptance Seed。

Python 不根据 Clause 文本猜测试方法。Agent / Runtime Adapter 决定使用 `deterministic / runtime_probe / semantic_behavior` 中哪种方式以及实际 Probe / Scenario。

## `validate`

最终 Validator 强制：

- Semantic / Environment / Adoption / Adaptation Plan / Candidate Fingerprint 全部仍然一致；
- Candidate Artifact 的 `content_sha256` 与目标工作区真实文件一致；
- Verification Report 与 Verification Plan 绑定，Acceptance Receipt 与 Verification Report 绑定；
- 每个 Covered Clause 至少有一个通过且有证据的验证结果；
- 每个 Candidate Artifact 被真实 Runtime 证明可见，而不只是文件存在；
- 每个 Selected Provider 被证明当前 active；
- 每个计划中的 Semantic Mutation 都被检测；
- Blocking Verification Finding 为零；
- Fresh-Agent Executor 独立、Fresh，并提供 Isolation Evidence；
- 五类代表性 Fresh-Agent Acceptance Case 均执行并通过；
- 最终 Verdict 仅为 `READY` 或 `BLOCKED`。

Runtime-specific 启动方式不进入通用 Validator。Pi、Claude Code、Codex 等 Runtime 只需执行计划中的 Probe / Case，并返回可验证 Evidence。

## Failure Routing

第四阶段只验证与归因，不在验收层偷偷修 Harness：

```text
semantic    → Stage 1 Semantic Compile
environment → Stage 2 Environment Discover
adaptation  → Stage 3 Provider / Mapping
candidate   → Stage 3 Harness Synthesis
runtime     → Stage 2 refresh, then Stage 3 if mapping changes
```

> **Accept observable behavior, not generated files｜验收真实可观察行为，而不是“文件已经生成”。**
