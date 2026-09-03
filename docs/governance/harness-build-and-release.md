# Harness Build & Release｜Harness 构建与发布

本文件定义 Spec Coding 仓库维护者如何从当前 Canonical Workflow / Rules / Meta Protocol 创建、更新、验证并发布可复用 Harness Package。

它属于 Governance（治理）与 Release Engineering（发布工程），**不属于目标项目 Coding Agent 的执行流程**。使用方只消费已发布 Harness Package，不参与预编译过程。

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

本流程覆盖首次创建、Canonical 更新、Harness 缺陷修复、外部标准 / Packaging 变化、组件删除、发布与回滚。

---

# 1. Build Scope Establishment｜构建范围建立

## 1.1 目标

确定本轮采用 **Full Build（全量构建）** 还是 **Incremental Build（增量构建）**，以及真正需要创建、更新或删除的 Harness Artifact。

本步骤只确定受影响范围，不重新解释 Canonical 行为。

## 1.2 Resolve Build Baseline｜解析构建基线

首次没有可信 Harness Release 时直接执行 Full Build：

```text
No previous valid Harness Release
        ↓
FULL BUILD
        ↓
Complete Canonical Corpus
```

后续构建以上一个正式 Harness Release 在 Build Manifest 中绑定的 `source_revision` 为基线，而不是简单使用 `HEAD~1`：

```text
Previous Release source_revision
            ↓
      Current Candidate
```

以下情况同样回退 Full Build：

- 找不到可信的上一版 Build Manifest / `source_revision`；
- Source → Artifact 映射缺失、损坏或无法解释；
- Packaging / Build Architecture 发生全局变化；
- 构建机制变化会影响全部 Artifact；
- Maintainer 明确要求 Full Rebuild。

> **Incremental when provable; full when uncertain.｜能证明影响范围时增量构建，不能证明时全量构建。**

## 1.3 Detect Delta｜识别变化

有可靠基线时，Canonical 变化优先由 Git Diff 识别：

```text
git diff --name-status --find-renames <source_revision> <candidate_revision>
```

Diff 负责识别 `Added / Modified / Deleted / Renamed` Source，**不负责判断修改是否“足够语义化”**。Canonical 文件发生变化时，相关 Harness Artifact 默认视为 stale 并重新构建；若最终生成内容未变化，可由 Artifact Hash 证明。

除 Canonical Diff 外，Scope 还可来自：

- **Harness Defect**：Canonical 未变，但已发布 Harness 存在遗漏、弱化、错误装配或不可用表达；
- **Standard / Packaging Delta**：Agent Skills、Agent Plugins、MCP、AGENTS.md 等采用方式变化并实质影响当前 Package。

仅 Reference 文案、官方 URL 或版本号变化本身，不自动触发 Harness 重建；只有 Build / Packaging Decision 变化时才进入 Scope。

## 1.4 Resolve Affected Outputs｜解析受影响产物

上一正式 Release 的 Build Manifest 保存：

```text
Harness Artifact
      ↓
Exact Canonical Source Files
```

增量构建时反向查询：

```text
Changed Canonical Source
        ↓
Previous Build Manifest
        ↓
Affected Harness Artifacts
```

处理规则：

- `Modified`：按上一版 Source → Artifact 映射反查；
- `Deleted`：必须使用上一版 Manifest 反查，不能依赖当前文件仍存在；
- `Renamed`：迁移旧 Source Mapping，并重建关联 Artifact；
- `Added`：根据所属 Canonical Workflow / Rule / Meta Protocol 分组确定候选 Artifact；无法可靠归属时由 Maintainer 建立首次绑定；
- `Harness Defect`：直接将已确认的 Artifact 加入 Scope；
- `Standard / Packaging Delta`：按受影响 Artifact Type 或 Package Surface 扩展 Scope。

Package Envelope（如 package manifest、artifact inventory、hash list、routing / bootstrap index）成本较低，**每次构建都重新生成**；只有 Skill、MCP、Bootstrap 等实际 Harness 内容采用增量重建。

