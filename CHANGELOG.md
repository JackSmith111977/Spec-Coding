# Changelog｜变更记录

本文件记录 Spec Coding 规范体系的版本级变化。

版本遵循 Semantic Versioning（语义化版本）：

- `MAJOR`：进入稳定版本后，核心阶段、Artifact Contract（产物契约）、状态模型、Gate（门禁）或消费者行为发生不兼容变化。
- `MINOR`：新增或增强兼容能力、规则、治理机制、验证机制或自动化能力；`0.x` 阶段的主要语义演进通常使用 MINOR。
- `PATCH`：不改变流程或规则语义的文案、链接、拼写、格式或纯文档修正。

## Unreleased｜未发布

### Added｜新增

- 新增 Harness Compiler V2 工具实现：双根目录输入、Adoption Baseline / Final Workflow Route 硬前置、Canonical + Adoption 来源解析、稳定 Markdown Block 引用、Compilation State JSON Schema、受限 Compose 与通用 Probe 验证。
- 新增工具级确定性、失败路径、语义审查场景和受控目标级 E2E 测试；实际 Canonical Corpus 仅执行 Resolver / Scanner 集成扫描。

### Changed｜调整

- Harness Compilation Protocol 明确 V2 工具只承担可确定性验证的编译边界；Agent 仍持有自然语言 Contract 推导、Runtime Discovery 与独立语义审查，所有生成状态均为短生命周期证据而非新的 Canonical 事实源。

### Notes｜说明

- 未更新 `VERSION`、Manifest 版本或 Git Tag；只有工具完整验证、文档对齐与后续独立 Review 收敛后，才可评估是否形成版本发布变更。

## 0.10.0 - 2026-08-31

### Added｜新增

- 新增 `docs/reference/harness-primitives.md`，建立跨 Coding Agent Runtime 的 Harness Primitive（Harness 原语）共同语言，并区分 Open Standard / Open Format、De facto Convention 与 Common Harness Primitive。
- 新增 `docs/reference/coding-agent-runtimes.md`，建立 Coding Agent Runtime Reference（运行时参考），首批覆盖 Claude Code、OpenAI Codex、Cursor、GitHub Copilot / VS Code Agent、Gemini CLI、Grok Build、OpenCode、Pi、TRAE / TraeCode、CodeBuddy Code、Qoder CLI、Qwen Code、Kimi Code、ZCode、DeepSeek Harness / DSH 与 MiniMax Code。
- Runtime Reference 对每个 Runtime 只固化 Architecture Invariant（架构不变量）、Harness Implication、Lifecycle 与 Official Sources；当前模型、Thinking、Hook、Feature Flag、Quota 与版本参数继续运行时重新发现。
- 新增 Runtime Capability `native / composable / external / unavailable / unknown` 的轻量归一语义，并明确 `Unknown ≠ Unavailable`。

### Changed｜调整

- Harness Compilation 在既有 `Read → Derive → Compose → Verify` 四步上补齐 `Semantic Guarantee → Harness Primitive → Runtime Architecture → Current Runtime Evidence → Runtime-native Surface` 编译链，不新增第三个 Meta Protocol。
- Read 阶段增加 Runtime Knowledge Resolution：识别实际 Execution Runtime，按需加载 Primitive / Runtime Reference，再结合 Version-matched Official Documentation 与 Local Executable Evidence 建立 Effective Runtime Capability。
- Derive 阶段明确禁止从 Workflow / Rule 直接机械映射到 Vendor-specific Skill / Agent / Workflow 配置；同一 Requirement 可由多个 Primitive 与 Runtime Surface 组合承载。
- Compose 阶段增加 `Portable when equivalent; native when necessary` 原则，并将 Plugin / Extension 纳入 Runtime-specific 组合机制。
- Verify 阶段增加 Runtime Mapping、Version-specific Source Validity、Unknown Closure 与 Reference Drift 检查；Reference 与当前 Runtime 证据冲突时始终以 Current Evidence 为准。
- Repository Governance 明确 Reference 是 non-normative knowledge source，并建立 Feature Delta、Source / Lifecycle Delta、Architecture Delta 三类 Runtime Reference 演进治理。
- `manifest.yaml` 在现有 `reference` / `navigation` 结构中登记 `harness_primitives` 与 `coding_agent_runtimes`；`schema_version` 保持 `4`。
- Glossary 新增 Harness Primitive、Runtime Reference、Runtime Architecture Invariant、Runtime Discovery，并更新 Harness Compilation 定义。
- 根 README、Human Overview、Documentation Index 与 Meta Protocol Index 同步 Runtime-aware Harness Compilation 与两个 Reference 入口。

