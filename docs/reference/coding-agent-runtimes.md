# Coding Agent Runtime Reference｜Coding Agent 运行时参考

本文件为 Harness Compilation 提供 Coding Agent Runtime 的 Architecture Invariant（架构不变量）与 Official Sources（官方事实入口）。它属于 Reference（参考）文档，不定义 Workflow / Rule / Meta Protocol，也不作为当前 Runtime Capability 的权威事实源。

> **Architecture guides mapping; current evidence decides capability｜架构指导映射，当前证据决定能力。**

**Last verified:** 2026-08-31

---

## 1. 使用规则

本文件只长期保存：

1. Runtime Identity / Lifecycle；
2. 会影响 Harness 编译策略的 Architecture Invariant；
3. 由架构不变量推导出的 Harness Implication；
4. 可在编译时重新 fetch 的官方 Docs / Repo / Release / Changelog 入口。

本文件不作为以下事实的权威来源：

- 当前安装版本；
- 当前模型列表与 Thinking / Effort 档位；
- Feature Flag / Preview 状态；
- Quota / Pricing / Availability；
- Hook Event 全量列表；
- Runtime-specific 配置字段；
- 版本特定行为。

这些事实必须由 Harness Compilation 使用当前 Official Evidence 与 Local Executable Evidence 重新发现。

---

## 2. Runtime Scope

`Primary` 表示值得为 Harness Compiler 建立一等参考，不表示绝对市场排名。

| Runtime | Region | Type | Coverage | Lifecycle |
|---|---|---|---|---|
| Claude Code | Global | CLI / Agent Runtime | Primary | active |
| OpenAI Codex | Global | CLI / IDE / App / Cloud Agent | Primary | active |
| Cursor | Global | Agentic IDE / CLI / Cloud | Primary | active |
| GitHub Copilot / VS Code Agent | Global | IDE / CLI / Cloud Agent | Primary | active |
| Gemini CLI | Global | Open CLI / ACP Agent | Primary | active |
| Grok Build | Global | CLI / Headless / ACP Agent | Primary | active |
| OpenCode | Global | Open Coding Harness | Primary | active |
| Pi Coding Agent | Global | Minimal Open Harness / SDK | Primary | active |
| TRAE / TraeCode | China / Global | Agentic IDE / Coding Agent | Primary | active |
| CodeBuddy Code | China | CLI / IDE Coding Agent | Primary | active |
| Qoder CLI | China / Global | CLI / Agentic IDE Companion | Primary | active |
| Qwen Code | China / Global | Open CLI / ACP / SDK Runtime | Primary | active |
| Kimi Code | China / Global | CLI Multi-Agent Runtime | Primary | active |
| ZCode | China / Global | Agentic Development Environment | Primary | active |
| DeepSeek Harness / DSH | China / Global | Open Agent Harness | Primary | preview |
| MiniMax Code | China / Global | Coding Agent / Agent Team Runtime | Primary | active |

可继续观察但暂不建立同等深度 Architecture Entry 的 Runtime，例如 WorkBuddy、Devin Desktop、Cline / Roo Code / Kilo Code、CodeArts Agent、Lingma 等；真正需要编译时仍可通过官方资料执行 Generic Runtime Discovery。

---

## 3. Architecture Invariant Admission Rule｜架构不变量准入

只有同时满足以下条件的信息才进入本文件：

1. **Compilation-relevant**：会改变 Spec Coding → Runtime 的编译策略；
2. **Version-stable**：跨多个版本具有较高稳定性；
3. **Architecture-level**：若发生根本变化，通常意味着 Runtime 本身架构明显变化；
4. **Officially evidenced**：具有官方文档、官方源码或官方技术材料支持。

Architecture Evidence 使用以下强度：

- `explicit`：官方直接描述架构原则；
- `official-surface`：由多个长期稳定的官方 Surface 归纳编译模式，不声称知道未公开内部实现；
- `none`：暂无值得长期固化的 Architecture Invariant，只保留官方入口。

以下信息不得作为 Architecture Invariant：

```text
当前默认模型
某版本 Hook 数量
某个 maxTurns 默认值
当前 Beta Feature
当前价格 / Quota
```

---

# Global Runtime

## 4. Claude Code

**Type:** CLI / agentic coding runtime  
**Evidence:** explicit

### Architecture Invariant

**Agentic Loop + Composable Extension Layer**

核心执行持续围绕 Context → Action → Verification 运行；项目指令、Skills、MCP、Subagents、Hooks、Plugins 等位于核心 Loop 之上的扩展层。

