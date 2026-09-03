# Harness Build & Release｜Harness 构建与发布

本文件定义 Spec Coding 仓库维护者如何从当前 Canonical Workflow / Rules / Meta Protocol 创建、更新、验证并发布可复用 Harness Package。

它属于 Governance（治理）与 Release Engineering（发布工程），**不属于目标项目 Coding Agent 的执行流程**。使用方只消费已发布 Harness Package，不需要参与本文件描述的预编译过程。

> **Canonical defines behavior; released Harness is derived.｜Canonical 定义行为，发布 Harness 是派生产物。**

---

## 1. 总体流程

```text
Canonical Workflow / Rules / Meta Protocol
                    ↓
1. Build Scope Establishment
   构建范围建立
                    ↓
2. Harness Precompile & Assembly
   Harness 预编译与装配
                    ↓
3. Package Verification & Review
   包验证与独立审查
                    ↓
4. Release & Lifecycle Convergence
   发布与生命周期收敛
                    ↓
       Versioned Harness Package
```

本流程同时覆盖：

- 首次创建 Harness 资产；
- Canonical 变化后的更新；
- Harness 编译缺陷修复；
- 外部标准 / Packaging 变化后的重建；
- 已无价值资产的删除；
- 版本发布与回滚。

---

# 1. Build Scope Establishment｜构建范围建立

## 1.1 目标

确定**为什么需要构建、哪些 Canonical Source 或构建机制受影响、哪些 Harness Artifact 需要创建 / 更新 / 删除**。

本步骤只建立受影响范围，不重新解释或修改已经确认的 Canonical 行为。

## 1.2 构建触发

### Canonical Change

Workflow、Rule 或 Meta Protocol 的行为语义发生变化：

```text
Canonical Change
      ↓
Affected Harness Rebuild
```

### Harness Defect

Canonical 正确，但已生成 Harness 存在遗漏、弱化、越权、错误装配或不可用表达：

```text
Canonical unchanged
      ↓
Fix Build / Artifact
      ↓
Rebuild
```

### Standard / Packaging Change

Agent Skills、Agent Plugins、MCP、AGENTS.md 等外部标准或 Packaging 约定变化，而 Canonical 语义未变：

```text
Standard / Packaging Delta
      ↓
Affected Builder / Package Update
```

外部标准事实以 [`../reference/harness-standards.md`](../reference/harness-standards.md) 的当前采用基线与官方来源为准。

## 1.3 Scope 判定

至少确认：

- `reason`：本轮构建触发类型；
- `sources`：受影响 Canonical Source；
- `outputs`：需要创建 / 更新 / 删除的 Harness Artifact；
- `semantic_change`：是否涉及 Canonical 行为语义变化；
- `validation_focus`：本轮特别需要挑战的风险点。

可以使用临时 Build Scope 清单，但不要求建立复杂 DSL 或长期状态机。

## 1.4 完成条件

- 构建原因清楚；
- 受影响 Source 与 Output 可以追溯；
- 未把无关 Canonical / Harness 资产扩大进本轮改动；
- 如果真正问题在 Canonical，已先回到 Canonical 修正，而不是在 Harness 中覆盖规范错误。

---

# 2. Harness Precompile & Assembly｜Harness 预编译与装配

## 2.1 目标

直接从当前 Canonical 文档生成适合复用和分发的 Harness Artifact，并优先采用业界已有公开标准 / 开放格式。

```text
Canonical Docs
      ↓
Understand stable behavior
      ↓
Select standard Harness form
      ↓
Generate / Update / Remove artifacts
      ↓
Assemble Harness Package
```

## 2.2 Standards-first Mapping｜标准优先映射

默认优先级：

| Canonical / Capability | Preferred Harness Form |
|---|---|
| Workflow / Procedure | Agent Skills |
| Debug / Review / Onboarding Procedure | Agent Skills |
| Template / Example / Checklist / Reference | Skill `assets/` / `references/` |
| External Tool / Data / Resource | MCP |
| Portable Bundle | Agent Plugins |
| Bootstrap / Routing | AGENTS.md where supported |
| Runtime-specific Agent / Hook / Gate / Worktree / Model Routing | 不强行标准化，留给目标侧 Runtime Adaptation |

如果一段行为需要多个 Harness Mechanism 承载，直接组合已有标准和 Runtime Requirement，不再为“组合”额外创造 Spec Coding 私有 Component Protocol。