### Notes｜说明

- 本版本不新增或修改 Main Workflow、Exception Workflow、Canonical Rule 或 Canonical Meta Protocol 集合；34 份 Canonical Stage Documents、4 份 Canonical Rule Documents、4 份 Debug Exception Workflow Documents 与 2 份 Canonical Meta Protocol Documents 保持不变。
- Project Onboarding 与 Agent Delegation & Coordination 语义保持不变：Adoption Baseline 继续不持久化 Agent Capability；Main Agent / Subagent 稳定协作语义继续由现有 Rule 定义，Harness 只负责 Runtime-specific 映射。
- Reference 不是 Runtime Truth，也不是新的 Canonical Source of Truth；其目标是为 Fresh Agent 提供稳定 Bootstrap Knowledge，并通过官方入口引导编译时重新发现版本事实。
- 本次版本收敛前已完成受影响文件完整性检查、Canonical / Manifest 检查、Runtime Fact / Reference 边界检查与跨文档术语 / 消费顺序对齐检查。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与 2–3 个真实项目 Pilot 仍是进入 `1.0.0` 前的稳定门槛。

## 0.9.0 - 2026-08-31

### Added｜新增

- 新增 `docs/rules/agent-delegation-and-coordination.md`，建立 Agent Delegation & Coordination Rules（Agent 委派与协调规则），统一 Main Agent / Subagent 的角色、权限、委派、协调、结果回传与升级语义。
- 正式定义 `Scout / Researcher / Worker / Reviewer / Oracle` 五类 Canonical Subagent Role（规范子 Agent 角色），按认知职责而非前端 / 后端 / 数据库等技术领域划分。
- 新增 Effective Runtime Capability（有效运行时能力）、Capability-aware Routing（能力感知路由）、Minimum Sufficient Capability（最低充分能力）、Thinking Effort（思考强度）、Selection Gap（选择缺口）、Capability / Boundary Problem 等运行时能力语义。
- Harness Compilation 增加 Runtime Capability Discovery：先扫描当前 Coding Agent 实际可用的 Agent / Model / Thinking / Context / Tool / Isolation / Quota，再按需补充 Artificial Analysis、OpenRouter、SWE-bench / Hugging Face Benchmark 或 Local Execution Evidence。

### Changed｜调整

- Global Contracts 明确三层职责：Human / Agent Authority 决定“谁有权决定”，Human-Agent Collaboration 负责 Human ↔ Main Agent，共享认知与决策就绪；Agent Delegation & Coordination 负责 Main Agent ↔ Subagent。
- Human-Agent Collaboration 在 Multi-Agent Harness 中明确 Main Agent 为默认 Human Interaction Surface；Subagent 的局部 Evidence / Finding / Decision Need 先返回 Main Agent，不建立平行的人机决策链。
- Formal Task 继续复用现有 Task Contract + Execution Unit，不新增第二套 Delegation Contract；`tasks.md` 不持久化 Agent、Role、Model、Thinking、Fresh / Fork、Workspace、Attempt 或 Wave。
- Task Set Validation 的大规模独立检查统一映射为 Fresh Reviewer / 其他只读 Subagent；Subagent Review 不成为新的 Gate 或 Task State。
- Ready Task Scheduling 增强 Single Writer Boundary、冲突上报、Execution Attempt 与最低充分 Agent Capability 语义；Model / Thinking / Workspace 等仍由 Harness 运行时推导。
- Autonomous Implementation 明确 Worker 是标准 Worker Role；Capability Problem 优先通过 Context / Thinking / Model / Tool / Strategy 调整解决，不误升级为 Human Authority 问题。
- Task Verification 与 Verification Convergence 统一 Reviewer / Verifier 分工：Verifier 是 Workflow 验证职责，Reviewer 是按需独立推理型 Subagent Role；Reviewer 不替代 Deterministic Gate，也不默认修改被验证实现。
- State Commit 明确 Worker / Role / Model / Thinking / Attempt / Workspace / Fallback 为短生命周期 Execution Metadata，不写入任务权威事实源。
- Harness Compilation 将 `Agent Capability` 深化为 `Discover Runtime → Normalize → External Evidence（按需）→ Role + Work Match → Model + Thinking + Context + Tools + Workspace`，并要求 Fallback 继续满足当前 Capability Requirement。
- README、Human Overview、Rules / Meta Protocol Index、Glossary 与 Manifest 同步 Agent Delegation、能力路由与第 4 份 Canonical Rule Document。