### Harness Implication

- 长期项目约束优先项目指令 Surface；
- 程序性方法优先 Skill；
- 外部 Tool 优先 MCP；
- Context Isolation / delegated work 优先 Subagent；
- 确定性生命周期控制优先 Hook；
- 优先组合扩展层，不为 Spec Coding 改写核心 Agent Loop。

### Official Sources

- Docs: https://code.claude.com/docs/
- How Claude Code works: https://code.claude.com/docs/en/how-claude-code-works
- Feature / extension overview: https://code.claude.com/docs/en/features-overview
- Subagents: https://code.claude.com/docs/en/subagents
- Hooks: https://code.claude.com/docs/en/hooks
- Docs index: https://code.claude.com/docs/llms.txt

**Fetch at compile time:** models / effort、Agent Teams、worktree、permissions、Hook Event 与 managed settings。

---

## 5. OpenAI Codex

**Type:** CLI / IDE / app / cloud coding agent family  
**Evidence:** official-surface

### Architecture Invariant

**Repository-scoped Context + Bounded Autonomous Execution + Packaged Capabilities**

长期稳定 Surface 包括 repository-scoped instructions、Sandbox / Approval 边界，以及 Skills / Plugins / Apps 等可组合能力。具体 Agent / Model Surface 随产品形态变化，应运行时重新发现。

### Harness Implication

- 跨 Runtime 项目约束优先 `AGENTS.md`；
- 程序性能力优先 Agent Skills；
- 高风险 Write / Network / Tool 行为映射到 Sandbox + Approval / Policy，而不是只依赖 Rule；
- 不在 Reference 固化具体模型与 reasoning 配置。

### Official Sources

- Codex docs: https://learn.chatgpt.com/docs
- Open-source CLI: https://github.com/openai/codex
- AGENTS.md implementation: https://github.com/openai/codex/blob/main/docs/agents_md.md
- Agent Skills examples: https://github.com/openai/codex/tree/main/codex-rs/skills
- Plugins: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex
- Releases: https://github.com/openai/codex/releases

**Fetch at compile time:** active Codex surface、subagent / child-agent support、sandbox、approval、plugins / tools、model / reasoning options。

---

## 6. Cursor

**Type:** agentic IDE / CLI / cloud agent  
**Evidence:** official-surface

### Architecture Invariant

**Editor-integrated Agent Runtime + Composable Customization + Isolated Workspace**

公开长期 Surface 围绕 Rules、Skills、Agents、Commands、MCP、Hooks、Plugins 与 Worktree / isolated workspace 组织。内部 Loop 未完整公开，因此不进一步推断私有实现。

### Harness Implication

- 持续项目约束 → Rules / AGENTS.md；
- 程序性能力 → Agent Skills；
- Cursor-specific Agent / Rule / Hook → Cursor extension surface；
- 并行 Writer → isolated workspace / worktree；
- 不把 Cursor Plugin 的所有组件误认为跨 Runtime Agent Plugins 标准。

### Official Sources

- Docs: https://cursor.com/docs
- Plugins: https://cursor.com/docs/plugins
- Plugin reference: https://cursor.com/docs/reference/plugins
- Rules: https://cursor.com/docs/context/rules
- Worktrees: https://cursor.com/docs/configuration/worktrees

**Fetch at compile time:** Agent modes、cloud/background execution、subagent/model routing、plugin fields、Hook 与 worktree behavior。

---

## 7. GitHub Copilot / VS Code Agent

**Type:** IDE / CLI / GitHub cloud coding agent  
**Evidence:** explicit

### Architecture Invariant

**Declarative Agent Profiles + Scoped Governance + Runtime Delegation**

Custom Agent 使用 Prompt / Tool / MCP 等声明式配置形成 Agent Profile；Customization 可存在 repository / organization / enterprise scope，并由 Runtime 进行子 Agent 或并行编排。

### Harness Implication

- 团队共享约束优先 repo / org / enterprise instruction surface；
- Spec Coding Role 可映射为 Custom Agent Profile；
- 独立 Work Unit 可映射为 Subagent；
- 确定性审计 / 验证优先 Hook；
- 企业硬约束应优先进入治理 / Policy，而不是只靠 Prompt。

### Official Sources

