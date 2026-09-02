# Meta Protocols｜元协议

本目录维护 Spec Coding 自身的 Meta Protocol（元协议）：它们不推进业务开发阶段，而是定义 Spec Coding 如何被项目接入、解释、装配或转换为可执行机制。

当前正式 Meta Protocol：

1. [`project-onboarding.md`](project-onboarding.md)：Project Onboarding Protocol（项目接入协议），在 Harness 之前建立、复用、刷新或迁移 Target 的 Adoption Baseline。
2. [`harness-compilation.md`](harness-compilation.md)：Harness Compilation Protocol（Harness 编译协议），消费有效 Adoption Baseline、Applicable Workflow / Rules 与当前项目能力；按需读取 Harness Primitive / Runtime Reference，将规范语义归一后，再结合当前官方资料与本地 Runtime Evidence 编译为最小充分 Harness，并按最低充分能力动态完成 Agent / Model / Thinking / Context / Tool / Workspace 路由。仓库自身的编译示例只在测试夹具中验证，不作为项目运行时入口。

正常依赖关系：

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
Enter / Resume Workflow
```

`按需` 表示：已有 Adoption Baseline 或 Harness 仍有效时直接复用，不为每个 Requirement / Task 机械重跑 Meta Protocol。

Meta Protocol 与 Workflow / Rules 的职责不同：Workflow 规定“怎么推进”，Rules 规定“什么必须持续成立”，Project Onboarding 规定“Spec Coding 如何在当前 Target 中使用”，Harness Compilation 规定“如何把这些规范变成当前环境中的可靠执行机制”。Agent Delegation & Coordination Rules 定义 Main Agent / Subagent 稳定协作语义，Harness Compilation 只负责把这些语义映射到当前 Coding Agent 的实际运行能力。

Harness Compilation 可消费 [`../reference/harness-primitives.md`](../reference/harness-primitives.md) 与 [`../reference/coding-agent-runtimes.md`](../reference/coding-agent-runtimes.md) 作为非规范编译知识；Reference 只提供共同语言、架构不变量与官方事实入口，当前 Runtime Capability 仍由编译时的 Current Official / Local Evidence 决定。

生成出的 Adoption Baseline 与 Harness 都不替代 Workflow / Rules 的规范事实源，Reference 也不成为新的规范事实源。

正式 Meta Protocol 必须在完成设计后登记到 [`../manifest.yaml`](../manifest.yaml)，不以空文档或占位协议提前形成事实源。
