# Repository Governance｜仓库维护与版本管理

本文件负责仓库维护、Canonical（规范事实源）治理、Harness Package 发布与版本管理，不定义具体业务开发阶段行为。

## 1. 目录职责

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 持续适用规则
├── meta-protocols/  # 目标项目接入协议
├── governance/      # 仓库、版本、Harness Build & Release 治理
├── reference/       # 术语、Harness Primitive、公开标准、Runtime 参考
├── README.md
├── overview.md
└── manifest.yaml

packages/
└── harness/         # 当前版本的可发布 Harness Package 入口
```

机器可读 Canonical 清单仍以 [`../manifest.yaml`](../manifest.yaml) 为准。

事实源边界：

```text
Canonical Markdown under docs/
        ↓
Harness Build & Release
        ↓
Released Harness Package under packages/harness/
```

`packages/harness/` 是 Derived Artifact（派生产物），不成为平行规范事实源。发现行为错误时优先定位最早失真位置：Canonical、Build、Package Assembly 或 Verification；不得通过直接手工修改 Release Artifact 改变 Spec Coding 语义。

---

## 2. 仓库维护规则

1. **Canonical Only｜当前正式版本唯一**：`main` 上不维护 `old / v2 / backup` 平行副本；历史交给 Git / Release。
2. **Branch First｜先分支后修改**：功能、修复、审核、规则演进与 Harness Build 变化从 `main` 创建独立分支。
3. **Affected Trace Only｜只改受影响链路**：只修改真实受影响的定义点、消费者、派生产物和治理文件。
4. **Manifest Sync｜Manifest 同步**：Canonical 集合、机器导航或 Reference Entry 变化时同步 `manifest.yaml`。
5. **Source of Truth Separation｜事实源分离**：Canonical Workflow / Rules / Meta Protocol、Adoption Baseline、Released Harness Package 与 Target Runtime Fact 各自承担不同生命周期。
6. **Harness Is Derived｜Harness 是派生产物**：Harness Package 从 Canonical 构建并经过验证；不得通过直接修改 Release Artifact 静默改变规范行为。
7. **Build Internals Stay Internal｜构建内部实现不外溢**：临时 Worklist、Checklist、语义拆解、Reviewer scratch state 等只服务维护者构建，不成为使用方必须消费的正式层。
8. **Standards First｜公开标准优先**：等价可靠时优先 Agent Skills、Agent Plugins、MCP、AGENTS.md 等公开标准 / 开放格式；不能等价时保留 Runtime-specific Requirement，不强行伪标准化。
9. **Adoption Persists Stable Intent｜Adoption 只持久化稳定接入**：只保存 Declared Intent、Target / Workspace / Repository Binding、Publication / Authority Constraint；动态 Runtime / Loader / Model / Tool / CI / Existing Harness 不进入 Baseline。
10. **Environment Facts Stay Dynamic｜环境事实保持动态**：当前 Runtime 能力始终由目标侧根据 Current Local / Official Evidence 重发现；Reference 不充当能力缓存。
11. **Reference Is Non-normative｜参考资料非规范**：`reference/` 只提供共同语言、Harness Primitive、公开标准采用基线、Runtime 架构不变量与官方事实入口。
12. **No Silent Semantic Change｜禁止静默语义变化**：润色、Reference Refresh、目录迁移、Packaging 调整不得顺带改变 Canonical 契约。
13. **Glossary Sync｜术语同步**：核心术语或规范译法变化时同步 Glossary。
14. **Version Evidence｜版本证据**：形成正式版本时统一同步 `VERSION + manifest + CHANGELOG + Harness Package Release`；普通功能分支可在收敛前保持当前版本。

---

## 3. Harness Build & Release 治理

正式维护流程见 [`harness-build-and-release.md`](harness-build-and-release.md)：

```text
Build Scope Establishment
        ↓
Harness Precompile & Assembly
        ↓
Package Verification & Review
        ↓