- Docs: https://docs.github.com/en/copilot
- Custom agents: https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- Custom agent configuration: https://docs.github.com/en/copilot/reference/custom-agents-configuration
- Custom instructions: https://docs.github.com/en/copilot/reference/custom-instructions-support
- Hooks: https://docs.github.com/en/copilot/concepts/agents/hooks
- Hooks reference: https://docs.github.com/en/copilot/reference/hooks-reference

**Fetch at compile time:** active Copilot surface、custom-agent schema、parallel / subagent capability、policy、model selection、cloud workspace behavior。

---

## 8. Gemini CLI

**Type:** open CLI / ACP agent / local & remote agent runtime  
**Evidence:** explicit

### Architecture Invariant

**Protocol-oriented Extensibility + Policy-controlled Delegation**

Gemini CLI 通过开放协议组合能力：MCP 连接工具，Agent Skills 承载程序性能力，ACP 暴露 Agent Runtime，A2A 可连接远程 Agent，本地 Subagent 提供隔离执行，Policy / Sandbox 控制边界。

### Harness Implication

```text
Tool         → MCP
Skill        → Agent Skills
IDE Adapter  → ACP
Remote Agent → A2A
Local Role   → Subagent
Hard Boundary→ Policy / Sandbox / Hook
```

### Official Sources

- Docs: https://geminicli.com/docs/
- Core: https://geminicli.com/docs/core/
- Subagents: https://geminicli.com/docs/core/subagents/
- Remote agents: https://geminicli.com/docs/core/remote-agents/
- ACP: https://geminicli.com/docs/cli/acp-mode/
- Skills: https://geminicli.com/docs/cli/skills/
- Hooks: https://geminicli.com/docs/hooks/
- Policy Engine: https://geminicli.com/docs/reference/policy-engine/
- Configuration: https://geminicli.com/docs/reference/configuration/

**Fetch at compile time:** experimental status、subagent schema、policy、sandbox、model routing 与计划 / workspace 功能。

---

## 9. Grok Build

**Type:** terminal / headless / ACP coding agent  
**Evidence:** explicit

### Architecture Invariant

**Compatibility-first Extension Runtime + Protocol-accessible Agent Surface**

长期设计强调 TUI / headless / ACP 多入口，以及 Skills、Agents、Hooks、MCP、Plugins 等组合能力，并提供对既有 Coding Agent 资产的兼容路径。

### Harness Implication

- 已有兼容 Harness 资产先尝试复用；
- Skill / MCP 等优先使用可移植表示；
- IDE / orchestration embedding 优先 ACP；
- Grok-specific 能力再使用 Runtime-native Extension / Hook；
- 兼容范围必须按当前版本现场确认。

### Official Sources

- Docs: https://docs.x.ai/build/overview
- Skills / Plugins: https://docs.x.ai/build/features/skills-plugins-marketplaces
- Settings: https://docs.x.ai/build/settings
- Source: https://github.com/xai-org/grok-build
- Releases: https://github.com/xai-org/grok-build/releases

**Fetch at compile time:** compatibility coverage、agents、workflow / hook schema、sandbox / permission、models / effort、ACP version。

---

## 10. OpenCode

**Type:** open provider-agnostic coding harness  
**Evidence:** explicit

### Architecture Invariant

**Explicit Primary-Agent / Subagent Runtime + Permission-first Tool Governance**

Agent 明确区分 Primary Agent 与 Subagent，并可为 Agent 配置 Prompt、Model、Tools 与 Permission；Tool / Skill / Task 等动作统一进入权限模型。

### Harness Implication

- Main Agent / Subagent 语义可直接映射；
- 角色权限优先进入 Agent-specific Permission；
- Spec Coding Role Profile 可编译为显式 Agent config；
- 模型列表与 Provider 能力仍运行时发现。

### Official Sources

- Docs: https://opencode.ai/docs/
- Agents: https://opencode.ai/docs/agents/
- Skills: https://opencode.ai/docs/skills
- Permissions: https://opencode.ai/docs/permissions/
- Config: https://opencode.ai/docs/config/

**Fetch at compile time:** Agent schema、recursive delegation、models/providers、permission keys、workspace / sessions、plugin / MCP behavior。

---

## 11. Pi Coding Agent

**Type:** minimal open coding harness / TUI / SDK  
**Evidence:** explicit

### Architecture Invariant

**Minimal Core + Extension / Resource-loader-first Runtime**

核心保持最小；可定制行为主要由 Extensions、Skills、Prompt / Context Resources、Packages 与 Resource Loader 组合。非核心能力不应假定存在，应检查当前安装的 extension / package。

### Harness Implication

