# Reference｜参考资料

本目录维护 Spec Coding 的非规范知识层，为 Human 设计与 Harness Compilation 提供统一术语、抽象能力、公开标准和 Runtime 架构参考。

Reference 不定义 Workflow、Rule 或 Meta Protocol，也不作为当前 Runtime Capability 的最终事实源；当前能力始终由 Environment Discover 使用 Local / Official Evidence 重新确认。

## 文档职责

| 文档 | 回答的问题 |
|---|---|
| [`glossary.md`](glossary.md) | Spec Coding 中关键术语是什么意思？ |
| [`harness-primitives.md`](harness-primitives.md) | Harness 有哪些稳定、跨 Runtime 的抽象能力？ |
| [`harness-standards.md`](harness-standards.md) | 哪些能力已有公开协议 / 开放格式，Portable 与 Runtime Adapter 的边界如何划分？ |
| [`coding-agent-runtimes.md`](coding-agent-runtimes.md) | 各 Coding Agent 的稳定架构特征是什么，编译时应去哪里重新获取官方事实？ |

## 使用顺序

```text
Semantic Requirement
        ↓
Harness Primitive
        ↓
Harness Standard / Open Format
        ↓
Runtime Architecture
        ↓
Current Official + Local Evidence
        ↓
Runtime-native Harness
```

其中：

- `harness-primitives.md` 维护稳定能力语言，不追逐 Runtime 当前配置；
- `harness-standards.md` 维护公开协议的采用基线、官方 Source 与 Freshness；
- `coding-agent-runtimes.md` 维护 Runtime Architecture Invariant 与可重新 fetch 的官方入口；
- Fast-changing 外部事实只有在当前设计相关时才刷新，遵循 **Stale + Relevant → Refresh**。