Release & Lifecycle Convergence
```

### Build Scope

构建必须来自明确触发：Canonical Change、Harness Defect 或 Standard / Packaging Change。Scope 只覆盖真实受影响 Source 与 Output。

### Precompile & Assembly

Harness 直接从 Canonical 生成。复杂行为需要多个机制时直接组合公开标准与必要 Runtime Requirement，不创造无必要的 Spec Coding 私有 Component Protocol。

### Verification & Review

至少区分：

- Structural Verification：格式、引用、路径、Hash、Manifest；
- Semantic Review：Canonical ↔ Generated Harness 直接对照；
- Behavioral Test：必要时由 Fresh Agent 消费候选 Package 挑战关键流程、Boundary、Authority / Gate 与 Exception。

验证失败回到最早失真源，不在验证层形成新的行为事实源。

### Release & Lifecycle

当前阶段默认：

```text
Spec Coding VERSION = Harness Package VERSION
```

不提前建立独立 IR / Component / Compiler 版本森林。历史发行通过 Git Tag / GitHub Release 获取；`packages/harness/` 只维护当前版本结构。

---

## 4. External Reference Governance｜外部参考治理

Reference 分工：

| Reference | 长期维护内容 | 不承担 |
|---|---|---|
| `harness-primitives.md` | 稳定 Harness Primitive 与能力边界 | 外部协议当前版本 / Runtime 当前事实 |
| `harness-standards.md` | 公开协议采用基线、Portable / Runtime-specific 边界、官方 Source、Freshness | 当前 Runtime 是否真的支持该标准 |
| `coding-agent-runtimes.md` | Runtime Architecture Invariant 与官方事实入口 | 当前版本、模型、Feature Flag、动态配置 |

外部高频变化按 Delta 类型处理：

| Delta | 示例 | 默认处理 |
|---|---|---|
| Standard Delta | Agent Plugins / Skills / MCP 发布新规范 | 刷新 Source Baseline；只有 Packaging / Build Decision 变化时重建受影响 Harness |
| Feature Delta | 新模型、新 Hook、新参数、Feature Flag | 留给目标侧环境发现，不要求维护者提前固化 |
| Source / Lifecycle Delta | 产品改名、文档迁移、deprecated | 更新 Reference 的身份 / 官方入口 |
| Architecture Delta | Plugin / Agent Runtime 边界根本变化 | 更新 Architecture Invariant；必要时影响 Build / Target Adaptation 设计 |

Fast-changing Reference 遵循：

> **Stale + Relevant → Refresh｜陈旧且当前相关时刷新。**

---

## 5. 版本管理

遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 稳定版本后的不兼容阶段 / Artifact / 状态 / Gate / 消费者行为变化 |
| `MINOR` | `0.x` 阶段的主要结构 / 语义演进，或新增兼容能力、规则、治理、Meta Protocol / Harness 发行能力 |
| `PATCH` | 不改变 Canonical 语义的 Harness 修复、拼写、链接、格式或纯文档修正；若 Harness 修复改变实际执行行为，应在 CHANGELOG 中明确 |

形成版本时在同一收敛变更中同步：

- `VERSION`
- `docs/manifest.yaml` 的 `spec_coding_version / status`
- `CHANGELOG.md`
- 当前 Harness Package / Release Metadata

Git Tag / GitHub Release 用于稳定里程碑，但不替代上述版本事实。

---

## 6. 标准变更流程

```text
main
  ↓
independent branch
  ↓
change earliest affected source
  ↓
Cross-Artifact Check
  ↓
Harness Build Scope（若影响 Harness）
  ↓
Precompile / Assembly
  ↓
Structural + Semantic + Behavioral Verification
  ↓
Version convergence（需要时）
  ↓
Merge / Release
```

合入前至少确认：

- 上下游术语、状态、Artifact Contract 与适用 Rules 一致；
- Manifest、Human Navigation、Governance 与实际目录一致；
- Harness Package 的 Source Trace 指向当前 Canonical；
- 生成 Harness 没有遗漏、弱化或新增 Canonical 行为；
- Package 内容 Hash 与验证对象一致；
- 不存在旧 Semantic IR / V3 compiler、废弃 fixture 或平行事实源残留；
- Runtime 动态事实没有被错误固化进 Portable Package；
- 受影响 Trace 可追溯。

---

## 7. Maintainer / User Boundary｜维护者与使用方边界

维护者：

```text
Canonical
→ Build
→ Verify
→ Release
```

使用方：

```text
Released Harness Package
→ Current Environment Adaptation
→ Harness Acceptance
→ Workflow Execution
```

目标项目 Coding Agent 不需要读取维护者构建内部状态，也不需要重新执行 Canonical → Harness 的预编译工作。目标侧只处理当前 Runtime / Project 才能确定的动态差异。

---

## 8. 1.0.0 稳定门槛

进入 `1.0.0` 前至少完成：

- 全量 Canonical → Harness Package 构建并通过直接 Semantic Review；
- Package Structural Verification；
- Scenario Stress Test / Fresh-Agent Blind Run；
- 2–3 个真实 Runtime / 项目 Pilot；
- Target-side Package Adoption / Adaptation Protocol 收敛；
- 未发现重大 Trace 逃逸、静默假设或无法解释的人工依赖。
