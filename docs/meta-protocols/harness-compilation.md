# Harness Compilation Protocol｜Harness 编译协议

本协议定义 Spec Coding 如何从稳定规范语义与当前项目事实，生成目标 Coding Agent Runtime 中的最小充分 Harness。

对使用者保持单一入口：

```text
按照 Spec Coding 接入当前项目并继续开发。
```

Agent 内部按需执行：

```text
Project Onboarding（若需要）
        ↓
Adoption Baseline
        ↓
Semantic IR
        ↓
Environment Discover
        ↓
Harness Adapt
        ↓
Verify & Accept
        ↓
Harness Ready
```

> **完整性在规范侧解决；定制化在目标侧解决；可靠性在验证侧解决。**

---

## 1. Semantic Compile｜规范语义编译

Semantic Compile 属于 Spec Coding 发布侧，不在每个目标项目中重新执行。Canonical Workflow、Rules、Exception Workflow 与 Meta Protocol 由 [`Semantic Compilation`](../governance/semantic-compilation.md) 一次性编译为版本绑定的 Semantic IR。

```text
Canonical Corpus
      ↓
Atomic Clauses
      +
Execution Relations
      ↓
Semantic IR
```

Semantic IR 保留 Gate、Trigger、Transition、Authority、Artifact、Routing 与必要执行关系，但不规定具体 Runtime Strategy，例如 Subagent、Model、Thinking、Worktree 或 Vendor-specific Surface。

目标项目消费 Semantic IR，不再从完整 Markdown prose 中重新发现规范语义。

---

## 2. Environment Discover｜环境认知建立

本阶段只回答：

> **当前 Runtime / Project / Existing Harness 实际提供什么，以及缺少能力时可以去哪里按需寻找 Provider？**

不决定最终 Harness 组件。

### 2.1 Discovery Scope｜发现范围解析

从 Semantic IR 推导当前适配真正需要回答的环境问题。每条 Clause 必须明确：

```text
需要环境能力 / 机制
→ discover

不依赖环境适配
→ no_environment_dependency + reason
```

同时必须确认五类基础事实：

- 当前实际 Runtime Identity / Execution Surface；
- Runtime 的真实 Loader / Procedure / Extension Surface；
- 可按需查询的 Provider Surface，例如 Runtime Package / Plugin / Extension / MCP Registry；
- 项目已有 Build / Test / Lint / CI / Git 等可复用机制；
- Existing Harness：Instructions、Skills、Hooks、Extensions、MCP、Scripts、Automation 等。

> **Need-driven Discovery｜需求驱动发现。**

Provider Surface 只描述“去哪里查、如何查、如何取得以及信任边界”，不预加载整个插件或包市场。

### 2.2 Evidence Discovery｜证据发现

以当前可执行事实为主扫描 Runtime、Project 与 Existing Harness。

证据优先级：

```text
Local executable / runtime metadata
        ↓
Local configuration / repository evidence
        ↓
Version-matched official documentation
        ↓
Official repository / release / registry
        ↓
External evidence
```

Reference 只指导发现，不替代当前 Runtime Evidence。Project Discovery 只回答“有哪些机制可承载 Spec Coding”，不重复 Project Understanding。

### 2.3 Capability Normalization｜能力归一

原始 Vendor / Project 事实归一为跨 Runtime Capability：

```text
Observed Fact + Evidence
        ↓
Normalized Capability
```

Support Mode：`native / composable / external / unavailable / unknown`。

事实与判断必须分离；非 `unknown` Capability 至少需要一个当前 Confirmed Fact 支撑。

Provider Surface 同样必须绑定当前事实，可使用 `runtime_package / plugin_registry / extension_registry / mcp_registry / package_manager / other`，并标记 `reachable / unavailable / unknown`。

### 2.4 Environment Validation & Handoff｜环境验证与移交

验证重点：

