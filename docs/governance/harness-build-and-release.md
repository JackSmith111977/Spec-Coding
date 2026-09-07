# Harness Build & Release｜Harness 构建与发布

本文件定义 Spec Coding 仓库维护者如何从当前 Canonical Workflow / Rules / Meta Protocol 创建、更新、验证并发布可复用 Harness Package。

它属于 Governance（治理）与 Release Engineering（发布工程），**不属于目标项目 Coding Agent 的执行流程**。正式使用方只消费已发布 Harness Package，不参与预编译过程；维护者可在 Stage 3 受控地验证未发布候选。

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

维护者输出与目标侧输入统一遵循 [`Harness 读取与适配：包消费契约`](../meta-protocols/harness-adoption-and-adaptation.md#2-package-consumption-contract包消费契约)。Build 负责提供完整的包内入口、行为、适配要求和验收依据；目标侧按该契约读取和实现环境差异。

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

- **Manifest Delta｜规范清单变化**：比较上一 `source_revision` 与当前候选源版本中的 `docs/manifest.yaml`，识别规范登记、所属阶段、Rule 适用范围、入口 / 路由以及其他影响构建解释的字段变化；即使 Markdown 文件没有变化，也必须进入范围判定；
- **Harness Defect**：Canonical 未变，但已发布 Harness 存在遗漏、弱化、错误装配或不可用表达；
- **Standard / Packaging Delta**：Agent Skills、Agent Plugins、MCP、AGENTS.md 等采用方式变化并实质影响当前 Package。

仅 Reference 文案、官方 URL 或版本号变化本身，不自动触发 Harness 重建；只有 Build / Packaging Decision 变化时才进入 Scope。

两侧 Manifest 必须与各自源版本绑定，不能用当前 Manifest 解释旧 Release 的适用关系。纯导航文案或版本元数据变化可只刷新相应 Package Envelope；涉及执行路由或行为适用范围的变化必须传播到实际 Harness 内容。无法判断新字段或 Schema 变化的影响时回退 Full Build。Manifest 是构建输入，不因此计入 Canonical 正文数量或混入 Artifact 的 `sources`。

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
- `Manifest Delta`：联合旧、新规范集合及适用关系解析消费者。只从清单移除但仍在磁盘上的 Source 也按移除处理；新增登记按新增处理。Rule 适用范围、所属阶段或执行路由改变时，重建需要新增、移除或调整该行为的消费者及受影响共享依赖；不能只更新清单而保留旧 Skill 组合；
- `Harness Defect`：直接将已确认的 Artifact 加入 Scope；
- `Standard / Packaging Delta`：按受影响 Artifact Type 或 Package Surface 扩展 Scope。

Package Envelope（如 package manifest、artifact inventory、hash list、routing / bootstrap index）成本较低，**每次构建都重新生成**；只有 Skill、MCP、Bootstrap 等实际 Harness 内容采用增量重建。

正文 Source 映射与 Manifest 变化的影响集合取并集，再沿资产依赖扩展到受影响消费者。旧、新映射不能完整解释影响时回退 Full Build；`validation_focus` 必须包含适用范围增减、入口转换及共享规则组合的相关挑战。

## 1.5 Build Scope Result｜范围结果

Build Scope 只需要形成短生命周期结果：

```yaml
mode: full | incremental
baseline:
  version: <previous release>
  source_revision: <commit>
candidate_revision: <commit>
changes:
  - <正文变化 / 规范清单变化 / 缺陷 / 标准变化>
affected_artifacts:
  - <artifact id>
validation_focus:
  - <risk to challenge>
```

它属于 Build Internals，不是长期事实源。真正长期保存的是发布后的 Build Manifest。

## 1.6 完成条件

- 首次构建明确进入 Full Build；
- 增量构建绑定到上一正式 Release 的 `source_revision`；
- 所有正文 Diff / Manifest Delta / Defect / Standard Delta 均已解析到受影响 Artifact；
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

Full / Incremental Build 均按当前候选源版本的 Manifest 解释集合、适用条件和路由；即使正文未变，因 Manifest Delta 受影响的 Artifact 也必须按当前关系完整重建。旧 Manifest 仅用于判定变化范围，不用于生成新行为。

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

### Consumer Handoff｜消费者交接

按包消费契约装配接入入口及其依赖：

- 将 Project Onboarding 与 Harness Adoption & Adaptation 一并预编译；Bootstrap 提供安装前即可直接读取的入口，不能依赖尚未加载的 Skill 才能完成接入。
- 全局约束、阶段路由与异常触发必须在相关动作之前可取得；流程正文、Guidance 和参考资源可以渐进加载。
- 包内明确适用条件、共享依赖、环境能力的行为要求、允许适配边界和验收预期。能力名称不能替代完整要求，客户端不得被迫回读 Canonical 才能确定必要语义。
- 当前包内执行所需引用绑定同一发行版本。Runtime 动态事实留给客户端发现，不与稳定能力要求混淆。
- 检查完整 Canonical 集合中的适用行为是否都有承载位置，包括跨 Artifact 的共享规则与接入行为；不能只审查已经生成的 Artifact 而漏掉未分配的行为。

本节定义构建交付责任，具体信息要求以包消费契约为准，不另建平行格式。

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

同时提供 Artifact 实际路径及包内 Bootstrap / 路由入口定位。适用条件、依赖、适配要求与验收依据可直接放在资产正文或配套资源中，由清单或入口明确引用；不要求把自然语言契约展开为结构化 IR。完整性信息应覆盖执行所需文件，目录型资产须明确其文件清单与 Hash 计算范围。

## 2.5 完成条件

- Scope 内 Artifact 已创建 / 更新 / 删除；
- 所有受影响 Artifact 均由完整当前 Canonical 重新读取并生成，而不是按 Diff patch；
- Portable Artifact 优先使用公开标准且未弱化 Canonical 语义；
- Hard Semantics、Procedure 与执行所需 Guidance 保持完整可达；
- Runtime-specific 能力只保留 Requirement / Extension Boundary；
- Builder Source Backcheck 已完成且无未处理偏差；
- Build Manifest 已更新 `source_revision`、实际直接读取的 Source Trace 与 Artifact Hash；
- Package Envelope 已基于当前候选全量重生成。
- 包消费契约所需信息已随候选提供，客户端无需读取构建内部状态或重新预编译 Canonical。

---

# 3. Package Verification & Review｜包验证与独立审查

## 3.1 Goal & Candidate Freeze｜目标与候选固定

证明候选 Package **结构合法、语义忠实，并能作为真实 Harness 被 Agent 消费**。

进入验证后必须固定 Candidate 的内容身份（Commit / Hash）。验证期间一旦修改任何 Harness Artifact、Manifest 或 Package Envelope，当前 Candidate 即失效，必须形成新的 Candidate 并重新验证。

```text
Fixed Harness Package Candidate
        ↓
Structural Verification
        ↓
Independent Semantic Review
        ↓
Behavioral Challenge
        ↓
PASS / BLOCKED
```

> **Verify the exact candidate you intend to release.｜只验证准备发布的那个确定候选。**

## 3.2 Structural Verification｜结构验证

能确定性验证的全部优先使用确定性工具检查：

- Agent Skill / Agent Plugin / MCP / Bootstrap 格式；
- 引用、路径、Assets / References；
- Build Manifest、`source_revision` 与 Source Trace；
- Artifact Hash 与 Package Envelope；
- 悬空引用、重复文件和旧版本残留。
- 安装前入口及其必要引用可达，包内路径、版本绑定和完整性范围明确。

Structural Verification 不判断语义优劣，只证明候选包的结构与身份自洽。

## 3.3 Independent Semantic Review｜独立语义审查

使用与 Builder 尽量隔离的 Fresh Reviewer。Reviewer 必须直接读取 Canonical 原文与固定 Candidate，不依赖 Builder Summary、Stage 2 Source Backcheck 结论、Builder 推理或临时语义拆解作为判断依据。

```text
Canonical Docs
      ↕
Fixed Harness Candidate
```

重点检查：

- `MUST / MUST NOT / Gate / Authority / Boundary / Trigger / State / Transition / Exception / Routing` 是否遗漏、弱化或改变；
- 是否新增 Canonical 不存在的强制行为；
- Guidance 是否被错误升级为 Normative Rule；
- Procedure、阶段边界、状态推进与 Human Authority 是否发生漂移；
- 对 Agent 实际执行有价值的 Guidance / Example 是否仍然可达；
- Rule 分散到多个 Skill / Bootstrap 后是否出现语义空洞、重复或冲突。
- 从完整 Canonical 集合反查是否有适用行为没有承载位置；包内适配要求和验收预期是否足以指导客户端且未发明新的规范行为。

> **Reviewer reads Canonical directly.｜Reviewer 直接读 Canonical，不复用 Builder 的解释。**

## 3.4 Behavioral Challenge｜行为挑战

使用 Fresh Agent 或隔离 Session，只向 Test Agent 提供：

```text
Harness Candidate
+
Representative Scenario
```

**Test Agent 不读取 Canonical。** Canonical 只由 Reviewer 作为 Test Oracle（测试判定依据）判断行为是否符合预期，从而验证 Harness 本身是否足以驱动正确行为。

默认挑战四类场景：

```text
normal process
boundary
authority / gate
exception / routing
```

并根据 Stage 1 的 `validation_focus` 增加针对性场景。具体 Runtime Compatibility 留给目标侧适配和认证，不要求 Portable Build 穷举全部 Runtime。

首次构建或接入入口、消费契约发生变化时，按 [`受控候选验证`](../meta-protocols/harness-adoption-and-adaptation.md#31-受控候选验证) 从未安装 Harness 的起点执行包内 Bootstrap、Project Onboarding、环境发现、适配和验收，并在测试项目内执行约定场景，检查安装循环依赖和对 Canonical 的隐式依赖。

维护者将候选 Commit / 内容 Hash、测试项目和隔离范围、允许的副作用及停止条件作为 Scenario 中的显式测试授权。授权与测试记录位于冻结候选之外，不通过修改候选内容或伪造 Release Metadata 绕过发行检查。测试结论只对该候选及测试范围有效，作为 Stage 3 证据；不能代替完整发布验证或授予正式接入资格。

> **Test Agent reads Harness only.｜行为测试 Agent 只消费 Harness。**

## 3.5 Verification Scope｜验证范围

### Full Build

首次 Full Build 建立完整发行基线：

- Package Structural Verification 全量执行；
- Semantic Review 覆盖全部新生成 Harness Artifact；
- Behavioral Challenge 至少覆盖代表性跨 Workflow 场景。

### Incremental Build

后续增量构建：

- Package Structural Verification 仍然全量执行；
- Semantic Review 覆盖 Stage 1 的 `affected_artifacts`；
- Behavioral Challenge 围绕 `validation_focus` 与受影响行为执行；
- Global Rule、Bootstrap、Routing、Package Composition 或其他共享行为变化时，增加 Package-level Integration Challenge（包级集成挑战）。
- Manifest Delta 影响适用范围或消费者关系时，即使正文 Hash 不变，也对受影响消费者执行语义审查，并挑战行为新增、移除及路由转换。

未受影响且内容 Hash 未变化的 Artifact 不要求机械重复全文 Semantic Review；如果影响边界无法可靠证明，则扩大验证范围。

## 3.6 Verdict & Failure Routing｜结论与失败回流

最终结论只使用：

```text
PASS
BLOCKED
```

失败必须回到最早失真位置：

```text
Canonical semantics wrong → Canonical Source
Build Scope missed artifact → Stage 1 Build Scope
Generated expression wrong → Stage 2 Transform
Package / Manifest assembly wrong → Stage 2 Assembly
Verification method wrong → Stage 3 Verification
```

Stage 3 负责发现、归因和阻断，不直接修改 Candidate 后继续判定 PASS。任何修改都会产生新 Candidate，并重新进入验证。

只有同时满足以下条件才允许 PASS：

- Structural Verification 通过；
- Independent Semantic Review 无 Blocking Finding；
- 必要 Behavioral Challenge 通过；
- Candidate 内容身份与全部验证对象一致；
- 本轮 `validation_focus` 已得到覆盖。

---

# 4. Release & Lifecycle Convergence｜发布与生命周期收敛

## 4.1 Release Identity Convergence｜发布身份收敛

Stage 4 只接受 Stage 3 `PASS` 的固定 Candidate。进入最终验证前，应已确定本次预期发布身份；Stage 4 只核对，不再改变候选内容。

当前阶段保持：

```text
Spec Coding VERSION = Harness Package VERSION
```

发布前至少核对：

- Repository `VERSION`；
- `docs/manifest.yaml` 的版本 / 状态；
- Harness Package / Build Manifest version；
- Build Manifest 的 `source_revision`；
- Package / Artifact Hash 与通过验证的 Candidate；
- CHANGELOG / Release Note 与必要兼容约束。

如果此时必须修改 Harness Artifact、Build Manifest、Package Envelope 或其他会改变 Candidate 内容身份的发布元数据，则该 Candidate 失效，必须形成新 Candidate 并重新进入 Stage 3。

> **Release the verified candidate unchanged.｜发布已验证 Candidate 的原样内容。**

## 4.2 Publish Release｜正式发布

只有 `PASS` Candidate 可以形成正式 Release：

```text
Verified Candidate
        ↓
Merge / Release Commit
        ↓
Git Tag
        ↓
GitHub Release
```

正式 Release 至少绑定：

- Harness Package；
- Build Manifest 与 `source_revision`；
- Package version 与必要 Integrity Metadata；
- CHANGELOG / Release Note；
- 已确认的最低兼容 / 使用约束。
- 固定发行包的接入入口及其验证依据；随发布提供的验证记录应回指 Stage 3 候选身份，不修改已冻结包内容或形成自引用 Hash。

`packages/harness/` 只维护当前版本；历史通过 Git Tag / GitHub Release 获取，不维护平行版本目录。

## 4.3 Lifecycle Convergence｜生命周期收敛

发布后的任何变化都重新进入 Stage 1，包括：

- Canonical Delta；
- 影响构建解释的 Manifest Delta；
- Harness Defect；
- Standard / Packaging Delta；
- Artifact Add / Update / Remove。

```text
Post-release Delta
        ↓
Stage 1 Build Scope
        ↓
Stage 2 Build
        ↓
Stage 3 Verify
        ↓
Stage 4 Release
```

发布后发现 Harness Defect 时：能可靠修复则进入新的 Build Scope；无法立即可靠修复则回滚到最近已验证 Release。不得直接修改已发布 Artifact 绕过 Source / Build / Verification Trace。

> **Every post-release change re-enters the build pipeline.｜发布后的任何修改都重新进入构建链。**

## 4.4 完成条件

- Release identity 与 Stage 3 `PASS` Candidate 完全一致；
- Git Tag / GitHub Release 绑定正式版本与对应内容身份；
- Build Manifest、`source_revision` 与 Integrity Metadata 正确；
- CHANGELOG / Release Note 与实际变化一致；
- 最近已验证 Release 可作为可靠回滚点；
- 正式使用方只消费 Released Harness Package；维护者的受控候选验证证据不能被当作正式发布身份。

---

# 5. 与其他流程的边界

## Process Review Improvement｜流程复盘改进

Stage 7 负责“为什么改、问题根因是什么、应该修改哪一层”；本流程负责“已经确定的 Canonical / Harness 变化如何构建、验证和发布”。

## Project Onboarding｜项目接入

Project Onboarding 只建立 Adoption Baseline，不参与 Harness Build。

## Target-side Harness Adaptation｜目标侧 Harness 适配

目标 Coding Agent 按 [`Harness Adoption & Adaptation`](../meta-protocols/harness-adoption-and-adaptation.md) 消费 Released Harness Package，并根据当前 Runtime / Project 完成必要 Adaptation / Enhancement / Acceptance；它不重新执行 Canonical → Harness 预编译。该协议本身属于构建输入，其预编译程序随包提供。

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
- **Reviewer reads source｜独立 Reviewer 直接读取 Canonical**；
- **Test Agent reads Harness only｜行为测试只以 Harness 驱动执行**；
- **Verify fixed candidate｜只发布被验证过的确定 Candidate**；
- **Release unchanged｜发布阶段不修改已验证 Candidate**；
- **Git-backed history｜历史版本由 Git Tag / GitHub Release 承担**；
- **Re-enter on change｜发布后任何变化重新进入 Stage 1**；
- **Build internals stay internal｜构建内部状态不暴露给使用方**；
- **Release is versioned｜使用方只消费经过验证的版本化 Harness Package**。
