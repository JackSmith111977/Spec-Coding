# Rules｜规则

本目录维护跨阶段持续适用的正式规则。Rule（规则）定义执行过程中需要持续遵守的原则、约束或质量要求，本身不推进 Workflow（流程）状态，也不形成新的阶段。

当前专项规则：

- [`code-quality.md`](code-quality.md)：Code Quality Rules（代码质量规则），定义代码产物的可理解性、信息质量、变更清晰度与一致性原则。

全局执行规则仍由 [`../global-contracts.md`](../global-contracts.md) 维护，并与本目录规则一起通过 `manifest.yaml` 的 `rule_documents` 进入 Applicable Rules；为避免无意义路径迁移，本次不搬动既有文件。