- 每条 Semantic Clause 均有 Discovery Disposition；
- 五类核心环境问题均已处理；
- Confirmed Question 能追溯到 Confirmed Fact；
- Confirmed Fact 有当前 Evidence；
- Capability 与 Provider Surface 判断有事实支撑；
- 影响强制 Clause / Gate / Authority / Verification 的关键 Unknown 已解决或明确阻断。

最终形成短生命周期 **Environment Model**：

```text
identity
facts + evidence
capabilities
provider_surfaces
project_mechanisms
existing_harness
constraints
unknowns
```

Environment Model 只描述“当前有什么、去哪里还能找能力”，不包含 Harness 设计决策。

确定性支持工具位于 [`../../tools/environment_discovery/`](../../tools/environment_discovery/)。

---

## 3. Harness Adapt｜Harness 适配与组合

本阶段消费 `Semantic IR + Environment Model + Adoption Baseline`，只回答：

> **每条 Clause 需要什么能力，由哪个可靠 Provider 提供，并怎样组成最小充分 Harness？**

### 3.1 Capability Requirement Analysis｜能力需求分析

逐 Clause 提取后续实现不能重新猜测的 Capability Requirement / Harness Primitive：

```text
Clause
    ↓
Semantic Guarantee
    ↓
Required Capability / Primitive
```

此处不直接选择 AGENTS.md、Skill、Plugin、Subagent 或具体模型。

每条 Clause 最终只有三类适配结论：

- `covered`：存在可靠实现路径；
- `not_applicable`：对当前 Target 明确不适用，并有理由；
- `blocked`：当前无法可靠满足。

Coverage 是最终结果，不与 Provider 来源混为一层。

### 3.2 Provider Resolution & Selection｜能力提供者解析与选择

对于每个 Capability Requirement，优先检查当前已存在能力，再在真实缺口出现时按需查询 Environment Model 中已确认的 Provider Surface。

Provider Source：

```text
runtime_native
project_existing
installed_extension
registry
external
custom
```

典型链路：

```text
Required Capability
      ↓
Active / Existing Provider?
      ├─ yes → evaluate
      └─ no
          ↓
Query relevant Provider Surface（按需）
          ↓
Candidate Providers
          ↓
Semantic Sufficiency Filter
          ↓
Trust / Authority / Dependency / Maintenance Optimization
          ↓
Selected Provider
```

选择顺序不是“Native 永远优先”。必须先证明 Provider 能完整保持 Clause 语义，再优化已有能力、信任、Authority / Permission / Supply-chain 风险、维护成本以及 Portable / Runtime-native 等价性。

Registry Provider 必须引用当前可达 Provider Surface 和当前 Provider Evidence。“市场中可能存在”不能作为 Coverage。

若安装、配置、连接或构建 Provider 会改变环境：

```text
Select Provider
      ↓
Authority Check
      ↓
Install / Configure / Connect / Build
      ↓
Targeted Environment Refresh
      ↓
继续 Adapt
```

需要 Human Approval 的变更未取得 Approval Evidence 时不得继续；只刷新受影响能力链路，不全量重扫环境。

### 3.3 Harness Planning & Synthesis｜Harness 规划与生成

多个 Clause 可以共享同一个 Harness Component，但语义覆盖仍逐 Clause 保存：

```text
Clause
  ↓
Capability Requirement
  ↓
Selected Provider
  ↓
Harness Component
  ↓
Artifact / Runtime Configuration
```

Component 优先 `Reuse Existing → Configure Existing / Acquired Provider → Create Minimal New Harness`。

实现层可动态使用 Instruction、Skill、Hook、Script、MCP、Plugin / Extension、Agent / Subagent、Permission、Workspace、Model / Thinking 等当前 Runtime Surface。

> **Minimality happens at the implementation layer, not the semantic layer｜最小化发生在实现层，不发生在语义层。**

### 3.4 Candidate Validation & Handoff｜候选验证与移交

