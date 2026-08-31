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

Adoption Baseline 中不应复制技术栈、CI 命令、模型列表或 Harness 组件清单；这些动态事实继续在本协议中按需发现。

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
- 当前 Coding Agent Runtime 实际可用的 Agent / Subagent、Model、Thinking、Context、Tool、Modality、Fresh / Fork、Workspace Isolation、Quota / Availability 与相关限制。

Agent Capability 以当前 Runtime 可执行事实为准。Provider 理论能力与当前 Runtime 暴露能力不一致时，后续路由使用当前有效能力，不在 Adoption Baseline 固化易变模型信息。

Applicable Rules 以 `manifest.yaml` 中的 `rule_documents` 为机器可读入口；Human-Agent Collaboration 在需要 Human Interaction 的正式 Workflow / Meta Protocol 中适用；Agent Delegation & Coordination 在存在 Agent 委派、角色隔离或运行时模型路由时适用；其他专项规则按其 `applies_to` 加载。Exception Workflow 以 `exception_workflows` 为机器可读入口，仅在 Trigger 成立时加载对应正式文档，不要求常驻全部异常流程。

```text
Applicable Workflow
=
Current Main Workflow
+
Triggered Exception Workflow（若有）
```

**完成条件**

Agent 已能明确判断：当前 Harness 必须保障哪些 Workflow / Rules / Adoption 约束、是否存在已触发的 Exception Workflow、现有环境已可靠覆盖什么，以及当前 Runtime 真正可以提供哪些 Agent Capability。

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
2. 当前能力为什么不能可靠覆盖，或为什么存在实质 Selection Gap？
3. 如果不补充，是否会影响流程正确性、接入边界、代码质量、可靠性或合理成本？

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
2. 复用 Agent 原生能力与原生 Model Routing；
3. 复用项目已有工具、脚本与 CI；
4. 组合已有能力；
5. 仅在确有缺口时新增 Harness。

组件按问题性质选择，而不是按流程章节、规则文件或 Adoption 字段创建：

| 需求性质 | 常见 Harness 机制 |
|---|---|
| 持续遵守的原则 | Rule / Instruction |
| 可复用的复杂方法 | Skill |
| 外部执行能力 | Tool / MCP |
| 独立上下文或角色隔离 | Subagent |
| 确定性检查 | Script / Hook / CI |
| 不可绕过的流程边界 | Gate / Permission |
| 固定多步协调逻辑 | Workflow |

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

Harness Plan 默认不是长期事实源，只有在确需跨 Agent / 跨会话解释转换决策时才持久化。模型榜单、运行时模型清单与路由缓存默认不进入 Harness Plan 的长期事实部分。

---

### 3.4 Verify｜转换验证与收敛

验证重点不是“配置是否能加载”，而是生成的 Harness 是否忠实承载了当前 Spec Coding + Adoption Context。

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

删除后无实质影响的组件应移除。没有真实 Selection Gap 时，不为形式完整强制接入外部 Benchmark API 或独立 Model Router。

#### Executability｜实际可用

确认：

- 文件与引用路径正确；
- Skill / Rule 可被 Agent 发现；
- Tool / Hook / Script 实际存在且可执行；
- 配置语法有效；
- 依赖与权限满足运行条件；
- Agent / Model / Thinking / Workspace 路由与当前 Runtime 能力一致；
- Harness 放置与共享方式符合 Adoption Baseline。

**失败处理**

```text
Verify Fail
    ↓
定位最早失真点
    ├─ Adoption Fact 失效 → Project Onboarding
    ├─ Runtime Capability 失效 → Refresh affected capability / routing
    └─ Read / Derive / Compose 失真 → 对应步骤修正
    ↓
重新 Verify
```

避免在下游通过临时补丁掩盖上游接入、理解、能力发现或推导错误。

**完成条件**

```text
Coverage      Pass
Fidelity      Pass
Minimality    Pass
Executability Pass

Result        Ready
```

---

## 4. 最终约束

Harness 编译不要求将 Spec Coding 完全形式化，也不要求引入复杂 DSL、IR、固定 Agent 组织或额外人工步骤。

Agent 可以在内部自由完成理解与推理，但最终结果必须满足：

> **基于有效 Adoption Baseline，完整承载当前 Applicable Workflow 与 Rules，只补真实缺口；先发现当前 Runtime 能力，再按需补充外部能力证据，以最低充分能力形成可执行、可验证的 Agent / Model / Thinking / Tool / Workspace 路由；需要 Human 判断时保持 Decision Readiness，不需要 Human 时保持契约内自治。**
