# Repository Governance｜仓库维护与版本管理

本文件负责仓库维护、Canonical（规范事实源）治理与版本管理，不定义具体开发阶段行为。

## 目录职责

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 持续适用规则
├── meta-protocols/  # 项目接入与 Harness 编译
├── governance/      # 仓库、版本、Semantic Compilation 治理
├── reference/       # 术语、Harness Primitive、公开标准、Runtime 参考
├── README.md
├── overview.md
└── manifest.yaml

semantic/            # 版本绑定的派生 Semantic IR

tools/
├── semantic_compiler/
├── environment_discovery/
├── harness_adapt/
└── harness_acceptance/
```

机器可读 Canonical 清单仍以 [`../manifest.yaml`](../manifest.yaml) 为准。`semantic/` 是 Derived Artifact（派生产物），不成为平行规范事实源。

## 仓库维护规则

1. **Canonical Only｜当前正式版本唯一**：`main` 上不维护 `old / v2 / backup` 平行副本；历史交给 Git。
2. **Branch First｜先分支后修改**：功能、修复、审核与规则演进从 `main` 创建独立分支。
3. **Affected Trace Only｜只改受影响链路**：只修改真实受影响的定义点、消费者和治理文件。
4. **Manifest Sync｜Manifest 同步**：Canonical 集合、机器导航或 Reference Entry 变化时同步 `manifest.yaml`。
5. **Source of Truth Separation｜事实源分离**：Workflow / Rules / Meta Protocol / Adoption Baseline / Semantic IR / Environment Model / Harness 各自承担不同生命周期，不互相复制成平行事实源。
6. **Semantic IR Is Derived｜Semantic IR 是派生物**：Canonical Markdown 改变后必须重新编译；不得通过直接修改 released IR 改变 Spec Coding 语义。
7. **Adoption Persists Stable Intent｜Adoption 只持久化稳定接入**：只保存 Declared Intent、Target / Workspace / Repository Binding、Publication / Authority Constraint；动态 Runtime / Loader / Model / Tool / CI / Existing Harness 不进入 Baseline。
8. **Environment Facts Stay Dynamic｜环境事实保持动态**：Environment Discovery 使用 Current Local / Official Evidence 重发现事实；Reference 与当前证据冲突时 Current Evidence 优先。
9. **Reference Is Non-normative｜参考资料非规范**：`reference/` 只提供共同语言、Harness Primitive、公开标准采用基线、Runtime 架构不变量与官方事实入口。
10. **No Silent Semantic Change｜禁止静默语义变化**：润色、Reference Refresh 或目录迁移不得顺带改变 Canonical 契约。
11. **Glossary Sync｜术语同步**：核心术语或规范译法变化时同步 Glossary。
12. **Version Evidence｜版本证据**：形成版本时统一同步 `VERSION + manifest + CHANGELOG`；普通功能分支可在收敛前保持当前版本。

## V3 编译边界治理

Harness Compilation V3 明确分为：

```text
Canonical Corpus
      ↓
Semantic Compile
      ↓
Semantic IR
      ↓
Environment Discover
      ↓
Environment Model
      ↓
Harness Adapt
      ↓
