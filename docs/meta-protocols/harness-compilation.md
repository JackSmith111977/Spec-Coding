# Harness Compilation Protocol｜Harness 编译协议

本协议属于 Meta Protocol（元协议），定义如何将 Spec Coding 的 Applicable Workflow（适用流程）、Rules（规则）与当前有效 Adoption Baseline（接入基线）稳定转换为目标项目可执行的最小 Harness（执行框架）。Workflow 包括当前适用的 Main Workflow（主流程）以及由实际异常触发的 Exception Workflow（异常流程）。

Harness Compilation 不是项目接入协议。若当前 Target 不存在有效 Adoption Baseline，或 Baseline 已发生冲突 / 失效，应先执行 [`Project Onboarding Protocol`](project-onboarding.md)，不得在 Harness 编译阶段自行猜测接入范围、共享方式、Artifact Publication 或 Authority。

对使用者仍可保持单一意图入口，例如：

```text
按照 Spec Coding 接入当前项目并继续开发。
```

Agent 内部按需执行：

```text
Project Onboarding（若需要）
        ↓
Adoption Baseline
        ↓
Harness Compilation
        ↓
Harness Ready
        ↓
Enter / Resume Workflow
```

读取、推导、组合与验证由 Agent 内部完成，不要求 Human 手工执行额外转换步骤。

---

## 1. 核心原则

- **Adoption before Compilation｜先接入，再编译**：Harness 编译只消费已收敛的 Adoption Context；接入意图未解决时先回到 Project Onboarding。
- **Local First｜本地优先**：优先取得 Spec Coding 规范仓库与目标项目仓库 / Workspace 的一致视图；已有本地工作区时同步并确认基线，不重复拉取。远程接口主要用于获取、同步、版本确认与必要补充。
- **Process as Cognition｜流程用于认知**：流程规定 Agent 如何理解、判断和推进，不强制把中间认知全部结构化。
- **Artifact as Contract｜产物用于对齐**：只对需要稳定交接与验证的结果明确约束，减少重复对齐成本。
- **Reuse before Add｜复用优先**：优先复用 Agent 原生能力、项目已有工具与既有 Harness，仅补齐真实缺口。
- **Minimum Sufficient Harness｜最小充分 Harness**：以最低复杂度可靠满足当前流程、规则与 Adoption 约束，避免重复包装与过度设计。
- **Minimum Sufficient Capability｜最低充分能力**：对于 Agent / Model / Thinking 等运行时选择，使用能够可靠满足当前 Contract 的最低充分能力，而不是统一选择最强或最便宜配置。
- **Discover before Route｜先发现，再路由**：先确认当前 Coding Agent Runtime 实际可用能力，再评价候选并形成 Model / Thinking / Context / Tool 路由，不从外部排行榜反向假设运行时能力。
- **Reference guides discovery｜参考指导发现**：Harness Primitive 与 Runtime Reference 用于提供跨 Runtime 共同语言、架构不变量与官方事实入口，不作为当前 Runtime Capability 的权威事实源。
- **Current Evidence wins｜当前证据优先**：Reference、Provider 理论能力或历史资料与当前 Local / Official Runtime Evidence 冲突时，以当前可执行事实为准。
- **Constraint Preservation｜约束保持**：Harness 不得弱化原流程、规则或 Adoption Baseline 语义，也不应无依据增强约束。
- **Deterministic First｜确定性优先**：可由脚本、测试、Hook、Gate 等确定性机制保障的要求，不依赖模型自觉记忆。

---

## 2. 输入模型

Harness Compilation 同时消费三类上下文：

```text
Normative Context
= Applicable Workflow + Applicable Rules

Adoption Context
= Adoption Baseline + Final Workflow Route

Execution Context
= Current Target Environment + Existing Harness + Effective Agent Capability
```

职责边界：

- Workflow / Rules 定义“必须做什么、什么必须持续成立”；
- Adoption Baseline 定义“Spec Coding 在这个 Target 中如何使用、共享和受约束”；
- Current Target Environment 提供当前工具、CI、配置与运行条件；
- Effective Agent Capability 提供当前 Coding Agent 实际暴露的 Agent / Model / Thinking / Context / Tool / Isolation 能力；
- Harness Compilation 只负责把三者转换为最小充分执行机制。

