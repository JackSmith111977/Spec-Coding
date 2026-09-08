# Meta Protocols｜元协议

本目录维护目标项目侧的 Meta Protocol（元协议）：它们定义 Spec Coding 如何与当前项目建立稳定接入关系，以及如何读取发行包、按环境适配并验收 Harness，随后移交业务 Workflow。

当前正式 Meta Protocol：

1. [`project-onboarding.md`](project-onboarding.md)：建立、复用、刷新或迁移稳定的 Adoption Baseline，只持久化长期意图与稳定绑定。
2. [`harness-adoption-and-adaptation.md`](harness-adoption-and-adaptation.md)：定义仓库与客户端共用的包消费契约，以及读取、环境发现、适配、验收和恢复步骤。

Harness 的维护者构建与发布不再属于目标项目 Meta Protocol。仓库维护者使用 [`../governance/harness-build-and-release.md`](../governance/harness-build-and-release.md) 将 Canonical Workflow / Rules / Meta Protocol 预编译、验证并发布为 Versioned Harness Package。

```text
Maintainers:
Canonical Docs
      ↓
Harness Build & Release
      ↓
Versioned Harness Package

Target:
Target / Intent + 固定发行包
      ↓
包内 Bootstrap 与预编译接入程序
      ↓
Project Onboarding → Adoption Baseline
      ↓
环境发现 → 适配与装配 → 验证与接管
      ↓
Workflow Entry / Resume
```

两份 Meta Protocol 均由维护者预编译到发行包。客户端从安装前可读取的 Bootstrap 启动，只处理当前 Runtime / Project 才能确定的动态环境差异，不重新执行维护者的 Canonical → Harness 预编译。

两个协议在产物定位、存储、导航和维护时共同消费[产物组织与读取规则](../rules/artifact-organization-and-reading.md)；仅接入请求在适配验收后结束，具体开发目标由后续 Workflow 承接。

职责边界：

- Workflow：怎么推进；
- Rules：什么必须持续成立；
- Project Onboarding：当前 Target 如何与 Spec Coding 建立稳定接入关系；
- Harness Build & Release：维护者如何创建、验证和发布可复用 Harness Package；
- Target-side Adaptation：使用方如何读取包内要求，根据当前环境选配、增强并验收已发布 Package。

[`../reference/harness-primitives.md`](../reference/harness-primitives.md)、[`../reference/harness-standards.md`](../reference/harness-standards.md) 与 [`../reference/coding-agent-runtimes.md`](../reference/coding-agent-runtimes.md) 继续作为非规范 Reference。
