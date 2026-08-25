# Changelog｜变更记录

本文件记录 Spec Coding 规范体系的版本级变化。

版本遵循 Semantic Versioning（语义化版本）：

- `MAJOR`：进入稳定版本后，核心阶段、Artifact Contract（产物契约）、状态模型、Gate（门禁）或消费者行为发生不兼容变化。
- `MINOR`：新增或增强兼容能力、规则、治理机制、验证机制或自动化能力；`0.x` 阶段的主要语义演进通常使用 MINOR。
- `PATCH`：不改变流程语义的文案、链接、拼写、格式或纯文档修正。

## Unreleased｜未发布

## 0.4.0 - 2026-08-25

### Added｜新增

- 新增 `docs/rules/code-quality.md`，建立与具体语言、框架、架构层次和代码组织方式无关的 Code Quality Rules（代码质量规则），覆盖 Understandability（可理解性）、Information Quality（信息质量）、Change Clarity（变更清晰度）与 Consistency（一致性）。
- 新增 `docs/rules/README.md` 作为专项 Rules（规则）导航入口。
- `manifest.yaml` 新增 `rule_documents` 与 `canonical_rule_document_count`，正式区分 Canonical Stage Document（正式阶段文档）与 Canonical Rule Document（正式规则文档）。
- Glossary 新增 Workflow（流程）与 Rule（规则）规范定义。

### Changed｜调整

- 将 Spec Coding 规范本体明确划分为 Workflow（流程）与 Rules（规则）：Workflow 负责阶段 / 状态推进，Rules 负责跨阶段持续约束；Human 概要与 Meta / Governance 文档继续作为导航、编译和治理支持层。
- Harness Compilation Protocol 改为读取当前 Workflow + Applicable Rules（适用规则），按 `manifest.yaml` 动态加载规则并转换为最小充分 Harness，不要求机械映射每条规则为独立组件。
- Development Execution 在存在代码变更时正式消费 Code Quality Rules；Worker 仍保留契约边界内的实现自治，不因质量规则引入具体语言 / 框架约束。
- Task Verification 与最终 Verification Convergence 在机器难以稳定判定代码质量时，使用 Fresh Reviewer / Fresh Verifier 对照同一 Code Quality Rules 审查，避免个人风格偏好成为事实源。
- Repository Governance 增加 Canonical Rule Document、Rule Source of Truth 与 Applicable Rules 消费规则；阶段文档仅引用规则，不复制规则正文。
- README、Human Overview 与文档索引同步 Workflow / Rules 新导航与消费方式。
- `manifest.yaml` `schema_version` 升级为 `2`，正式表达阶段文档与规则文档两类规范事实源。

### Notes｜说明

- 34 份正式阶段文档数量保持不变；本版本没有新增流程阶段，也没有搬动 `global-contracts.md`。
- Code Quality Rules 只定义普遍质量原则；具体语言、框架、格式、静态检查与 Reviewer 机制由目标项目及 Harness 动态决定。
- 当前状态继续为 `candidate`。

## 0.3.0 - 2026-08-25

### Added｜新增

- 新增面向 Human 的全流程概要，以及 1A / 1B / 2–7 各阶段概要 README，用于快速理解目标、输入、输出与完成条件。
- 新增 Debug / Defect Resolution（调试与缺陷解决）异常流程首个阶段 `Failure Intake & Reproduction（异常接管与复现）`，建立可信 Failure Baseline（故障基线）。
- 新增 `docs/harness-compilation-protocol.md`，将 Harness 构建收敛为 `Read → Derive → Compose → Verify` 四步协议，并建立 Local First、Reuse before Add、Minimum Sufficient Harness、Constraint Preservation 与 Deterministic First 等原则。
- 在文档索引与 `manifest.yaml` 中增加 Harness 编译协议和 Exception Flow 的跨阶段导航入口。

### Changed｜调整

- 将根 README 与全流程概要中的“必读万能 Prompt”替换为轻量 `Build Harness` 入口，由 Agent 内部完成 Harness 编译协议，不把转换步骤转嫁给 Human。
- 明确 Harness 构建优先基于 Spec Coding 与目标项目的本地一致工作区，远程接口主要用于获取、同步、版本确认与必要补充。
- 明确 Harness 只承载正式阶段文档和 Global Contracts 的流程要求，不替代规范事实源；生成时优先复用现有能力，只补真实 Capability Gap / Reliability Gap。
- 将根 `README.md` 收敛为项目简介、快速使用方法与文档入口。
- 将全局执行契约独立为 `docs/global-contracts.md`，将仓库维护与版本管理独立为 `docs/repository-governance.md`。
- 将 `docs/README.md` 收敛为文档索引，并补充跨阶段规则入口。

### Notes｜说明

- 本版本完成 Harness 生成入口从开放式 Prompt 到轻量编译协议的收敛，正式阶段文档仍保持 34 份。
- 当前状态继续为 `candidate`；Debug 异常流程仍在扩展中，Scenario Stress Test、Fresh-Agent Blind Run 与真实项目 Pilot 仍待完成。

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
