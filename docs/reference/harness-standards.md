# Harness Standards & Interoperability｜Harness 标准与互操作参考

> **Status:** Non-normative Reference  
> **Purpose:** 为 Harness Build & Release、Portable Harness Package 与后续 Target-side Harness Adaptation 提供公开标准基线。  
> **Last verified:** 2026-09-03  
> **Freshness:** S · Stable / M · Moderate / F · Fast

本文件维护与 Spec Coding Harness 直接相关的公开协议、开放格式和基础工程标准。它不定义新的 Workflow、Rule 或 Meta Protocol，也不替代外部协议自身的 Normative Specification（规范正文）。

外部协议的官方规范始终是对应外部事实的最高来源；本文件只记录当前采用基线、Spec Coding 的使用边界与可重新获取的官方入口。

```text
Canonical Behavior
        ↓
Harness Primitive
        ↓
Public Standard available?
   ├─ yes → Portable Standard Artifact
   └─ no  → Runtime Capability Requirement
        ↓
Released Harness Package
        ↓
Target-side Runtime Adaptation（按需）
```

---

## 1. Standards-first Principle｜标准优先原则

### Public Standard First｜公开标准优先

成熟公开标准能够完整保持 Spec Coding 行为语义时，维护者预编译 Harness 应优先采用公开标准，而不是创建 Spec Coding 私有格式。

### Semantics before Portability｜语义优先于可移植性

公开标准不能完整满足 Required Behavior（必需行为保证）时，不得为了形式兼容弱化语义。

> **Portable when equivalent; native when necessary｜等价时优先可移植，必要时优先原生能力。**

### Compose, Don't Reinvent｜组合而不是重复发明

一个 Canonical 行为需要多个 Harness Mechanism 时，直接组合 Agent Skills、MCP、Bootstrap 与必要 Runtime Requirement，不为了“组件组合”额外创造 Spec Coding 私有 Component Protocol。

### Portable Core, Runtime Extension｜可移植核心，运行时特化

Portable Package 只固化具备明确跨 Runtime 互操作语义的标准能力。Rule、Hook、Agent / Subagent、Permission / Gate、Sandbox、Workspace / Worktree、Model Routing、Thinking 与其他 Runtime-specific 能力由目标侧根据当前 Runtime 完成 Adaptation（适配）与 Enhancement（增强）。

### Experimental Features Are Not Hard Guarantees｜实验能力不承担强语义

Experimental、Draft、Preview 或 Runtime-dependent 标准字段不得单独承担不可弱化的 Required Behavior。

### Current Evidence Wins｜当前证据优先

Reference 记录“标准定义了什么”，不证明“当前 Runtime 已实现什么”。目标侧最终能力判断仍需使用当前 Official Evidence 与 Local Executable Evidence。

---

## 2. Standards Matrix｜标准矩阵

| Standard | Layer | Standardizes | Spec Coding Usage | Adoption | Freshness |
|---|---|---|---|---|---|
| Agent Skills | Procedure / Knowledge | `SKILL.md`、程序性知识、Scripts、References、Assets | Workflow / Debug / Onboarding 等 Portable Procedure | Preferred | F |
| Agent Plugins | Package | Agent Skills + MCP 的 Portable Package 与 Client Extension | Versioned Harness Package | Preferred | F |
| MCP | Tool / Data | Tool、Resource、Prompt 与外部能力连接 | Portable Capability Provider | Preferred | F |
| AGENTS.md | Bootstrap Instruction | Coding Agent 项目级指令入口 | Portable Bootstrap / Routing | Preferred where supported | F |
| ACP | Client ↔ Agent | Client / Agent 通信与 Capability Negotiation | Target-side Discovery / Host Integration | Optional | F |
| A2A | Agent ↔ Agent | 独立 Agent 发现、任务与消息互操作 | Remote Agent Provider | Optional | F |
| Agent Control Specification | Policy / Enforcement | 生命周期策略与确定性 Verdict | Runtime Gate Candidate | Experimental | F |
| JSON Schema 2020-12 | Machine Schema | JSON 数据结构与验证契约 | Package / Build Manifest / Receipt | Core where JSON contract exists | M |
| BCP 14 | Normative Language | MUST / SHOULD / MAY 等要求等级 | Protocol / Schema 规范语义 | Core | S |
| RFC 8785 JCS | Canonicalization | JSON Canonical Representation | Fingerprint / Signature Input | Recommended | S |
| Semantic Versioning 2.0.0 | Versioning | Public Contract Version | Spec Coding / Harness Package Version | Core | S |

