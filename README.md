# Spec Coding

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）是一套面向 AI Coding 的轻量、可追溯开发流程。

它覆盖从项目认知 / 定义、需求澄清、技术设计、实施规划、开发实施，到验证收敛与流程改进的完整链路；同时允许 Agent 根据任务风险和自身能力动态建立最小充分 Harness（执行框架）。

当前版本见 [`VERSION`](VERSION)，当前正式流程由 [`docs/manifest.yaml`](docs/manifest.yaml) 定义。

## 全流程

```text
新项目：项目定义建立 ─┐
                    ├→ 需求澄清 → 技术方案设计 → 实施规划 → 开发实施 → 验证收敛 → 流程复盘改进
存量项目：项目认知建立 ─┘
```

面向 Human（人类）建议先阅读：[`docs/overview.md`](docs/overview.md)。

## 使用方法

1. Human 先通过全流程概要判断当前大致处于哪个阶段。
2. 将下面的必读 Prompt 交给 Agent。
3. Agent 阅读完整流程与当前阶段正式规则，判断目标、输入、输出和完成条件。
4. Agent 按需建立最小充分 Harness，并依据执行反馈动态调整。

## 必读万能 Prompt

> **先阅读并理解完整的 Spec Coding 流程，判断当前任务所处阶段，以及该阶段的目标、输入、输出和完成条件。**
>
> **基于当前 Agent 的原生能力、项目环境和已有上下文，识别完成当前阶段所缺少的能力，并按需选择或建立最小充分 Harness，包括 Rules、Skills、Tools、Subagents、Checklists 等；已有能力足够时不要额外增加 Harness。**
>
> **执行过程中根据新发现的能力缺口动态调整 Harness，始终以流程目标和验证结果为准，避免过度设计。**

## 文档入口

- [`docs/overview.md`](docs/overview.md)：全流程概要与阶段入口，主要给 Human 查看。
- [`docs/README.md`](docs/README.md)：全部文档索引。
- [`docs/global-contracts.md`](docs/global-contracts.md)：所有阶段共同继承的全局执行契约。
- [`docs/glossary.md`](docs/glossary.md)：规范术语与统一中文解释。
- [`docs/repository-governance.md`](docs/repository-governance.md)：仓库维护与版本管理规则。
- [`docs/manifest.yaml`](docs/manifest.yaml)：机器可读的正式阶段文档清单。
- [`CHANGELOG.md`](CHANGELOG.md)：版本变化记录。
