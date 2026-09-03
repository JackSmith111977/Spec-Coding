# Harness Primitives｜Harness 原语参考

本文件为 Harness Compilation 提供跨 Coding Agent Runtime 的共同能力语言。它属于 Reference（参考）文档，不定义 Workflow、Rule 或 Meta Protocol 的规范语义，也不描述某个 Runtime 当前版本的完整能力。

核心目标是：**先把 Spec Coding 的语义要求归一为稳定 Harness Primitive，再由公开标准与当前 Runtime Evidence 决定具体实现。**

```text
Spec Coding Semantic
        ↓
Harness Primitive
        ↓
Public Standard / Runtime-native Surface
```

公开协议的当前采用基线、版本 / 状态、Official Sources 与 Freshness 统一见 [`harness-standards.md`](harness-standards.md)；本文件只维护 Primitive 的稳定语义与分类，避免重复维护快速变化的协议事实。

---

## 1. 分类原则

不能把所有 Coding Agent 常见能力都称为行业标准。本参考区分三类：

| Category | 含义 | 编译用途 |
|---|---|---|
| **Open Standard / Open Format｜开放标准 / 开放格式** | 有公开规范、明确互操作目标或开放格式。 | 等价可靠时优先形成可移植 Harness。 |
| **De facto Convention｜事实约定** | 被多个主流 Runtime 采用、相对稳定，但约束弱于正式协议。 | 可作为共享约定，仍需确认当前 Runtime 支持。 |
| **Common Harness Primitive｜常见 Harness 原语** | 多个 Runtime 都存在的稳定能力语义，但实现方式没有统一。 | 作为 Compiler 的抽象能力词汇，由 Runtime 决定映射。 |

> **Portable when equivalent; preserve semantics when not｜等价时优先可移植，不能等价时优先保持语义。**

---

## 2. Open Standards / Formats｜开放标准与开放格式

以下条目只用于说明 Primitive 与公开标准之间的概念关系；当前规范版本、成熟度和采用边界以 [`harness-standards.md`](harness-standards.md) 为准。

### MCP｜Model Context Protocol（模型上下文协议）

**Classification:** Open Protocol

用于 Agent / Host 与外部 Tool、Data、Resource 之间的标准连接。

**Harness Usage**

```text
External Capability Need
        ↓
MCP available and sufficient?
   ├─ yes → prefer MCP
   └─ no  → runtime-native tool / extension / script
```

### Agent Skills｜Agent 技能开放格式

**Classification:** Open Format

以包含 `SKILL.md` 的目录封装可发现、按需加载的程序性知识、脚本与参考资料。

适合可复用的复杂方法，不适合存储动态模型信息、Task State 或长期项目事实。

### AGENTS.md｜Coding Agent 项目指令格式

**Classification:** Open Format / De facto Convention

面向 Coding Agent 提供项目级或目录级长期指令，适合构建、测试、代码规范与局部行为约束。

适合多个 Runtime 共享的轻量项目约束；不应承载会话状态、模型路由缓存或 Task State。

### ACP｜Agent Client Protocol（Agent 客户端协议）

**Classification:** Open Protocol

标准化 Editor / IDE / Agent Client 与 Coding Agent Runtime 之间的通信，使 Agent Runtime 与客户端 UI 解耦。

适合 IDE 嵌入、长期 Agent Host、跨客户端复用同一 Agent Runtime。

### A2A｜Agent2Agent Protocol（Agent 间协议）

**Classification:** Open Protocol

用于独立 Agent 系统之间的发现与任务协作。与 MCP 不同：MCP 主要连接 Tool / Data，A2A 连接独立 Agent。

当 Subagent 是远程独立 Agent Service，而不是当前 Runtime 的本地子会话时，可优先检查 A2A。

### Agent Plugins｜Agent 插件开放格式

**Classification:** Open Package Format

Agent Plugins 提供 vendor-neutral 的可移植插件封装。当前可移植核心以 Agent Skills 与 MCP Server 为主；Hooks、Agents、Rules 等 Runtime-specific 能力不能因为被某个 Plugin 支持就被视为统一标准。

---

## 3. Common Harness Primitives｜常见 Harness 原语

以下能力在主流 Coding Agent 中广泛存在，但没有统一、足够稳定的跨 Runtime 配置标准。Harness Compilation 只固化它们的语义。