Freshness 含义：

- `S · Stable`：长期稳定，无明确变化信号时不机械刷新；
- `M · Moderate`：缓慢演进，涉及相关格式设计时核验；
- `F · Fast`：Agent 生态快速变化，进入相关 Package / Target Adaptation 设计前默认检查官方当前状态。

---

## 3. Portable Harness Standards｜可移植 Harness 标准

### 3.1 Agent Skills

**Role:** Portable Procedure / Knowledge  
**Adoption:** Preferred  
**Freshness:** F  
**Source:** `SRC-AS-SPEC`

Agent Skills 使用包含 `SKILL.md` 的目录封装可发现、可复用、按需加载的程序性知识；标准结构支持 `scripts/`、`references/`、`assets/` 等按需资源，并明确推荐 Progressive Disclosure（渐进式披露）。

```text
skill-name/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
└── assets/        # optional
```

Spec Coding 的 Main Workflow、Debug & Defect Resolution 与 Project Onboarding 等稳定 Procedure，应优先直接从 Canonical 编译为 Agent Skills-compatible 资产。

Portable Skill 保持流程语义与程序性知识，不固化 Model、Thinking、Subagent、Workspace 等 Runtime Strategy。

Agent Skills 当前 `allowed-tools` 字段仍为 Experimental，且支持可能因 Agent 实现而异，因此不能单独证明真实 Permission / Authority Boundary 已成立。

### 3.2 Agent Plugins

**Role:** Portable Harness Package  
**Baseline:** 1.0.0 / Published  
**Adoption:** Preferred  
**Freshness:** F  
**Sources:** `SRC-AP-SPEC`, `SRC-AP-SCHEMA`

Agent Plugins v1 定义 Vendor-neutral 的 Portable Plugin Package。当前 Portable Core 标准化的主要内容是：

```text
Agent Skills
+
MCP Servers
```

典型结构：

```text
plugin/
├── plugin.json
├── skills/
├── mcp.json
└── <client-extension-namespace>/
```

Spec Coding 应优先将可发布 Harness Bundle 设计为 Agent Plugins-compatible Package；`plugin.json` / `mcp.json` 使用对应规范版本的官方 Machine Schema。

Agent Plugins 还定义 Client Extensions：Runtime-specific Manifest Data 可放在 `extensions` 的 reverse-domain namespace 下，Runtime-specific Files 可放在对应顶层 namespace 目录中；不理解该 namespace 的 Client 应忽略它而不改变 Portable Core 的语义。

因此 Codex / Pi / Claude Code 等特化应优先遵循：

```text
Portable Core
+
Runtime-owned Extension / Overlay
```

而不是复制并修改 Portable Source。

Agent Plugins v1 没有把 Commands、Hooks、Agents、Rules、Permissions 等定义为 Portable Component Type；这些能力仍由目标侧根据当前 Runtime 实际 Surface 处理。

### 3.3 Model Context Protocol｜MCP

**Role:** Portable Tool / Resource Protocol  
**Baseline:** 2026-07-28  
**Adoption:** Preferred for external capabilities  
**Freshness:** F  
**Sources:** `SRC-MCP-SPEC`, `SRC-MCP-RELEASE`

