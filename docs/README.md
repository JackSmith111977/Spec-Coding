# Spec Coding 文档索引

本目录分为四层：**Human 概要、正式阶段规则、跨阶段规则、全局治理**。

## Human 概要

- [`overview.md`](overview.md)：全流程概要、使用方法与阶段入口。
- [`01a-project-definition/README.md`](01a-project-definition/README.md)：项目定义建立（新项目）。
- [`01b-project-understanding/README.md`](01b-project-understanding/README.md)：项目认知建立（存量项目）。
- [`02-requirement-clarification/README.md`](02-requirement-clarification/README.md)：需求澄清。
- [`03-technical-design/README.md`](03-technical-design/README.md)：技术方案设计。
- [`04-implementation-planning/README.md`](04-implementation-planning/README.md)：实施规划。
- [`05-development-execution/README.md`](05-development-execution/README.md)：开发实施。
- [`06-verification-convergence/README.md`](06-verification-convergence/README.md)：验证收敛。
- [`07-process-review-improvement/README.md`](07-process-review-improvement/README.md)：流程复盘改进。

这些 README 只用于快速理解与导航，不属于 34 份正式阶段文档。

## 正式阶段规则

正式文档集合以 [`manifest.yaml`](manifest.yaml) 为唯一清单。Agent 执行流程时应读取对应阶段的正式文档，而不是仅依赖概要。

```text
01A / 01B → 02 → 03 → 04 → 05 → 06 → 07
```

## 跨阶段规则

- [`harness-compilation-protocol.md`](harness-compilation-protocol.md)：将 Spec Coding 流程转换为当前项目最小充分 Harness 的统一协议，采用 `Read → Derive → Compose → Verify`。
- [`exception-flows/`](exception-flows/)：跨阶段异常流程，按实际异常类型按需读取；当前 Debug & Defect Resolution（调试与缺陷处理）流程仍在建设中。

跨阶段规则不计入 34 份正式阶段文档，除非后续明确纳入 `stages.documents`。

## 全局治理

- [`global-contracts.md`](global-contracts.md)：Terminology、Tailoring、Open Item、Human / Agent Authority 等全局契约。
- [`glossary.md`](glossary.md)：规范术语。
- [`repository-governance.md`](repository-governance.md)：仓库维护与版本管理。
- [`manifest.yaml`](manifest.yaml)：Canonical Corpus（规范文档集）与机器可读导航。

历史版本由 Git 保存，不在当前文档目录维护并行旧副本。
