# 7. 流程复盘改进

基于真实执行证据，判断 Spec Coding / SDD 的**可复用规则与 Harness 是否需要改进**。

## 阶段流程

```text
收集证据 → 重建过程 → 发现问题 → 分析根因 → 形成改进方案 → 实施与验证
```

| 步骤 | 主要做什么 |
|---|---|
| 收集证据 | 收集需求、执行、验证、反馈与修正等事实。 |
| 重建过程 | 还原关键时序与追溯链。 |
| 发现问题 | 从异常信号中形成明确 `ISS-xxx`。 |
| 分析根因 | 定位流程 / Harness 层真正根因 `RC-xxx`。 |
| 形成改进方案 | 设计最小、可复用、可验证的 `IMP-xxx`。 |
| 实施与验证 | 修改规则 / Harness，并通过后续真实运行验证效果。 |

## 输入

真实 Spec Coding 运行中的 Requirement、Design、Task、Change、Verification、Evidence、会话和反馈等证据。

## 输出

`EV-xxx`、`ISS-xxx`、`RC-xxx`、`IMP-xxx`，以及经验证演进后的 Rules / Harness。

## 完成条件

根因已经转化为明确改进或确认 `No Process Change`；需要实施的改进已进入验证闭环，并能在后续真实流程中判断其效果。

> 本阶段只改进可复用 SDD / Harness 规则，不修改某个具体项目的 Requirement、Design、Task 或代码产物。

## 详细规则

1. [收集证据](01-evidence-collection.md)
2. [重建过程](02-process-reconstruction.md)
3. [发现问题](03-issue-detection.md)
4. [分析根因](04-root-cause-analysis.md)
5. [形成改进方案](05-improvement-design.md)
6. [实施与验证](06-implementation-and-validation.md)

完成后，改进进入后续真实 Spec Coding 运行继续验证。
