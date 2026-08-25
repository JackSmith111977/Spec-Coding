# Repository Governance｜仓库维护与版本管理

本文件负责仓库维护、Canonical（规范事实源）治理与版本管理，不定义具体开发阶段行为。

## 仓库维护

1. **Canonical Only｜只维护一个当前正式版本**：`main` 上每份正式文档只保留一个当前路径，不使用 `v1`、`v2`、`old`、`backup` 等副本保存历史。
2. **Branch First｜先分支后修改**：功能、修复、审核与规则演进从 `main` 创建独立分支，再进入 Review / Verification。
3. **Affected Trace Only｜只改受影响链路**：只修改真实受影响的定义点、消费者和治理文件，不顺手重写无关阶段。
4. **Manifest 同步**：新增、删除、移动或重命名 Canonical Stage Document（正式阶段文档）或 Canonical Rule Document（正式规则文档），或改变机器可读导航入口时，同步更新 `manifest.yaml`。
5. **Glossary 同步**：新增核心术语、修改规范译法或改变术语语义时，同步更新 `glossary.md`。
6. **Rule Source of Truth｜规则事实源唯一**：跨阶段持续适用的规则维护在 `manifest.yaml` 登记的 Rule Document 中；阶段文档只引用适用规则，不复制规则正文形成并行事实源。
7. **Global Contract 同步**：影响全部阶段的通用执行规则维护在 `global-contracts.md`，避免复制到各阶段形成重复事实源。
8. **Changelog 同步**：改变 Workflow / Rule 语义、Artifact Contract、状态、Gate、Authority 或下游消费方式的变化进入 `CHANGELOG.md`。
9. **Git Owns History｜历史交给 Git**：旧版本、删除内容与重命名关系由 Commit / PR / Changelog 保存。
10. **No Silent Semantic Change｜禁止静默语义变化**：纯润色不得顺带改变正式契约或规则；确需改变时按语义变更治理。

## 版本管理

版本遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 稳定版本后的不兼容阶段 / Artifact / 状态 / Gate / 消费者行为变化。 |
| `MINOR` | 新增或增强兼容能力、规则、治理、验证或自动化机制；`0.x` 阶段的主要语义演进通常使用 MINOR。 |
| `PATCH` | 不改变流程或规则语义的拼写、链接、格式、说明或纯文档修复。 |

普通分支提交不必每次修改 `VERSION`。形成版本时，在同一收敛变更中同步：

- `VERSION`
- `docs/manifest.yaml` 中的 `spec_coding_version` 与 `status`
- `CHANGELOG.md`

若同时改变正式 Workflow / Rules 集合、全局契约或术语，再同步 `manifest.yaml`、对应 Rule Document、`global-contracts.md`、`glossary.md` 等治理文件。

Git Tag 可用于稳定里程碑或长期引用，但不替代 `VERSION + manifest + CHANGELOG` 的版本判定。

## 标准变更流程

```text
main
  ↓
独立分支
  ↓
修改受影响 Workflow / Rules / 文档
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
- 没有引入并行事实源或废弃副本。
- 受影响 Trace 可追溯。
- 必要 Manifest / Rule Document / Glossary / Changelog 已同步。

## Agent 消费顺序

执行与 Harness 构建优先使用本地一致视图。已有本地工作区时先同步并确认基线；尚无本地副本时先获取到本地。远程接口主要用于获取、同步、版本确认与必要补充。

Agent 构建 Harness 时建议按顺序读取：

```text
本地取得 Spec Coding 与目标项目的一致工作区
  ↓
VERSION
  ↓
manifest.yaml
  ↓
Applicable Rules
  ↓
harness-compilation-protocol.md
  ↓
当前阶段正式 Workflow 文档
  ↓
必要上游引用 / Exception Workflow
```

Applicable Rules 由 `manifest.yaml` 的 `rule_documents` 解析；`global-execution` 始终加载，其他专项规则只在适用阶段 / 任务加载。

Harness 达到 `Ready` 后，阶段执行继续以正式 Workflow 文档与 Applicable Rules 为权威依据；Harness 只是承载这些要求的执行框架，不替代规范事实源。

Human 快速理解流程优先使用 [`overview.md`](overview.md) 与各阶段 README，不以概要替代正式执行规则。

## 1.0.0 稳定门槛

`0.x` 仍属于审核与 Pilot（试运行）阶段。进入 `1.0.0` 前至少完成：

- 静态审核中的重大问题收敛。
- Scenario Stress Test（场景压力测试）。
- Fresh-Agent Blind Run（新 Agent 盲跑）。
- 2–3 个真实项目 Pilot。
- 未发现重大 Trace 逃逸、静默假设或不可解释的人工作业依赖。
