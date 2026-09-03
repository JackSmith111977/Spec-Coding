# Meta Protocols｜元协议

本目录维护目标项目侧的 Meta Protocol（元协议）：它们不推进业务开发阶段，而是定义 Spec Coding 如何与当前项目建立稳定接入关系。

当前正式 Meta Protocol：

1. [`project-onboarding.md`](project-onboarding.md)：建立、复用、刷新或迁移稳定的 Adoption Baseline，只持久化长期意图与稳定绑定。

Harness 的维护者构建与发布不再属于目标项目 Meta Protocol。仓库维护者使用 [`../governance/harness-build-and-release.md`](../governance/harness-build-and-release.md) 将 Canonical Workflow / Rules / Meta Protocol 预编译、验证并发布为 Versioned Harness Package。

```text
Maintainers:
Canonical Docs
      ↓
Harness Build & Release
      ↓
Versioned Harness Package

Target:
Target / Intent
      ↓
Project Onboarding
      ↓
Adoption Baseline
      ↓
Released Harness Package Adoption / Adaptation
      ↓
Workflow Entry / Resume
```

目标侧 Released Harness Package Adoption / Adaptation 将作为后续独立协议设计。它只处理当前 Runtime / Project 才能确定的动态环境差异，不重新执行维护者的 Canonical → Harness 预编译。

职责边界：

- Workflow：怎么推进；
- Rules：什么必须持续成立；
- Project Onboarding：当前 Target 如何与 Spec Coding 建立稳定接入关系；
- Harness Build & Release：维护者如何创建、验证和发布可复用 Harness Package；
- Target-side Adaptation：使用方如何根据当前环境选配、增强并验收已发布 Package（后续单独定义）。

[`../reference/harness-primitives.md`](../reference/harness-primitives.md)、[`../reference/harness-standards.md`](../reference/harness-standards.md) 与 [`../reference/coding-agent-runtimes.md`](../reference/coding-agent-runtimes.md) 继续作为非规范 Reference。