## 1.5 Build Scope Result｜范围结果

Build Scope 只需要形成短生命周期结果：

```yaml
mode: full | incremental
baseline:
  version: <previous release>
  source_revision: <commit>
candidate_revision: <commit>
changes:
  - <changed source / defect / standard delta>
affected_artifacts:
  - <artifact id>
validation_focus:
  - <risk to challenge>
```

它属于 Build Internals，不是长期事实源。真正长期保存的是发布后的 Build Manifest。

## 1.6 完成条件

- 首次构建明确进入 Full Build；
- 增量构建绑定到上一正式 Release 的 `source_revision`；
- 所有 Diff / Defect / Standard Delta 均已解析到受影响 Artifact；
- 无法可靠解释的影响范围已回退 Full Build；
- 未把无关 Canonical / Harness 资产扩大进 Scope；
- 如果真正问题在 Canonical，已先修正 Canonical，而不是在 Harness 中覆盖错误。

---

# 2. Harness Precompile & Assembly｜Harness 预编译与装配

## 2.1 目标

直接读取当前 Canonical，并将 Build Scope 内 Harness Artifact 重新生成、装配为可验证的 Harness Package Candidate。

```text
Build Scope
      ↓
Direct Canonical Read
      ↓
Transform & Assemble
      ↓
Source Backcheck & Record
      ↓
Harness Package Candidate
```

> **Diff scopes the build; Canonical drives the content.｜Diff 只决定重建谁，Canonical 原文决定生成什么。**

## 2.2 Direct Canonical Read｜直接读取规范

Builder 直接读取当前 Canonical Markdown，不通过 Summary、Clause、IR 或其他 Agent 的二次转述替代原文。

### Full Build

首次 Full Build 依据 `docs/manifest.yaml` 的 Canonical 集合与 Rule 适用范围，逐 Artifact 直接读取所需 Workflow / Rule / Meta Protocol。可以分批处理，但每个 Builder 必须直接消费原始 Canonical。

### Incremental Build

Stage 1 只负责确定 `affected_artifacts`。一旦 Artifact 被判定为受影响，Builder 必须重新读取该 Artifact **完整、当前的 Canonical Sources**，再重新生成整个 Artifact。

```text
Git Diff
      ↓
Affected Artifact
      ↓
Reread complete current Canonical
      ↓
Rebuild complete Artifact
```

禁止将 Git Diff 作为 Harness 内容生成输入并直接 patch 旧 Artifact：

```text
Diff → patch old Skill        # 禁止
Diff → stale Artifact → reread Canonical → rebuild   # 正确
```

这样可以避免多轮增量构建积累语义漂移。

## 2.3 Transform & Assemble｜转化与装配

读取 Canonical 后直接转化为适合复用和分发的公开标准 / 开放格式，不增加长期中间表示。

### Standards-first Mapping｜标准优先映射

| Canonical / Capability | Preferred Harness Form |
|---|---|
| Workflow / Procedure | Agent Skills |
| Debug / Review / Onboarding Procedure | Agent Skills |
| Template / Example / Checklist / Reference | Skill `assets/` / `references/` |
| External Tool / Data / Resource | MCP |
| Portable Bundle | Agent Plugins |
| Bootstrap / Routing | AGENTS.md where supported |
| Runtime-specific Agent / Hook / Gate / Worktree / Model Routing | 留给目标侧 Runtime Adaptation |

一段行为需要多个 Harness Mechanism 时直接组合已有标准与必要 Runtime Requirement，不额外创造 Spec Coding 私有 Component Protocol。

信息转化以**执行保真与可达性**为目标，不以字数压缩率为目标：

```text
Main Procedure
→ SKILL.md

Supporting Guidance / Explanation / Example
→ references/ 或仍保留在 SKILL.md

Template / Checklist
→ assets/

Portable Capability
→ standard Harness surface

Runtime-specific Capability
→ requirement / adaptation boundary
```