### Notes｜说明

- 本版本不新增 Main Workflow 阶段、Exception Workflow、Meta Protocol 或 Task 状态；34 份 Canonical Stage Documents、4 份 Debug Exception Workflow Documents 与 2 份 Meta Protocol Documents 保持不变。
- Canonical Rule Documents 从 3 份增加到 4 份；`schema_version` 保持 `4`，因为 Manifest 数据模型没有变化。
- 具体模型名称、模型排行榜与 Benchmark 数据不成为 Spec Coding 长期事实源；Harness 始终先发现当前 Runtime Candidate Set，再按真实 Selection Gap 决定是否补外部能力证据。
- `Reviewer ≠ Verification`、`Subagent Result ≠ Canonical Truth`、`Capability Problem ≠ Boundary Problem ≠ Authority Escalation` 均作为兼容现有流程的运行时约束，不引入平行状态机。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与 2–3 个真实项目 Pilot 仍是进入 `1.0.0` 前的稳定门槛。

## 0.8.0 - 2026-08-31

### Added｜新增

- 新增 `docs/meta-protocols/project-onboarding.md`，正式建立 Project Onboarding Protocol（项目接入协议），作为 Harness Compilation 前置的 Canonical Meta Protocol。
- 新增 Adoption Baseline（接入基线）、Usage Contract（使用契约）、Spec Workspace（Spec Coding 工作空间）、Collaboration Mode（协作模式）、Target Identity / Scope、Repository Binding 与 Relevant Delta 等接入语义。
- Project Onboarding 支持 `Initialize / Reuse / Refresh / Migrate` 接入操作，并以 Target / Usage / Spec Coding / Integration Delta 驱动 Affected Trace Only 的增量对齐。
- `manifest.yaml` 正式登记第二份 Canonical Meta Protocol Document，并增加 `project_onboarding` 机器导航入口。

### Changed｜调整

- Spec Coding 使用模型从“直接 Build Harness”调整为 `Project Onboarding → Adoption Baseline → Harness Compilation → 01A / 01B / Resume`，同时保持 Human 只需表达一个自然语言意图，不要求手工执行多个协议命令。
- Harness Compilation 增加 Adoption Context 前置输入，并明确 `Normative Context + Adoption Context + Execution Context → Minimum Sufficient Harness`；Adoption Baseline 缺失或失效时回到 Project Onboarding，而不是静默猜测接入方式。
- Usage Contract 改为由 Collaboration Mode 派生：Local 优先 Human Working Convention，Shared 优先 Team / Shared Workspace Convention，Repository-native 优先 Applicable Repository Convention；Spec Artifact 是否进入目标仓库不再与 Canonical 语义绑定。
- 明确 Workflow 决定 Artifact Contract 与 Task Commit / Requirement Push 语义；Onboarding 只解析 Spec Workspace、Publication Boundary、稳定 Repository / Remote Binding 与 Authority / Integration Constraint，不重复定义 Git 时机或 Worktree 等运行时策略。
- Human-Agent Collaboration Rules 扩展到涉及 Human 意图、权限或关键判断的 Applicable Meta Protocol；Project Onboarding 复用 Evidence before Interaction、Decision Readiness 与 Feedback Integration，不新增独立人工审批层。
- Repository Governance、Human Overview、Documentation Index、Meta Protocol Index 与根 README 同步 Onboarding-first 消费顺序、Adoption Source of Truth 与两份 Meta Protocol 的职责边界。
- Glossary 同步 Project Onboarding / Adoption 相关规范术语，并更新 Harness Compilation / Minimum Sufficient Harness 的定义以包含 Adoption Context。

### Notes｜说明

