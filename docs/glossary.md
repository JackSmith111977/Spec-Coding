# Glossary｜术语表

本文件定义 Spec Coding 文档中的 Canonical Terminology（规范术语）。它属于治理文档，不计入 34 份正式阶段文档。

## 使用规则

- 非直观英文术语在单篇文档首次承担关键语义时，使用 `English Term（中文解释）`；含义建立后可直接使用英文。
- 同一个英文术语只使用本表中的一个规范中文解释，避免同义词漂移。
- 中文解释以**语义准确**为优先，不做机械直译。例如 `Harness` 统一为“执行框架”，不采用字面翻译。
- Schema 字段、状态值、ID、代码标识等可以保留英文，例如 `status = open`、`code_ref`、`REQ-01`；必要说明使用中文。
- `Spec Coding` 是整套流程 / 方法名称，不默认对应独立 `Spec` 产物。具体项目存在真实机器规格时，使用 `Technical Contract（技术契约）` 或 `Executable Specification（可执行规格）` 等准确名称。
- 新增会影响流程理解的核心英文术语时，优先先更新本表，再在阶段文档中使用。

## 核心流程术语

| English | 中文 | 含义 |
|---|---|---|
| Specification-Driven Development (SDD) | 规格驱动开发 | 以明确需求、设计、任务和验证契约驱动实施的开发方式。 |
| Canonical Corpus | 规范文档集 | 当前版本唯一有效的正式文档集合。 |
| Canonical Source of Truth | 规范事实源 | 当前应被下游视为权威依据的唯一来源。 |
| Manifest | 清单 | 机器可读的正式文档与阶段结构定义。 |
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
| Handoff | 交接 | 一个阶段将已收敛结果交给下游继续消费的过程。 |
| Tailoring | 流程裁剪 | 根据风险和影响范围动态调整流程执行深度。 |
| Gate | 门禁 | 必须满足后才能进入下一状态或阶段的准入条件。 |

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
| Main Agent | 主 Agent | 负责整体编排、汇总与跨任务协调的 Agent。 |
| Worker Agent | 执行 Agent | 在既定 Task Contract 内完成具体实施的 Agent。 |
| Subagent | 子 Agent | 为上下文隔离、并行或独立检查而临时委派的 Agent。 |
| Harness | 执行框架 | 组织 Agent、工具、上下文、状态、规则与验证的运行机制。 |
| Context Isolation | 上下文隔离 | 只给执行单元提供最小必要上下文，降低相互干扰。 |
| Runnable | 当前可执行 | 当前依赖与运行条件均满足，可立即被调度执行。 |
| Blocked | 阻塞 | 当前对象因缺失条件或未决问题无法继续推进。 |

## 验证与证据术语

| English | 中文 | 含义 |
|---|---|---|
| Verification | 验证 | 使用证据证明结果满足既定 Requirement / Design / Task 契约。 |
| Validation | 有效性确认 | 判断对象是否适合当前用途或满足预期；避免与当前流程正式 `Verification` 产物混用。 |
| Evidence | 证据 | 可复核、可追溯并支持某个结论的事实。 |
| Finding | 验证发现 | Verification 中观察到、需要判定或处理的具体事实。 |
| Deterministic Verification | 确定性验证 | 能由工具产生明确 Pass / Fail 或可判定结果的验证。 |
| Read-only Verification | 只读验证 | 不修改业务代码 / 配置 / 数据模型，只观察并验证实际结果。 |
| Independent Review | 独立审查 | 由与实现过程尽量隔离的 Reviewer / Verifier 重新检查结果。 |
| Human Acceptance | 人工验收 | 机器证据不足以替代业务 / UX 判断时，由 Human 完成最终确认。 |
| Fresh Context | 新上下文 | Reviewer / Verifier 不继承实现过程中的中间推理和偏见。 |
| Evidence over Claim | 证据优于声明 | 结论以可复核证据为准，而不是以执行者自述为准。 |

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
| Change Set | 变更集 | 当前需要被验证的实际代码、配置、数据与接口变更集合。 |
| Ready | 就绪 | 已通过规划准入，但不一定当前可执行。 |
| Verifying | 验证中 | 已形成稳定待验结果，正在执行正式 Verification。 |
| Done | 完成 | Task Verification 已通过，Task 已闭环。 |

## 权限与治理术语

| English | 中文 | 含义 |
|---|---|---|
| Authority | 决策权限 | Human / Agent 对某类动作或决策可自主执行到什么程度。 |
| Autonomous | Agent 自主 | 在既定契约内可直接执行，无需重复请求确认。 |
| Confirm | Agent 提议 + Human 确认 | Agent 先基于证据给出建议，由 Human 确认后生效。 |
| Human Decision | Human 决策 | 直接改变业务意图、正确性标准或风险接受边界的决策。 |
| Process Review | 流程复盘 | 基于真实执行证据分析流程问题与可复用机制缺口。 |
| Improvement | 改进 | 对可复用 SDD / Harness 规则本身进行可验证调整。 |

## 术语变更规则

若需要修改某个规范译法或含义，应同时检查其所有关键定义点和下游契约。纯措辞调整可按文档修复处理；若术语变化会改变 Artifact、状态、Gate 或消费者行为，应按语义变更进行版本治理。
