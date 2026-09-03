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

## Build Manifest｜构建清单

Build Manifest 同时承担 Package BOM（发布物料清单）与后续增量构建的 Source Mapping（来源映射），至少记录：

```yaml
version: <harness package version>
source_revision: <verified canonical commit>
artifacts:
  - id: <artifact id>
    type: <agent-skill | mcp | bootstrap | ...>
    sources:
      - <exact canonical source file>
    requires:
      - <portable capability requirement>
    sha256: <artifact content hash>
```

`sources` 表示**生成当前 Artifact 时 Builder 实际直接读取并依赖的 Canonical Markdown 文件**。它不是摘要来源、IR、宽泛目录或推理中间产物。

首次 Full Build 建立 `artifact → exact source files` 映射；后续构建以上一正式 Release 的 `source_revision` 为 Git Diff 基线，并反向查询 Source → Artifact 得到增量 Build Scope。受影响 Artifact 重建后，必须根据本轮真实直接读取的 Canonical 刷新 `sources`。

原则：

- 不在这里复制 Canonical Workflow / Rules 原文作为第二套事实源；
- 不保存 Semantic IR、Clause Release、Builder Summary、Coverage Scratch State 或其他维护者构建中间层；
- `sources` 记录实际直接读取的精确 Canonical 文件，不记录宽泛目录；
- Git Diff 只用于确定 Build Scope，不能替代 Canonical 作为 Harness 生成输入；
- 受影响 Artifact 必须从完整当前 Canonical 重新生成，不能按 Diff 直接 patch 旧 Harness；
- 不把当前 Runtime / Model / Tool / Hook / Worktree 等动态环境事实固化进 Portable Package；
- Package Envelope 每次构建全量重生成，实际 Harness 内容可以按 Scope 增量重建；
- 需要多个标准机制时直接组合；
- Runtime-specific enhancement 留给目标侧适配；
- `packages/harness/` 只维护当前版本，历史通过 Git Tag / GitHub Release 获取。

> **Build once, release a reusable package, adapt only what is environment-specific.｜稳定部分一次构建并发布，只适配环境相关差异。**
