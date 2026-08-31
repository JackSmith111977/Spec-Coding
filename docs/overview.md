# Spec Coding 全流程概要

本文件面向 Human（人类），用于快速判断当前任务处于哪里、下一步要做什么。详细执行要求由当前 Workflow（流程）与 Applicable Rules（适用规则）共同定义；Spec Coding 如何接入和转换为项目执行机制，由 Applicable Meta Protocol（适用元协议）负责。

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
 Evolved Workflow / Rules / Harness
```

Main Workflow（主流程）描述正常推进路径。任一阶段出现无法可靠归因的 Failure（故障）、Unexpected Behavior（异常行为）或需要进一步诊断的 Unresolved Finding（未决验证发现）时，可按需进入 Exception Workflow（异常流程）：

```text
Any Main-flow Stage
        ↓
Failure / Unresolved Finding
        ↓
Debug & Defect Resolution
        ↓
Correction / Failure Closure Evidence
        ↓
Owner Stage
        ↓
Main Workflow Continues
```

Exception Workflow 不作为新的主流程阶段，也不维护主流程权威状态副本。

## Human-Agent Collaboration｜人机协作

Human 不需要跟踪 Agent 的全部搜索、推理和 Task 级执行。所有正式 Workflow 适用 [`Human-Agent Collaboration Rules`](rules/human-agent-collaboration.md)，但交互由事件触发：当重要共享模型建立或变化、即将进入 Human 决策边界、权限需要升级、既有共享模型被证据推翻，或重要 Requirement / Design / Verification 等完成收敛时，Agent 才同步 Human 判断所需的最小认知。

核心原则是：**Agent 保持契约内自治；Human 在真正需要介入时保持 Decision Readiness（决策就绪）。** 已有上下文仍有效时只同步关键 Delta，不重复重放整个项目；Human 的有效反馈应更新对应 Canonical Source of Truth，而不是只停留在会话里。

## 阶段一览

| 阶段 | 主要做什么 | 概要 |
|---|---|---|
| 1A 项目定义建立 | 从想法建立项目、业务、系统与需求骨架 | [查看](workflows/main/01a-project-definition/README.md) |
| 1B 项目认知建立 | 理解存量项目，并定位本次变化 | [查看](workflows/main/01b-project-understanding/README.md) |
| 2 需求澄清 | 明确需求意图、范围、规则和验收标准 | [查看](workflows/main/02-requirement-clarification/README.md) |
| 3 技术方案设计 | 分析影响、完成技术决策并形成可实施设计 | [查看](workflows/main/03-technical-design/README.md) |
| 4 实施规划 | 将设计拆成可执行、可验证的 Task | [查看](workflows/main/04-implementation-planning/README.md) |
| 5 开发实施 | 调度 Task，完成实现、Task Commit 与需求级收敛 | [查看](workflows/main/05-development-execution/README.md) |
| 6 验证收敛 | 对完整变更建立最终证据并收敛到 Verified / Blocked | [查看](workflows/main/06-verification-convergence/README.md) |
| 7 流程复盘改进 | 用真实证据改进可复用 Workflow / Rules / Harness | [查看](workflows/main/07-process-review-improvement/README.md) |

### Exception Workflow｜异常流程

| 流程 | 主要做什么 | 概要 |
|---|---|---|
| Debug & Defect Resolution | 从异常接管、证据定位、根因确认到修复验证与流程回接 | [查看](workflows/exceptions/debug-and-defect-resolution/README.md) |

## 使用方法

1. 先通过本页判断当前任务所处阶段；若存在异常，再判断是否触发 Exception Workflow。
2. 让 Agent 执行 `Build Harness`。
3. Agent 按 [`Harness Compilation Protocol`](meta-protocols/harness-compilation.md) 完成 `Read → Derive → Compose → Verify`，以本地仓库为主要事实源，读取当前 Main Workflow、Triggered Exception Workflow（若有）与 Applicable Rules，复用已有能力并只补真实缺口。
4. Harness 达到 `Ready` 后，按当前 Workflow 与适用规则推进；Human-Agent Collaboration 按 Trigger 发生，不为普通 Autonomous 工作增加人工审批；若发现上游事实失效，回到最早失效位置纠正，只重新对齐受影响链路。

## Meta Protocol 与 Harness

当前正式 Harness 构建入口仍为：

```text
Build Harness
```

该入口由 `harness-compilation` Meta Protocol 承接。Meta Protocol 定义如何读取与转换 Spec Coding，Harness 则是最终在目标项目中生成或复用的执行机制；两者都不替代 Workflow / Rules 的规范事实源。

## 详细规则

- Workflow 清单：[`workflows/`](workflows/)
- Rules 清单：[`rules/`](rules/)
- Meta Protocols：[`meta-protocols/`](meta-protocols/)
- Human-Agent Collaboration Rules：[`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md)
- Exception Workflow：[`workflows/exceptions/README.md`](workflows/exceptions/README.md)
- Harness 编译协议：[`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)
- 全局执行规则：[`rules/global-contracts.md`](rules/global-contracts.md)
- Code Quality Rules：[`rules/code-quality.md`](rules/code-quality.md)
- 规范术语：[`reference/glossary.md`](reference/glossary.md)
- 仓库治理：[`governance/repository-governance.md`](governance/repository-governance.md)
- 机器入口：[`manifest.yaml`](manifest.yaml)
