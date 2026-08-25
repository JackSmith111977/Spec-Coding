# Spec Coding

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）是一套面向 AI Coding 的轻量、可追溯开发流程。

它覆盖从项目认知 / 定义、需求澄清、技术设计、实施规划、开发实施，到验证收敛与流程改进的完整链路；同时通过统一 Harness Compilation Protocol（Harness 编译协议），将流程要求转换为当前项目的最小充分 Harness（执行框架）。

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
2. 让 Agent 执行 `Build Harness`。
3. Agent 按 [`docs/harness-compilation-protocol.md`](docs/harness-compilation-protocol.md) 完成 `Read → Derive → Compose → Verify`：先取得 Spec Coding 与目标项目的本地一致视图，再识别真实缺口并生成最小充分 Harness。
4. Harness 达到 `Ready` 后，Agent 按当前阶段正式文档与全局契约推进任务。

## Harness 构建入口

```text
Build Harness
```

这是一条简化的语义入口，不要求特定 CLI。Agent 应自行完成协议规定的读取、推导、组合与验证，不把转换步骤转嫁给 Human。

## 文档入口

- [`docs/overview.md`](docs/overview.md)：全流程概要与阶段入口，主要给 Human 查看。
- [`docs/harness-compilation-protocol.md`](docs/harness-compilation-protocol.md)：将 Spec Coding 稳定转换为最小充分 Harness 的跨阶段协议。
- [`docs/README.md`](docs/README.md)：全部文档索引。
- [`docs/global-contracts.md`](docs/global-contracts.md)：所有阶段共同继承的全局执行契约。
- [`docs/glossary.md`](docs/glossary.md)：规范术语与统一中文解释。
- [`docs/repository-governance.md`](docs/repository-governance.md)：仓库维护与版本管理规则。
- [`docs/manifest.yaml`](docs/manifest.yaml)：机器可读的正式阶段文档清单与导航。
- [`CHANGELOG.md`](CHANGELOG.md)：版本变化记录。
