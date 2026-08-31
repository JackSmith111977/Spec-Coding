# Glossary｜术语表

本文件定义 Spec Coding 文档中的 Canonical Terminology（规范术语）。它属于 Reference（参考）文档，不计入正式 Workflow、Rule 或 Meta Protocol 文档。

## 使用规则

- 非直观英文术语在单篇文档首次承担关键语义时，使用 `English Term（中文解释）`；含义建立后可直接使用英文。
- 同一个英文术语只使用本表中的一个规范中文解释，避免同义词漂移。
- 中文解释以**语义准确**为优先，不做机械直译。例如 `Harness` 统一为“执行框架”，不采用字面翻译。
- Schema 字段、状态值、ID、代码标识等可以保留英文，例如 `status = open`、`code_ref`、`REQ-01`；必要说明使用中文。
- `Spec Coding` 是整套流程 / 方法名称，不默认对应独立 `Spec` 产物。具体项目存在真实机器规格时，使用 `Technical Contract（技术契约）` 或 `Executable Specification（可执行规格）` 等准确名称。
- 新增会影响规范理解的核心英文术语时，优先先更新本表，再在正式文档中使用。

## 核心流程术语

| English | 中文 | 含义 |
|---|---|---|
| Specification-Driven Development (SDD) | 规格驱动开发 | 以明确需求、设计、任务和验证契约驱动实施的开发方式。 |
| Canonical Corpus | 规范文档集 | 当前版本唯一有效的正式文档集合。 |
| Canonical Source of Truth | 规范事实源 | 当前应被下游视为权威依据的唯一来源。 |
| Manifest | 清单 | 机器可读的正式 Workflow、Rule、Meta Protocol 与导航结构定义。 |
| Workflow | 流程 | 规定活动如何按阶段、状态与反馈路径推进的执行路径。 |
| Main Workflow | 主流程 | Spec Coding 正常情况下由项目定义 / 认知建立推进到流程复盘改进的主路径。 |
| Exception Workflow | 异常流程 | 由故障、异常或未决问题按需触发的跨阶段流程，完成处理后将可信结论回交主流程。 |
| Rule | 规则 | 执行过程中持续适用的原则、约束或质量要求；本身不负责推进阶段状态。 |
| Meta Protocol | 元协议 | 定义 Spec Coding 如何被项目接入、解释、装配或转换为可执行机制的上层协议；本身不作为业务开发阶段推进。 |
| Artifact | 产物 | 流程中形成并可被后续阶段消费的结构化结果。 |
| Requirement | 需求 | 需要实现或改变的业务 / 系统目标与行为。 |
| Acceptance Criteria (AC) | 验收标准 | 用于明确判断 Requirement 是否成立的可验证标准。 |
| Scope | 范围 | 当前 Requirement 明确包含与不包含的内容。 |
| Boundary | 边界 | 限制行为、职责或影响扩张的明确界线。 |
| Baseline | 基线 | 已经收敛、可供下游稳定消费的一组有效事实。 |
| Contract | 契约 | 对目标、边界、输入输出、验证或行为的明确约束。 |
| Context | 上下文 | 当前任务理解与执行所需的相关信息集合。 |
| Trace | 追溯链 | 当前对象与其上游 / 下游来源之间的关联链。 |
| Traceability | 可追溯性 | 能从结果回查其 Requirement、Design、Task、Change 与 Evidence 的能力。 |
| Handoff | 交接 | 一个阶段或 Workflow 将已收敛结果交给下游继续消费的过程。 |
| Tailoring | 流程裁剪 | 根据风险和影响范围动态调整流程执行深度。 |
| Gate | 门禁 | 必须满足后才能进入下一状态或阶段的准入条件。 |

## 接入与元协议术语

