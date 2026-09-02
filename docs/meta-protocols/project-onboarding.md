# Project Onboarding Protocol｜项目接入协议

本协议属于 Meta Protocol（元协议），定义 Spec Coding 在进入 Harness Compilation（Harness 编译）之前，如何与目标项目建立、复用、刷新或迁移稳定的接入关系。

Project Onboarding 不推进业务开发阶段，不替代 Project Definition / Project Understanding，也不生成 Harness。它只负责回答：**Spec Coding 当前作用于哪个 Target、以什么协作方式运行、哪些稳定约定需要持久化，以及现有接入是否仍然有效。**

```text
Target / Intent
      ↓
Project Onboarding
      ↓
Adoption Baseline
      ↓
Harness Compilation
      ↓
Workflow Entry
```

Onboarding 属于 Pre-Harness（Harness 前置）协议。没有有效 Adoption Baseline 时，Harness Compilation 不应自行猜测项目接入方式，而应先回到本协议。

---

## 1. 核心原则

- **Discover before Ask｜先发现，再询问**：能够通过仓库、配置、现有 Artifact、Git 与运行环境可靠获得的事实由 Agent 自主发现；只把真实意图、歧义与权限边界交给 Human。
- **Intent before Execution｜先确定接入意图**：先明确 Spec Coding 服务谁、共享到哪里，再派生 Artifact、Repository 与 Harness 约定。
- **Persist Intent and Stable Bindings｜持久化意图与稳定绑定**：Adoption Baseline 只保存跨会话仍需要稳定复用的接入事实；技术栈、CI、Agent Capability 等易变环境事实由下游重新发现。
- **Reference over Duplication｜引用优先**：已有可靠事实源可满足需要时直接引用，不在 Adoption Baseline 复制项目结构、Requirement、Design、Task 或 Harness 状态。
- **Affected Trace Only｜只处理受影响链路**：项目、协作方式、Spec Coding 或 Agent Integration 发生变化时，只刷新或迁移真正失效的接入事实及其派生项。
- **Constraint Precedence｜约束优先级**：接入配置不得弱化 Spec Coding 强制规则、目标项目更严格约束或安全边界。

涉及 Human 意图、权限或重要接入决策时，适用 [`Human-Agent Collaboration Rules`](../rules/human-agent-collaboration.md)：Agent 先取证并形成 Decision-ready Interaction（可决策交互），不把可自动发现的信息转交 Human。

---

## 2. Onboarding Trigger｜接入触发

仅在接入关系可能不存在或失效时运行本协议：

- 当前 Target 没有有效 Adoption Baseline；
- Target / Scope 或稳定 Repository Binding 发生变化；
- Human 改变 Collaboration Mode、Artifact Publication 或其他长期 Usage Intent；
- 目标项目与接入相关的 Repository / Authority 约束发生变化；
- Spec Coding 版本或语义变化可能影响当前 Adoption；
- Agent / Harness Integration 发生相关变化；
- 发现现有 Adoption Baseline 冲突、缺失或无法验证；
- Human 明确要求重新接入、刷新或迁移。

普通 Requirement、Feature、Bug Fix、Task 或代码变化不自动触发 Onboarding；它们继续由 Main / Exception Workflow 承接。

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

先确认 Target Identity（目标身份）与 Target Scope（目标范围），并识别是否已经存在可复用的接入状态。

重点识别：

- 当前作用对象是单仓、Monorepo、Workspace、模块还是多仓协作边界；
- 是否存在与该 Target 匹配的 Adoption Baseline、Spec Workspace 或已有 Spec Coding Artifact；
- 当前变化来自首次接入、目标项目、Usage Intent、Spec Coding 还是 Integration；
- 本次可能需要 `Initialize`、`Reuse`、`Refresh`、`Migrate` 中哪些操作。

`Initialize / Reuse / Refresh / Migrate` 是本次接入操作类型，不要求持久化为互斥状态；例如 Project Delta 与 Spec Coding Delta 可以同时触发 `Refresh + Migrate`。

Target Scope 表示 Spec Coding 管理哪条变化边界，不等于 Harness 最终放置范围。Greenfield 尚未建立 Git Repository 时允许使用 provisional Target Binding（临时目标绑定），后续仓库形成后再轻量 Refresh。

**完成条件**

当前 Target 可稳定识别，Existing Adoption 已被发现或确认不存在，且本次需要处理的接入变化来源已经明确。