- 本版本不新增 Stage 0，不修改 34 份 Main Workflow Stage Documents 或 4 份 Debug Exception Workflow Documents；Project Onboarding 属于 Meta Protocol，不推进业务开发阶段。
- Main Workflow 继续拥有 Requirement / Design / Task / Verification 与 Task Commit + Requirement Push 等正式语义；Worktree、Agent、Model 与并行方式继续运行时推导。
- `schema_version` 保持 `4`：本版本只在现有 `meta_protocols` / `navigation` 结构中登记新的 Canonical Meta Protocol 与入口，没有改变 Manifest 数据模型。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与 2–3 个真实项目 Pilot 仍是进入 `1.0.0` 前的稳定门槛。

## 0.7.0 - 2026-08-31

### Added｜新增

- 新增 `docs/workflows/README.md`，将 Main Workflow 与 Exception Workflow 统一收敛到 Workflow 层，并分别归入 `workflows/main/` 与 `workflows/exceptions/`。
- 新增 `docs/meta-protocols/README.md`，正式建立 Meta Protocol（元协议）层；Harness Compilation Protocol 作为首个 Canonical Meta Protocol 登记，不提前创建尚未设计完成的项目接入协议占位文档。
- `manifest.yaml` 新增 `meta_protocols` 与 `canonical_meta_protocol_document_count`，正式登记 1 份 Canonical Meta Protocol Document。
- Glossary 新增 `Meta Protocol（元协议）`，明确其负责 Spec Coding 的项目接入、解释、装配与转换，不作为业务开发阶段推进。

### Changed｜调整

- 文档物理结构按 `workflows / rules / meta-protocols / governance / reference` 五类职责重新组织，使文件系统架构与规范概念模型一致。
- 34 份 Main Workflow Stage Documents 迁移到 `docs/workflows/main/`；4 份 Debug Exception Workflow Documents 迁移到 `docs/workflows/exceptions/`，Stage Identity、顺序与流程语义保持不变。
- `docs/global-contracts.md` 迁移为 `docs/rules/global-contracts.md`，使 3 份 Canonical Rule Documents 统一位于 Rules 层。
- `docs/harness-compilation-protocol.md` 迁移并规范命名为 `docs/meta-protocols/harness-compilation.md`，明确 Meta Protocol 与最终项目侧 Harness 的职责边界。
- `docs/repository-governance.md` 迁移为 `docs/governance/repository-governance.md`；`docs/glossary.md` 迁移为 `docs/reference/glossary.md`。
- `manifest.yaml` `schema_version` 从 `3` 升级为 `4`，同步全部 Canonical 路径、Human 导航入口、治理 / 参考入口与 Agent 消费顺序。
- 根 README、Documentation Index、Human Overview、Rules Index 与 Repository Governance 同步五层目录模型、Meta Protocol 定义和新路径。
- 修正因目录迁移受到影响的 Human-Agent Collaboration、Code Quality、Debug Exception Workflow 与 Manifest 相对引用；未受影响的阶段正文继续复用原 Git blob，避免结构调整引入无关语义 Diff。

### Notes｜说明

- 本版本属于 Directory Architecture Refactor（目录架构重构）：不新增 Main Workflow 阶段，不改变 Stage、Artifact Contract、状态、Gate、Authority、Trigger 或既有流程行为语义。
- Main Workflow 保持 34 份 Canonical Stage Documents，Canonical Rule Documents 保持 3 份，Canonical Exception Workflow Documents 保持 4 份；新增 1 份 Canonical Meta Protocol Document。
- `docs/README.md`、`docs/overview.md` 与 `docs/manifest.yaml` 继续留在 `docs/` 根目录，分别承担 Human Navigation、Human Overview 与 Machine Entry Point。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与 2–3 个真实项目 Pilot 仍是进入 `1.0.0` 前的稳定门槛。

## 0.6.0 - 2026-08-31

### Added｜新增

- 新增 `docs/rules/human-agent-collaboration.md`，建立跨 Main / Exception Workflow 的 Human-Agent Collaboration Rules（人机协作规则），定义 Shared Cognitive Baseline、事件驱动 Cognitive Sync、Decision Readiness 与 Human Feedback Integration。
- `manifest.yaml` 正式登记 `human-agent-collaboration` Canonical Rule Document，规则文档数量从 2 增至 3，并默认适用于所有正式 Workflow。
- Glossary 新增 Human-Agent Collaboration、Shared Cognitive Baseline、Cognitive Sync、Decision Readiness 与 Requirement Sync 等规范术语。

