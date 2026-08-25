# Spec Coding 全流程概要

本文件面向 Human（人类），用于快速判断当前任务处于哪里、下一步要做什么。详细执行规则以各阶段正式文档为准。

## 全流程

```text
Initial Context
      ↓
 ┌───────────────┬────────────────┐
 │ Greenfield    │ Brownfield     │
 │ 新项目         │ 存量项目        │
 ↓               ↓
项目定义建立      项目认知建立
 └───────┬───────┘
         ↓
      需求澄清
         ↓
    技术方案设计
         ↓
      实施规划
         ↓
      开发实施
         ↓
      验证收敛
         ↓
    流程复盘改进
         ↓
 Evolved Harness / Rules
```

## 阶段一览

| 阶段 | 主要做什么 | 概要 |
|---|---|---|
| 1A 项目定义建立 | 从想法建立项目、业务、系统与需求骨架 | [查看](01a-project-definition/README.md) |
| 1B 项目认知建立 | 理解存量项目，并定位本次变化 | [查看](01b-project-understanding/README.md) |
| 2 需求澄清 | 明确需求意图、范围、规则和验收标准 | [查看](02-requirement-clarification/README.md) |
| 3 技术方案设计 | 分析影响、完成技术决策并形成可实施设计 | [查看](03-technical-design/README.md) |
| 4 实施规划 | 将设计拆成可执行、可验证的 Task | [查看](04-implementation-planning/README.md) |
| 5 开发实施 | 调度 Task，完成实现、Task Commit 与需求级收敛 | [查看](05-development-execution/README.md) |
| 6 验证收敛 | 对完整变更建立最终证据并收敛到 Verified / Blocked | [查看](06-verification-convergence/README.md) |
| 7 流程复盘改进 | 用真实证据改进可复用 SDD / Harness 规则 | [查看](07-process-review-improvement/README.md) |

## 使用方法

1. 先通过本页判断当前任务所处阶段。
2. 让 Agent 执行 `Build Harness`。
3. Agent 按 [`harness-compilation-protocol.md`](harness-compilation-protocol.md) 完成 `Read → Derive → Compose → Verify`，以本地仓库为主要事实源，复用已有能力并只补真实缺口。
4. Harness 达到 `Ready` 后，按当前阶段正式文档推进；若执行中发现上游事实失效，回到最早失效位置纠正，只重新对齐受影响链路。

## Harness 构建入口

```text
Build Harness
```

该入口不要求 Human 手工拆解 Harness。Agent 负责读取有效规范与目标项目、推导需求、组合最小充分 Harness，并验证覆盖、语义忠实、最小性与可执行性。

## 详细规则

- Harness 编译协议：[`harness-compilation-protocol.md`](harness-compilation-protocol.md)
- 正式文档清单：[`manifest.yaml`](manifest.yaml)
- 全局执行契约：[`global-contracts.md`](global-contracts.md)
- 规范术语：[`glossary.md`](glossary.md)