---

### 3.2 Usage Contract｜使用契约

先确定 Spec Coding 的共享边界，再派生具体约定，而不是逐项独立询问语言、目录或 Git。

#### Collaboration Mode｜协作模式

第一版使用三类语义：

| Mode | 含义 | 默认约定来源 |
|---|---|---|
| `Local` | Spec Coding 工作状态主要服务当前 Human + Agent，不进入目标项目共享边界。 | Human Working Convention 优先。 |
| `Shared` | Spec Coding 工作状态由团队共享，但不要求进入目标代码仓库。 | Shared Workspace / Team Convention 优先。 |
| `Repository-native` | Spec Coding Artifact 作为目标项目正式资产进入 Repository。 | Applicable Repository Convention 优先。 |

> **The closer an artifact is to the target project, the more it inherits target-project conventions｜产物越进入目标项目共享边界，就越应继承适用的项目约定。**

#### Spec Workspace｜Spec Coding 工作空间

Spec Workspace 是 Requirement、Design、Task、Evidence、Adoption Baseline 等 Spec Coding 持久状态的承载空间。它与目标代码仓库可以相同，也可以完全分离：

```text
Local              → Local Spec Workspace
Shared             → Shared Spec Workspace
Repository-native  → Target Repository Workspace
```

工作空间位置必须能够稳定关联 Target Identity / Scope，避免多个 clone、fork 或项目之间串联错误。

#### Artifact Convention｜产物约定

根据 Collaboration Mode 至少解析：

- `Working Language`：面向 Human-Agent 协作的默认语言；Local 模式优先继承 Human Working Language；Repository-native 模式遵守适用的项目 / 团队文档约定。
- `Persistence`：哪些 Workflow 已定义为 Canonical 的工作状态需要跨会话保存；Working Context、临时推理和搜索缓存默认不持久化。
- `Publication Boundary`：Spec Coding Artifact 是否仅存在 Spec Workspace、进入团队共享空间或进入目标 Repository。

Workflow 决定“什么 Artifact 需要成为事实源”；Onboarding 只决定“这些事实保存在哪里、对谁可见”，不得重新定义 Requirement / Design / Task Artifact Contract。

#### Repository Binding & Constraints｜仓库绑定与约束

只有目标已存在 Repository 时，识别执行现有 Workflow Git 语义所需的稳定绑定与硬约束，例如：

- Working / Base Repository 与稳定 Remote Identity；
- Base / Development Branch；
- fork / upstream / origin 等 Push 与 PR Target；
- 是否要求 Branch Isolation / Pull Request；
- Agent 的 Push / Merge Authority；
- 是否存在禁止额外 Workspace 等硬限制。

Task Commit、Requirement Integration、Requirement AC Gate 与 Requirement Push 的**时机和语义仍由 Development Execution Workflow 定义**；是否使用 Worktree、如何并行等运行时策略继续由 Workflow + Harness + Current Execution Set 动态推导。

#### Integration Constraint｜集成约束

只记录 Harness 的稳定共享 / 所有权边界，例如 Local、Shared、Project-level，以及现有 Harness 是否必须保留。具体使用 Rule、Skill、Hook、Tool、Subagent 或其他组件由 Harness Compilation 决定。

**完成条件**

Human Intent 已形成最小 Usage Contract；Agent 不再需要猜测 Spec Workspace、Artifact Publication、稳定 Repository Binding 或关键 Authority 边界。

---

### 3.3 Adoption Reconciliation｜接入状态对齐

对照 Existing Adoption Baseline、当前 Target、当前 Usage Intent、当前 Spec Coding 与 Integration 环境，只识别与接入关系有关的 Relevant Delta（相关变化）。

变化来源统一分为：

- **Target Delta**：Target / Scope / Repository Binding 或项目接入约束变化；
- **Usage Delta**：Collaboration Mode、Working Language、Publication Boundary 等 Human Intent 变化；
- **Spec Coding Delta**：当前版本中的 Meta Protocol、Rule、Artifact / Authority / Consumer 语义变化；
- **Integration Delta**：Agent / Harness 接入环境发生相关变化。

处理顺序：

```text
Relevant Delta
      ↓
Locate Earliest Affected Adoption Fact
      ↓
Re-derive Dependent Conventions
      ↓
Refresh / Migrate Affected Trace
      ↓
Determine Harness / Workflow Impact
```

