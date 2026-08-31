# Spec Coding 文档索引

Spec Coding 的规范本体分为三类：**Main Workflow（主流程）**、**Exception Workflow（异常流程）**与 **Rules（规则）**。Main Workflow 规定正常路径如何推进；Exception Workflow 承接跨阶段异常并回接主流程；Rules 规定推进过程中持续适用的原则与约束。除此之外，仓库保留 Human 概要与 Meta / Governance（元规则与治理）文档用于导航、编译与版本管理。

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
- [`exception-flows/README.md`](exception-flows/README.md)：跨阶段异常流程入口。

这些 README 只用于快速理解与导航，不属于正式 Workflow 文档。

## Workflow｜流程

### Main Workflow｜主流程

正式阶段文档集合以 [`manifest.yaml`](manifest.yaml) 的 `stages.documents` 为唯一清单。Agent 执行流程时读取当前适用阶段文档，而不是仅依赖概要。

```text
01A / 01B → 02 → 03 → 04 → 05 → 06 → 07
```

### Exception Workflow｜异常流程

正式异常流程以 [`manifest.yaml`](manifest.yaml) 的 `exception_workflows` 为机器可读入口，只在对应 Trigger 成立时加载。

- [`Debug & Defect Resolution`](exception-flows/debug-and-defect-resolution/README.md)：从异常接管与复现，经证据定位、根因确认与纠正路由，到修复验证和 Failure Closure，再将可信结论回交 Owner Stage。

Exception Workflow 不作为 Main Workflow 的新增阶段，也不维护 Task、Finding、Open Item 或 Verification 的并行状态事实源。

当前规范数量：34 份正式阶段文档、3 份正式规则文档、4 份正式异常流程文档。

## Rules｜规则

正式跨阶段规则以 [`manifest.yaml`](manifest.yaml) 的 `rule_documents` 为机器可读入口，按当前阶段与任务加载适用规则。

- [`global-contracts.md`](global-contracts.md)：Terminology、Tailoring、Open Item、Human / Agent Authority 等所有正式 Workflow 默认继承的全局执行规则。
- [`rules/`](rules/)：专项跨阶段规则。
  - [`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md)：Human-Agent Collaboration Rules（人机协作规则），维护 Shared Cognitive Baseline、Cognitive Sync、Decision Readiness 与反馈吸收。
  - [`rules/code-quality.md`](rules/code-quality.md)：与具体语言、框架和架构无关的 Code Quality Rules（代码质量规则）。

Rules 本身不推进阶段状态；Workflow 文档通过引用消费规则，不复制规则正文。

## Meta / Governance｜元规则与治理

- [`harness-compilation-protocol.md`](harness-compilation-protocol.md)：将 Applicable Workflow + Rules 转换为当前项目最小充分 Harness 的统一协议，采用 `Read → Derive → Compose → Verify`。
- [`manifest.yaml`](manifest.yaml)：Canonical Corpus（规范文档集）、Main / Exception Workflow、Rules 与机器可读导航。
- [`glossary.md`](glossary.md)：规范术语。
- [`repository-governance.md`](repository-governance.md)：仓库维护与版本管理。

历史版本由 Git 保存，不在当前文档目录维护并行旧副本。