Harness Compilation 还可按需消费两类 Reference Knowledge（参考知识）：

```text
Harness Primitive Reference
= 跨 Runtime 的稳定能力语义与开放标准入口

Runtime Reference
= Coding Agent 的 Architecture Invariant + Official Sources
```

它们是编译知识，不是第四类项目 Context，也不替代当前 Runtime Evidence。机器入口由 `manifest.yaml.reference` 提供；当前内置参考分别位于 [`../reference/harness-primitives.md`](../reference/harness-primitives.md) 与 [`../reference/coding-agent-runtimes.md`](../reference/coding-agent-runtimes.md)。

Adoption Baseline 中不应复制技术栈、CI 命令、模型列表、Runtime Reference 内容或 Harness 组件清单；这些动态事实与编译知识继续在本协议中按需读取或发现。

### V2 Tooling Boundary｜V2 工具边界

仓库内的 [`Harness Compiler V2 tools`](../../tools/harness_compiler/README.md) 将确定性部分收敛为 `resolve → scan → validate → compose → verify`：它们显式区分 `spec-root` 与 `target-root`，以有效 Adoption Baseline 为硬前置条件，生成 JSON 来源清单和短生命周期 Compilation State（编译状态）报告。

工具不自动从自然语言生成 Contract 或 Harness，也不替代 Agent 的 Runtime Discovery、Gap 判断与独立语义审查。Agent 仍负责 Read / Derive 和构造带来源、运行时证据、组件摘要及十一项验证证据的 State；工具负责稳定引用、完整性、边界、摘要、确定性 Probe 与写入门禁。`Compose` 是唯一 Writer，`Validate` / `Verify` 只读；任一阻断条件出现时不得把 Harness 标记为 Ready。

这是一层可验证实现，不新增平行 Canonical 事实源：Workflow / Rules 继续持有规范语义，Adoption Baseline 继续持有目标接入事实，Current Runtime Evidence 继续持有当前能力事实。

---

## 3. 转换流程

```text
Read
  ↓
Derive
  ↓
Compose
  ↓
Verify
  ↓
Harness Ready
```

### 3.1 Read｜基线接管与能力发现

先确认当前 Target 的 Adoption Baseline 有效，并取得 Spec Coding 规范仓库、Spec Workspace 与目标项目的可用一致视图。

若出现以下情况，停止编译并回到 Project Onboarding：

- 没有与当前 Target 匹配的 Adoption Baseline；
- Target Identity / Scope 无法稳定解析；
- Collaboration / Publication / Authority 等关键 Adoption Fact 冲突或缺失；
- Relevant Delta 已使当前 Baseline 失效。

Baseline 有效后，以本地确定性搜索和文件读取为主，建立生成 Harness 所需的最小完整认知，重点识别：

- 当前有效的 `VERSION`、`manifest.yaml`、Applicable Rules 与 Final Workflow Route 对应的 Main Workflow 文档；
- `manifest.yaml` 中已登记的 Exception Workflow，以及当前 Failure / Finding 是否触发其中某一流程；
- Adoption Baseline 中与 Harness 直接相关的 Target Scope、Spec Workspace、Publication Boundary、Repository / Authority Constraint 与 Integration Constraint；
- 当前任务需要的关键上游引用；
- Gate、Verification、Traceability、Human / Agent Authority、Human-Agent Collaboration、Agent Delegation & Coordination、Code Quality 等持续约束；
- 目标项目已有 Harness、规则、工具、脚本与 CI；
- 当前实际执行 Coding Agent 的 Runtime Identity / Surface，以及其 Agent / Subagent、Model、Thinking、Context、Tool、Modality、Fresh / Fork、Workspace Isolation、Quota / Availability 与相关限制。

#### Runtime Knowledge Resolution｜运行时知识解析

Runtime Capability Discovery 应按需使用 Reference，而不是依赖 Agent 的产品记忆：

```text
Identify Active Runtime / Surface
        ↓
Load Harness Primitive Reference
        ↓
Resolve Matching Runtime Reference（若存在）
        ↓
Read Architecture Invariant
        ↓
Fetch Relevant Current Official Sources
        +
Probe Local Runtime
        ↓
Normalize Effective Runtime Capability
```

