# Harness Adapt V3

Harness Adapt 是 Harness Compilation V3 的第三阶段工具层。它消费 Semantic IR、Environment Model 与 Adoption Context，把规范语义转换为当前环境中的最小充分 Harness Candidate。

它回答：

> **当前 Clause 需要什么能力，由哪个可靠 Provider 提供，并以什么最小组件实现？**

## Flow

```text
Semantic IR + Environment Model + Adoption Context
        ↓
prepare
        ↓
Per-Clause Capability Worklist
        ↓
Agent derives Capability Requirements
        ↓
Provider Resolution & Selection
        ↓
Harness Planning & Synthesis
        ↓
validate
        ↓
Harness Candidate
```

## Capability Requirement Analysis

`prepare` 为每条 Semantic Clause 生成不可跳过的 `derive_capability_requirements` 工作项。Agent 只提取稳定能力需求 / Harness Primitive，不直接选择 Pi Package、Claude Plugin、AGENTS.md 或 Subagent。

## Provider Resolution & Selection

Provider 是能力实现候选，不等于 Coverage，也不等于 Harness。Provider Source 使用 `runtime_native / project_existing / installed_extension / registry / external / custom`；先满足 Semantic Sufficiency，再优化已有复用、信任、依赖、权限风险与维护成本。

`registry` Provider 必须引用 Environment Discovery 已确认的 `provider_surface`。需要安装 / 配置 / 连接 / 构建的 Provider 必须明确 Authority；需要 Human Approval 时，没有 Approval Evidence 不得通过第三阶段。

## Harness Planning & Synthesis

多个 Clause 可以共享同一个 Component，但 Clause Coverage 不能消失。Component 使用 `reuse / configure / create`；实际 Artifact 可以是 Instruction、Skill、Hook、Script、MCP 配置、Plugin 配置、Agent Profile 等当前 Runtime 可加载 Surface。

## Candidate Validation

`validate` 检查 Clause → Capability Requirement → Selected Provider → Component → Artifact 的完整追踪、Provider Evidence / Authority、Registry Surface、Provider Change 的 Targeted Refresh Evidence、Artifact 边界 / 存在性与结构性 Minimality。

工具通过只表示 **Harness Candidate 的适配链完整且可进入第四阶段**，不表示 Runtime 已真实加载，也不替代 Semantic Mutation / Fresh-agent Behavioral Acceptance。

## Provider Surface Boundary

Environment Discover 只记录“可以去哪里查找额外能力”，例如 Pi Packages、Runtime Plugin Registry、MCP Registry 或项目 Package Manager；不预加载完整市场目录。Harness Adapt 只有在 Capability 缺口真实存在时才按需查询。

> **Coverage is the result; Provider is the implementation source.**
