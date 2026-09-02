# Spec Coding

> **AI can write code. Spec Coding keeps it aligned.**

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）是一套面向 AI Coding 的轻量、可追溯开发方法。

它把模糊意图逐步收敛为：

```text
Requirement → Design → Task → Change → Verification
```

并通过可复用 Workflow、Rules 与 Harness 让 Coding Agent 在不同项目和 Runtime 中保持相同的核心语义。

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
- **Adaptation｜适配**：规范稳定，Harness 根据当前项目和 Runtime 动态适配。

---

## Harness Compilation V3

新的 Harness Compilation 将“完整理解规范”和“适配目标环境”拆开：

```text
Canonical Workflow / Rules / Meta Protocol
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
                 ↓
           Harness Ready
```

核心原则：

> **完整性在规范侧解决；定制化在目标侧解决；可靠性在验证侧解决。**

### 1. Semantic Compile｜规范语义编译

在 Spec Coding 版本发布侧，将完整 Canonical Corpus 一次性编译为 Atomic Clauses + Execution Relations。目标项目不再重新从几十份 Markdown 中发现规范细节。

- 治理：[`docs/governance/semantic-compilation.md`](docs/governance/semantic-compilation.md)
- 工具：[`tools/semantic_compiler/`](tools/semantic_compiler/)
- Pilot：[`semantic/pilot/`](semantic/pilot/)

### 2. Environment Discover｜环境认知建立

根据 Semantic IR，只发现当前 Harness 适配真正需要的 Runtime / Project / Existing Harness 事实，并形成 Evidence-backed Environment Model。

- 工具：[`tools/environment_discovery/`](tools/environment_discovery/)

### 3. Harness Adapt｜Harness 适配

逐 Clause 判断当前环境可以原生复用、组合已有能力，还是需要新增最小 Harness；语义覆盖保持完整，最小化只发生在实现层。

### 4. Verify & Accept｜验证与接管

用 Clause Coverage、Runtime Visibility、Semantic Challenge 与 Fresh-agent Behavior 证明 Harness 真正生效。

完整协议：[`docs/meta-protocols/harness-compilation.md`](docs/meta-protocols/harness-compilation.md)

---

## Use it with your coding agent

Human 仍然只需要表达自然语言目标，例如：

```text
按照 Spec Coding 接入当前项目，并按当前任务继续推进。
```

Agent 应自行：

```text
Project Onboarding（若需要）
        ↓
Adoption Baseline
        ↓
Environment Discover
        ↓
Harness Adapt / Reuse
        ↓
Verify & Accept
        ↓
01A / 01B / Resume
```

Adoption Baseline 只持久化长期意图与稳定绑定；Runtime Loader、Model、Tool、Subagent、CI 与 Existing Harness 等动态事实按需重新发现。

> **Persist intent, rediscover facts｜持久化意图，重发现动态事实。**

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
- Persist Intent, Rediscover Facts｜持久化意图，重发现动态事实；
- Reuse before Add｜复用优先；
- Minimum Sufficient Harness｜最小充分 Harness。

---

## Explore

| 我想…… | 从这里开始 |
|---|---|
| 快速理解完整流程 | [`docs/overview.md`](docs/overview.md) |
| 查看机器可读规范入口 | [`docs/manifest.yaml`](docs/manifest.yaml) |
| 接入目标项目 | [`docs/meta-protocols/project-onboarding.md`](docs/meta-protocols/project-onboarding.md) |
| 理解 Harness Compilation V3 | [`docs/meta-protocols/harness-compilation.md`](docs/meta-protocols/harness-compilation.md) |
| 查看 Workflow | [`docs/workflows/`](docs/workflows/) |
| 查看 Rules | [`docs/rules/`](docs/rules/) |
| 查看 Runtime / Harness Reference | [`docs/reference/`](docs/reference/) |
| 维护 Spec Coding | [`docs/governance/`](docs/governance/) |

---

## Project status

当前仍处于 `candidate` 阶段。V3 正在通过 Semantic IR Pilot、Environment Discovery、真实项目 Harness 编译与 Fresh-Agent Blind Run 逐步验证。

## License

除非另有说明，本仓库的文档、规范、图示及其他非软件内容采用 [Creative Commons Attribution 4.0 International](LICENSE)（CC BY 4.0）许可。
