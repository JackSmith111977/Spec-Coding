# Repository Governance｜仓库维护与版本管理

本文件负责仓库维护、Canonical（规范事实源）治理与版本管理，不定义具体开发阶段行为。

## 目录职责

`docs/` 按规范职责组织：

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 持续适用规则
├── meta-protocols/  # Spec Coding 接入、装配与转换协议
├── governance/      # 仓库与版本治理
├── reference/       # 术语、Harness Primitive 与 Runtime 参考资料
├── README.md        # Human 文档导航
├── overview.md      # Human 全流程概要
└── manifest.yaml    # Machine Entry Point
```

目录表达规范身份，但机器可读 Canonical 清单仍以 [`../manifest.yaml`](../manifest.yaml) 为准。

## 仓库维护

1. **Canonical Only｜只维护一个当前正式版本**：`main` 上每份正式文档只保留一个当前路径，不使用 `v1`、`v2`、`old`、`backup` 等副本保存历史。
2. **Branch First｜先分支后修改**：功能、修复、审核与规则演进从 `main` 创建独立分支，再进入 Review / Verification。
3. **Affected Trace Only｜只改受影响链路**：只修改真实受影响的定义点、消费者和治理文件，不顺手重写无关阶段。
4. **Manifest 同步**：新增、删除、移动或重命名 Canonical Stage Document（正式阶段文档）、Canonical Rule Document（正式规则文档）、Canonical Exception Workflow Document（正式异常流程文档）或 Canonical Meta Protocol Document（正式元协议文档），或改变机器可读导航 / Reference 入口时，同步更新 `manifest.yaml`。
5. **Glossary 同步**：新增核心术语、修改规范译法或改变术语语义时，同步更新 `reference/glossary.md`。
6. **Rule Source of Truth｜规则事实源唯一**：持续适用规则维护在 `manifest.yaml` 登记的 Rule Document 中；Workflow / Meta Protocol 只引用适用规则，不复制规则正文形成并行事实源。
7. **Exception Workflow Source of Truth｜异常流程事实源唯一**：正式 Exception Workflow 维护在 `manifest.yaml` 的 `exception_workflows` 中，仅在 Trigger 成立时加载；异常流程形成调查、纠正与关闭证据，不复制主流程自身状态事实源。
8. **Meta Protocol Source of Truth｜元协议事实源唯一**：正式 Meta Protocol 维护在 `manifest.yaml` 的 `meta_protocols` 中，负责 Spec Coding 的项目接入、装配或转换，不替代 Workflow / Rules 本身的规范语义。
9. **Adoption Source of Truth｜接入事实源唯一**：Project Onboarding 形成的 Adoption Baseline 是目标项目侧的接入事实源，只保存 Declared Intent、Stable Binding 与 Override / Constraint；项目动态环境、Workflow Artifact 与 Harness 事实继续由各自来源承担。
10. **Reference is Non-normative｜参考资料非规范事实源**：`reference/` 可为 Human 与 Meta Protocol 提供术语、开放标准、Harness Primitive、Runtime Architecture 与官方事实入口，但不得覆盖 Workflow / Rule / Meta Protocol、Adoption Baseline 或 Current Runtime Evidence。
11. **Runtime Facts Stay Dynamic｜运行时事实保持动态**：Reference 不维护当前模型、Thinking、Hook 全量、Feature Flag、Quota、价格或版本特定配置；Harness Compilation 使用当前 Local / Official Evidence 重新发现。Reference 与当前事实冲突时，Current Evidence 优先。
12. **Architecture Evidence Required｜架构结论需要官方证据**：Runtime Architecture Invariant 必须具有官方文档、官方源码或官方技术材料支撑。社区资料可用于发现线索，但不能单独成为长期 Architecture Invariant。
13. **Global Contract 同步**：影响全部正式 Workflow 的通用执行规则维护在 `rules/global-contracts.md`，避免复制形成重复事实源。
14. **Changelog 同步**：改变 Workflow / Rule / Meta Protocol 语义、Artifact Contract、状态、Gate、Authority、目录消费路径或下游消费方式的变化进入 `CHANGELOG.md`；仅刷新易变 Runtime Link / Feature Snapshot 且不改变消费者语义时可作为普通 Reference Maintenance 处理。
15. **Git Owns History｜历史交给 Git**：旧版本、删除内容、Runtime 改名、迁移与退役关系由 Commit / PR / Changelog 保存，不创建 `old` / `v2` 等平行参考副本。
16. **No Silent Semantic Change｜禁止静默语义变化**：纯润色、Reference Refresh 或结构迁移不得顺带改变正式契约或规则；确需改变时按语义变更治理。

### Runtime Reference 变化分类

Coding Agent Runtime 高频变化按以下方式治理：

| Delta | 示例 | 默认处理 |
|---|---|---|
| **Feature Delta** | 新模型、新 Hook、新参数、Feature Flag | Harness Compilation 运行时重新发现；不要求立即更新 Reference。 |
| **Source / Lifecycle Delta** | 文档迁移、产品改名、deprecated / retired | 更新 `reference/coding-agent-runtimes.md` 的身份 / 官方入口。 |
| **Architecture Delta** | Plugin-first 架构、Agent Runtime 边界发生根本变化 | 更新 Architecture Invariant 与 Harness Implication；若现有 Primitive / Protocol 已无法表达，再进入 Spec Coding 语义演进。 |

Reference Drift 默认不阻塞业务 Workflow。只有当前关键 Capability / Permission / Safety Mapping 无法可靠确定时，Harness Compilation 才应 Block `Harness Ready`。

## 版本管理

版本遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 稳定版本后的不兼容阶段 / Artifact / 状态 / Gate / 消费者行为变化。 |
| `MINOR` | 新增或增强兼容能力、规则、治理、验证、Meta Protocol 或自动化机制；`0.x` 阶段的主要结构 / 语义演进通常使用 MINOR。 |
| `PATCH` | 不改变流程或规则语义的拼写、链接、格式、说明或纯文档修复。 |

普通分支提交不必每次修改 `VERSION`。形成版本时，在同一收敛变更中同步：

- `VERSION`
- `docs/manifest.yaml` 中的 `spec_coding_version` 与 `status`
- `CHANGELOG.md`

若同时改变正式 Workflow / Rules / Meta Protocol 集合、全局契约或术语，再同步 `manifest.yaml`、对应 Workflow / Rule / Meta Protocol Document、`rules/global-contracts.md`、`reference/glossary.md` 等治理与参考文件。

单纯更新 Runtime 官方链接、Lifecycle 或易变生态资料，且不改变 Harness Compilation 消费语义时，不要求独立提升 Spec Coding 语义版本；若 Reference 新增导致 Meta Protocol 消费方式或 Harness Compilation 行为发生兼容增强，则按 MINOR 治理。

Git Tag 可用于稳定里程碑或长期引用，但不替代 `VERSION + manifest + CHANGELOG` 的版本判定。

## 标准变更流程

```text
main
  ↓
