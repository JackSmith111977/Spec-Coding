# Governance｜治理

本目录维护 Spec Coding 仓库自身的治理、版本与 Harness Build / Release 规则，不作为目标项目 Workflow 的 Canonical 行为输入。

- [`repository-governance.md`](repository-governance.md)：仓库结构、Canonical Source、分支、版本与发布治理。
- [`harness-build-and-release.md`](harness-build-and-release.md)：维护者如何从 Canonical 创建、更新、验证、发布和移除可复用 Harness Package。
- [`patch-release.md`](patch-release.md)：修复版本的基线核验、增量范围、完整候选冻结、受影响验证与回滚；附维护工具用法。

## 版本设计与实施

- [下一阶段：可恢复、可复核的Harness](designs/harness-reliability/README.md)：综合对抗性评审、真实项目实践与全流程留存审计，规划证据身份、状态恢复、按需适配及业务闭环验证；尚未实施，不增加客户端默认门禁。
- [0.13.0 产物组织与渐进读取](designs/artifact-organization/README.md)：统一产物目录、导航、读取、维护与迁移方案，附验收矩阵。规则与协议已在0.13.0实施并完成必要发行验证；本设计仍非客户端输入，正式行为由Manifest登记的规范及对应发行包承担。

Harness Build & Release 属于仓库维护者流程。它可以使用临时 Worklist、Checklist、Fresh Review、语义拆解或确定性工具提高可靠性，但这些 Build Internals 不作为面向使用方的稳定架构层。

目标项目只消费已发布 Harness Package；Project Onboarding 与后续 Target-side Harness Adaptation 不需要参与维护者的预编译过程。