MCP 为 LLM Application 与外部 Context / Tool 提供开放协议。2026-07-28 规范采用 Stateless Core，并正式提供 Extension Framework；当前协议核心继续提供 Resources、Prompts、Tools 等能力。

Spec Coding 在 Search、Browser、Repository Service、Database、Documentation、Verification Service 与其他外部能力存在等价可靠 MCP Provider 时，应优先考虑 MCP。

以下概念不得机械等价：

```text
Tool ≠ MCP
Workflow ≠ MCP Server
Skill ≠ MCP Server
Subagent ≠ MCP Server
```

MCP 解决能力连接，不替代完整 Spec Coding Workflow 语义。

### 3.4 AGENTS.md

**Role:** Portable Bootstrap Instruction  
**Adoption:** Preferred where supported  
**Freshness:** F  
**Source:** `SRC-AGENTS`

AGENTS.md 是面向 Coding Agent 的开放项目指令格式，以普通 Markdown 提供可预测的 Agent Instruction Surface，并支持目录级嵌套与就近覆盖。

Spec Coding 优先将其定位为 Bootstrap / Routing Surface，而不是完整规范正文：

```text
AGENTS.md
├── declare Spec Coding adoption
├── locate released Harness Package
├── resolve current workflow entry
├── route always-on semantics
├── route stage-specific Skills
└── route exception triggers
```

AGENTS.md 不应长期承载完整 Canonical Workflow 正文、Runtime Capability Cache、Model Routing、Task State 或 Acceptance Evidence。

> **AGENTS.md should route, not teach｜AGENTS.md 负责路由，不负责重新教学完整 Spec Coding。**

---

## 4. Adaptation & Interoperability Standards｜适配与互操作协议

### 4.1 Agent Client Protocol｜ACP

**Role:** Client ↔ Agent Protocol  
**Baseline:** v1  
**Adoption:** Optional Target-side Discovery / Integration Source  
**Freshness:** F  
**Source:** `SRC-ACP-SPEC`

ACP 使用 JSON-RPC 2.0 标准化 Client 与 Coding Agent 的双向通信，包含 Initialization、Session、Permission Request、File / Terminal 等能力面。

如果当前 Runtime / Host 暴露 ACP，目标侧环境发现可以优先消费协议提供的 Capability Evidence，再对协议未覆盖或当前实现不确定的能力执行 Local / Official Probe。

```text
ACP available
    ↓
Capability Negotiation / Protocol Evidence

ACP unavailable
    ↓
Local / Official Probe
```

ACP 不用于承载 Workflow 或 Skill。

### 4.2 Agent2Agent Protocol｜A2A

**Role:** Independent Agent Interoperability  
**Baseline:** 1.0.0  
**Adoption:** Optional  
**Freshness:** F  
**Source:** `SRC-A2A-SPEC`

A2A 用于独立、可能跨 Framework / Language / Vendor 的 Agent 系统之间进行 Capability Discovery、Message / Task 管理与 Artifact 交换。

Spec Coding 仅在 Subagent 实际是独立 Agent Service 时考虑 A2A；当前 Runtime 内部的普通 Child Session / Subagent 不应为了形式标准化而强制转换成 A2A。

### 4.3 Agent Control Specification｜ACS

**Role:** Runtime Policy / Enforcement Candidate  
**Baseline:** 0.3.1-beta / Draft / Public Preview  
**Adoption:** Optional  
**Freshness:** F  
**Source:** `SRC-ACS-SPEC`

ACS 当前提供 Stateless、Deterministic、Fail-closed 的 Policy Decision Runtime，在定义的 Intervention Point 返回 `allow / warn / deny / escalate / transform` 等 Verdict，由 Host Adapter 执行真正 Enforcement。

其 API 与 Manifest 在 GA 前仍可能变化，因此当前不得成为 Spec Coding Portable Core 的基础依赖。

Hard Semantic Gate 的目标侧适配可按以下顺序评估：