- 项目约束优先 AGENTS.md；
- 程序性能力优先 Agent Skills；
- Pi-specific Runtime Behavior 优先 Extension；
- 分发复用优先 Package；
- 不为 Spec Coding 修改 Pi Core；
- Subagent / permission / sandbox 等由当前 Extension Surface 动态确认。

### Official Sources

- Repository: https://github.com/badlogic/pi-mono
- Coding-agent docs: https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/docs
- Extensions: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md
- SDK: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/sdk.md
- Skills: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md
- Packages: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md

**Fetch at compile time:** installed packages/extensions、subagent capability、models/providers、thinking、permission / sandbox extensions 与 resource paths。

---

# China Runtime

## 12. TRAE / TraeCode

**Type:** agentic IDE / coding agent  
**Evidence:** official-surface

### Architecture Invariant

**IDE-native Composition of Rules + On-demand Skills + Configurable Agents + MCP**

官方长期 Surface 稳定区分持续 Rule、按需 Skill、Agent / Subagent 与 MCP。内部 Agent Loop 未完整公开，因此只固化可直接影响 Harness Compilation 的公开 Surface。

### Harness Implication

- 跨 Runtime 项目约束优先 AGENTS.md 等便携项目指令；
- TRAE-specific 持续规则使用其 Rule Surface；
- 程序性能力使用 Skill；
- 角色隔离使用 Agent / Subagent；
- Tool integration 优先 MCP；
- 先生成便携资产，再补 Runtime-specific 配置。

### Official Sources

- Docs: https://docs.trae.cn/
- Rules: https://docs.trae.cn/ide_rules
- Skills: https://docs.trae.cn/ide_skills
- Work Rules: https://docs.trae.cn/work_rules
- Work Skills: https://docs.trae.cn/work_skills
- MCP: https://docs.trae.cn/enterprise_model-context-protocol

**Fetch at compile time:** active TRAE surface、Agent schema、subagent、model routing、sandbox / permission、cloud execution。

---

## 13. CodeBuddy Code

**Type:** terminal coding agent / IDE ecosystem  
**Evidence:** explicit

### Architecture Invariant

**Composable Plugin Package + Scoped Agent / Skill Lifecycle + Layered Permission Pipeline**

Plugin 可组合 Skills、Agents、Hooks、MCP、LSP 等能力；Permission 使用分层求值形成 deterministic boundary，Agent / Skill 可拥有局部生命周期配置。

### Harness Implication

- 项目局部配置使用 Runtime-native project surface；
- 团队复用优先 Plugin；
- Spec Role → Agent / Subagent；
- Hard enforcement → Permission + Hook；
- Tool → MCP / plugin tool；
- Runtime Plugin 私有字段不视为 Agent Plugins 开放标准。

### Official Sources

- Docs: https://www.codebuddy.cn/docs/
- CLI settings: https://www.codebuddy.cn/docs/cli/settings
- Subagents: https://www.codebuddy.cn/docs/cli/sub-agents
- Skills: https://www.codebuddy.cn/docs/cli/skills
- Plugins: https://www.codebuddy.cn/docs/cli/plugins
- Hooks: https://www.codebuddy.cn/docs/cli/hooks
- Permissions: https://www.codebuddy.cn/docs/cli/permissions

**Fetch at compile time:** permission precedence、agent fields、model / effort、Hook maturity、worktree、plugin trust policy。

---

## 14. Qoder CLI

**Type:** terminal coding agent / agentic IDE companion  
**Evidence:** explicit

### Architecture Invariant

**Declarative Subagent Profile + Explicit Capability / Permission / Isolation Controls**

Subagent Profile 可声明 Model / Effort、Tools、Skills、MCP、Memory、Hooks、Permission、Background 与 Workspace Isolation 等能力，是“Spec Role → Runtime Agent Profile”映射的典型 Runtime。

### Harness Implication

```text
Spec Role
+ Scoped Context
+ Tool Requirement
+ Permission Boundary
+ Capability Requirement
+ Workspace Isolation
        ↓
Declarative Agent Profile
```

模型与 Effort 仍属于运行时短生命周期路由事实。

### Official Sources

- Docs: https://docs.qoder.com/
- CLI: https://docs.qoder.com/cli
- Subagent: https://docs.qoder.com/cli/subagent
- Permissions: https://docs.qoder.com/cli/permissions

**Fetch at compile time:** Agent schema、built-in roles、worktree limits、MCP / Hook、Memory switch、model aliases。

---