- Runtime Identification 优先使用当前 Agent Environment、Executable / CLI、Runtime Metadata、Known Configuration 与 Host Environment 等直接证据；
- Host Runtime 与真正拥有执行能力的 Execution Runtime 不一致时，以实际承载该 Harness Capability 的 Runtime Surface 为映射对象；
- Runtime Registry 中没有当前 Runtime 时，不阻断 Generic Discovery：继续使用 Harness Primitive 作为共同语言，并从当前 Runtime 的官方资料与本地环境建立能力视图；
- 不要求读取某个 Runtime 的全部官方文档。先根据当前 Workflow / Rules 推导需要确认的 Primitive，再执行 Minimum Sufficient Discovery（最低充分发现）。

例如只需要 Independent Reviewer + Workspace Isolation 时，优先获取 Agent / Subagent、Permission 与 Workspace / Isolation 相关官方资料，而不是全量扫描产品文档。

#### Runtime Evidence Priority｜运行时证据优先级

当前 Capability 以当前证据决定：

```text
Local Executable Evidence
        ↓
Version-matched Official Documentation
        ↓
Official Repository / Release / Changelog
        ↓
Provider Documentation
        ↓
External Benchmark / Community Evidence
```

Runtime Reference 负责告诉 Compiler“去哪里查、架构上如何理解”，不负责声明“当前一定支持什么”。Provider 理论能力与当前 Runtime 暴露能力不一致时，后续路由使用当前有效能力，不在 Adoption Baseline 固化易变模型信息。

Runtime Capability 可在本次编译内轻量归一为：

| Support Mode | 含义 |
|---|---|
| `native` | 当前 Runtime 原生且可靠支持。 |
| `composable` | 可通过 Runtime Extension / Plugin / 多机制组合可靠实现。 |
| `external` | 需要 Script / CI / MCP Service / 外部机制承担。 |
| `unavailable` | 已确认当前无法可靠实现。 |
| `unknown` | 尚未取得足够证据。 |

> **Unknown ≠ Unavailable｜未知不等于不支持。**

与 MUST / Gate / Permission / Verification 等关键 Contract 相关的 `unknown` 必须继续发现、改用其他可靠机制或 Block；不得静默假设。

Applicable Rules 以 `manifest.yaml` 中的 `rule_documents` 为机器可读入口；Human-Agent Collaboration 在需要 Human Interaction 的正式 Workflow / Meta Protocol 中适用；Agent Delegation & Coordination 在存在 Agent 委派、角色隔离或运行时模型路由时适用；其他专项规则按其 `applies_to` 加载。Exception Workflow 以 `exception_workflows` 为机器可读入口，仅在 Trigger 成立时加载对应正式文档，不要求常驻全部异常流程。

```text
Applicable Workflow
=
Current Main Workflow
+
Triggered Exception Workflow（若有）
```

**完成条件**

Agent 已能明确判断：当前 Harness 必须保障哪些 Workflow / Rules / Adoption 约束、这些约束需要哪些 Harness Primitive、是否存在已触发的 Exception Workflow、现有环境已可靠覆盖什么，以及当前 Runtime 真正可以提供哪些 Agent Capability。

---

### 3.2 Derive｜Harness 与能力需求推导

对照 Applicable Workflow / Rules / Adoption Baseline 与现有能力，识别真正需要 Harness 补齐的缺口。

重点关注：

- MUST / MUST NOT；
- Gate 与 Blocking Condition；
- Verification；
- Human / Agent Authority；
- Cognitive Sync / Decision Readiness 等 Human-Agent Collaboration 要求；
- Main Agent / Subagent Role、Delegation Boundary、Context Isolation 与 Result Integration；
- Traceability；
- Artifact Publication / Spec Workspace / Repository Constraint；
- 持续适用的质量与执行规则；
- 明确的上下文与执行约束。

#### Semantic → Primitive → Runtime Mapping｜语义到运行时映射

不要从 Workflow / Rule 直接跳到某个 Vendor-specific 配置。先建立语义与 Harness Primitive 的中间映射：