> **Use standards as artifacts; use Spec Coding only for the semantics standards cannot define.｜标准负责产物形式，Spec Coding 只定义标准本身无法替代的行为语义。**

## 2.3 Canonical-first Generation｜Canonical 直接生成

Harness Artifact 直接消费 Canonical Workflow / Rules / Meta Protocol，而不是先生成长期 Semantic IR 再从 IR 重建流程。

原因：

- Canonical prose 保留 Procedure、例子、上下文和启发式表达；
- 这些信息对 Agent Skills 等程序性资产本身有直接价值；
- 额外 IR 层会引入再次拆解与重组，并增加同步和审计成本。

构建内部**可以**临时使用：

- Worklist；
- Checklist；
- 原子化语义拆解；
- Fresh Reviewer；
- Mutation / Adversarial Challenge；
- 任何有助于提高构建可靠性的确定性工具。

但这些只属于 **Build Internals（构建内部实现）**，不作为正式 Release Artifact，也不要求使用方 Coding Agent 消费。

## 2.4 Build Manifest｜构建清单

Package 只需要维护最薄的构建 / 发布追踪信息，用于回答：

- 这个 Artifact 来自哪些 Source；
- 它依赖哪些目标环境能力；
- 内容身份是什么；
- 当前版本是什么。

示意：

```yaml
version: 0.12.0
artifacts:
  - id: requirement-clarification
    type: agent-skill
    sources:
      - docs/workflows/main/02-requirement-clarification/
    requires:
      - human-interaction
    sha256: ...
```

Build Manifest 是 Release Bill of Materials（发布物料清单），**不是新的 Harness Protocol 或第二套规范事实源**。

## 2.5 完成条件

- 所有 Scope 内 Output 已创建 / 更新 / 删除；
- Portable Artifact 优先使用公开标准且没有为了可移植性弱化 Canonical 语义；
- Runtime-specific 能力只以 Requirement / Extension Boundary 保留，没有伪造跨 Runtime 标准；
- Package 内不存在明显重复实现；
- Source Trace 与内容 Hash 可以建立。

---

# 3. Package Verification & Review｜包验证与独立审查

## 3.1 目标

证明当前候选 Package **完整、准确地表达 Canonical 行为，并能作为真实 Harness 被 Agent 消费**。

验证对象是：

```text
Canonical Docs
      ↕
Generated Harness Package
```

而不是验证某个额外 IR 是否自洽。

## 3.2 Structural Verification｜结构验证

能确定性检查的先确定性检查，例如：

- Agent Skill / Agent Plugin / MCP / Bootstrap 格式是否合法；
- 引用、路径、Assets / References 是否真实存在；
- Package Metadata / Build Manifest 是否完整；
- Source Trace 是否指向当前 Canonical；
- Artifact Hash 是否与真实内容一致；
- 不存在悬空引用、重复文件或旧版本残留。

> **Deterministic first｜能确定性验证的先确定性验证。**

## 3.3 Semantic Review｜语义审查

由与生成过程尽量隔离的 Reviewer 直接对照 Canonical 与候选 Harness，重点检查：

- Canonical `MUST / MUST NOT / Gate / Authority / Trigger / Routing` 是否遗漏或弱化；
- Harness 是否新增 Canonical 不存在的强制行为；
- 是否把 Guidance 错误升级为 Normative Rule；
- 是否改变阶段边界、状态推进或 Human Authority；
- 是否保留对 Agent 实际执行有价值的 Procedure、边界说明和必要示例；
- 复杂 Rule 被分散编入多个 Skill / Bootstrap 时，是否存在语义空洞或重复冲突。

如果临时语义拆解有助于审查，可以使用；它仍然只作为 Review Technique（审查技术），不形成发布 IR。

## 3.4 Behavioral Test｜行为测试

对于高价值 / 高风险 Harness，使用 Fresh Agent 或隔离 Session 直接消费候选 Package，至少抽取代表性场景挑战：

```text
normal process
boundary
authority / gate
exception / routing
```

需要时再增加 Runtime Loader / Capability 测试；具体 Runtime compatibility 属于后续目标侧适配和认证范围，不要求在 Portable Build 阶段穷举所有 Runtime。

## 3.5 Failure Routing｜失败回流

