# Harness Package｜Harness 发行包

本目录是当前 Spec Coding 版本的可发布 Harness Package 入口。

当前阶段只建立发行边界，尚未生成正式全量 Package。后续 Harness Artifact 必须通过 [`../../docs/governance/harness-build-and-release.md`](../../docs/governance/harness-build-and-release.md) 的维护者流程创建、验证和发布。

目标结构优先遵循公开标准：

```text
packages/harness/
├── README.md
├── plugin.json              # 当采用 Agent Plugins 时
├── skills/                  # Agent Skills-compatible procedures
├── mcp.json                 # 只有存在 portable MCP provider 时才需要
├── bootstrap/               # portable bootstrap / routing assets
└── manifest.*               # 最薄的 build / release metadata
```

原则：

- 不在这里复制 Canonical Workflow / Rules 原文作为第二套事实源；
- 不保存 Semantic IR、Clause Release 或维护者构建 scratch state；
- 不把当前 Runtime / Model / Tool / Hook / Worktree 等动态环境事实固化进 Portable Package；
- 需要多个标准机制时直接组合；
- Runtime-specific enhancement 留给目标侧适配；
- `packages/harness/` 只维护当前版本，历史通过 Git Tag / GitHub Release 获取。

> **Build once, release a reusable package, adapt only what is environment-specific.｜稳定部分一次构建并发布，只适配环境相关差异。**
