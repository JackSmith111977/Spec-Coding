# Governance｜治理

本目录维护 Spec Coding 仓库自身的治理与派生编译规则，不作为目标项目 Workflow 的 Canonical 行为输入。

- [`repository-governance.md`](repository-governance.md)：仓库结构、版本、Canonical Source 与历史治理。
- [`semantic-compilation.md`](semantic-compilation.md)：Harness Compilation V3 的规范前端；定义 Canonical Docs → Atomic Clauses → Semantic IR 的一次性版本侧编译与发布门禁。

Semantic Compilation 的治理文档本身不自动进入 Semantic IR，避免“编译协议递归编译自身”；目标行为语义仍只来自 `docs/manifest.yaml` 已登记的 Workflow、Rules、Exception Workflow 与 Meta Protocol。
