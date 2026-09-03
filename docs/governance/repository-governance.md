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

机器可读 Canonical 清单以 [`../manifest.yaml`](../manifest.yaml) 为准。

```text
Canonical Markdown under docs/
        ↓
Harness Build & Release
        ↓
Released Harness Package under packages/harness/
```

`packages/harness/` 是 Derived Artifact（派生产物），不成为平行规范事实源。

---

## 2. 仓库维护规则

1. **Canonical Only｜当前正式版本唯一**：`main` 不维护 `old / v2 / backup` 平行副本；历史交给 Git / Release。
2. **Branch First｜先分支后修改**：功能、修复、审核、规则演进与 Harness Build 变化从 `main` 创建独立分支。
3. **Affected Trace Only｜只改受影响链路**：只修改真实受影响的定义点、消费者、派生产物和治理文件。
4. **Manifest Sync｜Manifest 同步**：Canonical 集合、机器导航或 Reference Entry 变化时同步 `manifest.yaml`。
5. **Source of Truth Separation｜事实源分离**：Canonical、Adoption Baseline、Released Harness Package 与 Target Runtime Fact 各自承担不同生命周期。
6. **Harness Is Derived｜Harness 是派生产物**：Harness Package 从 Canonical 构建并经过验证；不得通过直接修改 Release Artifact 静默改变规范行为。
7. **Build Internals Stay Internal｜构建内部实现不外溢**：临时 Worklist、Build Scope、Checklist、语义拆解、Reviewer scratch state 等不成为使用方必须消费的正式层。
8. **Standards First｜公开标准优先**：等价可靠时优先 Agent Skills、Agent Plugins、MCP、AGENTS.md 等公开标准 / 开放格式。
9. **Adoption Persists Stable Intent｜Adoption 只持久化稳定接入**：动态 Runtime / Loader / Model / Tool / CI / Existing Harness 不进入 Baseline。
10. **Environment Facts Stay Dynamic｜环境事实保持动态**：当前 Runtime 能力由目标侧根据 Current Local / Official Evidence 重发现。
11. **Reference Is Non-normative｜参考资料非规范**：`reference/` 只提供共同语言、公开标准采用基线、Runtime 架构不变量与官方事实入口。
12. **No Silent Semantic Change｜禁止静默语义变化**：润色、Reference Refresh、目录迁移、Packaging 调整不得顺带改变 Canonical 契约。
13. **Glossary Sync｜术语同步**：核心术语或规范译法变化时同步 Glossary。
14. **Version Evidence｜版本证据**：正式版本统一同步 `VERSION + manifest + CHANGELOG + Harness Package Release`。

---

## 3. Harness Build & Release 治理

正式流程见 [`harness-build-and-release.md`](harness-build-and-release.md)：

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

Build Scope 采用两种模式：

```text
First build / no reliable baseline
→ FULL

Previous valid Harness Release exists
→ DIFF-DRIVEN INCREMENTAL
```

增量构建的 Baseline 必须是上一正式 Harness Release 在 Build Manifest 中绑定的 `source_revision`，不是 `HEAD~1` 或任意最近 Commit。

Canonical Delta 使用 Git Diff 识别，上一版 Build Manifest 通过 `artifact → exact source files` 提供反向 Source → Artifact 映射：

```text
Previous Release source_revision
        ↓
Git Diff
        ↓
Changed Canonical Sources
        ↓
Previous Build Manifest
        ↓
Affected Harness Artifacts
```

Diff 只判断“哪些 Source 变化”，不预先判断变化是否足够语义化。Canonical Source 变化后，相关 Artifact 默认重建；最终 Artifact 是否实际变化由内容 Hash 判断。

Harness Defect 与 Standard / Packaging Delta 可以显式加入 Scope。新增 Canonical Source 无现有映射时，先按所属 Workflow / Rule / Meta Protocol 解析候选 Artifact；无法可靠归属时由 Maintainer 建立首次绑定。

无法证明受影响范围时必须回退 Full Build：

> **Incremental when provable; full when uncertain.｜能证明范围时增量，不能证明时全量。**

Package Manifest、Artifact Inventory、Hash List、Routing / Bootstrap Index 等 Package Envelope 每轮全量重生成；实际 Harness 内容按 Scope 增量构建。

### Precompile & Assembly

Harness 直接从 Canonical 生成，并遵守以下边界：

- **Direct Source｜直接读源**：Builder 直接读取当前 Canonical Markdown；Summary、Clause、IR 或其他 Agent 的二次转述不得替代原文；
- **Complete Rebuild｜完整重建**：被 Stage 1 判定受影响的 Artifact 必须重新读取其完整当前 Canonical Sources，并重建整个 Artifact；
- **Diff Is Scope Only｜Diff 只定范围**：Git Diff 只用于确定 stale Artifact，不作为内容生成依据，也不允许据此直接 patch 旧 Harness；
- **Source Backcheck｜原文回查**：生成后由 Builder 直接回到实际读取的 Canonical 检查 Hard Semantics、Procedure、Authority / Gate、Exception / Routing 与有效 Guidance 是否保持完整。

复杂行为需要多个机制时直接组合公开标准与必要 Runtime Requirement，不创造无必要的 Spec Coding 私有 Component Protocol。

Build Manifest 至少保存：

