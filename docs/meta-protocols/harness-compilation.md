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

目标项目消费 Semantic IR，不再从全部 Markdown prose 中重新发现规范语义。

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

---

## 2. Environment Discover｜环境认知建立

### 2.1 Discovery Scope｜发现范围解析

从 Semantic IR 推导当前适配真正需要回答的环境问题，而不是全量扫描 Runtime 或项目。

每条 Clause 必须明确：

```text
需要环境能力 / 机制
→ discover

不依赖环境适配
→ no_environment_dependency + reason
```

同时始终确认四类基础事实：

- 当前实际 Runtime Identity / Execution Surface；
- Runtime 的真实 Loader / Procedure / Extension Surface；
- 项目已有 Build / Test / Lint / CI / Git 等可复用机制；
- Existing Harness：Instructions、Skills、Hooks、Extensions、MCP、Scripts、Automation 等。

> **Need-driven Discovery｜需求驱动发现。**

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
Official repository / release / changelog
        ↓
External evidence
```

Reference 只指导发现，不替代当前 Runtime Evidence。能够通过本地命令、配置、仓库或 Runtime Metadata 确认的事实，不依赖模型记忆。

Project Discovery 只回答“有哪些机制可承载 Spec Coding”，不重复 Project Understanding 对业务与系统结构的认知建立。

### 2.3 Capability Normalization｜能力归一

原始 Vendor / Project 事实归一为跨 Runtime Capability：

```text
Observed Fact + Evidence
        ↓
Normalized Capability
```

Support Mode：

- `native`
- `composable`
- `external`
- `unavailable`
- `unknown`

事实与判断必须分离；非 `unknown` Capability 至少需要一个当前 Confirmed Fact 支撑。

例如，规范只表达：

```text
Independent Review
requires context isolation
```

Environment Model 可以确认：

```text
independent_execution = native
context_isolation = native
```

但此阶段不能决定“因此使用 Reviewer Subagent”。具体实现留给 Harness Adapt。

### 2.4 Environment Validation & Handoff｜环境验证与移交

验证重点：

- 每条 Semantic Clause 均有 Discovery Disposition；
- Discovery Question 能追溯到需要它的 Clause；
- Confirmed Question 能追溯到 Confirmed Fact；
- Confirmed Fact 有当前 Evidence；
- Capability 判断有事实支撑；
- 影响强制 Clause / Gate / Authority / Verification 的关键 Unknown 已解决、找到替代机制或明确阻断。

不要求所有环境 Unknown 清零；与当前适配无关的未知项可以保留。

最终形成短生命周期 **Environment Model**：

```text
identity
facts + evidence
capabilities
project_mechanisms
existing_harness
constraints
unknowns
```

Environment Model 只描述“当前有什么”，不包含 Harness 设计决策。

仓库中的确定性支持工具位于 [`../../tools/environment_discovery/`](../../tools/environment_discovery/)。

---

## 3. Harness Adapt｜Harness 适配与组合

本阶段消费：

```text
Semantic IR
+
Environment Model
+
Adoption Baseline
```

逐 Clause 判断当前环境如何承载其语义，典型 Disposition：

```text
NATIVE
PROJECT_EXISTING
HARNESS
NOT_APPLICABLE
BLOCKED
```

语义覆盖必须逐 Clause 保留；最小化只发生在实现层。多条 Clause 可以由同一个 Harness Component 承载，但不能为了减少 Component 数量先把独立 Clause 摘要掉。

优先级：

```text
Reuse Native / Existing
        ↓
Compose Existing Capabilities
        ↓
Create Minimal New Harness
```

具体 Subagent、Model、Thinking、Skill、Hook、Instruction、Script、Workspace 与 Loader Layout 在这里基于 Environment Model 动态决定。

---

## 4. Verify & Accept｜验证与行为验收

Harness Ready 至少需要四类证据：

1. **Clause Coverage**：每条 Applicable Clause 有唯一 Disposition 与实现 / 证据映射；
2. **Structural & Runtime**：输出真实存在、位于当前 Runtime Loader Surface、边界与引用正确；
3. **Semantic Challenge**：删除 Gate / Trigger、`MUST → SHOULD`、扩大 Authority 等变异能够被检测；
4. **Fresh-agent Behavior**：由未参与编译的 fresh-context Agent 在真实 Runtime 中验证 Load、Process、Boundary、Git / Lifecycle 与当前高风险 Clause 行为。

确定性工具负责可以机械证明的不变量；Agent / Reviewer 负责语义判断。二者不得互相伪装成对方的证据。

---

## 5. 与 Project Onboarding 的边界

Adoption Baseline 只持久化长期意图和稳定绑定：Target / Scope、Spec Workspace、Collaboration / Publication、Repository / Authority Constraint 等。

Runtime Loader、Model、Tool、Subagent、CI Command、Existing Harness 等动态事实不进入 Adoption Baseline，由 Environment Discover 按需重新发现。

> **Persist intent, rediscover facts｜持久化意图，重发现动态事实。**

---

## 6. 完成标准

Harness Compilation 只有在以下条件同时成立时完成：

- 使用与当前 Spec Coding 版本绑定且通过发布门禁的 Semantic IR；
- Environment Model 对当前适配所需关键事实有充分证据；
- Applicable Clause 均已映射且无静默缺口；
- Harness 位于当前 Runtime 实际可发现 Surface；
- 确定性验证、语义挑战与 Fresh-agent 行为验收均满足当前风险要求；
- 没有未解决的 Blocking Clause / Environment Unknown。

最终原则：

> **Spec Coding 先形成稳定无损语义；目标 Agent 再发现当前环境并进行最小适配；验证证明这些语义确实在真实 Runtime 中生效。**