```text
Canonical semantics wrong
→ Canonical Source

Generated expression wrong / missing
→ Precompile

Package structure / assembly wrong
→ Assembly

Test / Review design wrong
→ Verification assets
```

Verification 负责发现与归因，不在验证层直接形成新的行为事实源。

## 3.6 完成条件

只有同时满足以下条件才允许进入发布：

- Structural Verification 通过；
- Semantic Review 无 Blocking Finding；
- 必要 Behavioral Test 通过；
- Source Trace / Hash 与当前候选 Package 一致；
- 已知高风险语义没有未处理缺口。

最终结论只使用：

```text
PASS
BLOCKED
```

---

# 4. Release & Lifecycle Convergence｜发布与生命周期收敛

## 4.1 目标

将已经通过验证的 Harness Package 形成清晰、可追溯、可升级和可回滚的正式发行。

## 4.2 Version Binding｜版本绑定

当前阶段默认：

```text
Spec Coding VERSION
=
Harness Package VERSION
```

不提前建立 `semantic_ir_version / component_version / compiler_version / bundle_version` 等独立版本体系。

只有未来出现真实独立生命周期需求时再拆分版本。

## 4.3 Release Content｜发布内容

正式 Release 至少包含：

- 当前 Harness Package；
- Package / Build Manifest；
- 必要 Integrity Metadata；
- Release Note / CHANGELOG 中的相关行为变化；
- 对外说明的最低兼容 / 使用约束（如果已确认）。

当前仓库只维护**当前版本**的 Package 结构；历史版本通过 Git Tag / GitHub Release 获取，不在 `packages/` 下长期保存 `old / vN / backup` 平行副本。

## 4.4 Create / Update / Remove｜组件生命周期

同一流程同时处理创建、更新和删除：

```text
Create
→ Build → Verify → Release

Update
→ Affected Build → Verify → Release

Remove
→ Prove required behavior remains covered
→ Remove → Verify → Release
```

组件已经存在不意味着必须永久保留。若某资产被标准能力、其他 Harness 机制或更简单实现替代，可以删除，只要 Canonical 行为仍有可靠承载。

## 4.5 Rollback｜回滚

若发布后发现 Harness Defect：

- 能安全修复时进入新的 Build Scope；
- 影响当前可靠性且无法立即修复时，回滚到最近已验证 Release；
- 不通过手工修改发布包绕过 Source / Build / Verification Trace。

## 4.6 完成条件

- Package 版本与仓库版本事实一致；
- Release Artifact 与验证通过的 Candidate 内容一致；
- Release Note / CHANGELOG 能解释实际行为变化；
- 历史通过 Git / Release 治理，没有平行旧副本；
- 后续 Target 只需取得已发布 Package，不需要重新执行维护者预编译流程。

---

# 5. 与其他流程的边界

## Process Review Improvement｜流程复盘改进

Stage 7 负责：

```text
为什么要改？
问题根因是什么？
应该修改 Workflow / Rule / Meta Protocol / Harness 哪一层？
```

本流程负责：

```text
已经确定的 Canonical / Harness 变化
如何构建、验证和发布？
```

因此：

```text
EV → ISS → RC → IMP
          ↓
若需要 Canonical Change
→ 先修改 Canonical
          ↓
Harness Build & Release
```

## Project Onboarding｜项目接入

Project Onboarding 属于目标项目侧，只建立 Adoption Baseline。它不参与 Harness Build，也不需要知道维护者构建内部如何完成。

## Target-side Harness Adaptation｜目标侧 Harness 适配

目标 Coding Agent 只消费 Released Harness Package，并根据当前 Runtime / Project 环境完成必要 Adaptation / Enhancement / Acceptance。该流程与维护者 Build & Release 分离，后续单独设计。

---

# 6. 最终原则

- **Canonical Only｜Canonical 唯一事实源**；
- **Build once｜稳定行为由维护者预编译**；
- **Standards first｜公开标准优先**；
- **Compose, don't reinvent｜需要多个机制时直接组合，不创造无必要协议层**；
- **Verify against source｜生成 Harness 直接对照 Canonical 验证**；
- **Build internals stay internal｜构建内部技术不暴露给使用方**；
- **Version the package｜以正式 Package + Release 管理分发**；
- **Adapt only dynamic facts｜目标侧只处理当前环境才能确定的差异**。
