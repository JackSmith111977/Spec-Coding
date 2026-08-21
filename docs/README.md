# Spec Coding 文档索引

本目录按 Spec Coding 主流程阶段组织当前正式文档。

当前 Canonical Corpus（规范文档集）的机器可读定义见 [`manifest.yaml`](manifest.yaml)。该 Manifest 是判断“哪些阶段文档属于当前版本”的唯一清单；本文件负责导航，并承载所有阶段默认继承的全局执行契约。

## 流程

```text
新项目：项目定义建立 ─┐
                    ├→ 需求澄清 → 技术方案设计 → 实施规划 → 开发实施 → 验证收敛 → 流程复盘改进
存量项目：项目认知建立 ─┘
```

## 目录

- `01a-project-definition/`：新项目入口——项目定义建立
- `01b-project-understanding/`：存量项目入口——项目认知建立
- `02-requirement-clarification/`：需求澄清
- `03-technical-design/`：技术方案设计
- `04-implementation-planning/`：实施规划
- `05-development-execution/`：开发实施
- `06-verification-convergence/`：验证收敛
- `07-process-review-improvement/`：流程复盘改进

两种入口在需求澄清阶段汇合；流程复盘改进针对可复用 SDD / Harness（执行框架）规则本身。

## Canonical 规则

- 当前版本共有 34 份正式阶段文档；单次真实流程只消费其中一条入口分支，因此通常执行 30 份阶段规则。
- `README.md`、`manifest.yaml`、`glossary.md`、`CHANGELOG.md` 等属于治理或导航文件，不计入正式阶段文档数量。
- 本文件中的全局 Contract（契约）默认适用于全部正式阶段文档；阶段文档存在更严格规则时，以更严格规则为准。
- 正式文件的新增、删除和重命名必须同步更新 `manifest.yaml`。
- 历史版本由 Git 保存，不在 `docs/` 中保留带 `(1)`、`(2)`、`v1`、`old` 等后缀的并行正式副本。

## Terminology Contract｜术语治理契约

所有核心英文术语及规范中文解释统一见 [`glossary.md`](glossary.md)。Glossary（术语表）是唯一术语锚点，阶段文档不得自行创造同义译法。

- 非直观英文术语在单篇文档首次承担关键语义时，使用 `English Term（中文解释）`；含义建立后可直接使用英文。
- Schema 字段、状态值、ID 与代码标识可保留英文，例如 `status = open`、`code_ref`、`REQ-01`，不要求机械双语化。
- 中文解释以语义准确为优先，不做字面直译；例如 `Harness` 固定解释为“执行框架”。
- 同一英文术语应使用 Glossary 中的唯一规范中文解释；如需改变译法或含义，应先更新 Glossary 并检查受影响定义点。
- `Spec Coding` 是流程 / 方法名称，不默认对应独立 `Spec` 产物；真实 API / Schema 等规格应按 `Technical Contract（技术契约）`、`Executable Specification（可执行规格）` 等实际类型命名。

> **First occurrence bilingual, terminology canonical｜首次关键出现双语，后续术语保持统一。**

## Tailoring Contract｜流程裁剪契约

Tailoring（流程裁剪）用于根据**变更风险、影响范围与不确定性**动态调整执行深度，而不是机械要求每次都以同样篇幅执行全部阶段。

核心原则：

> **Mandatory Invariants + Risk-based Depth｜核心不变量固定，执行深度按风险调整。**

阶段责任不会因为裁剪而消失，但可以被已有、仍然有效的 Artifact（产物）或 Evidence（证据）直接满足，不要求重复分析或重新生成同类文档。

### 执行深度

| 深度 | 适用情况 | 执行方式 |
|---|---|---|
| `Reuse`（复用） | 已有上下文、设计或证据仍完整覆盖当前变化 | 验证其相关性与有效性后直接复用，只更新受影响 Trace（追溯链） |
| `Light`（轻量） | 局部、低风险、边界清晰的变化 | 最小必要分析与产物更新，聚焦受影响路径和验证 |
| `Standard`（标准） | 一般 Feature（功能）或常规跨层变化 | 按阶段正常展开，保留必要决策、任务与验证证据 |
| `Deep`（深度） | 高风险、高不确定、跨系统或难回滚变化 | 扩大影响分析、方案比较、独立审查、Subagent 与验证范围 |

默认选择**能够可靠证明正确性的最轻深度**；执行中发现风险或不确定性上升时动态升级，无需从头重跑全部流程。

### 不可裁剪的核心不变量

无论采用哪种深度，都必须保持：

- **Intent & Scope（意图与范围）**：当前 Requirement（需求）、关键规则与 Acceptance Criteria（验收标准）明确且未被静默改变。
- **Traceability（可追溯性）**：Requirement → Design → Task → Change → Verification 的受影响链可回查。
- **Open Item / Gate（开放项 / 门禁）**：`blocking = true` 的问题不能通过裁剪绕过。
- **Verification & Evidence（验证与证据）**：必须有与风险匹配、能够证明结果的验证与可复核证据。
- **Authority（决策权限）**：Tailoring 不降低 Human / Agent Authority Contract 中既定的确认与人工决策边界。
- **Correction（纠偏）**：发现上游事实源失效时仍遵循 `Correct the Earliest Invalid Source（修正最早失效事实源）` 与 `Affected Trace Only（仅处理受影响追溯链）`。
- **Git Trace（代码追溯）**：存在需 Git 固化的代码变更时，仍遵循 Task Commit（任务提交）与 `code_ref` 契约。

### 可以动态调整的内容

根据深度可以减少或扩大：

