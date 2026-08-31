# Spec Coding 文档索引

Spec Coding 的规范按职责分为五个目录层：**Workflows（流程）**、**Rules（规则）**、**Meta Protocols（元协议）**、**Governance（治理）** 与 **Reference（参考）**。目录负责表达规范身份，机器可读 Canonical 清单仍以 [`manifest.yaml`](manifest.yaml) 为唯一入口。

```text
docs/
├── workflows/       # Main / Exception Workflow
├── rules/           # 跨阶段持续规则
├── meta-protocols/  # 项目接入、装配与转换协议
├── governance/      # 仓库与版本治理
├── reference/       # 术语等参考资料
├── README.md        # Human 文档导航
├── overview.md      # Human 全流程概要
└── manifest.yaml    # Machine Entry Point
```

## Human 概要

- [`overview.md`](overview.md)：全流程概要、使用方法与阶段入口。
- [`workflows/README.md`](workflows/README.md)：Main / Exception Workflow 总入口。
- [`workflows/main/01a-project-definition/README.md`](workflows/main/01a-project-definition/README.md)：项目定义建立（新项目）。
- [`workflows/main/01b-project-understanding/README.md`](workflows/main/01b-project-understanding/README.md)：项目认知建立（存量项目）。
- [`workflows/main/02-requirement-clarification/README.md`](workflows/main/02-requirement-clarification/README.md)：需求澄清。
- [`workflows/main/03-technical-design/README.md`](workflows/main/03-technical-design/README.md)：技术方案设计。
- [`workflows/main/04-implementation-planning/README.md`](workflows/main/04-implementation-planning/README.md)：实施规划。
- [`workflows/main/05-development-execution/README.md`](workflows/main/05-development-execution/README.md)：开发实施。
- [`workflows/main/06-verification-convergence/README.md`](workflows/main/06-verification-convergence/README.md)：验证收敛。
- [`workflows/main/07-process-review-improvement/README.md`](workflows/main/07-process-review-improvement/README.md)：流程复盘改进。
- [`workflows/exceptions/README.md`](workflows/exceptions/README.md)：跨阶段异常流程入口。

这些 README 用于快速理解与导航，不替代正式 Canonical Document。

## Workflows｜流程

### Main Workflow｜主流程

正式阶段文档集合以 [`manifest.yaml`](manifest.yaml) 的 `stages.documents` 为唯一清单。Agent 执行流程时读取当前适用阶段文档，而不是仅依赖概要。

```text
01A / 01B → 02 → 03 → 04 → 05 → 06 → 07
```

### Exception Workflows｜异常流程

正式异常流程以 [`manifest.yaml`](manifest.yaml) 的 `exception_workflows` 为机器可读入口，只在对应 Trigger 成立时加载。

- [`Debug & Defect Resolution`](workflows/exceptions/debug-and-defect-resolution/README.md)：从异常接管与复现，经证据定位、根因确认与纠正路由，到修复验证和 Failure Closure，再将可信结论回交 Owner Stage。

Exception Workflow 不作为 Main Workflow 的新增阶段，也不维护 Task、Finding、Open Item 或 Verification 的并行状态事实源。

## Rules｜规则

正式跨阶段规则以 [`manifest.yaml`](manifest.yaml) 的 `rule_documents` 为机器可读入口，按当前阶段与任务加载适用规则。

- [`rules/global-contracts.md`](rules/global-contracts.md)：所有正式 Workflow 默认继承的 Global Contracts（全局执行契约）。
- [`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md)：Human-Agent Collaboration Rules（人机协作规则）。
- [`rules/code-quality.md`](rules/code-quality.md)：Code Quality Rules（代码质量规则）。

Rules 本身不推进阶段状态；Workflow 文档通过引用消费规则，不复制规则正文。

## Meta Protocols｜元协议

Meta Protocol 定义 Spec Coding 如何被项目接入、解释、装配或转换为可执行机制，本身不作为 Main / Exception Workflow 阶段。

- [`meta-protocols/README.md`](meta-protocols/README.md)：Meta Protocol 导航。
- [`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)：Harness Compilation Protocol，将 Applicable Workflow + Rules 转换为当前项目最小充分 Harness。

当前正式 Meta Protocol 以 [`manifest.yaml`](manifest.yaml) 的 `meta_protocols` 为机器可读入口。未来协议在完成正式设计后再登记，不维护空占位事实源。

## Governance｜治理

- [`governance/repository-governance.md`](governance/repository-governance.md)：Canonical、目录职责、仓库维护与版本管理。

## Reference｜参考

- [`reference/glossary.md`](reference/glossary.md)：规范术语及中文解释。

## Canonical Corpus｜规范文档集

当前版本包含：

- 34 份 Canonical Stage Documents。
- 3 份 Canonical Rule Documents。
- 4 份 Canonical Exception Workflow Documents。
- 1 份 Canonical Meta Protocol Document。

历史版本由 Git 保存，不在当前文档目录维护并行旧副本。