| English | 中文 | 含义 |
|---|---|---|
| Project Onboarding | 项目接入 | 在 Harness Compilation 之前，建立、复用、刷新或迁移 Spec Coding 与当前 Target 的稳定接入关系。 |
| Adoption Baseline | 接入基线 | 当前 Target 如何采用 Spec Coding 的唯一接入事实源，只保存长期使用意图、稳定绑定及必要 Override / Constraint。 |
| Usage Contract | 使用契约 | 由 Collaboration Mode 派生的 Spec Workspace、Artifact Publication、Repository Binding、Authority 与 Integration 等长期使用约定。 |
| Spec Workspace | Spec Coding 工作空间 | Requirement、Design、Task、Evidence、Adoption Baseline 等 Spec Coding 持久工作状态的承载空间；可与目标 Repository 分离。 |
| Collaboration Mode | 协作模式 | Spec Coding 工作状态的共享边界；当前规范使用 `Local`、`Shared`、`Repository-native` 三类语义。 |
| Target Identity | 目标身份 | 用于稳定识别当前 Spec Coding 接入对象的身份锚点，防止不同 clone、fork、Repository 或项目之间误复用接入状态。 |
| Target Scope | 目标范围 | Spec Coding 当前负责管理和追踪的变化边界；不等同于 Harness 放置范围。 |
| Repository Binding | 仓库绑定 | 为执行现有 Workflow Git 语义而解析的稳定 Repository、Remote、Base / Development Branch、Push / PR Target 等绑定关系。 |
| Relevant Delta | 相关变化 | 足以使当前 Adoption Fact 或其派生约定失效的 Target、Usage、Spec Coding 或 Integration 变化。 |
| Initialize | 初始化接入 | 当前 Target 尚无可复用 Adoption 时建立新的接入基线。 |
| Reuse | 复用接入 | 当前 Adoption 仍有效，无需重建或修改。 |
| Refresh | 刷新接入 | Target / Usage 等项目侧事实变化后，只更新受影响接入链路。 |
| Migrate | 迁移接入 | Spec Coding / Integration 语义变化导致旧 Adoption 需要转换时，只迁移受影响语义。 |

## 设计与实施术语

| English | 中文 | 含义 |
|---|---|---|
| Design | 设计 | 为满足 Requirement 所形成的技术决策与具体方案。 |
| Technical Contract | 技术契约 | API、Schema、协议等具有明确机器 / 系统边界的技术规格。 |
| Executable Specification | 可执行规格 | 能被工具直接检查或执行的规格定义。 |
| Trade-off | 取舍 | 为获得某项收益而接受的成本、限制或风险。 |
| Task | 任务 | 可独立实施且可独立证明正确的执行单元。 |
| Primary Requirement | 主需求 | Task 用于 Requirement 级汇合的唯一主要归属。 |
| Coverage | 覆盖范围 | Task 或 Verification 必须覆盖的关键行为路径。 |
| Task Contract | 任务契约 | Task 的 Goal、Boundary、Coverage、Verification、Done 等约束集合。 |
| Main Agent | 主 Agent | 当前 Workflow 的全局协调与收敛主体，持有 Workflow State、跨 Agent 协调、结果整合、Authority Routing 与最终责任。 |
| Subagent | 子 Agent | 由 Main Agent 为上下文隔离、独立执行、独立审查或其他有界工作临时委派的 Agent。 |
| Scout | 侦察 Agent | 探索项目内部事实、定位入口与链路，并返回最小充分 Context / Evidence 的 Subagent Role。 |
| Researcher | 研究 Agent | 获取外部官方资料、标准、当前行为、Benchmark 与技术证据的 Subagent Role，不拥有项目决策权。 |
| Worker | 执行 Agent | 在既定 Delegation / Task Contract 内完成具体修改、局部验证与必要修复的 Subagent Role。 |
| Reviewer | 审查 Agent | 对候选结果执行独立、证据驱动审查并形成 Finding / Verdict 的 Subagent Role；不替代正式 Verification。 |
| Oracle | 一致性顾问 Agent | 检查当前方向是否偏离继承决策、约束或已确认事实的只读 Challenge Role，不拥有最终决策权。 |
| Delegation | 委派 | Main Agent 将目标、边界、上下文、权限与预期结果明确交给 Subagent 执行的运行时协作行为。 |
| Single Writer Boundary | 单写入者边界 | 同一可变工作边界在同一时刻默认只有一个 Worker Owner，避免共享写入冲突。 |
| Harness | 执行框架 | 组织 Agent、工具、上下文、状态、规则与验证的运行机制。 |
| Harness Primitive | Harness 原语 | 跨 Coding Agent Runtime 描述 Rule、Skill、Tool、Subagent、Hook、Permission、Sandbox、Workspace 等稳定能力语义的中间抽象；具体实现由当前 Runtime 决定。 |
| Runtime Reference | 运行时参考 | 为 Harness Compilation 提供 Coding Agent 的架构不变量与官方事实入口的非规范 Reference；不作为当前 Runtime Capability 的权威来源。 |
| Runtime Architecture Invariant | 运行时架构不变量 | 会实质影响 Harness 编译策略、跨版本相对稳定且具有官方证据的 Runtime 底层设计特征。 |
| Runtime Discovery | 运行时发现 | 在 Harness Compilation 中识别当前执行 Runtime，并结合当前官方资料与本地可执行证据确认实际 Capability 的过程。 |
| Harness Compilation | Harness 编译 | 通过 Harness Compilation Meta Protocol，将 Applicable Workflow / Rules 与有效 Adoption Baseline 的语义要求归一为必要 Harness Primitive，再结合 Runtime Architecture 与当前 Runtime Evidence 映射为最小充分 Harness 的过程。 |
| Minimum Sufficient Harness | 最小充分 Harness | 只保留可靠满足当前流程、规则与接入约束所需的最少 Harness 组件，避免重复能力与过度设计。 |
| Effective Runtime Capability | 有效运行时能力 | 当前 Coding Agent Runtime 实际暴露并可执行的 Model、Thinking、Context、Tool、Isolation、Quota 等能力，而非 Provider 理论能力。 |
| Capability-aware Routing | 能力感知路由 | 先发现当前 Runtime 可用能力，再结合 Role、任务特征与必要证据选择 Model / Thinking / Context / Tool 等执行配置。 |
| Minimum Sufficient Capability | 最低充分能力 | 能够可靠满足当前 Delegation / Execution Contract 的最低充分运行时能力配置。 |
| Thinking Effort | 思考强度 | Runtime 对模型推理预算或推理深度的可调级别；具体档位由当前 Coding Agent / Model 实现决定。 |
| Capability Gap | 能力缺口 | 当前 Agent 或项目环境缺少完成某项流程 / 规则要求所需的能力。 |
| Reliability Gap | 可靠性缺口 | 所需能力已经存在，但当前机制无法稳定保证流程 / 规则要求被执行。 |
| Selection Gap | 选择缺口 | 当前 Runtime 存在多个有效候选且不同配置会实质影响质量、成本或延迟，但缺少可靠路由依据。 |
| Capability Problem | 能力问题 | 当前失败主要来自 Context、Model、Thinking、Tool 或 Runtime 能力不足，而不是业务契约或权限本身失效。 |
| Boundary Problem | 边界问题 | 继续工作必须突破当前 Delegation / Task Boundary，需要 Main Agent 重新判断工作划分或上游事实。 |
| Context Isolation | 上下文隔离 | 只给执行单元提供最小必要上下文，降低相互干扰。 |
| Runnable | 当前可执行 | 当前依赖与运行条件均满足，可立即被调度执行。 |
| Blocked | 阻塞 | 当前对象因缺失条件或未决问题无法继续推进。 |