```text
Required Hard Gate
      ↓
Runtime-native enforcement available?
   ├─ yes → prefer native
   └─ no
        ↓
ACS-compatible enforcement available and sufficient?
   ├─ yes → use after verification
   └─ no  → BLOCK when prompt-only enforcement is insufficient
```

---

## 5. Machine Representation Standards｜机器表示标准

### 5.1 JSON Schema 2020-12

**Role:** Machine Contract Schema  
**Adoption:** Core where structured JSON contract exists  
**Freshness:** M  
**Source:** `SRC-JSON-SCHEMA`

Spec Coding 的 Package Manifest、Build Manifest、Verification / Release Receipt 等结构化 JSON 产物，应使用 JSON Schema 定义可验证 Contract，并显式声明使用的 Dialect / Schema Version。

不因为 JSON Schema 可用就要求所有 Harness 资产额外复制成一套 Machine Spec；只有真实需要机器验证的结构才建立 Schema。

### 5.2 BCP 14

**Role:** Normative Requirement Language  
**Adoption:** Core  
**Freshness:** S  
**Sources:** `SRC-RFC2119`, `SRC-RFC8174`

Spec Coding 自身定义 Protocol / Schema Contract 时，规范关键词 `MUST / MUST NOT / SHOULD / SHOULD NOT / MAY` 应按 BCP 14 解释。Human-facing Workflow Markdown 不要求机械改写为 RFC 文风。

### 5.3 RFC 8785 JSON Canonicalization Scheme｜JCS

**Role:** Canonical JSON Representation  
**Adoption:** Recommended  
**Freshness:** S  
**Source:** `SRC-RFC8785`

需要跨实现进行 Hash、Content Identity 或 Signature 的 JSON Artifact，应使用明确 Canonicalization Contract：

```text
JSON Artifact
    ↓
JCS Canonicalization
    ↓
SHA-256
    ↓
Stable Fingerprint
```

### 5.4 Semantic Versioning｜SemVer

**Role:** Public Contract Versioning  
**Baseline:** 2.0.0  
**Adoption:** Core  
**Freshness:** S  
**Source:** `SRC-SEMVER`

当前阶段 Spec Coding Method Version 与 Harness Package Version 保持一致，避免提前制造版本森林。只有未来出现真实独立生命周期的公开契约时，再为独立 Adapter / Package Format / Schema 建立单独版本。

---

## 6. Portable / Runtime Boundary｜可移植层与运行时层边界

当前标准基线下，推荐边界为：

```text
Portable Harness Package
│
├── Agent Plugin（where appropriate）
│   ├── Agent Skills
│   └── MCP
│
├── Bootstrap / Routing
│   └── AGENTS.md where supported
│
└── Build / Release Metadata
```

目标侧 Runtime-specific Layer 负责：

```text
Runtime-specific Layer
│
├── Rule / Instruction Surface
├── Hook / Event
├── Agent / Subagent
├── Permission / Gate
├── Sandbox
├── Workspace / Worktree
├── Model Routing
├── Thinking / Reasoning
├── Background / Concurrency
├── Runtime-specific Skill Extension
└── Runtime-specific Plugin Extension
```

目标顺序是：

1. Preserve Canonical Behavior；
2. Prefer Deterministic Enforcement；
3. Exploit Native Capability when useful；
4. Preserve Progressive Loading；
5. Prefer Portable Representation when equivalent；
6. Minimize Complexity and Runtime Cost。

---

## 7. Source Registry｜官方来源注册表

Source Registry 只登记官方 / 规范性入口，不复制完整协议正文。