```text
Workflow / Rule / Adoption Requirement
        ↓
Required Semantic Guarantee
        ↓
Required Harness Primitive Set
        ↓
Runtime Architecture Preference
        ↓
Effective Runtime Capability
        ↓
Gap Analysis
```

例如：

```text
Independent Reviewer
        ↓
Independent Reasoning
+ Fresh Context
+ Read-oriented Authority
        ↓
Subagent
+ Context Isolation
+ Permission Boundary
        ↓
Current Runtime-native Surface
```

同一 Requirement 可以需要多个 Primitive，同一 Primitive 也可能由多个 Runtime Surface 组合实现。不得采用“一条 Rule = 一个 Skill”“一个 Role = 一个固定 Subagent 文件”“一个 Stage = 一个 Workflow 配置”等机械映射。

Runtime Architecture Invariant 只提供实现倾向。例如 Plugin-first Runtime 优先通过 Plugin Composition 实现能力，Declarative Agent Runtime 优先通过 Agent Profile 实现角色；最终仍以当前 Runtime Evidence 能否可靠满足语义为准。

优先判断现有能力是否已经可靠覆盖，避免将流程章节、规则条目或 Adoption 字段机械映射成 Skill、Agent 或其他 Harness 组件。尤其不应把 Human-Agent Collaboration 机械转换为每阶段人工审批，也不应把 Agent Delegation Rules 机械转换为每阶段必须创建 Scout / Reviewer / Oracle；只有真实 Trigger、Work Unit 与 Capability Need 成立时才实例化对应机制。

同时区分：

- **Capability Gap｜能力缺口**：当前 Agent 或项目环境缺少完成要求所需的能力；
- **Reliability Gap｜可靠性缺口**：能力已经存在，但无法稳定保证要求被执行；
- **Selection Gap｜选择缺口**：当前 Runtime 有多个有效候选，但模型 / Thinking / Context / Tool 选择会实质影响质量、成本或延迟，且现有 Runtime 没有可靠路由策略。

根据要求强度选择保障级别：

```text
指导性要求
→ Rule / Skill

需要稳定执行
→ Workflow / Checklist / Verifier

不可绕过
→ Script / Hook / Permission / Gate
```

对于 Agent Work Unit，进一步推导：

```text
Role Requirement
+
Work Complexity / Risk / Uncertainty / Novelty
+
Context / Tool Requirement
+
Current Runtime Capability
        ↓
Required Capability Profile
```

只有 Selection Gap 实际成立时，才需要进一步获取 Artificial Analysis、OpenRouter、SWE-bench / Hugging Face Benchmark、其他当前专项评测或 Local Execution Evidence。外部评测用于补充候选能力证据，不成为项目 Canonical Artifact，也不覆盖当前 Runtime Fact。

**完成条件**

每一个待新增 Harness 或能力路由都能回答：

1. 它对应什么真实 Workflow、Rule 或 Adoption 要求？
2. 它需要保持什么 Semantic Guarantee，并映射到哪些 Harness Primitive？
3. 当前 Runtime 的什么 Surface 能承载这些 Primitive，证据是什么？
4. 当前能力为什么不能可靠覆盖，或为什么存在实质 Selection Gap？
5. 如果不补充，是否会影响流程正确性、接入边界、代码质量、可靠性或合理成本？

---

### 3.3 Compose｜Harness 组合与运行时路由

将已确认的缺口转换为最小可用 Harness。

组合顺序遵循：

```text
Reuse
  ↓
Compose
  ↓
Create
```

优先级依次为：

1. 复用已有 Harness；
2. 复用当前 Runtime 原生能力与原生 Model Routing；
3. 复用项目已有工具、脚本与 CI；
4. 组合已有能力；
5. 仅在确有缺口时新增 Harness。

组件按问题性质选择，而不是按流程章节、规则文件或 Adoption 字段创建：

| 需求性质 | 常见 Harness 机制 |
|---|---|
| 持续遵守的原则 | Rule / Instruction |
| 可复用的复杂方法 | Skill |
| 外部执行能力 | Tool / MCP |
| 独立上下文或角色隔离 | Agent / Subagent |
| 确定性检查 | Script / Hook / CI |
| 不可绕过的流程边界 | Gate / Permission |
| 固定多步协调逻辑 | Workflow |
| Runtime-specific 组合扩展 | Plugin / Extension |