### Changed｜调整

- Global Contracts 将 Human / Agent Authority 与 Human-Agent Collaboration 明确分工：Authority 决定“谁能决定”，Collaboration 决定“什么时候协作、Human 判断前需要同步什么，以及反馈如何回到事实源”。
- Tailoring 的核心不变量补充 Human-Agent Collaboration：真实 Sync Trigger 或 Human 决策边界成立时，必要 Cognitive Sync / Decision Readiness 不得因流程裁剪而消失，同时不为未触发场景增加人工审批。
- Harness Compilation Protocol 将 Human-Agent Collaboration 纳入 Applicable Rules 的 Read / Derive / Verify，并明确不得把事件驱动同步机械编译成每阶段 Human Review。
- Business Understanding 在形成或显著修正关键业务模型时按 Trigger 进行必要 Cognitive Sync，要求 Agent 先完成证据探索，再请求 Human 校正业务语义。
- Ambiguity & Gap Identification 在向 Human 发起澄清前先基于 Context / Evidence 缩小问题，提供当前理解、不确定性与影响；可自主确认的信息不转交 Human，涉及关键语义决策时继续满足 Decision Readiness。
- Scope / Rule、Acceptance Criteria 与 Technical Decision 在进入关键 Human Decision / Confirm 前要求满足 Decision Readiness；已有共享上下文仍有效时只同步关键 Delta。
- Development Execution 保持 Contract-bound Autonomy：普通 Task 内搜索、实现、局部修复与验证不触发 Human；只有 Contract Boundary / Authority Escalation 等真实 Trigger 才升级协作。
- Human Acceptance 与 Verification Finding Triage 改为提供可判断上下文；Accepted Deviation 或上游共享模型失效时先同步 Expected / Actual、Evidence、Impact / Risk 与 Affected Trace，再进入 Human 判断。
- Brownfield Requirement 在 Requirement Interpretation 首次进入需求澄清链时建立稳定 `REQ-xx`；Greenfield 继续继承 Requirement Framework 身份，Acceptance Criteria 不再承担二次分配职责。
- Detailed Technical Design 与 Task Set Validation 统一使用全局 `Open Item / OI-xxx`，移除 `Open Issues` 平行未决对象语义。
- 技术设计正式 Artifact 名称统一为 `Impact Baseline → Solution Decision → Detailed Technical Design → Design Acceptance Result`，与实施规划和 Debug 消费名称一致。
- Requirement Sync 明确为 Requirement Integration、Requirement AC Gate、Requirement Push 状态及必要 `code_ref` 的非权威聚合视图，不形成第四个需求级状态事实源。
- Multi-dimensional Verification 移除旧的统一 `Human Triage` 语义，改为按 Human / Agent Authority Contract 进行 Finding 分类与路由；Evidence Closure 将 Finding `Decision` 与生命周期 `Status` 分离维护。
- Verification Convergence 概要补齐 Implementation Baseline 输入；Development Execution 的正式 `Verification` 统一使用“验证”表述，Human Acceptance 继续保持“人工验收”。
- Process Review Improvement 的改进对象统一为可复用 `Workflow / Rules / Harness`，并修正 Evidence Collection 的前向链路为 `source → EV → Process Timeline → ISS → RC → IMP`。
- `Validation` 的正式中文解释按 Glossary 统一为“有效性确认”，Task Set Validation 与 Implementation & Validation 的阶段入口同步规范译法。
- README、Human Overview、Rules Index 与 Documentation Index 同步 Human-Agent Collaboration 导航、规则数量与流程复盘对象。

### Notes｜说明

- 本版本不新增 Main Workflow 阶段，也不引入独立 Human Review Stage；协作规则全局适用，但 Human Interaction 由真实 Trigger 驱动。
- Main Workflow 保持 34 份正式阶段文档，Canonical Rule Documents 为 3 份，Canonical Exception Workflow Documents 为 4 份；`schema_version` 保持 `3`。
- 当前状态继续为 `candidate`；Scenario Stress Test、Fresh-Agent Blind Run 与 2–3 个真实项目 Pilot 仍是进入 `1.0.0` 前的稳定门槛。

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
