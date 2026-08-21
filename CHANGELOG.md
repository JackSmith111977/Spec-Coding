# Changelog｜变更记录

本文件记录 Spec Coding 规范体系的版本级变化。

版本遵循 Semantic Versioning（语义化版本）：

- `MAJOR`：进入稳定版本后，核心阶段、Artifact Contract（产物契约）、状态模型、Gate（门禁）或消费者行为发生不兼容变化。
- `MINOR`：新增或增强兼容能力、规则、治理机制、验证机制或自动化能力；`0.x` 阶段的主要语义演进通常使用 MINOR。
- `PATCH`：不改变流程语义的文案、链接、拼写、格式或纯文档修正。

## Unreleased｜未发布

### Added｜新增

- 新增面向 Human 的全流程概要，以及 1A / 1B / 2–7 各阶段概要 README，用于快速理解目标、输入、输出与完成条件。
- 在根 README 与全流程概要中加入必读万能 Prompt，引导 Agent 读取完整流程并按需建立最小充分 Harness。

### Changed｜调整

- 将根 `README.md` 收敛为项目简介、快速使用方法与文档入口。
- 将全局执行契约独立为 `docs/global-contracts.md`，将仓库维护与版本管理独立为 `docs/repository-governance.md`。
- 将 `docs/README.md` 收敛为纯文档索引，提高 Human 阅读信噪比。

## 0.2.0 - 2026-08-21

### Changed｜调整

- 统一 Greenfield（新项目）与 Brownfield（存量项目）进入 Requirement Clarification（需求澄清）的输入契约。
- 统一 Design Acceptance（方案验收）术语及上下游产物名称。
- 将流程复盘阶段的 Artifact Ontology（产物体系定义）对齐为 Requirement / Acceptance Criteria / Design / Task / Change / Verification / Evidence。
- 补齐稳定 `REQ-xx`、AC 归属、Task Primary Requirement、Task Commit、`code_ref`、Requirement Integration、Requirement AC Gate 与 Requirement Push 的 Git 生命周期契约。
- 明确 Requirement Push 仅表示远程开发分支同步，不代表 Merge、Release、Deploy 或最终 Verified。
- 建立稳定 `OI-xxx` Open Item（开放项）生命周期，并区分 Risk、Finding 与 Open Item。
- 建立 Human / Agent Authority（人机决策权限）契约，区分 Autonomous、Confirm 与 Human Decision。
- 建立 Risk-based Tailoring（风险驱动流程裁剪），允许按风险动态调整执行深度但不得裁掉核心不变量。
- 建立 `docs/glossary.md` 作为 Canonical Terminology（规范术语）唯一词义锚点。
- 补充仓库维护、版本收敛、治理文件同步、Agent 消费顺序与 `1.0.0` 稳定发布门槛。

### Notes｜说明

- 本版本完成当前静态审核发现的 P1 / P2 规则问题收敛。
- 当前状态为 `candidate`：规范结构已收敛，但 Scenario Stress Test、Fresh-Agent Blind Run 与真实项目 Pilot 仍待完成。

## 0.1.0 - 2026-08-20

### Added｜新增

- 导入当前 Spec Coding As-Is Baseline（现状基线）。
- 按流程阶段整理 34 份正式文档。
- 建立 `VERSION`、`CHANGELOG.md` 与 `docs/manifest.yaml` 版本治理入口。

### Notes｜说明

- `0.1.0` 用于固化初始现状，不代表流程已经完成可靠性验证。
- 后续审核问题通过独立版本变更修复，不在本基线中隐式改写历史语义。