Portable Surface 与 Runtime-native Surface 都能完整、可靠满足同一 Contract 时，可优先可移植方案；若 Runtime-native Surface 提供 Contract 必需的更强隔离、权限或确定性保证，则优先原生机制。

> **Portable when equivalent; native when necessary｜等价时优先可移植，必要时优先原生能力。**

Agent 委派遵循 [`../rules/agent-delegation-and-coordination.md`](../rules/agent-delegation-and-coordination.md)：Main Agent 保留全局一致性与最终责任；Scout / Researcher / Worker / Reviewer / Oracle 按认知职责使用；Formal Task 继续以 Task Contract + Execution Unit 作为正式执行委派，不额外生成平行 Delegation Artifact。

#### Runtime Capability Routing｜运行时能力路由

当需要动态选择 Agent / Model / Thinking 时，按以下顺序：

```text
Discover Runtime
      ↓
Normalize Effective Capability
      ↓
External Evidence Enrichment（按需）
      ↓
Role + Work Profile Matching
      ↓
Model + Thinking + Context + Tools + Workspace
```

路由目标是 Minimum Sufficient Capability：优先选择可靠满足当前 Contract 的最低充分配置。Role 只定义相对能力倾向，Thinking 不按 Role 写死；复杂度、风险、上下文规模或失败历史增加时可提高 Thinking、模型能力或独立验证强度。

Model / Thinking / Fresh / Fork / Workspace / Attempt / Fallback 等属于短生命周期 Execution Metadata，默认不写入 `tasks.md`、Requirement、Design 或 Adoption Baseline。

Fallback 只有在候选仍满足当前 Required Capability Profile 时才可静默使用；若能力不再充分，应显式升级、降级或阻断，而不是仅因 API 可用就视为等价。

Harness 的共享 / 放置方式不得越过 Adoption Baseline 的 Integration / Publication Boundary。Local Adoption 不应无依据把个人 Harness 写入目标 Repository；Repository-native Adoption 则应遵守适用项目约定。

Human-Agent Collaboration 可按项目能力映射为轻量 Summary、Decision Packet、Checkpoint、UI 提示或共享状态，但不得要求 Human 持续跟踪 Agent 全部 Working Context，也不得无依据增加强制 Gate。

生成完成后执行一次 Simplify Pass（简化检查），删除重复、无必要或可由现有能力替代的组件。

**产物**

必要时可形成轻量 **Harness Plan**，仅说明：

- `Reuse`：复用了什么；
- `Add`：新增了什么；
- `Reason`：为什么需要。

需要跨 Agent / 跨会话解释重大 Runtime Mapping 时，`Reason` 可简要记录 `Requirement → Primitive → Runtime Surface`，但 Harness Plan 仍不是长期 Runtime Capability 事实源。模型榜单、运行时模型清单与路由缓存默认不进入 Harness Plan 的长期事实部分。

---

### 3.4 Verify｜转换验证与收敛

验证重点不是“配置是否能加载”，而是生成的 Harness 是否忠实承载了当前 Spec Coding + Adoption Context，并确实能在当前 Runtime 中实现。

#### Coverage｜覆盖完整

关键 Workflow、Rules 与 Adoption 约束均得到可靠保障，尤其是 MUST / MUST NOT、Gate、Verification、Human / Agent Authority、必要 Cognitive Sync / Decision Readiness、Agent Delegation Boundary、Blocking Condition、Traceability、Publication / Repository Boundary 与适用质量规则；存在已触发 Exception Workflow 时，其必要语义同样必须被覆盖。

不要求每条规则或异常流程步骤都生成独立文件，只要求其语义被可靠满足。

#### Fidelity｜语义忠实

不得发生约束弱化或无依据增强，例如：

```text
MUST      → SHOULD
MUST NOT  → “注意避免”
Human Decision → Agent 自主决定
Trigger-driven Sync → 每阶段强制 Human Review
Subagent Role → 固定技术领域 Persona
Reviewer → 替代 Deterministic Verification
Formal Task → 重复生成第二套 Delegation Contract
Agent / Model / Thinking → 写入 Task 长期定义
不可绕过 Gate → 可跳过 Checklist
Local Publication Boundary → 自动写入目标 Repository
```