独立分支
  ↓
修改受影响 Workflow / Rules / Meta Protocol / Reference / 文档
  ↓
Cross-Artifact Check
  ↓
同步治理文件（按需）
  ↓
Review / Verification
  ↓
Merge to main
  ↓
新的 Canonical Source of Truth
```

合入前至少确认：

- 上下游术语、状态、Artifact Contract 与适用 Rules 一致。
- 目录职责、Manifest 路径、Reference Entry 与 Human 导航一致。
- Meta Protocol 的先后依赖、目标项目侧 Adoption Baseline 与 Harness 输入关系一致。
- Runtime Reference 没有覆盖 Current Runtime Evidence，没有把版本易变事实固化为长期能力真相。
- 没有引入并行事实源、废弃副本或旧路径残留。
- 受影响 Trace 可追溯。
- 必要 Manifest / Rule / Exception Workflow / Meta Protocol / Reference / Glossary / Changelog 已同步。

## Agent 消费顺序

执行、接入与 Harness 构建优先使用本地一致视图。已有本地工作区时先同步并确认基线；尚无本地副本时先获取到本地。远程接口主要用于获取、同步、版本确认与必要补充。

建议按顺序处理：

```text
取得 Spec Coding 与 Target 的可用一致视图
  ↓
VERSION
  ↓
docs/manifest.yaml
  ↓
Project Onboarding
  ├─ Valid Adoption Baseline → Reuse
  └─ Missing / Relevant Delta → Initialize / Refresh / Migrate
  ↓
Adoption Baseline + Final Workflow Route
  ↓
Load Applicable Workflow / Rules
  ↓
Harness Compilation
  ├─ Harness Primitive Reference（按需）
  ├─ Runtime Reference（按需）
  └─ Current Official / Local Runtime Evidence
  ↓
Harness Ready
  ↓
Enter / Resume Main Workflow
  ↓
Triggered Exception Workflow（若有）
```

Project Onboarding 只需读取接入判断所需的最小规范与 Target Evidence，不要求预加载全部 Workflow 或 Runtime Reference。Human-Agent Collaboration 在 Onboarding 中涉及 Human Intent、Authority 或关键判断时适用；Global Contracts 仍由正式 Workflow 默认继承，不因 Meta Protocol 引用 Authority 语义而整体扩展到 Meta Protocol。

Harness Compilation 消费三类上下文：Applicable Workflow / Rules 作为 Normative Context、Adoption Baseline 作为 Adoption Context、当前 Target Environment / Existing Harness / Agent Capability 作为 Execution Context。Reference Knowledge 用于语义归一、Runtime Architecture 理解和官方事实定位，不作为第四类项目 Context；动态项目事实不应为了 Harness 编译被复制到 Adoption Baseline。

Applicable Rules 由 `manifest.yaml` 的 `rule_documents` 解析；Human-Agent Collaboration 在正式 Workflow 与需要 Human Interaction 的 Meta Protocol 中加载，其他专项规则只在适用阶段 / 任务加载。Exception Workflow 由 `exception_workflows` 解析，只在对应 Trigger 成立时加载。Meta Protocol 由 `meta_protocols` 解析，Project Onboarding 在 Harness Compilation 之前建立或验证接入基线。

Harness 达到 `Ready` 后，执行继续以正式 Workflow 文档与 Applicable Rules 为权威依据；Meta Protocol 定义接入 / 转换方法，Adoption Baseline 是目标项目侧接入事实，Harness 是项目侧执行机制，Reference 提供非规范编译知识，四者都不替代 Workflow / Rules 的规范事实源。

Human 快速理解流程优先使用 [`../overview.md`](../overview.md)、[`../workflows/README.md`](../workflows/README.md)、各阶段 README 与 [`../workflows/exceptions/README.md`](../workflows/exceptions/README.md)，不以概要或 Reference 替代正式执行规则。

## 1.0.0 稳定门槛

`0.x` 仍属于审核与 Pilot（试运行）阶段。进入 `1.0.0` 前至少完成：

- 静态审核中的重大问题收敛。
- Scenario Stress Test（场景压力测试）。
- Fresh-Agent Blind Run（新 Agent 盲跑）。
- 2–3 个真实项目 Pilot。
- 未发现重大 Trace 逃逸、静默假设或不可解释的人工作业依赖。