Verify & Accept
```

边界要求：

- Semantic Compiler 不读取 Target / Adoption / Runtime；
- Environment Discovery 不重新解释完整 Canonical prose，也不产生 Harness 设计决策；
- Harness Adapt 不允许压缩或丢弃 Applicable Clause，只允许在实现层合并 Component；
- Verify & Accept 的确定性证据、语义审查和 Fresh-agent 行为证据不得互相伪装；
- Harness Verify & Accept 不替代 Main Workflow Stage 6 Verification Convergence：前者验证 Harness，后者验证 Requirement / Change Set。

### Semantic Compilation

正式 Semantic Release 必须满足 [`semantic-compilation.md`](semantic-compilation.md)：完整 Canonical Corpus、Atomic Clause、Source Binding、Execution Relation、Fresh per-document Review、Global Review 与 Mutation Review。

Pilot 可以验证表达能力，但不得被描述为完整 Semantic Release。

### Environment Discovery

Environment Discovery 的最终 Handoff 必须保证：

- 每条 Clause 有 Discovery Disposition；
- 关键 Environment Question 有当前 Evidence；
- 已解析 Capability / Provider Surface 回指 Confirmed Fact；
- Blocking Unknown 为零；
- Environment Model 不包含 Skill / AGENTS / Subagent 等 Harness 设计结论。

### Harness Adapt

Stage 3 Handoff 必须保证：

- 每条 Clause 有唯一适配结论；
- `blocked` Clause 为零；
- Covered Clause 能追溯到 Capability Requirement、Selected Provider 与 Component；
- Provider Change 已完成并有 Targeted Refresh Evidence；
- Candidate Artifact 位于 Target 内、真实存在，并保存经验证的 `content_sha256`；
- Candidate Fingerprint 因此绑定具体 Harness 内容，而不是只有路径与结构。

### Harness Verify & Accept

Stage 4 只消费已经通过 Stage 3 的 Candidate，不在验收层静默修复语义、环境或映射。最终 `READY` 至少需要：

- Semantic / Environment / Adoption / Adaptation Plan / Candidate Fingerprint 连续一致；
- Artifact 内容 Hash 在验收期间未漂移；
- Candidate Artifact 被真实 Runtime 证明可见；
- Selected Provider 被证明 active；
- 每条 Covered Clause 至少有一个通过的验证结果；
- Required Mutation 全部被检测；
- Blocking Verification Finding 为零；
- Independent Fresh Agent 有 Isolation Evidence，并通过 `load / process / boundary / gate_lifecycle / exception` 五类代表性场景。

Verification Finding 必须标记最早 Fault Layer：`semantic / environment / adaptation / candidate / runtime`，并回到最早失真源修正，而不是在 Stage 4 形成新的设计事实源。

## External Reference Governance｜外部参考治理

Reference 分工：

| Reference | 长期维护内容 | 不承担 |
|---|---|---|
| `harness-primitives.md` | 稳定 Harness Primitive 与能力边界 | 外部协议当前版本 / Runtime 当前事实 |
| `harness-standards.md` | 公开协议采用基线、Portable / Adapter 边界、官方 Source、Freshness | 当前 Runtime 是否真的支持该标准 |
| `coding-agent-runtimes.md` | Runtime Architecture Invariant 与官方事实入口 | 当前版本、模型、Feature Flag、动态配置 |

外部高频变化按 Delta 类型处理：

| Delta | 示例 | 默认处理 |
|---|---|---|
| Standard Delta | Agent Plugins / Skills / MCP 发布新规范 | 先刷新 Source Baseline；只有 Adoption Decision 改变时才传播到受影响 Component / Adapter |
| Feature Delta | 新模型、新 Hook、新参数、Feature Flag | Environment Discover 重新发现，不要求立即更新 Runtime Reference |
| Source / Lifecycle Delta | 产品改名、文档迁移、deprecated | 更新 Reference 的身份 / 官方入口 |
| Architecture Delta | Plugin / Agent Runtime 边界根本变化 | 更新 Architecture Invariant；必要时进入 Spec Coding 语义演进 |

Fast-changing Reference 遵循：

> **Stale + Relevant → Refresh｜陈旧且当前相关时刷新。**

Reference Drift 默认不阻塞业务 Workflow；只有当前关键 Capability / Permission / Loader 无法可靠确定时，Environment Handoff / Harness Ready 才被阻断。

## 版本管理

遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 稳定版本后的不兼容阶段 / Artifact / 状态 / Gate / 消费者行为变化 |
| `MINOR` | `0.x` 阶段的主要结构 / 语义演进，或新增兼容能力、规则、治理、Meta Protocol / 自动化 |
| `PATCH` | 不改变语义的拼写、链接、格式或纯文档修正 |

形成版本时在同一收敛变更中同步：

- `VERSION`
- `docs/manifest.yaml` 的 `spec_coding_version / status`
- `CHANGELOG.md`

Git Tag 用于稳定里程碑，但不替代上述版本事实。

## 标准变更流程

```text
main
  ↓
independent branch
  ↓
change earliest affected source
  ↓
Cross-Artifact Check
  ↓
Deterministic tests + semantic review
  ↓
Version convergence（需要时）
  ↓
Merge
```

合入前至少确认：

- 上下游术语、状态、Artifact Contract 与适用 Rules 一致；
- Manifest、Human Navigation、Governance 与实际目录一致；
- Semantic IR 与 Canonical Source Fingerprint 一致；
- Environment Fact / Adoption Fact / Runtime Reference 边界没有混淆；
- Harness Candidate 内容 Hash 与真实 Artifact 一致；
- Verify & Accept 绑定当前 Candidate，而不是过期 Manifest / 文件；
- 没有旧 compiler、废弃 fixture 或平行事实源残留；
- 受影响 Trace 可追溯。

## Agent 消费顺序

```text
取得 Spec Coding 与 Target 的一致视图
  ↓
VERSION + docs/manifest.yaml
  ↓
Load matching released Semantic IR
  ↓
Project Onboarding
  ├─ valid Adoption Baseline → Reuse
  └─ missing / relevant delta → Initialize / Refresh / Migrate
  ↓
Adoption Baseline + Semantic IR
  ↓
Environment Discover
  ├─ Runtime / Loader Evidence
  ├─ Provider Surfaces
  ├─ Project Mechanisms
  └─ Existing Harness
  ↓
Environment Model
  ↓
Harness Adapt
  ↓
Adaptation Plan + content-bound Harness Candidate
  ↓
Verify & Accept
  ├─ Verification Plan
  ├─ Verification Report
  └─ Independent Acceptance Receipt
  ↓
Harness Ready
  ↓
Enter / Resume Main Workflow
  ↓
Triggered Exception Workflow（若有）
```

目标项目不重新从全部 Canonical Markdown 发现规范语义；Canonical prose 仍是规范 Source of Truth，Semantic IR 是稳定编译输入。

## 1.0.0 稳定门槛

进入 `1.0.0` 前至少完成：

- Semantic IR 全量发布与 Mutation Review；
- Scenario Stress Test；
- Fresh-Agent Blind Run；
- 2–3 个真实项目 Pilot；
- 未发现重大 Trace 逃逸、静默假设或不可解释的人工作业依赖。