#### Runtime Mapping｜运行时映射可信

确认：

- `Requirement → Semantic Guarantee → Primitive → Runtime Surface` 可追溯；
- Architecture Invariant 只用于指导映射，没有覆盖当前 Runtime Evidence；
- Version-specific Capability 具有 Current Official Evidence 或 Local Executable Evidence；
- Runtime-native Surface 能被当前环境发现、加载并实际执行；
- 与关键 Contract 相关的 `unknown` 已继续发现、替代或 Block；
- Reference 中没有某个 Runtime 时，Generic Discovery 仍能建立可靠映射。

#### Capability Routing｜能力路由可信

若 Harness 使用动态 Model Routing，确认：

- 推荐只发生在当前 Runtime 实际可用候选中；
- Role / Work Requirement 与候选能力匹配；
- 外部 Benchmark 仅作为可追溯补充证据，未覆盖 Runtime Fact；
- Thinking / Model / Fallback 没有因成本优化降到无法可靠满足 Contract；
- Capability Problem 不被误判为 Human Authority Problem；
- 运行时模型信息没有被错误固化进 Adoption / Task 等长期事实源。

#### Minimality｜最小充分

逐项反查新增组件：

- 为什么存在？
- 对应哪个真实 Workflow / Rule / Adoption Gap？
- 删除后是否降低流程或规则执行可靠性？

删除后无实质影响的组件应移除。没有真实 Selection Gap 时，不为形式完整强制接入外部 Benchmark API 或独立 Model Router；没有真实 Runtime Mapping Need 时，也不要求全量扫描所有 Runtime Reference / Official Docs。

#### Executability｜实际可用

确认：

- 文件与引用路径正确；
- Skill / Rule 可被 Agent 发现；
- Tool / Hook / Script / Plugin 实际存在且可执行；
- 配置语法有效；
- 依赖与权限满足运行条件；
- Agent / Model / Thinking / Workspace 路由与当前 Runtime 能力一致；
- Harness 放置与共享方式符合 Adoption Baseline。

#### Reference Drift｜参考漂移

若当前 Official / Local Evidence 与 Runtime Reference 冲突：

```text
Current Evidence wins
        ↓
Compile using current truth
        ↓
Record Reference Drift
        ↓
Update Reference separately
```

Reference Drift 默认不阻塞业务开发；只有无法确定关键 Capability、Permission 或安全映射时才阻塞 Harness Ready。

**失败处理**

```text
Verify Fail
    ↓
定位最早失真点
    ├─ Adoption Fact 失效 → Project Onboarding
    ├─ Runtime Capability 失效 → Refresh affected discovery / routing
    ├─ Runtime Reference 漂移 → Current Evidence 优先 + 后续更新 Reference
    └─ Read / Derive / Compose 失真 → 对应步骤修正
    ↓
重新 Verify
```

避免在下游通过临时补丁掩盖上游接入、理解、能力发现或推导错误。

**完成条件**

```text
Coverage       Pass
Fidelity       Pass
RuntimeMapping Pass
Minimality     Pass
Executability  Pass

Result         Ready
```

---

## 4. 最终约束

Harness 编译不要求将 Spec Coding 完全形式化，也不要求引入复杂 DSL、固定 Agent 组织、Vendor-specific Workflow 或额外人工步骤。

Agent 可以在内部自由完成理解与推理，但最终结果必须满足：

> **基于有效 Adoption Baseline，完整承载当前 Applicable Workflow 与 Rules；先把规范语义归一为必要 Harness Primitive，再结合 Runtime Architecture 与当前 Official / Local Evidence 映射到真实 Runtime Surface；只补真实 Capability / Reliability / Selection Gap，以最低充分能力形成可执行、可验证的 Agent / Model / Thinking / Tool / Workspace 路由；需要 Human 判断时保持 Decision Readiness，不需要 Human 时保持契约内自治。**

最终保持：

> **Spec Coding owns semantics; Reference owns reusable ecosystem knowledge; Runtime Discovery owns current facts｜Spec Coding 持有语义，Reference 持有可复用生态知识，Runtime Discovery 持有当前事实。**