## 验证与证据术语

| English | 中文 | 含义 |
|---|---|---|
| Verification | 验证 | 使用证据证明结果满足既定 Requirement / Design / Task 契约。 |
| Validation | 有效性确认 | 判断对象是否适合当前用途或满足预期；避免与当前流程正式 `Verification` 产物混用。 |
| Verifier | 验证执行者 | 在 Workflow 中承担 Verification 职责的 Agent、工具或组合机制；可以调用 Reviewer，但不与 Reviewer Role 等同。 |
| Evidence | 证据 | 可复核、可追溯并支持某个结论的事实。 |
| Finding | 验证发现 | Verification 中观察到、需要判定或处理的具体事实。 |
| Deterministic Verification | 确定性验证 | 能由工具产生明确 Pass / Fail 或可判定结果的验证。 |
| Read-only Verification | 只读验证 | 不修改业务代码 / 配置 / 数据模型，只观察并验证实际结果。 |
| Independent Review | 独立审查 | 由与实现过程尽量隔离的 Reviewer / Verifier 重新检查结果。 |
| Human Acceptance | 人工验收 | 机器证据不足以替代业务 / UX 判断时，由 Human 完成最终确认。 |
| Fresh Context | 新上下文 | Reviewer / Verifier 不继承实现过程中的中间推理和偏见。 |
| Evidence over Claim | 证据优于声明 | 结论以可复核证据为准，而不是以执行者自述为准。 |
| Reverification | 重新验证 | 在纠正后仅对受影响范围及必要回归重新执行 Verification，并形成新的有效 Evidence。 |

## 异常与调试术语

| English | 中文 | 含义 |
|---|---|---|
| Reproduction | 复现 | 在明确条件下重新观察原始 Failure，或建立可靠的替代观察方式。 |
| Failure Baseline | 故障基线 | 对 Failure 的现象、Expected / Actual、上下文、复现状态与原始 Evidence 的稳定记录。 |
| Fault Boundary | 故障边界 | 基于 Evidence 已经收敛出的具体异常范围，用于限制后续根因调查空间。 |
| Root Cause | 根因 | 能够以充分 Evidence 解释关键 Failure 与 Divergence 的底层原因。 |
| Root Cause Resolution | 根因处置结果 | Root Cause、Invalid Source、Affected Trace、Correction Route 与 Reverification Scope 的结构化结论。 |
| Failure Closure | 故障关闭结果 | 对当前 Failure 的纠正、原始故障回归、受影响链路 Reverification 与 Resolved / Blocked 状态的最终记录；不替代主流程权威状态。 |