| Primitive | 稳定语义 | 常见用途 |
|---|---|---|
| **Instruction / Rule** | 在某个用户、项目、目录或任务范围持续约束 Agent 行为。 | 项目规范、目录约束、长期执行原则。 |
| **Skill** | 可发现、可复用、按需加载的程序性方法。 | Debug 方法、CR 方法、专项流程。 |
| **Tool** | Agent 可调用的确定性或外部执行能力。 | Shell、搜索、浏览器、数据库、内部服务。 |
| **Agent / Subagent** | 具有独立 Prompt / Context / Tool / Permission 边界的执行单元。 | 上下文隔离、并行、独立审查、专门能力。 |
| **Hook / Event** | 在 Runtime 生命周期或 Tool 调用前后触发确定性逻辑。 | 审计、验证、拦截、自动化。 |
| **Permission / Gate** | 决定某类操作是否允许、询问或阻断。 | 高风险写入、网络、生产操作、不可绕过边界。 |
| **Sandbox** | 隔离 Agent 对 OS、文件、网络或进程的访问。 | 风险隔离、安全执行。 |
| **Workspace / Worktree** | 隔离不同执行单元的文件修改边界。 | 并行 Worker、Single Writer Boundary。 |
| **Context / Memory** | 管理当前执行可见信息与 Runtime 记忆。 | Fresh Review、Scoped Context、长期 Runtime 辅助。 |
| **Model Routing** | 在 Runtime 可用候选中选择执行模型。 | 最低充分能力、成本 / 延迟权衡。 |
| **Thinking / Reasoning** | 控制模型推理预算或深度。 | 复杂度、风险、失败历史驱动的动态能力调整。 |
| **Background / Concurrency** | 允许 Work Unit 异步或并行执行。 | 独立探索、批量检查、并行 Agent Work。 |
| **Plugin / Extension** | 向 Runtime 组合新增行为、Tool、Skill、Agent 或生命周期逻辑。 | Runtime-specific Harness 扩展与分发。 |

---

## 4. 语义边界

以下概念不得机械等价：

```text
Tool      ≠ MCP
Skill     ≠ Workflow
Subagent  ≠ Task
Hook      ≠ Gate
Sandbox   ≠ Worktree
Model     ≠ Agent
Memory    ≠ Canonical Context
Plugin    ≠ Agent Plugins Standard
```

例如：

- `Tool` 是 Harness Primitive，MCP 是实现外部 Tool / Resource 的一种开放协议；
- `Skill` 是程序性能力语义，Agent Skills 是其可移植表示之一；
- `Subagent` 是运行时执行单元，Formal Task 仍由 Spec Coding Task Contract 定义；
- Runtime Memory 只能辅助执行，不替代 Requirement / Design / Task / Evidence 等 Canonical Source of Truth。

---

## 5. Compilation Use｜编译使用方式

Harness Compilation 应按以下顺序使用 Reference：

```text
Workflow / Rule / Adoption Requirement
        ↓
Required Semantic Guarantee
        ↓
Required Harness Primitive Set
        ↓
Public Standard Adoption Reference
        ↓
Runtime Architecture Reference
        ↓
Current Official Evidence + Local Probe
        ↓
Runtime-native Mechanism
```

同一 Requirement 可以映射到多个 Primitive，同一 Primitive 也可能由多个 Runtime Surface 组合实现；不得采用“一条 Rule = 一个 Skill”“一个 Role = 一个固定 Subagent 文件”等机械转换。

当 Portable Surface 与 Runtime-native Surface 都能完整、可靠地满足同一 Contract 时，可优先可移植方案；若 Runtime-native Surface 提供 Contract 必需的更强隔离、权限或确定性保证，则优先原生机制。

> **Portable when equivalent; native when necessary｜等价时优先可移植，必要时优先原生能力。**

---

## 6. 维护边界

本文件只维护稳定 Primitive 语义与分类，不维护：

- 外部协议当前版本、成熟度或 Preview 状态；
- Runtime 当前版本；
- 当前模型或 Thinking 档位；
- 当前 Hook Event 数量；
- 当前 Feature Flag；
- Runtime-specific 配置字段；
- Pricing、Quota 或 Availability。

公开协议状态与 Freshness 由 [`harness-standards.md`](harness-standards.md) 维护；Runtime Architecture 与官方事实入口由 [`coding-agent-runtimes.md`](coding-agent-runtimes.md) 维护；当前环境能力由 [`../meta-protocols/harness-compilation.md`](../meta-protocols/harness-compilation.md) 的 Environment Discover 使用当前证据重新确认。
