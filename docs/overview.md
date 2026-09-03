# Spec Coding 全流程概要

本文件面向 Human，用于快速理解 Spec Coding 的两条主线：**规范如何被维护并发布为 Harness Package**，以及 **目标项目如何进入正式 Workflow**。

## 总体模型

```text
                 Spec Coding Maintainers
────────────────────────────────────────────────
Canonical Workflow / Rules / Meta Protocol
                    ↓
         Harness Build & Release
                    ↓
        Versioned Harness Package
                    │
════════════════════╪════════════════════════════
                    │
                    ↓
                 Target Project
────────────────────────────────────────────────
Target / Intent
      ↓
Project Onboarding（按需）
      ↓
Adoption Baseline
      ↓
Released Harness Package Adoption / Adaptation
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

当前架构先正式收敛维护者侧 Harness Build & Release；目标侧 Released Package Adoption / Adaptation 将在后续独立协议中定义，不再与维护者构建流程混合。

---

## Harness Build & Release｜维护者构建与发布

维护者只维护 Canonical Source；Harness Package 是可重新生成、可验证、可发布的 Derived Artifact（派生产物）。

```text
1. Build Scope Establishment
   构建范围建立
        ↓
2. Harness Precompile & Assembly
   Harness 预编译与装配
        ↓
3. Package Verification & Review
   包验证与独立审查
        ↓
4. Release & Lifecycle Convergence
   发布与生命周期收敛
```

### 1. Build Scope Establishment｜构建范围建立

识别本轮来自：

- Canonical Change；
- Harness Defect；
- Standard / Packaging Change。

只确定受影响 Source 与需要创建、更新、删除的 Harness Artifact，不在这里重新设计 Canonical 行为。

### 2. Harness Precompile & Assembly｜Harness 预编译与装配

直接消费 Canonical 文档生成标准 Harness 资产。公开标准能完整表达时优先使用公开标准：

```text
Workflow / Procedure → Agent Skills
External Tool / Data → MCP
Portable Bundle      → Agent Plugins
Bootstrap / Routing  → AGENTS.md where supported
```

需要多个机制时直接组合。Runtime-specific Agent、Hook、Gate、Worktree、Model Routing 等不强行伪装成 Portable Standard；它们留给目标侧根据当前 Runtime 适配和增强。

预编译内部可以临时使用 Worklist、Checklist、语义拆解、Fresh Reviewer 等方法，但这些不是发布给使用方的稳定中间产物。

### 3. Package Verification & Review｜包验证与独立审查

至少验证三层：

1. **Structural Verification**：标准格式、引用、路径、Package Metadata、Hash 等结构正确；
2. **Semantic Review**：Canonical Docs ↔ Generated Harness 直接对照，检查遗漏、弱化、越权或新增语义；
3. **Behavioral Test**：用 Fresh Agent 对正常流程、Boundary、Authority / Gate、Exception 等代表性行为做真实消费测试。

验证失败回到最早失真位置，不在验证层偷偷修复。

### 4. Release & Lifecycle Convergence｜发布与生命周期收敛

验证通过后形成当前版本的 Versioned Harness Package，并维护最薄的 Build / Release Manifest：记录版本、Source Trace、Artifact Identity、必要 Capability Requirement 与内容 Hash。

当前阶段优先使用 Spec Coding 仓库统一版本，不提前建立独立的 Component / IR / Compiler 版本森林。

详细规则：[`governance/harness-build-and-release.md`](governance/harness-build-and-release.md)

---

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

Runtime Loader、Model、Tool、Subagent、CI Command、Existing Harness 等动态事实不持久化到 Adoption Baseline；它们属于后续目标侧 Harness Package Adoption / Adaptation。

> **Persist intent, rediscover dynamic environment facts｜持久化意图，动态环境事实按需重发现。**

---

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

---

## Human-Agent Collaboration

Human 不跟踪 Agent 的全部搜索与推理。Agent 先自主发现事实，只有遇到真实意图、Authority 或 Decision Boundary 时，才同步最小充分认知，使 Human 保持 Decision Readiness。

Main Agent 可以按需委派 Scout、Researcher、Worker、Reviewer、Oracle，但继续持有 Workflow State、结果整合与最终责任。具体 Subagent / Model / Thinking / Workspace 由当前 Runtime 动态决定。

---

## 详细入口

- Project Onboarding：[`meta-protocols/project-onboarding.md`](meta-protocols/project-onboarding.md)
- Harness Build & Release：[`governance/harness-build-and-release.md`](governance/harness-build-and-release.md)
- Harness Package：[`../packages/harness/`](../packages/harness/)
- Workflow：[`workflows/`](workflows/)
- Rules：[`rules/`](rules/)
- Runtime / Harness Reference：[`reference/`](reference/)
- Manifest：[`manifest.yaml`](manifest.yaml)