- 没有相关影响时直接 `Reuse`；
- Target / Usage 侧事实失效时 `Refresh` 受影响部分；
- 当前 Adoption 依赖的 Spec Coding / Integration 语义不兼容时 `Migrate` 受影响部分；
- Version 不同本身不等于 Migration，应结合 VERSION、manifest、CHANGELOG 与必要 Diff 判断 Applicable Semantic Delta。

Harness 是否需要重新编译是对齐结果，不是操作类型；只有被 Harness 消费的 Adoption Fact 发生变化时才重编译受影响机制。

若 Target Scope 或其他接入变化使既有 Workflow Artifact 的前提失效，只返回最早失效的 Owner Stage；不在 Onboarding 内重新执行 Project Understanding、Requirement 或 Design。

**完成条件**

所有 Relevant Delta 已有明确归属，受影响 Adoption Trace 已收敛，并能判断 Harness 是否需要 Build / Recompile / Reuse，以及 Main Workflow 是否需要重新进入某个 Owner Stage。

---

### 3.4 Baseline Validation & Handoff｜基线验证与移交

将前三步结果收敛成唯一有效的 **Adoption Baseline（接入基线）**。

Adoption Baseline 只持久化三类信息：

1. **Declared Intent｜声明意图**：Collaboration Mode、Working Language、Publication Boundary 等 Human-owned 使用意图；
2. **Resolved Binding｜稳定绑定**：Target Identity / Scope、Spec Workspace、必要 Repository / Remote Binding，以及 Harness 输出所依赖的 Runtime Loader Profile（Runtime ID、可选版本、实际 Loader Surface 与发现证据）；
3. **Overrides / Constraints｜覆盖与硬约束**：Push / Merge / Production 等相对默认规则的 Authority 或项目约束。

不要复制完整项目结构、技术栈、Package Manager、CI / Test Command、Requirement / Design / Task 内容、Harness 组件清单、Agent Capability 或临时 Working Context。Loader Profile 仅记录“本次项目 Harness 应由哪里被发现”，不记录模型列表、Thinking、临时工具可用性或通用 Runtime Capability。

固化前执行四项轻量检查：

- **Completeness｜完整性**：后续关键接入动作无需继续猜测；
- **Consistency｜一致性**：Collaboration Mode、Publication、Repository 与 Integration 约定不存在依赖冲突；
- **Authority Safety｜权限安全**：Baseline 不弱化更高层 Spec Coding / 项目 / 安全约束；
- **Minimality｜最小性**：删除不会导致重要猜测的冗余字段。
- **Runtime Visibility｜运行时可见性**：若接入需要编译 Harness，Baseline 已有当前 Runtime Loader Profile；至少声明精确 `context_files`、或 Skill / Extension 目录及其当前证据，不能以“项目中某个子目录”替代真实加载规则。

Baseline 保存位置跟随 Spec Workspace 的共享边界。`Reuse` 时无 Relevant Delta 则不产生无意义修改；`Refresh / Migrate` 只更新受影响事实，不维护 `old / v2 / backup` 平行副本。

随后确定最终 Workflow Route：

- Greenfield 且尚无可复用 Workflow State → `01A Project Definition`；
- Brownfield 且尚无足够项目认知 → `01B Project Understanding`；
- 已有有效 Canonical Artifact / Workflow State → `Resume` 最早仍有效的 Owner Stage。

Onboarding 只解析 Route，不替代对应 Stage Gate 的正式有效性确认。

最终移交：

```text
Adoption Baseline
      +
Final Workflow Route
      ↓
Harness Compilation
      ↓
Harness Ready
      ↓
Enter / Resume Workflow
```

**完成条件**

Adoption Baseline 已有效、最小且可定位到当前 Target；最终 Workflow Route 已明确；Harness Compilation 已获得无需猜测的 Adoption Context。

---

## 4. 最终约束

Project Onboarding 不要求复杂 DSL、固定问卷或全量项目扫描。Agent 应利用原生文件、Git、搜索与环境能力先建立事实，再只向 Human 暴露真正的意图与权限决策。

协议最终必须保证：

> **先建立 Spec Coding 与 Target 的稳定接入关系，再编译执行 Harness；持久化长期意图与绑定，动态事实按需重新发现；项目、协作方式或 Spec Coding 演进时，只刷新真正失效的接入链路。**
