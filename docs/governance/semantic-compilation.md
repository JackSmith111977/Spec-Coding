# Semantic Compilation｜规范语义编译

Semantic Compilation 是 Harness Compilation V3 的规范前端：在 Spec Coding 版本发布侧，将人类可读 Canonical Corpus 一次性转换为稳定、可追溯的 Semantic IR（语义中间表示）。它不属于目标项目 Workflow，也不接触目标 Runtime、Adoption 或 Harness 输出。

> **完整性在规范侧解决；定制化在目标侧解决。**

## 1. Source Resolution｜规范源解析

由 `VERSION + docs/manifest.yaml` 解析当前版本完整 Canonical Corpus：

- Main Workflow；
- Rules；
- Exception Workflow；
- Meta Protocol。

Reference、Overview、README 与治理说明不作为目标行为语义输入。解析结果绑定 Document Path、Kind、Owner 与 SHA-256；Markdown Heading 只用于定位，不再被当作“一个 Heading = 一个语义单元”。

## 2. Atomic Extraction｜原子语义提取

按文档隔离执行语义抽取。Extractor 先区分 `NORMATIVE / GUIDANCE / EXAMPLE / RATIONALE / NAVIGATION`，再把每个独立规范思想拆成 Atomic Clause。

Clause 只保留后续编译不可重新猜测的稳定语义：

- `kind`：`invariant / trigger / gate / transition / authority / artifact / routing`；
- `source`：Canonical Document + Anchor；
- `when`：适用条件；
- `must / must_not`：义务与禁止；
- `relations`：跨 Clause 的稳定执行关系。

一个 Source Span 可以产生多条 Clause；多个 Source 也可以共同支撑同一 Clause。不得为了减少 Clause 数量提前摘要或合并独立 Gate、Trigger、状态转换、权限边界与失败路由。

## 3. Semantic Integration｜语义整合

Per-document Extractor 结果先经 Fresh Review，再进入全局 Integration。Integration 只处理：

- 等价重复；
- Dependency；
- Specialization / stricter rule；
- Conflict；
- Hard Order；
- Trigger；
- Isolation Requirement。

稳定关系可使用 `requires / before / triggers / blocks / specializes / isolated_from`。

Spec Coding 可以规定“独立审查必须与实现上下文隔离”，但不在 Semantic IR 中规定“使用某 Vendor 的 Reviewer Subagent”。具体 Agent / Model / Thinking / Fresh / Fork / Workspace / Parallelism 属于后续 Runtime Strategy。

无法可靠消解的 Canonical Conflict 阻断 Semantic Release，并返回最早 Canonical Source 修正；不得在 IR 层静默选择一边。

## 4. IR Verification & Release｜IR 验证与发布

验证分为三层：

1. **Deterministic Integrity**：Scope / Version / Source Fingerprint、Clause ID、Source Binding、Relation Target、Hard-order Cycle 与 Stale IR；
2. **Semantic Completeness Review**：逐文档 Fresh Reviewer 检查是否仍有未进入 Clause 的 Normative Behavior；
3. **Semantic Mutation Review**：对 `MUST → SHOULD`、删除 Gate / Trigger、反转 Transition、扩大 Authority 等变异执行回读挑战，确保语义弱化可被发现。

只有整个 Canonical Corpus 均完成并通过上述审查，并由独立审查过程产生与同一 Source Fingerprint 绑定的独立 Review Receipt 时，才允许 `scope.mode = release`。IR 本身不内嵌“自己审查自己通过”的声明。Pilot 可以使用 `scope.mode = pilot` 验证 IR 表达力，但不得被描述为完整 Spec Coding Semantic Release。

正式派生产物保持轻量：

```text
semantic/
├── manifest.json
└── clauses.json
```

Canonical Markdown 始终是 Source of Truth；Semantic IR 是版本绑定的 Derived Release Artifact。发现 IR 错误时必须回到 Canonical Source 或 Extraction / Integration 过程修正并重新生成，不直接手工维护一套平行规范。

## 执行分工

```text
Source Resolver        → Deterministic Tool
Per-document Extractor → Agent
Per-document Reviewer  → Fresh Agent
Integrator             → Agent
Global Reviewer        → Fresh Agent
Integrity Validator    → Deterministic Tool
```

Semantic Compilation 的完成标准不是“扫描了所有 Markdown Block”，而是：

> **所有 Canonical Normative Semantics 均以 Atomic Clause 与必要执行关系被无损保存，且任何目标 Coding Agent 后续不需要重新从完整 prose 中发现这些规范语义。**
