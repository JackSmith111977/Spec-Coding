# 6. 验证收敛

从完整 Requirement / Change 视角证明**实际变更已经正确、风险已处理、证据链可闭合**。

## 阶段流程

```text
验证基线建立 → 多维验证执行 → 偏差识别与闭环 → 证据沉淀与状态收敛
```

| 步骤 | 主要做什么 |
|---|---|
| 验证基线建立 | 基于实际 Change Set 识别最终验证缺口与范围。 |
| 多维验证执行 | 执行确定性验证、独立审查与必要 Human Acceptance。 |
| 偏差识别与闭环 | 判定 Finding，定位最早失效事实源并路由纠偏。 |
| 证据沉淀与状态收敛 | 汇总 Evidence、检查 Trace 闭环，判定 Verified / Blocked。 |

## 输入

Completed Tasks、`code_ref`、Requirement Sync、Actual Change Set、已有 Evidence 与 Open Item。

## 输出

Verification Baseline、Verification Results、Finding Resolution、Verification Closure Record。

## 完成条件

Required Verification 已完成，关键 Finding 已处置，Requirement → Evidence 追溯链完整，最终状态明确为 **Verified** 或 **Blocked**。

## 详细规则

1. [验证基线建立](01-verification-baseline-establishment.md)
2. [多维验证执行](02-multi-dimensional-verification-execution.md)
3. [验证发现判定与偏差收敛](03-verification-finding-triage-and-deviation-convergence.md)
4. [证据闭环与状态收敛](04-evidence-closure-and-status-convergence.md)

下一步：[`流程复盘改进`](../07-process-review-improvement/README.md)。
