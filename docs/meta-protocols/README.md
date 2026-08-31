# Meta Protocols｜元协议

本目录维护 Spec Coding 自身的 Meta Protocol（元协议）：它们不推进业务开发阶段，而是定义 Spec Coding 如何被项目接入、解释、装配或转换为可执行机制。

当前正式 Meta Protocol：

1. [`project-onboarding.md`](project-onboarding.md)：Project Onboarding Protocol（项目接入协议），在 Harness 之前建立、复用、刷新或迁移 Target 的 Adoption Baseline。
2. [`harness-compilation.md`](harness-compilation.md)：Harness Compilation Protocol（Harness 编译协议），消费有效 Adoption Baseline、Applicable Workflow / Rules 与当前项目能力，组合成最小充分 Harness。

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

Meta Protocol 与 Workflow / Rules 的职责不同：Workflow 规定“怎么推进”，Rules 规定“什么必须持续成立”，Project Onboarding 规定“Spec Coding 如何在当前 Target 中使用”，Harness Compilation 规定“如何把这些规范变成当前环境中的可靠执行机制”。生成出的 Adoption Baseline 与 Harness 都不替代 Workflow / Rules 的规范事实源。

正式 Meta Protocol 必须在完成设计后登记到 [`../manifest.yaml`](../manifest.yaml)，不以空文档或占位协议提前形成事实源。