第三阶段至少检查：

- 每条 Clause 有唯一适配结论；
- `covered` Clause 可追溯到 Capability Requirement；
- `not_applicable` Clause 有明确理由；
- `blocked` Clause 为零；任何未满足 Clause 都阻断 Stage 3 Handoff；
- Selected Provider 有当前 Evidence 并显式满足 Requirement；
- Registry Provider 来自可达 Provider Surface；
- Authority / Approval Constraint 已满足；
- Provider Change 已完成并有 Targeted Refresh Evidence；
- 每条 Covered Clause 由至少一个 Component 承载；
- Component / Provider / Artifact 无悬空引用；
- Candidate Artifact 位于 Target 边界内并真实存在；
- 每个 Artifact 保存并验证 `content_sha256`，使 Candidate Fingerprint 绑定具体 Harness 内容而非只有路径；
- 不存在明显重复 Component。

第三阶段输出：

```text
Adaptation Plan
+
Harness Candidate Manifest
+
Materialized Harness Candidate
```

确定性支持工具位于 [`../../tools/harness_adapt/`](../../tools/harness_adapt/)。

通过第三阶段只表示 Candidate 的适配链完整且内容身份已固定，不表示 Runtime 已真实加载。

---

## 4. Verify & Accept｜验证与行为验收

本阶段只回答：

> **这份具体 Harness Candidate 是否真的被当前 Runtime 接管，并在独立 Fresh Agent 的真实行为中保持了 Semantic IR 要求？**

它属于 Harness Compilation Meta Protocol，不等于 Main Workflow 的 Stage 6 Verification Convergence。Stage 6 验证 Requirement / Change Set；这里验证 Harness 本身。

### 4.1 Structural & Runtime Verification｜结构与运行时验证

第四阶段重新校验 Candidate / Artifact Fingerprint，确认验收期间 Harness 内容没有漂移，并由真实 Runtime 证明：

- 每个 Candidate Artifact 位于当前 Loader Surface 并实际可见；
- 每个 Selected Provider 当前真实 active；
- Runtime Identity / Version 与 Environment Model 一致；
- 文件存在、路径正确或配置合法不能单独作为“已加载”证据。

> **Exists ≠ Loaded｜文件存在不等于 Runtime 已接管。**

### 4.2 Semantic Verification｜语义验证

每个 `covered` Clause 必须至少有一个明确 Verification Method，并保留：

```text
Clause
→ Capability Requirement
→ Provider / Component
→ Verification Method
→ Expected Behavior
→ Evidence
```

Verification Method 可使用：

- `deterministic`：脚本、状态、Git、Hook、静态 / 结构不变量；
- `runtime_probe`：Loader、Provider、Runtime Surface 的实际执行证据；
- `semantic_behavior`：Authority、Isolation、Trigger、Routing 等无法仅靠机械检查证明的行为。

遵循：**Deterministic first; semantic challenge where determinism ends｜能确定性验证的先确定性验证，剩余语义再做行为挑战。**

### 4.3 Adversarial Challenge｜对抗验证

Stage 1 的 Mutation Review 验证 `Canonical → Semantic IR` 是否无损；本阶段只验证 `Semantic IR → Harness → Runtime Behavior` 是否被弱化。

至少设计能够挑战当前高风险语义的 Mutation / Adversarial Scenario，例如：

- 删除 Gate / Trigger；
- 弱化 `MUST`；
- 扩大 Authority；
- 移除 Context Isolation；
- 替换 Selected Provider / Component Mapping；
- 破坏 Hard Order / Transition。

计划中的每个 Mutation 必须有独立结果；未被检测即阻断 Harness Ready。

### 4.4 Fresh-Agent Acceptance｜新 Agent 行为验收

最终由未参与 Semantic Compile、Environment Discover 与 Harness Adapt 的 Independent Fresh Context 执行真实 Runtime 验收。

