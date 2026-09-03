# Project Onboarding Protocol｜项目接入协议

本协议定义 Spec Coding 如何与目标项目建立、复用、刷新或迁移稳定接入关系。

Project Onboarding 不推进业务开发阶段，不替代 Project Definition / Project Understanding，也不构建 Harness。它只回答：**Spec Coding 当前作用于哪个 Target、以什么协作方式运行、哪些长期意图与稳定绑定需要持久化，以及现有接入是否仍有效。**

```text
Target / Intent
      ↓
Project Onboarding
      ↓
Adoption Baseline
      ↓
Released Harness Package Adoption / Adaptation
      ↓
Workflow Entry / Resume
```

维护者如何从 Canonical 构建和发布 Harness，见 [`../governance/harness-build-and-release.md`](../governance/harness-build-and-release.md)。目标项目不参与该预编译过程。

---

## 1. 核心原则

- **Discover before Ask｜先发现，再询问**：仓库、配置、Git 与现有 Artifact 能可靠给出的事实由 Agent 自主发现；只把真实意图、歧义与权限边界交给 Human。
- **Intent before Execution｜先确定接入意图**：先明确 Spec Coding 服务谁、共享到哪里，再派生 Workspace、Repository 与 Publication 约定。
- **Persist Intent and Stable Bindings｜持久化意图与稳定绑定**：Adoption Baseline 只保存跨会话仍需要稳定复用的接入事实；Runtime、模型、工具、CI、Loader、Existing Harness 等动态事实由后续 Target-side Harness Adaptation 按需重新发现。
- **Reference over Duplication｜引用优先**：已有可靠事实源可满足需要时直接引用，不复制项目结构、Requirement、Design、Task 或 Harness 状态。
- **Affected Trace Only｜只处理受影响链路**：项目、协作方式或 Spec Coding 演进时，只刷新或迁移真正失效的接入事实及其派生项。
- **Constraint Precedence｜约束优先级**：接入配置不得弱化 Spec Coding 强制规则、目标项目更严格约束或安全边界。

涉及 Human 意图、权限或重要接入决策时，适用 [`Human-Agent Collaboration Rules`](../rules/human-agent-collaboration.md)。

---

## 2. Onboarding Trigger｜接入触发

仅在接入关系可能不存在或失效时运行：

- 当前 Target 没有有效 Adoption Baseline；
- Target / Scope 或稳定 Repository Binding 变化；
- Human 改变 Collaboration Mode、Artifact Publication 或其他长期 Usage Intent；
- Repository / Authority 等稳定约束变化；
- Spec Coding 语义变化影响当前 Adoption；
- Existing Adoption Baseline 冲突、缺失或无法验证；
- Human 明确要求重新接入、刷新或迁移。

普通 Requirement、Feature、Bug Fix、Task 或代码变化不自动触发 Onboarding。

---

## 3. 接入流程

```text
Adoption Resolution
        ↓
Usage Contract
        ↓
Adoption Reconciliation
        ↓
Baseline Validation & Handoff
```

### 3.1 Adoption Resolution｜接入解析

确认 Target Identity 与 Target Scope，并识别是否存在可复用的 Adoption Baseline / Spec Workspace。

重点识别：

- 当前对象是单仓、Monorepo、Workspace、模块还是多仓边界；
- Existing Adoption 是否存在且仍可绑定当前 Target；
- 本次变化来自首次接入、Target、Usage Intent 还是 Spec Coding；
- 本轮需要 `Initialize / Reuse / Refresh / Migrate` 中哪些操作。

Target Scope 表示 Spec Coding 管理哪条变化边界，不等于 Harness 最终放置范围。Greenfield 尚未建立 Repository 时可使用 provisional Target Binding，仓库形成后再轻量 Refresh。

**完成条件**：Target 可稳定识别，Existing Adoption 已发现或确认不存在，变化来源明确。

### 3.2 Usage Contract｜使用契约

先确定共享边界，再派生具体约定。

#### Collaboration Mode｜协作模式

| Mode | 含义 |
|---|---|
| `Local` | Spec Coding 工作状态主要服务当前 Human + Agent，不进入目标项目共享边界。 |
| `Shared` | Spec Coding 工作状态由团队共享，但不要求进入目标代码仓库。 |
| `Repository-native` | Spec Coding Artifact 作为目标项目正式资产进入 Repository。 |

#### Spec Workspace｜Spec Coding 工作空间

Spec Workspace 承载 Requirement、Design、Task、Evidence、Adoption Baseline 等需要持久化的 Spec Coding 状态。它可以与代码仓库相同，也可以分离，但必须稳定关联 Target Identity / Scope。

#### Artifact Convention｜产物约定

至少解析：

- `Working Language`；
- `Persistence`：哪些 Canonical Workflow Artifact 需要跨会话保存；
- `Publication Boundary`：Artifact 仅在 Spec Workspace、团队共享空间还是目标 Repository 中可见。

Workflow 决定“什么 Artifact 是事实源”；Onboarding 只决定“保存在哪里、对谁可见”。

