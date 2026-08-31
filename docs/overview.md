# Spec Coding 全流程概要

本文件面向 Human（人类），用于快速理解 Spec Coding 如何接入项目、当前任务处于哪里、下一步要做什么。详细执行要求由当前 Workflow（流程）与 Applicable Rules（适用规则）共同定义；Spec Coding 的项目接入与执行机制转换由 Applicable Meta Protocol（适用元协议）负责。

## 总体使用模型

```text
Target / Intent
      ↓
Project Onboarding（按需）
      ↓
Adoption Baseline
      ↓
Harness Compilation（按需）
      ↓
Harness Ready
      ↓
 ┌───────────────┬────────────────┬───────────────┐
 │ Greenfield    │ Brownfield     │ Existing State│
 ↓               ↓                ↓
项目定义建立      项目认知建立       Resume Owner Stage
 └───────┬───────┴────────────────┘
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
 Evolved Workflow / Rules / Meta Protocol / Harness
```

Project Onboarding 不作为 Stage 0：它只建立 Spec Coding 与当前 Target 的接入关系。已有 Adoption Baseline 仍有效时直接复用；Harness 仍满足当前 Workflow / Rules / Adoption 约束时同样直接复用。

## Meta Protocol Flow｜元协议链

```text
Project Onboarding
  ↓
Adoption Baseline
  ↓
Harness Compilation
  ↓
Harness Ready
```

- [`Project Onboarding Protocol`](meta-protocols/project-onboarding.md)：识别 Target 与 Existing Adoption，建立 Usage Contract，对齐 Relevant Delta，最终形成有效 Adoption Baseline 与 Workflow Route。
- [`Harness Compilation Protocol`](meta-protocols/harness-compilation.md)：消费 Adoption Baseline、Applicable Workflow / Rules 与当前 Target Environment，复用已有能力并只补真实缺口；需要 Agent 委派时先发现当前 Runtime 的有效能力，再动态编译 Role、Model、Thinking、Context、Tools 与 Workspace。

当 Adoption 或 Harness 已经有效时对应步骤直接 Reuse，不为每个 Requirement / Task 增加初始化开销。

## Main / Exception Workflow

Main Workflow（主流程）描述正常推进路径：

```text
01A / 01B / Resume
        ↓
02 → 03 → 04 → 05 → 06 → 07
```

任一阶段出现无法可靠归因的 Failure（故障）、Unexpected Behavior（异常行为）或需要进一步诊断的 Unresolved Finding（未决验证发现）时，可按需进入 Exception Workflow（异常流程）：

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

Human 不需要跟踪 Agent 的全部搜索、推理和 Task 级执行。正式 Workflow，以及 Project Onboarding 等涉及 Human 意图、权限或关键判断的 Meta Protocol Interaction，适用 [`Human-Agent Collaboration Rules`](rules/human-agent-collaboration.md)。

核心原则是：**Agent 先发现事实并保持契约内自治；Human 只在真实意图 / 决策边界保持 Decision Readiness（决策就绪）。** 已有上下文仍有效时只同步关键 Delta，不重复重放整个项目；Human 的有效反馈应更新对应 Canonical Source of Truth，例如 Adoption Intent 更新 Adoption Baseline，Requirement / Design 语义更新相应 Workflow Artifact。

## Agent Delegation & Coordination｜Agent 委派与协调

当上下文隔离、并行、独立审查、专门能力或决策一致性检查有真实收益时，Main Agent 可按 [`Agent Delegation & Coordination Rules`](rules/agent-delegation-and-coordination.md) 动态委派 Scout、Researcher、Worker、Reviewer 或 Oracle。

```text
Human
  ↕
Main Agent
  ├─ Scout / Researcher
  ├─ Worker
  ├─ Reviewer
  └─ Oracle
       ↓
Result / Evidence
       ↓
Main Agent → Canonical State
```

Main Agent 始终保留 Workflow State、跨 Agent 协调、结果整合与最终责任；Subagent 只在有界 Contract 内自治。Formal Task 继续使用既有 Task Contract + Execution Unit；Agent、Model、Thinking、Fresh / Fork、Workspace 与并行策略均由 Harness 根据当前 Runtime 动态推导，不进入 `tasks.md` 等长期事实源。

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
| 7 流程复盘改进 | 用真实证据改进可复用 Workflow / Rules / Meta Protocol / Harness | [查看](workflows/main/07-process-review-improvement/README.md) |

### Exception Workflow｜异常流程

| 流程 | 主要做什么 | 概要 |
|---|---|---|
| Debug & Defect Resolution | 从异常接管、证据定位、根因确认到修复验证与流程回接 | [查看](workflows/exceptions/debug-and-defect-resolution/README.md) |

## 使用方法

给 Coding Agent 提供 **Spec Coding** 与目标项目 / Intent，然后直接表达目标，例如：

```text
按照 Spec Coding 接入当前项目，并按当前任务继续推进。
```

Agent 应自行：

1. 读取 `VERSION` 与 [`manifest.yaml`](manifest.yaml)。
2. 根据 [`Project Onboarding Protocol`](meta-protocols/project-onboarding.md) 判断 Adoption Baseline 是否可复用；不存在或失效时执行 Initialize / Refresh / Migrate。
3. 解析最终 Workflow Route 与 Applicable Rules。
4. 根据 [`Harness Compilation Protocol`](meta-protocols/harness-compilation.md) Reuse / Compile 最小充分 Harness。
5. Harness 达到 `Ready` 后进入 01A / 01B 或 Resume 当前 Owner Stage；之后按正式 Workflow 与 Rules 推进。
6. 若发现上游事实失效，回到最早失效事实源纠正，只重新对齐受影响链路。

Human 不需要手工依次执行 `Onboard Project`、`Build Harness` 等命令；Meta Protocol 的路由由 Agent 根据当前状态内部完成。

## 详细规则

- Workflow 清单：[`workflows/`](workflows/)
- Rules 清单：[`rules/`](rules/)
- Meta Protocols：[`meta-protocols/`](meta-protocols/)
- Project Onboarding：[`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)
- Harness 编译协议：[`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)
- Human-Agent Collaboration Rules：[`rules/human-agent-collaboration.md`](rules/human-agent-collaboration.md)
- Agent Delegation & Coordination Rules：[`rules/agent-delegation-and-coordination.md`](rules/agent-delegation-and-coordination.md)
- Exception Workflow：[`workflows/exceptions/README.md`](workflows/exceptions/README.md)
- 全局执行规则：[`rules/global-contracts.md`](rules/global-contracts.md)
- Code Quality Rules：[`rules/code-quality.md`](rules/code-quality.md)
- 规范术语：[`reference/glossary.md`](reference/glossary.md)
- 仓库治理：[`governance/repository-governance.md`](governance/repository-governance.md)
- 机器入口：[`manifest.yaml`](manifest.yaml)
