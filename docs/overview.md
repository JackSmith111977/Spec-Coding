# Spec Coding 全流程概要

本文件面向 Human，用于快速理解 Spec Coding 如何接入项目、编译 Harness，并进入正式 Workflow。

## 总体使用模型

```text
Canonical Corpus
      ↓
Semantic Compile（发布侧）
      ↓
Semantic IR

Target / Intent
      ↓
Project Onboarding（按需）
      ↓
Adoption Baseline
      ↓
Environment Discover
      ↓
Harness Adapt
      ↓
Verify & Accept
      ↓
Harness Ready
      ↓
 ┌───────────────┬────────────────┬────────────────┐
 │ Greenfield    │ Brownfield     │ Existing State │
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
```

## Harness Compilation V3

Harness Compilation 被拆成四个职责明确的阶段：

1. **Semantic Compile｜规范语义编译**：Canonical Docs → Atomic Clauses + Execution Relations；完整性在 Spec Coding 发布侧一次解决。
2. **Environment Discover｜环境认知建立**：根据 Clause 需要发现 Runtime / Project / Existing Harness / Provider Surface 当前事实，形成 Environment Model。
3. **Harness Adapt｜Harness 适配**：Clause → Capability Requirement → Provider → Component → Artifact；最小化只发生在实现层，Candidate Artifact 用内容 Hash 固定身份。
4. **Verify & Accept｜验证与接管**：以 Runtime Visibility、Provider Active、逐 Clause Verification、Mutation 与 Independent Fresh-agent Behavior 证明 Harness 生效，最终只输出 `READY / BLOCKED`。

```text
Semantic IR       → 必须保持什么
Environment Model → 当前能够用什么、还能去哪里找能力
Harness Adapt     → 如何承载这些语义
Verify & Accept   → 真实 Runtime 中是否真的生效
```

Semantic IR 不包含 Vendor-specific Subagent / Model / Thinking / Worktree 策略；Environment Model 也不包含“应该创建 Skill / AGENTS.md”之类设计决策。

Harness Verify & Accept 属于 Meta Protocol 编译验收，不等于 Main Workflow Stage 6 Verification Convergence：前者验证 Harness，后者验证 Requirement / Change Set。

## Project Onboarding｜项目接入

Project Onboarding 只建立长期稳定接入关系：

```text
Declared Intent
+
Target / Spec Workspace / Repository Binding
+
Publication / Authority Constraints
        ↓
Adoption Baseline
```

Runtime Loader、Model、Tool、Subagent、CI Command、Existing Harness 等动态事实不持久化到 Adoption Baseline，由 Environment Discover 按需重新发现。

## Main / Exception Workflow

Main Workflow：

```text
01A / 01B / Resume
        ↓
02 → 03 → 04 → 05 → 06 → 07
```

| 阶段 | 主要职责 |
|---|---|
| 1A 项目定义建立 | 从想法建立项目、业务、系统与需求骨架 |
| 1B 项目认知建立 | 理解存量项目并定位变化 |
| 2 需求澄清 | 收敛意图、范围、规则和 AC |
| 3 技术方案设计 | 分析影响并形成可实施设计 |
| 4 实施规划 | 将设计拆成可执行、可验证 Task |
| 5 开发实施 | 调度、实现、Task Commit、Task Verification 与需求级收敛 |
| 6 验证收敛 | 对完整 Change Set 建立最终 Evidence |
| 7 流程复盘改进 | 用真实证据改进可复用机制 |

无法可靠归因的 Failure / Unexpected Behavior / Unresolved Finding 进入 [`Debug & Defect Resolution`](workflows/exceptions/debug-and-defect-resolution/README.md)，完成 Root Cause / Correction / Failure Closure Evidence 后回到对应 Owner Stage。

## Human-Agent Collaboration

Human 不跟踪 Agent 的全部搜索与推理。Agent 先自主发现事实，只有遇到真实意图、Authority 或 Decision Boundary 时，才同步最小充分认知，使 Human 保持 Decision Readiness。

Main Agent 可以按需委派 Scout、Researcher、Worker、Reviewer、Oracle，但继续持有 Workflow State、结果整合与最终责任。具体 Subagent / Model / Thinking / Workspace 由当前 Runtime 动态决定。

## 使用方法

给 Coding Agent 提供 Spec Coding 与目标项目，然后直接表达目标：

```text
按照 Spec Coding 接入当前项目，并按当前任务继续推进。
```

Agent 自行：

1. 读取 `VERSION`、`manifest.yaml` 与匹配的 Semantic IR；
2. 根据 Project Onboarding 判断 Adoption Baseline 是否可复用；
3. 从 Semantic IR 生成 Discovery Scope；
4. 扫描 Runtime / Provider Surface / Project / Existing Harness 当前证据并形成 Environment Model；
5. 逐 Clause 提取 Capability Requirement，选择可靠 Provider 并生成内容绑定的最小 Harness Candidate；
6. 在真实 Runtime 中完成结构 / Loader / Provider / Clause / Mutation 验证，并由 Independent Fresh Agent 完成五类代表性行为验收；
7. 只有 Acceptance Receipt 为 `READY` 才进入 01A / 01B / Resume；
8. 发现失败时按 `semantic / environment / adaptation / candidate / runtime` 归因并回到最早失真事实源。

## 详细入口

- Project Onboarding：[`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)
- Harness Compilation：[`meta-protocols/harness-compilation.md`](meta-protocols/harness-compilation.md)
- Semantic Compilation：[`governance/semantic-compilation.md`](governance/semantic-compilation.md)
- Semantic Compiler：[`../tools/semantic_compiler/`](../tools/semantic_compiler/)
- Environment Discovery：[`../tools/environment_discovery/`](../tools/environment_discovery/)
- Harness Adapt：[`../tools/harness_adapt/`](../tools/harness_adapt/)
- Harness Acceptance：[`../tools/harness_acceptance/`](../tools/harness_acceptance/)
- Workflow：[`workflows/`](workflows/)
- Rules：[`rules/`](rules/)
- Runtime / Harness Reference：[`reference/`](reference/)
- Manifest：[`manifest.yaml`](manifest.yaml)
