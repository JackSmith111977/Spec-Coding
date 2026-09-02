# Spec Coding 文档索引

Spec Coding 文档按职责分为：**Workflows（流程）**、**Rules（规则）**、**Meta Protocols（元协议）**、**Governance（治理）** 与 **Reference（参考）**。机器可读 Canonical 清单以 [`manifest.yaml`](manifest.yaml) 为唯一入口。

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 持续适用规则
├── meta-protocols/  # 项目接入与 Harness 编译
├── governance/      # 仓库、版本与 Semantic Compilation 治理
├── reference/       # 术语、Harness Primitive、Runtime 参考
├── overview.md
└── manifest.yaml
```

## V3 Harness Compilation

```text
Canonical Corpus
      ↓
Semantic Compile
      ↓
Semantic IR
      ↓
Project Onboarding → Adoption Baseline
      ↓
Environment Discover
      ↓
Harness Adapt
      ↓
Verify & Accept
```

- [`governance/semantic-compilation.md`](governance/semantic-compilation.md)：规范侧 Semantic IR 生成与发布治理；
- [`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)：长期接入意图与稳定绑定；
- [`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)：目标侧 Environment Discover、Harness Adapt、Verify & Accept；
- [`../tools/semantic_compiler/`](../tools/semantic_compiler/)：Semantic Compilation 确定性支持工具；
- [`../tools/environment_discovery/`](../tools/environment_discovery/)：Environment Discovery 确定性支持工具。

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

- [`meta-protocols/README.md`](meta-protocols/README.md)
- [`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)
- [`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)

## Governance｜治理

- [`governance/repository-governance.md`](governance/repository-governance.md)
- [`governance/semantic-compilation.md`](governance/semantic-compilation.md)

## Reference｜参考

Reference 是非规范知识层：

- [`reference/glossary.md`](reference/glossary.md)
- [`reference/harness-primitives.md`](reference/harness-primitives.md)
- [`reference/coding-agent-runtimes.md`](reference/coding-agent-runtimes.md)

Current Runtime Capability 始终由当前 Local / Official Evidence 决定。

## Canonical Corpus｜规范文档集

当前 `manifest.yaml` 登记：34 份 Canonical Stage Documents、4 份 Canonical Rule Documents、4 份 Canonical Exception Workflow Documents、2 份 Canonical Meta Protocol Documents。Governance、Reference、README 与 Overview 不计入 Canonical Corpus。