转化必须保持以下不变量：

1. **Hard Semantics Preserved｜强语义完整**：`MUST / MUST NOT / Gate / Authority / Boundary / Trigger / State / Transition / Exception / Routing` 不得遗漏、弱化或改变；
2. **Procedure Preserved｜流程完整**：进入条件、执行步骤、推进条件、失败路由与结束条件保持连贯；
3. **Useful Guidance Reachable｜有效指导可达**：会影响 Agent 正确执行的启发式、解释和示例不得因精炼而消失；
4. **No Invented Norms｜禁止新增规范行为**：不得把 Guidance 擅自升级为 MUST，也不得新增 Canonical 不存在的 Gate / Authority / Boundary。

## 2.4 Source Backcheck & Record｜原文回查与记录

Artifact 生成后，Builder 必须直接回到本轮实际读取的 Canonical 原文进行一次 Source Backcheck（原文回查）：

```text
Current Canonical
       ↕
Generated Harness
```

至少检查：

- Hard Semantics 是否遗漏、弱化或冲突；
- Procedure 是否断裂或改变执行顺序；
- Gate / Authority / Boundary 是否仍保持原意；
- Exception / Routing 是否完整；
- 对执行有价值的 Guidance / Example 是否仍然可达；
- Harness 是否新增 Canonical 不存在的强制行为。

发现问题时直接修正 Harness 并再次回查。此步骤不生成持久化 Coverage IR、Mapping DSL 或新的事实源；独立 Fresh Review 仍由 Stage 3 负责。

回查通过后更新 Build Manifest。`sources` 表示**生成当前 Artifact 时实际直接读取并依赖的 Canonical 文件**，而不是摘要、IR、宽泛目录或推理中间产物：

```yaml
version: 0.12.0
source_revision: <verified source commit>
artifacts:
  - id: requirement-clarification
    type: agent-skill
    sources:
      - docs/workflows/main/02-requirement-clarification/01-requirement-interpretation.md
      - docs/workflows/main/02-requirement-clarification/02-ambiguity-gap-identification.md
      - docs/workflows/main/02-requirement-clarification/03-scope-rule-confirmation.md
      - docs/workflows/main/02-requirement-clarification/04-acceptance-criteria-confirmation.md
      - docs/rules/human-agent-collaboration.md
    requires:
      - human-interaction
    sha256: ...
```

Build Manifest 只记录最终派生关系与内容身份，不记录 Builder 摘要、推理过程或审查 scratch state。

## 2.5 完成条件

- Scope 内 Artifact 已创建 / 更新 / 删除；
- 所有受影响 Artifact 均由完整当前 Canonical 重新读取并生成，而不是按 Diff patch；
- Portable Artifact 优先使用公开标准且未弱化 Canonical 语义；
- Hard Semantics、Procedure 与执行所需 Guidance 保持完整可达；
- Runtime-specific 能力只保留 Requirement / Extension Boundary；
- Builder Source Backcheck 已完成且无未处理偏差；
- Build Manifest 已更新 `source_revision`、实际直接读取的 Source Trace 与 Artifact Hash；
- Package Envelope 已基于当前候选全量重生成。

---

# 3. Package Verification & Review｜包验证与独立审查

## 3.1 目标

证明候选 Package **完整、准确地表达 Canonical 行为，并能作为真实 Harness 被 Agent 消费**。

```text
Canonical Docs
      ↕
Generated Harness Package
```

## 3.2 Structural Verification｜结构验证

优先确定性检查：

- Agent Skill / Agent Plugin / MCP / Bootstrap 格式；
- 引用、路径、Assets / References；
- Build Manifest、`source_revision`、Source Trace；
- Artifact Hash；
- 悬空引用、重复文件和旧版本残留。

## 3.3 Semantic Review｜语义审查

由与生成过程尽量隔离的 Reviewer 直接对照 Canonical 与候选 Harness，重点检查：