- 分析与文档展开程度。
- 候选方案数量与 Trade-off（取舍）深度。
- Task（任务）拆分细度，但仍需满足“可独立实施 + 可独立验证”。
- Main Agent / Subagent 数量及独立审查强度。
- Verification（验证）的覆盖广度与回归范围。
- Evidence（证据）的详细程度，但关键结论仍需可复核。

### 升级信号

出现以下任一情况时，应考虑从 `Reuse / Light` 升级到 `Standard / Deep`：

- Requirement、Scope、Business Rule 或 AC 仍存在关键不确定性。
- 跨服务、跨系统、跨数据存储或外部依赖边界。
- Schema、数据迁移、状态机、权限、安全、并发、异步、事务或兼容性变化。
- 影响范围无法可靠判断，或实际实现明显超出原 Task Boundary（任务边界）。
- 存在难回滚、长期维护或重大架构影响的技术决策。
- 验证无法通过局部确定性证据充分证明正确性。
- 运行中反复出现 Finding（验证发现）、返工或上游纠偏。

### 裁剪示例

```text
小型局部修复
已有 Context / Design 仍有效
        ↓
Reuse / Light
        ↓
确认 Requirement / AC
        ↓
最小 Task + Focused Verification
        ↓
Evidence
```

```text
跨服务 + 数据模型 + 异步链路变化
        ↓
Deep
        ↓
完整影响分析 + 技术决策
        ↓
细化 Task / 独立审查
        ↓
Cross-Task / Regression / Risk Verification
```

因此，Tailoring 的目标不是“少走步骤”，而是：

> **不重复已经可靠成立的工作，把精力集中到当前变化真正新增的风险、决策与验证上。**

## Open Item Contract｜开放项契约

Open Item（开放项）表示**尚未解决、且需要后续阶段继续承接的具体问题或决策**。它不是新的独立阶段，也不要求单独维护一份全局文件；可以继续存在于当前阶段产物中，但跨阶段追踪时必须保持稳定身份。

最小字段：

| 字段 | 说明 |
|---|---|
| `id` | 稳定唯一标识，使用 `OI-xxx`；首次需要跨阶段跟踪时分配，后续不重新编号。 |
| `origin` | 最初发现该问题的阶段、产物或可追溯来源。 |
| `description` | 当前仍待解决的问题或决策。 |
| `status` | `open` / `resolved` / `deferred`。 |
| `blocking` | 是否阻塞当前准入或后续推进，`true` / `false`。 |
| `owner_stage` | 当前应负责继续处理或完成决策的阶段。 |
| `related` | 相关 Requirement、AC、Design、Task、Finding、Evidence 等引用；无则省略。 |
| `resolution` | `resolved` 时记录最终结论及必要证据；其他状态省略。 |

生命周期遵循：

```text
首次发现
  ↓
OI-xxx / open
  ↓
跨阶段引用同一 ID
  ├─→ resolved
  └─→ deferred
```

- **Reference over Duplication｜引用优先**：下游引用并更新同一个 `OI-xxx`，不复制成新的开放项。
- `blocking = true` 时，不得绕过对应 Gate（门禁）继续推进；解除阻塞后再更新状态或阻塞标记。
- `deferred` 必须保留延期理由与后续承接阶段，不能作为静默丢弃。
- Risk（风险）表示可能发生的不利影响；Finding（验证发现）表示验证中观察到的事实。二者都不自动等同于 Open Item。只有确实存在尚待后续决策或处理的问题时，才创建或关联 `OI-xxx`。
- Open Item 的含义发生实质变化时，应新建 `OI-xxx` 并保留关联，而不是复用旧 ID 表达另一个问题。

## Human / Agent Authority Contract｜人机决策权限契约

Human / Agent Authority（人机决策权限）按**动作是否改变已确认事实源，以及错误决策的影响程度**划分，而不是按阶段固定角色。目标是在保留必要人工控制的同时，避免低风险动作处处等待确认。

| 权限 | 适用边界 | 典型行为 |
|---|---|---|
| `Autonomous`（Agent 自主） | 不改变已确认 Requirement / AC / Design 等语义契约，动作可回退、可验证且处于既定边界内 | 搜索与读取、证据收集、分析、候选方案生成、Task 编排、契约内实现与修复、确定性验证、按既定规则路由 |
| `Confirm`（Agent 提议 + Human 确认） | Agent 可基于证据形成推荐，但决策会产生明显技术、架构、兼容、数据、安全、运维或长期维护影响 | 重大技术取舍、架构边界变化、数据迁移策略、难回滚方案、可复用 SDD / Harness 语义规则调整 |
| `Human Decision`（Human 决策） | 决策直接定义业务意图、正确性标准或风险接受边界 | Requirement 语义、In / Out Scope、核心 Business Rule、Acceptance Criteria 的新增或语义变化、Accepted Deviation（接受偏差）、豁免强制 Gate 或其他明确风险接受 |

升级原则：

```text
既定契约内 + 可验证 + 可回退
        ↓
Autonomous

存在多个合理方案 + 影响显著
        ↓
Confirm

改变业务意图 / 正确性标准 / 风险接受
        ↓
Human Decision
```

- **Evidence before Escalation｜先取证，再升级**：Agent 应先通过代码、文档、运行结果与已有决策缩小问题，再请求必要确认，不把“存在不确定性”直接等同于“询问 Human”。
- Human 已明确确认的规则、策略或约束成为后续执行边界；Agent 在该边界内不重复请求确认。
- Agent 不得通过“技术实现选择”隐式修改 Requirement、AC、已固定 Design Decision 或已明确风险边界。
- `Confirm` 与 `Human Decision` 只约束语义和治理决策；具体工具、仓库或平台的写入授权仍遵循各自权限规则。
- 无法明确判断权限等级时，优先看“该决定失败后是否只需局部返工，还是会改变业务正确性 / 产生难逆影响”；后者应升级。