## 15. Qwen Code

**Type:** open CLI / headless / SDK / ACP coding runtime  
**Evidence:** explicit

### Architecture Invariant

**Runtime Core Decoupled from Clients via Direct + ACP Execution**

同一 Agent Runtime 可通过 Direct Execution 服务 TUI / headless，也可通过 ACP 暴露给外部 Client；长期 workspace / control plane 继续围绕该 Runtime Core 组织。Extension 可组合 prompts、MCP、Subagents、Skills 等能力。

### Harness Implication

- standalone CLI → Direct execution；
- IDE / orchestration / long-lived workspace → ACP / runtime service；
- portable procedure → Agent Skills；
- reusable bundle → Extension；
- external Tool → MCP；
- scoped Role → Subagent；
- Harness 应尽量与具体 UI / Client 解耦。

### Official Sources

- Docs: https://qwenlm.github.io/qwen-code-docs/
- Architecture: https://qwenlm.github.io/qwen-code-docs/en/developers/architecture/
- Extensions: https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/
- Subagents: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/
- Source: https://github.com/QwenLM/qwen-code

**Fetch at compile time:** ACP / daemon protocol、extension compatibility、Hook、model aliases、subagent approval、workspace limits。

---

## 16. Kimi Code

**Type:** terminal multi-agent coding runtime  
**Evidence:** explicit

### Architecture Invariant

**Main-Agent / Isolated-Subagent Delegation + Parallel Swarm Acceleration**

主 Agent 可委派具有独立 Context 的 Subagent，并可对真正独立的 Work Unit 使用 Agent Swarm 并行执行；主 Agent 负责协调与结果整合。

### Harness Implication

- Spec Coding Main Agent 保留 Workflow State 与最终责任；
- Scout / Worker / Reviewer 可映射为隔离 Subagent；
- 大量同构且真正独立 Work Unit 才考虑 Swarm；
- Swarm 仍遵守 Single Writer Boundary；
- model pool / effort 属于 Runtime Fact。

### Official Sources

- Docs: https://www.kimi.com/code/docs/
- Tools: https://www.kimi.com/code/docs/en/kimi-code-cli/reference/tools.html
- Changelog: https://www.kimi.com/code/docs/en/kimi-code/whats-new.html

**Fetch at compile time:** custom agent schema、swarm limits、models、MCP / Hook / ACP、background、fork / resume semantics。

---

## 17. ZCode

**Type:** agentic development environment  
**Evidence:** official-surface

### Architecture Invariant

**Plugin-composed Agent Environment + Project Instruction / Runtime Memory Separation**

Plugin 可组合 Skill、Command、Subagent、MCP、Hook；Subagent 使用隔离 Context。项目长期指令与 Runtime Memory 分离，因此 Memory 只能作为运行辅助，不能替代 Spec Coding Canonical Artifact。

### Harness Implication

- 项目长期约束 → AGENTS.md / Canonical Spec Artifact；
- procedure → Skill；
- role isolation → Subagent；
- reusable package → Plugin；
- external tool → MCP；
- Runtime Memory 不进入 Requirement / Design / Task / Evidence 事实源。

### Official Sources

- Docs: https://zcode.z.ai/en/docs/
- Plugins: https://zcode.z.ai/en/docs/plugin
- Subagents: https://zcode.z.ai/en/docs/subagents
- MCP: https://zcode.z.ai/en/docs/mcp-services
- Chinese docs: https://zcode.z.ai/cn/docs/

**Fetch at compile time:** instruction / memory precedence、plugin compatibility、Agent fields、Hooks、models、parallel/workspace behavior。

---

## 18. DeepSeek Harness / DSH

**Type:** open agent harness runtime  
**Evidence:** explicit  
**Lifecycle:** developer preview

### Architecture Invariant

**Everything is a Plugin + Minimal Cordis Kernel + Append-only Traceable Runtime**

Cordis Kernel 主要负责 Plugin 生命周期与依赖；Model、Tool、Skill、Session、Sandbox、Storage、Loop、Scheduling、UI 等由 Plugin 提供并通过配置组合。Runtime trajectory 使用可追溯的事件 / session 记录支持 Resume / Fork / Replay 等行为。

### Harness Implication

```text
Required Primitive
        ↓
Existing Plugin sufficient?
   ├─ yes → compose
   └─ no  → create extension / plugin / preset
        ↓
Avoid Core Modification
```

其可追溯 trajectory 还可作为 Verification / Traceability 的 Evidence Surface，但具体 Event Contract 必须按当前 Preview 版本确认。

