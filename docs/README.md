# Spec Coding 文档索引

Spec Coding 文档按职责分为：**Workflows（流程）**、**Rules（规则）**、**Meta Protocols（元协议）**、**Governance（治理）** 与 **Reference（参考）**。机器可读 Canonical 清单以 [`manifest.yaml`](manifest.yaml) 为唯一入口。

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 持续适用规则
├── meta-protocols/  # 目标项目接入协议
├── governance/      # 仓库、版本、Harness Build & Release 治理
├── reference/       # 术语、Harness Primitive、公开标准、Runtime 参考
├── overview.md
└── manifest.yaml
```

仓库级派生发行入口：

```text
packages/harness/    # 当前版本的可发布 Harness Package 入口
```

## Harness Build & Release｜Harness 构建与发布

维护者不再发布 Semantic IR，也不要求使用方 Coding Agent 重新从 Canonical 文档编译 Harness。

正式维护流程：

```text
Canonical Docs
      ↓
Build Scope Establishment
      ↓
Harness Precompile & Assembly
      ↓
Package Verification & Review
      ↓
Release & Lifecycle Convergence
      ↓
Versioned Harness Package
```

- [`governance/harness-build-and-release.md`](governance/harness-build-and-release.md)：维护者如何创建、更新、验证、发布和移除 Harness 资产；
- [`../packages/harness/`](../packages/harness/)：当前 Harness Package 的发行入口；
- [`reference/harness-standards.md`](reference/harness-standards.md)：Agent Skills、Agent Plugins、MCP、AGENTS.md 等公开标准采用基线。

Build Internals 可以临时使用 Checklist、Worklist、语义拆解、Fresh Review 等方法，但不形成面向使用方的正式中间架构层。

## Workflows｜流程

Main Workflow：

```text
01A / 01B → 02 → 03 → 04 → 05 → 06 → 07
```

- [`workflows/main/01a-project-definition/`](workflows/main/01a-project-definition/)：项目定义建立；
- [`workflows/main/01b-project-understanding/`](workflows/main/01b-project-understanding/)：项目认知建立；
- [`workflows/main/02-requirement-clarification/`](workflows/main/02-requirement-clarification/)：需求澄清；
- [`workflows/main/03-technical-design/`](workflows/main/03-technical-design/)：技术方案设计；
- [`workflows/main/04-implementation-planning/`](workflows/main/04-implementation-planning/)：实施规划；
- [`workflows/main/05-development-execution/`](workflows/main/05-development-execution/)：开发实施；
- [`workflows/main/06-verification-convergence/`](workflows/main/06-verification-convergence/)：验证收敛；
- [`workflows/main/07-process-review-improvement/`](workflows/main/07-process-review-improvement/)：流程复盘改进。

Exception Workflow：[`workflows/exceptions/`](workflows/exceptions/)。

## Rules｜规则

- [`rules/global-contracts.md`](rules/global-contracts.md)
- [`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md)
- [`rules/agent-delegation-and-coordination.md`](rules/agent-delegation-and-coordination.md)
- [`rules/code-quality.md`](rules/code-quality.md)

Rules 不推进阶段状态；正式消费者引用规则语义，不复制规则正文。

## Meta Protocols｜元协议

当前目标项目侧正式 Meta Protocol：

- [`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)：建立、复用、刷新或迁移 Adoption Baseline。

Harness 的维护者构建 / 发布属于 Governance，不再作为目标项目 Coding Agent 的 Meta Protocol。Released Package 的目标侧 Environment Adaptation 将作为后续独立协议设计。

## Governance｜治理

- [`governance/repository-governance.md`](governance/repository-governance.md)
- [`governance/harness-build-and-release.md`](governance/harness-build-and-release.md)

## Reference｜参考

Reference 是非规范知识层；统一入口见 [`reference/README.md`](reference/README.md)：

- [`reference/glossary.md`](reference/glossary.md)：术语与规范中文解释；
- [`reference/harness-primitives.md`](reference/harness-primitives.md)：跨 Runtime Harness 抽象能力；
- [`reference/harness-standards.md`](reference/harness-standards.md)：公开协议 / 开放格式、Portable / Runtime-native 边界、官方 Source 与 Freshness；
- [`reference/coding-agent-runtimes.md`](reference/coding-agent-runtimes.md)：Runtime Architecture Invariant 与官方事实入口。

## Canonical Corpus｜规范文档集

当前 `manifest.yaml` 登记：34 份 Canonical Stage Documents、4 份 Canonical Rule Documents、4 份 Canonical Exception Workflow Documents、1 份 Canonical Meta Protocol Document。

Governance、Reference、README、Overview 与发布后的 Harness Package 不计入 Canonical Corpus。Canonical Markdown 仍是规范 Source of Truth；Harness Package 是从其派生并经过发布验证的执行资产。
