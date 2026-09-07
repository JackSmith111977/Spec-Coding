# Governance｜治理

本目录维护 Spec Coding 仓库自身的治理、版本与 Harness Build / Release 规则，不作为目标项目 Workflow 的 Canonical 行为输入。

- [`repository-governance.md`](repository-governance.md)：仓库结构、Canonical Source、分支、版本与发布治理。
- [`harness-build-and-release.md`](harness-build-and-release.md)：维护者如何从 Canonical 创建、更新、验证、发布和移除可复用 Harness Package。

Harness Build & Release 属于仓库维护者流程。它可以使用临时 Worklist、Checklist、Fresh Review、语义拆解或确定性工具提高可靠性，但这些 Build Internals 不作为面向使用方的稳定架构层。

目标项目只消费已发布 Harness Package；Project Onboarding 与后续 Target-side Harness Adaptation 不需要参与维护者的预编译过程。