#### Repository Binding & Constraints｜仓库绑定与约束

目标已有 Repository 时，仅记录执行现有 Workflow Git 语义所需的稳定绑定与硬约束，例如：

- Repository / Remote Identity；
- Base / Development Branch；
- fork / upstream / origin 等稳定 Push / PR Target；
- 是否要求 Branch Isolation / Pull Request；
- Agent 的 Push / Merge Authority；
- 禁止额外 Workspace 等硬限制。

Task Commit、Requirement Push 的时机仍由 Development Execution Workflow 定义；Worktree、并行、具体工具属于运行时策略。

#### Integration Constraint｜集成约束

只保存长期 Harness 共享 / 所有权边界，例如 Local、Shared、Project-level，以及现有项目资产是否必须保留。

具体 Rule、Skill、Hook、Tool、Subagent、Loader Surface、Runtime Capability 等动态实现事实**不进入 Adoption Baseline**；它们由后续 Released Harness Package Adoption / Adaptation 根据当前环境决定。

**完成条件**：Human Intent 已形成最小 Usage Contract，不再需要猜测 Workspace、Publication、Repository Binding 或关键 Authority。

### 3.3 Adoption Reconciliation｜接入状态对齐

只识别与接入关系有关的 Relevant Delta：

- **Target Delta**：Target / Scope / Repository Binding 变化；
- **Usage Delta**：Collaboration Mode、Working Language、Publication Boundary 等变化；
- **Spec Coding Delta**：当前规范 / Harness Release 变化影响 Adoption；
- **Stable Integration Delta**：长期共享 / 所有权边界变化。

```text
Relevant Delta
      ↓
Locate Earliest Affected Adoption Fact
      ↓
Refresh / Migrate Affected Trace
      ↓
Determine Package / Workflow Impact
```

Version 不同本身不等于 Migration；应结合 VERSION、Manifest、CHANGELOG 与必要 Diff 判断实际行为影响。

动态 Runtime Capability、Model、Tool、Loader、CI 等变化不直接修改 Adoption Baseline；它们由后续 Target-side Adaptation 重新发现。只有长期接入意图或稳定绑定受影响时才 Refresh / Migrate Adoption。

**完成条件**：所有 Relevant Delta 已归属，受影响 Adoption Trace 已收敛，并能判断后续 Released Harness Package 是否需要重新接入 / 适配。

### 3.4 Baseline Validation & Handoff｜基线验证与移交

Adoption Baseline 只持久化三类信息：

1. **Declared Intent｜声明意图**：Collaboration Mode、Working Language、Publication Boundary 等 Human-owned 意图；
2. **Resolved Binding｜稳定绑定**：Target Identity / Scope、Spec Workspace、必要 Repository / Remote Binding；
3. **Overrides / Constraints｜覆盖与硬约束**：Push / Merge / Production 等 Authority 或项目稳定约束。

明确不持久化：

```text
Runtime Loader Profile
Model / Thinking
Tool / Subagent Capability
Package Manager / CI Command
Existing Harness inventory
Temporary Working Context
Runtime-specific Harness design
```

固化前检查：

- **Completeness**：后续接入动作无需继续猜测长期意图 / 绑定；
- **Consistency**：Collaboration、Publication、Repository 与 Authority 不冲突；
- **Authority Safety**：不弱化更高层约束；
- **Minimality**：删除不会导致关键猜测的冗余字段。

Baseline 保存位置跟随 Spec Workspace 共享边界。`Reuse` 无 Relevant Delta 时不产生无意义修改；`Refresh / Migrate` 只更新受影响事实。

随后解析最终 Workflow Route：

- Greenfield 且无可复用 Workflow State → `01A Project Definition`；
- Brownfield 且项目认知不足 → `01B Project Understanding`；
- 已有有效 Canonical Artifact / Workflow State → Resume 最早仍有效 Owner Stage。

最终移交：

```text
Adoption Baseline
      +
Final Workflow Route
      +
Compatible Released Harness Package
      ↓
Target-side Harness Adoption / Adaptation
      ↓
Harness Ready
      ↓
Enter / Resume Workflow
```

当前协议只保证 Adoption Baseline 与 Route 已稳定；目标侧如何扫描 Runtime、选配 Portable Artifact、使用 Runtime-native Enhancement 并完成 Harness Acceptance，将在独立协议中定义。

**完成条件**：Adoption Baseline 有效、最小且稳定绑定当前 Target；Route 明确；后续接入不再需要猜测长期使用意图。

---

## 4. 最终约束

Project Onboarding 不要求复杂 DSL、固定问卷或全量项目扫描。Agent 应先自主发现事实，再只向 Human 暴露真正的意图与权限决策。

Project Onboarding 也不要求目标 Coding Agent 重新阅读 Canonical Corpus 或执行维护者 Harness Build；它只为后续消费已发布 Harness Package 提供稳定 Target Context。

> **Persist intent, rediscover dynamic environment facts｜持久化意图，动态环境事实按需重发现。**