## 偏差与纠偏术语

| English | 中文 | 含义 |
|---|---|---|
| Open Item | 开放项 | 尚未解决且需要后续继续承接的具体问题或决策。 |
| Risk | 风险 | 未来可能发生并造成不利影响的不确定因素。 |
| Deviation | 偏差 | 实际结果与已确认事实源 / 契约之间的不一致。 |
| Accepted Deviation | 接受偏差 | 已确认存在，但经 Human 明确接受并记录风险的偏差。 |
| Correct the Earliest Invalid Source | 修正最早失效的事实源 | 纠偏时优先修改最早发生错误的权威来源。 |
| Affected Trace Only | 仅处理受影响追溯链 | 只重新对齐和验证真正受偏差影响的链路。 |
| Reference over Duplication | 引用优先 | 下游引用已有事实对象，而不是复制出新的事实源。 |
| Attribution before Escalation | 先归因，再升级 | 先判断问题所属层级，再决定是否需要升级处理。 |

## Git 与状态收敛术语

| English | 中文 | 含义 |
|---|---|---|
| Task Commit | 任务提交 | 单 Task 局部验证通过后形成的可追溯 Git 提交。 |
| code_ref | 代码引用 | 指向被正式验证实现版本的稳定 Commit / Patch 等引用。 |
| Requirement Integration | 需求级集成 | 将同一 Requirement 下已完成 Task 的结果汇合。 |
| Requirement AC Gate | 需求级验收门禁 | 在 Requirement Push 前确认该需求 Acceptance Criteria 已满足的门禁。 |
| Requirement Push | 需求级推送 | 将 Requirement 级已集成代码同步到远程开发 / Requirement 分支；不代表 Merge、Release、Deploy 或最终 Verified。 |
| Requirement Sync | 需求同步 | Requirement Integration、Requirement AC Gate 与 Requirement Push 状态及必要 `code_ref` 的聚合消费视图；不形成新的权威事实源。 |
| Change Set | 变更集 | 当前需要被验证的实际代码、配置、数据与接口变更集合。 |
| Ready | 就绪 | 已通过规划准入，但不一定当前可执行。 |
| Verifying | 验证中 | 已形成稳定待验证结果，正在执行正式 Verification。 |
| Done | 完成 | Task Verification 已通过，Task 已闭环。 |

## 权限与治理术语

| English | 中文 | 含义 |
|---|---|---|
| Authority | 决策权限 | Human / Agent 对某类动作或决策可自主执行到什么程度。 |
| Autonomous | Agent 自主 | 在既定契约内可直接执行，无需重复请求确认。 |
| Confirm | Agent 提议 + Human 确认 | Agent 先基于证据给出建议，由 Human 确认后生效。 |
| Human Decision | Human 决策 | 直接改变业务意图、正确性标准或风险接受边界的决策。 |
| Human-Agent Collaboration | 人机协作 | Human 与 Agent 在保持权限边界的同时，通过必要认知同步、决策就绪和反馈吸收共同推进工作。 |
| Shared Cognitive Baseline | 共享认知基线 | Human 与 Agent 为继续协作共同依赖的最小充分认知，包括目标、关键模型、状态、变化、不确定性、下一步与必要证据入口。 |
| Cognitive Sync | 认知同步 | 在关键认知建立、变化、失效或决策边界出现时，向 Human 同步做出后续判断所需的最小信息。 |
| Decision Readiness | 决策就绪 | Human 已拥有理解当前目标、模型、关键变化、证据、选项与影响所需的最小上下文，可以进行有效 Confirm / Human Decision / Human Acceptance。 |
| Process Review | 流程复盘 | 基于真实执行证据分析 Workflow / Rules / Meta Protocol / Harness 的可复用机制问题。 |
| Improvement | 改进 | 对可复用 Workflow / Rules / Meta Protocol / Harness 机制进行可验证调整。 |

## 术语变更规则

若需要修改某个规范译法或含义，应同时检查其所有关键定义点和下游契约。纯措辞调整可按文档修复处理；若术语变化会改变 Artifact、状态、Gate 或消费者行为，应按语义变更进行版本治理。