- Harness Package version；
- 最终 `source_revision`；
- 每个 Artifact 本轮实际直接读取并依赖的精确 Canonical Source 列表；
- Artifact type / requirement metadata；
- Artifact content hash。

首次 Full Build 同时建立后续增量构建所需的 Source → Artifact 派生关系；后续增量重建必须根据本轮真实读取结果刷新 Source Trace。

### Verification & Review

验证针对固定 Harness Package Candidate，并遵守以下边界：

- **Fixed Candidate｜固定候选**：进入验证后固定 Candidate 的 Commit / Hash；任何修改都会产生新 Candidate 并重新验证；
- **Deterministic Structural Verification｜确定性结构验证**：格式、引用、路径、Manifest、`source_revision`、Source Trace、Artifact Hash 与 Package Envelope 优先机器检查；
- **Independent Reviewer｜独立审查**：Semantic Reviewer 直接读取 Canonical 与 Candidate，不依赖 Builder Summary、Source Backcheck 结论或 Builder 推理；
- **Harness-only Behavioral Test｜仅 Harness 行为测试**：Fresh Test Agent 只消费 Harness Candidate 与 Scenario，不读取 Canonical；Canonical 仅作为 Reviewer 的 Test Oracle；
- **Affected Verification｜受影响验证**：Full Build 全量审查；Incremental Build 全量执行 Package Structural Verification，Semantic Review 聚焦 `affected_artifacts`，Behavioral Challenge 聚焦 `validation_focus`；共享 Rule / Bootstrap / Routing / Package Composition 变化时扩大到包级集成挑战。

验证失败回到最早失真源，不在验证层直接修 Candidate 后继续判定 PASS。最终只允许 `PASS / BLOCKED`。

### Release & Lifecycle

当前阶段默认：

```text
Spec Coding VERSION = Harness Package VERSION
```

不提前建立独立 IR / Component / Compiler 版本森林。历史发行通过 Git Tag / GitHub Release 获取；`packages/harness/` 只维护当前版本结构。

---

## 4. External Reference Governance｜外部参考治理

| Reference | 长期维护内容 | 不承担 |
|---|---|---|
| `harness-primitives.md` | 稳定 Harness Primitive 与能力边界 | 外部协议当前版本 / Runtime 当前事实 |
| `harness-standards.md` | 公开协议采用基线、Portable / Runtime-specific 边界、官方 Source、Freshness | 当前 Runtime 是否真的支持该标准 |
| `coding-agent-runtimes.md` | Runtime Architecture Invariant 与官方事实入口 | 当前版本、模型、Feature Flag、动态配置 |

外部高频变化按 Delta 类型处理：

| Delta | 默认处理 |
|---|---|
| Standard Delta | 刷新 Source Baseline；只有 Build / Packaging Decision 变化时重建受影响 Harness |
| Feature Delta | 留给目标侧环境发现 |
| Source / Lifecycle Delta | 更新 Reference 身份 / 官方入口 |
| Architecture Delta | 更新 Architecture Invariant；必要时影响 Build / Target Adaptation |

> **Stale + Relevant → Refresh｜陈旧且当前相关时刷新。**

---

## 5. 版本管理

遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 稳定版本后的不兼容阶段 / Artifact / 状态 / Gate / 消费者行为变化 |
| `MINOR` | `0.x` 阶段的主要结构 / 语义演进，或新增兼容能力、规则、治理、Meta Protocol / Harness 发行能力 |
| `PATCH` | 不改变 Canonical 语义的 Harness 修复、拼写、链接、格式或纯文档修正；Harness 修复改变实际执行行为时需在 CHANGELOG 明确 |

形成版本时同步：

- `VERSION`
- `docs/manifest.yaml` 的 `spec_coding_version / status`
- `CHANGELOG.md`
- 当前 Harness Package / Build Manifest / Release Metadata

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
Full or Incremental Precompile / Assembly
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
- Build Scope Baseline 与上一正式 Release 对齐；
- 受影响 Artifact 已从完整当前 Canonical 重新读取并生成，而不是按 Diff patch；
- Builder Source Backcheck 已完成；
- Harness Package 的 Source Trace 指向本轮实际直接读取的当前 Canonical；
- Build Manifest 的 `source_revision` 与最终验证对象一致；
- Independent Semantic Review 由直接读取 Canonical 的 Reviewer 完成；
- Behavioral Challenge 的 Test Agent 未读取 Canonical；
- 最终准备发布的 Package 内容身份与验证通过 Candidate 完全一致；
- 生成 Harness 没有遗漏、弱化或新增 Canonical 行为；
- Package 内容 Hash 与验证对象一致；
- 不存在旧 Semantic IR / V3 compiler、废弃 fixture 或平行事实源残留；
- Runtime 动态事实没有被错误固化进 Portable Package。

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

目标项目 Coding Agent 不读取维护者构建内部状态，也不重新执行 Canonical → Harness 预编译。

---

## 8. 1.0.0 稳定门槛

进入 `1.0.0` 前至少完成：

- 全量 Canonical → Harness Package 构建并建立完整 Source Mapping；
- Package Structural Verification；
- Scenario Stress Test / Fresh-Agent Blind Run；
- 至少一次真实 Diff-driven Incremental Build 演练；
- 2–3 个真实 Runtime / 项目 Pilot；
- Target-side Package Adoption / Adaptation Protocol 收敛；
- 未发现重大 Trace 逃逸、静默假设或无法解释的人工依赖。