- `MUST / MUST NOT / Gate / Authority / Trigger / Routing` 是否遗漏或弱化；
- 是否新增 Canonical 不存在的强制行为；
- Guidance 是否被错误升级为 Normative Rule；
- 阶段边界、状态推进、Human Authority 是否发生漂移；
- Procedure、边界说明和必要示例是否仍足以支持 Agent 执行；
- Rule 分散到多个 Skill / Bootstrap 后是否出现语义空洞或冲突。

## 3.4 Behavioral Test｜行为测试

对高价值 / 高风险 Harness 使用 Fresh Agent 或隔离 Session 挑战代表性场景：

```text
normal process
boundary
authority / gate
exception / routing
```

具体 Runtime compatibility 留给目标侧适配和认证，不要求 Portable Build 穷举全部 Runtime。

## 3.5 Failure Routing｜失败回流

```text
Canonical semantics wrong → Canonical Source
Generated expression wrong → Precompile
Package structure wrong → Assembly
Test / Review design wrong → Verification assets
```

最终结论只使用 `PASS / BLOCKED`。

---

# 4. Release & Lifecycle Convergence｜发布与生命周期收敛

## 4.1 Version Binding｜版本绑定

当前阶段默认：

```text
Spec Coding VERSION = Harness Package VERSION
```

不提前建立 IR / Component / Compiler / Bundle 的独立版本森林。

## 4.2 Release Content｜发布内容

正式 Release 至少包含：

- 当前 Harness Package；
- Build Manifest；
- 必要 Integrity Metadata；
- Release Note / CHANGELOG；
- 已确认的最低兼容 / 使用约束。

`packages/harness/` 只维护当前版本；历史通过 Git Tag / GitHub Release 获取。

## 4.3 Create / Update / Remove｜组件生命周期

```text
Create → Build → Verify → Release
Update → Affected Build → Verify → Release
Remove → Prove behavior remains covered → Remove → Verify → Release
```

## 4.4 Rollback｜回滚

发布后发现 Harness Defect 时：能安全修复则进入新 Build Scope；无法立即可靠修复则回滚到最近已验证 Release。不得手工修改 Release Artifact 绕过 Source / Build / Verification Trace。

## 4.5 完成条件

- Package 版本与仓库版本事实一致；
- Release Artifact 与验证通过的 Candidate 一致；
- Build Manifest 绑定最终 `source_revision`；
- Release Note / CHANGELOG 能解释实际行为变化；
- 后续 Target 只需消费已发布 Package。

---

# 5. 与其他流程的边界

## Process Review Improvement｜流程复盘改进

Stage 7 负责“为什么改、问题根因是什么、应该修改哪一层”；本流程负责“已经确定的 Canonical / Harness 变化如何构建、验证和发布”。

## Project Onboarding｜项目接入

Project Onboarding 只建立 Adoption Baseline，不参与 Harness Build。

## Target-side Harness Adaptation｜目标侧 Harness 适配

目标 Coding Agent 只消费 Released Harness Package，并根据当前 Runtime / Project 完成必要 Adaptation / Enhancement / Acceptance；它不重新执行 Canonical → Harness 预编译。

---

# 6. 最终原则

- **Canonical Only｜Canonical 唯一事实源**；
- **Full first｜首次构建全量建立 Package 与 Source Mapping**；
- **Diff-driven after release｜后续以上一正式 Release 为基线增量构建**；
- **Diff scopes, Canonical generates｜Diff 只定范围，Canonical 原文负责生成**；
- **Reread before rebuild｜受影响 Artifact 每次从完整当前 Canonical 重读重建**；
- **Incremental when provable｜能证明范围时增量，不能证明时全量**；
- **Standards first｜公开标准优先**；
- **Compose, don't reinvent｜组合已有机制，不创造无必要协议层**；
- **Backcheck against source｜生成后直接回到 Canonical 原文检查转化保真**；
- **Build internals stay internal｜构建内部状态不暴露给使用方**；
- **Release is versioned｜使用方只消费经过验证的版本化 Harness Package**。
