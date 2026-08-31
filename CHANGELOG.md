# Changelog｜变更记录

本文件记录 Spec Coding 规范体系的版本级变化。

版本遵循 Semantic Versioning（语义化版本）：

- `MAJOR`：进入稳定版本后，核心阶段、Artifact Contract（产物契约）、状态模型、Gate（门禁）或消费者行为发生不兼容变化。
- `MINOR`：新增或增强兼容能力、规则、治理机制、验证机制或自动化能力；`0.x` 阶段的主要语义演进通常使用 MINOR。
- `PATCH`：不改变流程或规则语义的文案、链接、拼写、格式或纯文档修正。

## Unreleased｜未发布

### Added｜新增

- 新增 `docs/rules/human-agent-collaboration.md`，建立跨 Main / Exception Workflow 的 Human-Agent Collaboration Rules（人机协作规则），定义 Shared Cognitive Baseline、事件驱动 Cognitive Sync、Decision Readiness 与 Human Feedback Integration。
- `manifest.yaml` 正式登记 `human-agent-collaboration` Canonical Rule Document，规则文档数量从 2 增至 3，并默认适用于所有正式 Workflow。
- Glossary 新增 Human-Agent Collaboration、Shared Cognitive Baseline、Cognitive Sync 与 Decision Readiness 等规范术语。

### Changed｜调整

- Global Contracts 将 Human / Agent Authority 与 Human-Agent Collaboration 明确分工：Authority 决定“谁能决定”，Collaboration 决定“什么时候协作、Human 判断前需要同步什么，以及反馈如何回到事实源”。
- Harness Compilation Protocol 将 Human-Agent Collaboration 纳入 Applicable Rules 的 Read / Derive / Verify，并明确不得把事件驱动同步机械编译成每阶段 Human Review。
- Business Understanding 在形成或显著修正关键业务模型时按 Trigger 进行必要 Cognitive Sync，要求 Agent 先完成证据探索，再请求 Human 校正业务语义。
- Scope / Rule、Acceptance Criteria 与 Technical Decision 在进入关键 Human Decision / Confirm 前要求满足 Decision Readiness；已有共享上下文仍有效时只同步关键 Delta。
- Development Execution 保持 Contract-bound Autonomy：普通 Task 内搜索、实现、局部修复与验证不触发 Human；只有 Contract Boundary / Authority Escalation 等真实 Trigger 才升级协作。
- Human Acceptance 与 Verification Finding Triage 改为提供可判断上下文；Accepted Deviation 或上游共享模型失效时先同步 Expected / Actual、Evidence、Impact / Risk 与 Affected Trace，再进入 Human 判断。
- Process Review Improvement 在改变规则 / Harness 行为语义前优先向 Human 展示 Behavior Delta、根因证据、收益与新增成本 / 风险，而不是让 Human 从完整 Rule Diff 重建影响。
- README、Human Overview、Rules Index 与 Documentation Index 同步 Human-Agent Collaboration 导航和规则数量。

### Notes｜说明

- 本次变更不新增 Main Workflow 阶段，也不引入独立 Human Review Stage；协作规则全局适用，但 Human Interaction 由真实 Trigger 驱动。
- `VERSION` 暂保持 `0.5.0`；待本轮规则 Review / Verification 收敛后再决定是否形成 `0.6.0` release。

## 0.5.0 - 2026-08-28

### Added｜新增

- 完成 Debug & Defect Resolution（调试与缺陷解决）四阶段 Exception Workflow（异常流程）：Failure Intake & Reproduction、Evidence Collection & Fault Localization、Root Cause Confirmation & Correction Routing、Fix Verification & Failure Convergence。
- 新增 `docs/exception-flows/README.md` 与 Debug Workflow 概要 README，建立异常流程的 Human 导航入口。
- 新增 `Failure Baseline`、`Fault Localization Result`、`Root Cause Resolution` 与 `Failure Closure` 等跨阶段 Debug 产物契约。
- `manifest.yaml` 新增 `exception_workflows` 与 `canonical_exception_document_count`，正式登记 4 份 Canonical Exception Workflow Document（正式异常流程文档）。
- Glossary 新增 Main Workflow、Exception Workflow、Reproduction、Failure Baseline、Fault Boundary、Root Cause、Root Cause Resolution、Failure Closure 与 Reverification 等规范术语。

### Changed｜调整

- `manifest.yaml` `schema_version` 升级为 `3`，机器可读规范从 Stage Documents + Rule Documents 扩展为 Stage + Rule + Exception Workflow 三类正式文档。
- Global Contracts 从“所有正式阶段默认继承”扩展为“所有正式 Workflow 默认继承”，使 Exception Workflow 正式继承 Tailoring、Open Item 与 Human / Agent Authority 等全局规则。
- Harness Compilation Protocol 通过 `manifest.yaml.exception_workflows` 识别并仅在 Trigger 成立时加载 Exception Workflow；Applicable Workflow 明确为 Current Main Workflow + Triggered Exception Workflow。
- Development Execution 在 Task Verification 无法可靠归因时进入 Debug Workflow；可明确归因的普通 Implementation Defect 仍保持最短局部修复路径。
- Verification Convergence 在 `Unresolved` Finding 需要进一步诊断故障边界或根因时进入 Debug Workflow，并在获得 Root Cause / Failure Closure Evidence 后回到原 Finding 流程继续收敛。
- 明确 Debug 只形成调查、纠正与 Failure Closure Evidence，不复制或替代 Task、Finding、Open Item、Verification 等主流程权威状态；`Failure Closure = Resolved` 不等于 Requirement `Verified`。
- Repository Governance 增加 Canonical Exception Workflow Document 与 Exception Workflow Source of Truth 治理规则。
- README、Human Overview 与文档索引同步异常流程入口、主流程回接关系与 `0.5.0` 版本信息。

### Notes｜说明

- Main Workflow 仍保持 34 份正式阶段文档，Rule Documents 仍为 2 份；新增 4 份正式 Exception Workflow 文档，不引入 Stage 8。
- Debug Workflow 按需触发，不要求普通 Task 内可局部闭环的 `Diagnose → Repair → Recheck` 全部升级为正式异常流程。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与真实项目 Pilot 仍待完成。

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