| Source ID | Standard | Baseline / Status | Freshness | Official Source |
|---|---|---|---|---|
| `SRC-AS-SPEC` | Agent Skills | Current public specification | F | https://agentskills.io/specification |
| `SRC-AP-SPEC` | Agent Plugins | 1.0.0 / Published | F | https://agent-plugins.org/specification |
| `SRC-AP-SCHEMA` | Agent Plugins Schemas | 1.0.0 | F | https://agent-plugins.org/schemas |
| `SRC-MCP-SPEC` | MCP | 2026-07-28 | F | https://modelcontextprotocol.io/specification/2026-07-28 |
| `SRC-MCP-RELEASE` | MCP Release Notes | 2026-07-28 | F | https://blog.modelcontextprotocol.io/posts/2026-07-28/ |
| `SRC-AGENTS` | AGENTS.md | Current open format | F | https://agents.md/ |
| `SRC-ACP-SPEC` | ACP | v1 | F | https://agentclientprotocol.com/protocol/v1/overview |
| `SRC-A2A-SPEC` | A2A | 1.0.0 | F | https://a2a-protocol.org/dev/specification/ |
| `SRC-ACS-SPEC` | ACS | 0.3.1-beta / Draft / Public Preview | F | https://github.com/microsoft/agent-governance-toolkit/blob/main/policy-engine/spec/SPECIFICATION.md |
| `SRC-JSON-SCHEMA` | JSON Schema | Draft 2020-12 | M | https://json-schema.org/draft/2020-12 |
| `SRC-RFC2119` | BCP 14 | RFC 2119 | S | https://www.rfc-editor.org/rfc/rfc2119 |
| `SRC-RFC8174` | BCP 14 | RFC 8174 | S | https://www.rfc-editor.org/rfc/rfc8174 |
| `SRC-RFC8785` | JCS | RFC 8785 | S | https://www.rfc-editor.org/rfc/rfc8785 |
| `SRC-SEMVER` | SemVer | 2.0.0 | S | https://semver.org/spec/v2.0.0.html |

每次核验外部标准时，应优先更新：

```text
Baseline / Status
Last verified
Adoption Decision（如发生变化）
Official Source（如官方入口迁移）
```

非官方 Blog、Community Implementation、Benchmark 与 Research 只作为补充 Evidence，不应单独改变 Portable Standard Adoption Decision。

---

## 8. Freshness & Maintenance｜时效性与维护

### Refresh Triggers｜刷新触发

以下情况应重新核验相关 Source：

1. Spec Coding 修改 Harness Package Architecture；
2. 新增或实质修改 Target-side Runtime Adaptation；
3. 公开协议发布新版本；
4. Experimental / Preview 能力变为 Stable、Deprecated 或 Removed；
5. Runtime 实际行为与本 Reference 冲突；
6. 当前设计首次依赖此前未采用的协议能力；
7. F-class Source 已明显陈旧且即将影响当前设计决策。

> **Stale + Relevant → Refresh｜陈旧且当前相关时刷新。**

不因日期经过而机械重新调查所有标准。

### External Standard Change｜外部标准变化

协议变化先更新 Source Baseline，再判断是否改变现有 Build / Adaptation Decision：

```text
External Standard Change
          ↓
Source Baseline Refresh
          ↓
Build / Adaptation Decision changed?
    ├─ no → update reference only
    └─ yes
          ↓
Affected Harness Artifact / Runtime Boundary
          ↓
Rebuild / Revalidate affected trace
```

外部版本号变化本身不自动使所有 Harness 失效。

---

## 9. Design Use｜设计使用方式

维护者设计 Harness Artifact 前：

```text
Canonical Behavior
        ↓
Resolve Harness Primitive
        ↓
Check this Standards Registry
        ↓
Portable Standard exists and is sufficient?
   ├─ yes → build standard artifact
   └─ no  → keep runtime capability requirement
        ↓
Package Verification
```

设计 Runtime-specific Enhancement 前：

```text
Released Portable Harness
        ↓
Current Runtime Capability
        ↓
Native Enhancement available?
   ├─ yes → Runtime-specific optimization
   └─ no  → portable / fallback implementation
        ↓
Verify behavioral equivalence
```

> **Standardize what can be portable; specialize what should be native｜能标准化的保持标准，应该特化的充分利用 Runtime 原生能力。**
