# Governance｜治理

本目录维护 Spec Coding 仓库自身的治理、版本与 Harness Build / Release 规则，不作为目标项目 Workflow 的 Canonical 行为输入。

- [`repository-governance.md`](repository-governance.md)：仓库结构、Canonical Source、分支、版本与发布治理。
- [`harness-build-and-release.md`](harness-build-and-release.md)：维护者如何从 Canonical 创建、更新、验证、发布和移除可复用 Harness Package。

## 版本设计与实施

- [0.13.0 产物组织与渐进读取](designs/artifact-organization/README.md)：统一产物目录、导航、读取、维护与迁移方案，附验收矩阵。规则与协议已在0.13.0实施并完成必要发行验证；本设计仍非客户端输入，正式行为由Manifest登记的规范及对应发行包承担。

Harness Build & Release 属于仓库维护者流程。它可以使用临时 Worklist、Checklist、Fresh Review、语义拆解或确定性工具提高可靠性，但这些 Build Internals 不作为面向使用方的稳定架构层。

目标项目只消费已发布 Harness Package；Project Onboarding 与后续 Target-side Harness Adaptation 不需要参与维护者的预编译过程。
