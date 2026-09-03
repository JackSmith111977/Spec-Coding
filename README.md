# Spec Coding

> **AI can write code. Spec Coding keeps it aligned.**

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）是一套面向 AI Coding 的轻量、可追溯开发方法。

它把模糊意图逐步收敛为：

```text
Requirement → Design → Task → Change → Verification
```

并通过可复用 Workflow、Rules 与 Harness 让 Coding Agent 在不同项目和 Runtime 中保持相同的核心行为。

**Version:** [`0.11.0`](VERSION) · **Status:** `candidate`

---

## Why Spec Coding?

Spec Coding 关注的不是“怎样让 Agent 多写代码”，而是：

- **Alignment｜对齐**：需求、设计、任务与实现持续指向同一目标；
- **Traceability｜可追溯**：结果可回查到 Requirement、Design、Task 与 Evidence；
- **Bounded Autonomy｜有边界的自治**：Agent 在契约内推进，越界时回到正确上游；
- **Human-Agent Collaboration｜人机协作**：Human 只在关键认知与决策边界保持 Decision Readiness；
- **Agent Delegation｜Agent 委派**：Main Agent 保留全局一致性，Subagent 只承担有界、可验证工作；
- **Verification｜验证**：用证据证明结果，而不是接受 Agent 自我声明；
- **Portable Harness｜可移植 Harness**：稳定流程由维护者预编译和发布，目标项目只处理当前环境差异。

---

## Harness Distribution｜Harness 分发模型

Spec Coding 不再要求每个使用方 Coding Agent 从完整 Canonical 文档重新编译 Harness。

仓库维护者负责：

```text
Canonical Workflow / Rules / Meta Protocol
                 ↓
      Harness Build & Release
                 ↓
      Versioned Harness Package
```

维护者侧正式流程：

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

核心原则：

> **Canonical defines behavior; maintainers build and verify the reusable Harness; users only adapt what depends on the current environment.**
>
> **Canonical 定义行为；维护者构建并验证可复用 Harness；使用方只处理当前环境才能确定的差异。**

完整维护协议：[`docs/governance/harness-build-and-release.md`](docs/governance/harness-build-and-release.md)

当前发行入口：[`packages/harness/`](packages/harness/)

---

## Build once, adapt where necessary

预编译优先使用公开标准与开放格式：

```text
Workflow / Procedure → Agent Skills
External Tool / Data → MCP
Portable Bundle      → Agent Plugins
Bootstrap / Routing  → AGENTS.md where supported
Runtime-native only  → target-side adaptation
```

复杂能力需要多个 Harness Mechanism 时直接组合，不再为组合本身创造额外 Component Protocol。

构建过程中可以临时使用 Worklist、Checklist、语义拆解、Fresh Reviewer 或 Mutation Challenge，但这些属于维护者的 Build Internals（构建内部实现），不作为面向使用方发布的正式中间层。

---

## Use it with your coding agent

Human 仍然只需要表达自然语言目标，例如：

```text
按照 Spec Coding 接入当前项目，并按当前任务继续推进。
```

Project Onboarding 只建立长期使用意图与稳定绑定。Released Harness Package 如何根据当前 Runtime 做 Environment Discovery、Adaptation 与 Enhancement，将在独立的目标侧接入协议中定义；它不再与维护者侧 Harness Build 混在同一条流程中。

> **Persist intent, rediscover dynamic environment facts｜持久化意图，动态环境事实按需重发现。**

---

## Workflow

Spec Coding 同时支持 Greenfield（新项目）、Brownfield（存量项目）与 Existing State Resume：

```text
新项目：项目定义建立 ─┐
存量项目：项目认知建立 ┼→ 需求澄清 → 技术方案设计 → 实施规划 → 开发实施 → 验证收敛 → 流程复盘改进
已有状态：Resume ─────┘
```

异常不强行塞进 Happy Path：无法可靠归因的 Failure / Defect 由 [`Debug & Defect Resolution`](docs/workflows/exceptions/debug-and-defect-resolution/README.md) 接管，完成后回到最早有效 Owner Stage。

---

## Principles

> **Process for cognition. Artifacts for alignment. Evidence for trust.**

- Process as Cognition｜流程用于认知；
- Artifact as Contract｜产物用于对齐；
- Evidence over Claim｜证据优于声明；
- Decision-ready Human｜Human 保持可判断；
- Delegate Work, Not Accountability｜委派工作，不转移责任；
- Affected Trace Only｜只处理受影响链路；
- Reuse before Add｜复用优先；
- Standards First｜公开标准优先；
- Build Once, Adapt Locally｜稳定部分一次构建，环境差异本地适配。

---

## Explore

| 我想…… | 从这里开始 |
|---|---|
| 快速理解完整流程 | [`docs/overview.md`](docs/overview.md) |
| 查看机器可读规范入口 | [`docs/manifest.yaml`](docs/manifest.yaml) |
| 接入目标项目 | [`docs/meta-protocols/project-onboarding.md`](docs/meta-protocols/project-onboarding.md) |
| 维护 / 发布 Harness | [`docs/governance/harness-build-and-release.md`](docs/governance/harness-build-and-release.md) |
| 查看当前 Harness Package 入口 | [`packages/harness/`](packages/harness/) |
| 查看 Workflow | [`docs/workflows/`](docs/workflows/) |
| 查看 Rules | [`docs/rules/`](docs/rules/) |
| 查看 Runtime / Harness Reference | [`docs/reference/`](docs/reference/) |
| 维护 Spec Coding | [`docs/governance/`](docs/governance/) |

---

## Project status

当前仍处于 `candidate` 阶段。本分支正在把旧的 Semantic IR / V3 target-side compilation 架构替换为维护者预编译、版本化 Harness Package 的分发模型。维护者侧 Build & Release 流程先完成收敛，目标侧 Package Adoption / Adaptation 协议随后独立设计。

## License

除非另有说明，本仓库的文档、规范、图示及其他非软件内容采用 [Creative Commons Attribution 4.0 International](LICENSE)（CC BY 4.0）许可。