### Official Sources

- Official site: https://deepseek.com/harness/en/
- Chinese site: https://deepseek.com/harness/
- Source: https://github.com/deepseek-ai/deepseek-harness
- Releases: https://github.com/deepseek-ai/deepseek-harness/releases

**Fetch at compile time:** breaking changes、plugin contract、preset schema、runtime modes、agent/workflow plugin、model adapter。

---

## 19. MiniMax Code

**Type:** coding agent / multi-agent team runtime  
**Evidence:** explicit

### Architecture Invariant

**Leader / Worker / Verifier Agent Team + Producer–Verifier Corrective Loop + Persistent Runtime Memory / Skills**

官方技术材料长期使用 Leader、Worker、Verifier 分工组织复杂任务，并通过生成—检查—纠正循环提高可靠性；Memory / Skills 用于沉淀 Runtime 经验。

### Harness Implication

- Spec Coding Main Agent 与 Leader-like coordination 可映射，但 Workflow State 与 Canonical Consistency 仍属于 Spec Coding Main Agent；
- Worker → bounded implementation；
- Reviewer / Verifier → independent validation；
- Runtime Memory 不成为 Canonical Source；
- 自动沉淀 Skill 在成为长期 Harness 前仍需验证。

### Official Sources

- MiniMax Code: https://agent.minimaxi.com/download
- Docs: https://agent.minimaxi.com/docs/
- Technical blog: https://agent.minimaxi.com/docs/techblog
- Docs index: https://agent.minimaxi.com/docs/llms.txt
- Changelog: https://agent.minimaxi.com/docs/changelog

**Fetch at compile time:** Agent Team availability、role customization、memory / skill lifecycle、models、workspace、Verifier、MCP / Tool behavior。

---

## 20. Runtime Fact Evidence Priority

本 Reference 不是 Runtime Fact 的证据优先级来源。Harness Compilation 判断当前能力时应使用：

```text
Local Executable Evidence
        ↓
Version-matched Official Documentation
        ↓
Official Repository / Release / Changelog
        ↓
Provider Documentation
        ↓
External Benchmark / Community Evidence
```

Provider 或社区描述的理论能力不能让当前 Runtime 中不存在的 Surface 变成可用能力。

---

## 21. Capability Normalization

Harness Compilation 可将当前版本的 Capability 临时归一为：

| Status | 含义 |
|---|---|
| `native` | 当前 Runtime 原生、可靠支持。 |
| `composable` | 可通过 Runtime Extension / Plugin / 多能力组合可靠实现。 |
| `external` | 需要 Script / CI / MCP Service / 外部机制承担。 |
| `unavailable` | 已确认当前无法可靠实现。 |
| `unknown` | 尚未取得足够证据。 |

> **Unknown ≠ Unavailable｜未知不等于不支持。**

与 MUST / Gate / Permission / Verification 等关键 Contract 相关的 `unknown` 必须继续发现、使用其他可靠机制，或 Block；不得静默假设。

---

## 22. Reference Drift｜参考漂移

Runtime 变化按三类处理：

- **Feature Delta**：模型、Hook、参数、Feature Flag 等变化，由 Runtime Discovery 自动重新发现，不要求更新本文件；
- **Source / Lifecycle Delta**：官方文档迁移、产品改名、deprecated / retired，更新 Runtime Entry；
- **Architecture Delta**：底层组合方式或稳定架构发生重大变化，更新 Architecture Invariant 与 Harness Implication。

如果 Current Official / Local Evidence 与本文件冲突：

```text
Current Evidence wins
        ↓
Compile using current truth
        ↓
Record Reference Drift
        ↓
Update Reference separately
```

Reference Drift 本身不阻塞业务开发；只有无法建立可靠、安全的 Runtime Mapping 时才阻塞 Harness Ready。

---

## 23. 最终约束

Runtime Reference 的目标不是建设实时 Coding Agent Wiki，而是为 Fresh Agent 提供最低充分 Bootstrap Knowledge：知道当前 Runtime 的稳定设计倾向、应该检查哪些 Primitive、以及官方事实去哪里找。

> **Persist primitives, preserve architecture, fetch version facts｜固化共同原语，保留架构不变量，版本事实随用随取。**

具体编译行为仍由 [`../meta-protocols/harness-compilation.md`](../meta-protocols/harness-compilation.md) 决定；Primitive 语义参见 [`harness-primitives.md`](harness-primitives.md)。