至少覆盖五类代表性场景：

```text
load
process
boundary
gate_lifecycle
exception
```

每个 Case 保存：

```text
input
expected_semantics
observed_behavior
covered_clauses
evidence
verdict
```

Fresh Agent 可以由 Runtime-native Subagent、独立 Session / Process 或其他可证明隔离的执行单元承载；具体机制由当前 Runtime 决定。Fresh / Independent 不能只写布尔自证，必须附带 Isolation Evidence。

### 4.5 Evidence Chain & Verdict｜证据链与结论

第四阶段使用三类短生命周期产物：

```text
Verification Plan
        ↓
Verification Report
        ↓
Acceptance Receipt
```

它们按 Fingerprint 连续绑定：Semantic IR、Environment Model、Adoption Baseline、Adaptation Plan、Harness Candidate；Verification Report 再绑定 Verification Plan，Acceptance Receipt 再绑定 Verification Report。

最终只有：

```text
READY
BLOCKED
```

`READY` 至少要求：

- Candidate Artifact 内容 Hash 未漂移；
- 每个 Covered Clause 的验证结果通过；
- 每个 Artifact 有真实 Runtime Visibility Evidence；
- 每个 Selected Provider 有 Active Evidence；
- Required Mutation 全部被检测；
- Blocking Verification Finding 为零；
- Fresh / Independent Acceptance 有 Isolation Evidence；
- 五类代表性 Fresh-Agent Case 全部通过。

确定性支持工具位于 [`../../tools/harness_acceptance/`](../../tools/harness_acceptance/)。Runtime-specific Driver 不固化在通用协议中；Pi、Claude Code、Codex 等只负责执行计划中的 Probe / Case 并返回 Evidence。

### 4.6 Failure Routing｜失败回流

第四阶段只验证与归因，不在验收层偷偷修改 Harness：

```text
semantic    → Stage 1 Semantic Compile
environment → Stage 2 Environment Discover
adaptation  → Stage 3 Provider / Mapping
candidate   → Stage 3 Harness Synthesis
runtime     → Stage 2 targeted refresh，再按需要回 Stage 3
```

> **Return to the earliest distorted source｜回到最早失真的事实源。**

---

## 5. 与 Project Onboarding 的边界

Adoption Baseline 只持久化长期意图和稳定绑定：Target / Scope、Spec Workspace、Collaboration / Publication、Repository / Authority Constraint 等。

Runtime Loader、Model、Tool、Subagent、Provider Registry、CI Command、Existing Harness 等动态事实不进入 Adoption Baseline，由 Environment Discover / Harness Adapt 按需重新发现和解析。

> **Persist intent, rediscover facts｜持久化意图，重发现动态事实。**

---

## 6. 完成标准

Harness Compilation 只有在以下条件同时成立时完成：

- 使用与当前 Spec Coding 版本绑定且通过发布门禁的 Semantic IR；
- Environment Model 对当前适配所需关键事实与 Provider Surface 有充分证据；
- Applicable Clause 均已映射且无静默缺口；
- Stage 3 没有 Blocking Clause，Candidate Artifact 内容身份已固定；
- Selected Provider 能保持对应语义并满足 Authority / Trust 要求；
- Harness 被当前 Runtime 实际发现和加载；
- 每个 Covered Clause 已形成并通过充分验证；
- Required Mutation / Adversarial Challenge 能发现语义弱化；
- Independent Fresh-Agent Acceptance 通过并具有 Isolation Evidence；
- 没有未解决的 Blocking Environment Unknown / Provider Change / Verification Finding；
- Acceptance Receipt 最终结论为 `READY`。

最终原则：

> **Spec Coding 先形成稳定无损语义；目标 Agent 再发现当前环境与可获取能力，选择最小充分 Provider 和 Harness 组合；只有真实 Runtime 中能够观察到这些语义确实生效，Harness 才能 Ready。**
