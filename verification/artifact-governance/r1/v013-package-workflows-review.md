# 0.13.0 固定包业务流程独立审查

结论：**BLOCKED**。9 个业务流程 Skill、其全部 38 份 Canonical（34 份主流程、4 份 Debug）及 5 份共享规则均已完整阅读并对照。发现 1 项阻断静态语义准入的问题：05 的 Task Graph Update 丢失必需字段与条件字段的区分。其余已审查部分未发现需要阻断的语义差异。

本结论只针对下述固定包的业务流程静态语义保真，不代表运行时行为验收或正式发行验收。没有执行行为测试，没有修改被审内容。

## 1. 对象、身份与方法

- 工作区：`[工作区]`。
- 指定源提交：`36b92f7257a8b69aeb2f93de8f90c40c66e3f402`。
- 固定包：`packages/harness`，版本 `0.13.0`，包清单中的 `source_revision` 与指定提交一致。
- 指定及独立重算的包 SHA-256 均为 `e4b84d88ab494b0503837674169bc0fb31814fcdb0a3c5ac7d9636a6f5ea6cd7`。
- 重算按包内 `README.md:11–21` 的定义：全部文件按 POSIX 相对路径排序，对每个原始文件取 SHA-256，以“哈希、两个空格、路径、换行”的 UTF-8 清单再取 SHA-256；包括 `manifest.json`。24 个包文件，清单列出的 23 个载荷文件哈希均匹配。
- 工作区 HEAD 为 `20b48366745db166fedbef83037e9d10189f8a3e`，没有将它误当指定源版本。对实际读取的 `docs/manifest.yaml`、38 份业务 Canonical、5 份规则逐一以 Git blob 对照指定提交，44 个文件全部相同；另以限定范围 Git diff 确认无内容差异。因此以下源码位置对应指定提交原文。
- 直接全文阅读 `docs/manifest.yaml`，依据其 `stages.documents`、`exception_workflows.documents`、`rule_documents` 确定范围；直接全文阅读每份源码及每个固定包 Skill/规则。没有读取 Builder 脚本、构建过程记录、设计摘要或既有审查报告作为语义依据。
- 额外读取固定包 `manifest.json`、`README.md`、`bootstrap/BOOTSTRAP.md`、`bootstrap/routes.md`、`bootstrap/requirements.md`；读取包内 `scripts/verify.py` 了解完整性定义，没有执行该脚本。两个 Meta Skill 的路由目标存在性纳入检查，其全文语义不属于本次 9 个业务流程审查范围。
- 对 9 个业务 Skill、5 个规则、3 个 bootstrap 文件的 Markdown 本地文件链接做静态存在性检查：113 条、0 个断链。这只证明文件可达，不证明目标行为正确，也不证明真实 Runtime 已加载。
- 本文采用“源码全文 → 固定包完整 Skill + 适用共享规则 + 路由/能力要求”的组合比较。允许压缩表达、合并章节、调整包内链接；不允许将必需字段变为可选，或改变权限、状态、准入、关闭条件。下文的“反例”是文本契约推演，不是运行测试结果。

## 2. 阻断项

### WF-01／P2：05 的 Task Graph Update 将整组字段泛化为“按需保存”

**位置：**`packages/harness/skills/spec-development-execution/SKILL.md:63`。

包内原文：

> Task Graph Update按需保存task、requirement、status、result、evidence、code_ref、blocker、dependency_updates、runnable_updates、requirement_sync、next_action。

**对应 Canonical：**`docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md:148–166`，并结合 `:15–26`、`:32–49`、`:53–77`、`:170–172`。

Canonical 的产物契约分别规定：

| 字段类别 | 原始要求 |
|---|---|
| 基本内容 | `task`、`requirement`、`status`、`result`、`evidence`、`dependency_updates`、`runnable_updates`、`next_action` 在产物表中列为输出内容，没有整体按需省略的许可。没有变化可以明确表示无变化，不等于省略契约。 |
| `code_ref` | 无代码引用时可省略；存在时须为已正式验证的 Task Commit 或其他代码引用。 |
| `blocker` | `Blocked` 时记录；同时需满足原因、证据、受影响契约、所需动作/决策及恢复点要求。 |
| `requirement_sync` | 尚未触发时可省略；触发后承载当前 REQ 的 task completion、integration、AC gate、push 及必要代码引用，仅为聚合视图。 |

Skill 保留了全部字段名称，却用同一个“按需保存”覆盖整个列表，未保留上述必需性区分。这使只读固定包的消费者可以把应输出的依赖变化、Runnable 变化或下一动作省去，并仍按本行末尾“确认……后继续循环”推进。特别是跨需求任务依赖变化后，执行了重算和将其结果可追溯地交给下游是不同责任。

**组合规则不能消除该歧义：**

- Skill `:55–61` 保留了状态写回、依赖重算和需求汇合行为，故这里不是“丢失任务状态机”，也不是“可以绕过 Gate”的发现；缺口在产物输出契约。
- `rules/artifacts.md:5` 把内容与必需字段交给 Workflow 决定；`:80` 只说明 Task Graph Update 的承载位置，`:133–139` 只规定写回、导航与恢复顺序，均未重新列出本产物的必需/条件字段。
- `rules/global.md:24–33` 的可追溯性要求不提供这一字段级区分，`bootstrap/requirements.md:8、11、15` 也没有补齐。
- 不应通过新增独立 Task Graph 状态库修复；它依旧是既有事实及运行时结论的输出视图，`tasks.md` 和 Integration/AC Gate/Push 原记录继续承担权威事实。

**最低修复要求：**明确基本输出字段必须保留，逐项保留 `code_ref`、`blocker`、`requirement_sync` 的原始条件；无变化时可以简洁表达，不要求重复完整任务表或制造新文档。将“按需”限定到表现形式、承载位置及真正可选字段。此处仅提出修复要求，本次没有修改 Skill 或包。

**裁定：BLOCKED。**这是静态文本中可定位的必需性弱化；未声称已观察到某个 Agent 的实际失败。即使作者本意是“按需选择承载形式”，固定包目前也没有明确表达该限定，不能在完整产物字段保真审查中将意图当作已保存的契约。

## 3. 全量流程覆盖与产物字段对照

位置记法：本节每个小节声明完整源码目录和包 Skill 路径。表内文件名均相对于该源码目录；`1–N` 表示已读该文件全部 N 行，不是只读产物表。包位置为对应完整 Skill 的一基行号。省略标注为“按需”的字段均按源码原有条件解释，不把所有字段一概可选。

### 01A：PASS

源码目录：`docs/workflows/main/01a-project-definition/`。包：`packages/harness/skills/spec-project-definition/SKILL.md`，已读 `1–56`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-project-positioning.md:1–151` | `12–22` | Project Positioning 的 Identity、Problem、Users & Scenarios、Value、Goals、Boundaries、按需 Assumptions/Open Items 全在。问题而非预设功能；用户场景、Before/After、项目级目标和基本边界；事实/假设/未知分开；新读者可独立说明定位后完成。详细范围留02，不提前设计业务/系统。 |
| `02-business-definition.md:1–195` | `24–34` | Business Scope、Business Model、Business Scenarios、按需 Assumptions/Open Items 全在；领域/核心与辅助能力、参与者、对象关系/变化、术语、场景规则异常、价值追溯、自洽检查；不下沉 DTO/表/权限实现。状态机按复杂度使用，非强制。 |
| `03-system-definition.md:1–164` | `36–46` | System Scope、System Model、System Flows、按需 Assumptions/Open Items 全在；内部/外部职责、同步异步、创建/修改/持有/消费归属、Constraint 与 Design Assumption 区别；业务覆盖和链路闭环；技术细节留03，已明确硬约束例外保留。 |
| `04-requirement-framework.md:1–157` | `48–56` | Requirement Map、Requirement Units、Core Flow、按需 Open Items 全在；一次分配稳定唯一 REQ、Actor/Scenario/Expected Result、依赖/支撑、核心闭环、价值来源和重复/缺口检查。Walking Skeleton 是组织线索，不是已确认版本范围；直接移交02，不重推需求空间或重编号。 |

Authority 由全局及协作规则承接；启发式问题没有变成强制问卷。`project/` 是默认位置，不要求四份空文件、不用目录存在推定定义已完成。

### 01B：PASS

源码目录：`docs/workflows/main/01b-project-understanding/`。包：`packages/harness/skills/spec-project-understanding/SKILL.md`，已读 `1–54`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-project-orientation.md:1–118` | `12–20` | Project Overview 的 Identity、Domain Map、System Map、Repository Map、Navigation Anchors、按需 Open/Conflicting Information 全在。文档→结构→Manifest/Build→入口→不足/冲突时代码验证的顺序保留；广浅地图、职责入口、高复用导航，不枚举 API/DTO/整棵目录树。 |
| `02-business-understanding.md:1–117` | `22–34` | Business Scope、Business Model、Business Scenarios 全在，证据和重要未知附着原章节。As-Is/To-Be 分离，代码仅是业务证据之一；业务权限非鉴权实现。用例/对象图适用性、必要关系语义/基数、核心活动图默认与状态图按需、文本权威/图为视图均在；先调查再必要 Human 校正。 |
| `03-system-understanding.md:1–121` | `36–44` | System Scope、System Model、System Flows 全在；组件职责/接口/数据归属/不变量、核心控制数据状态与同步异步链、证据和未知附着原模型。定向追踪到关键 Symbol，需要证明再下钻，不复制全部调用链；图表按需，现状不被拟议方案覆盖。 |
| `04-requirement-positioning.md:1–118` | `46–54` | Change Points、Business Position、System Position、Gaps 全在；Direct/Adjacent/Potential 区别、入口/组件/链路/数据/边界定位、四类能力/语义/边界 Gap；关联影响不自动进范围，冲突不默认需求或代码一方正确，不在定位中解决歧义或决定实现；仅存新增定位，转02。 |

与产物规则 `:76、89、110–123` 组合后，已有权威文档引用和按需定向发现可复用，没有补造平行01A产物的要求。

### 02：PASS

源码目录：`docs/workflows/main/02-requirement-clarification/`。包：`packages/harness/skills/spec-requirement-clarification/SKILL.md`，已读 `1–44`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-requirement-interpretation.md:1–136` | `12–18` | Requirement Interpretation 的 Requirement、Intent、As-Is/Existing Situation、Problem、To-Be、Known/Inference/Unknown 全在。Input Context 仅为消费视图；Greenfield 继承 REQ，Brownfield 缺 ID 时在本链入口只分配一次；身份不等于内容确认，不强造另一入口产物。 |
| `02-ambiguity-gap-identification.md:1–113` | `20–26` | ID 由稳定 OI 承接；Issue、Impact、Question、Status、Blocking、Owner Stage、已解决时 Resolution 全在，并明确按全局字段补 origin/related 等。歧义/缺失/冲突/假设分类；关键决策影响筛选；低价值未知不必建 OI；deferred 有理由和承接位置；先证据再决策就绪问题。 |
| `03-scope-rule-confirmation.md:1–85` | `28–34` | In Scope、Out of Scope、Boundaries、Business Rules、Decisions、按需非阻塞 Open Items 全在。Trigger/Behavior/State/Data/Exception 按需定义；整理已确认事实可自治，语义/范围/核心规则决策属 Human；阻塞关键未知回澄清，不能默认填充。 |
| `04-acceptance-criteria-confirmation.md:1–112` | `36–44` | AC 的 ID、Requirement、Scenario、Given、When、Then、按需 Trace 全在；唯一主 REQ、其他关系用 Trace；缺身份回解读。核心路径、重要边界异常、Rules/Decisions 覆盖、可明确 Pass/Fail；新增或改变正确性需 Human Decision，机械转写已确认含义无需再问；新歧义回前序，完成后进03。 |

`requirements/REQ-xx/` 不成为重新分配身份的理由。原 OI 状态独立于澄清对话和需求目录，blocking 不能随 deferred 或同步完成消失。

### 03：PASS

源码目录：`docs/workflows/main/03-technical-design/`。包：`packages/harness/skills/spec-technical-design/SKILL.md`，已读 `1–48`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-current-state-impact-analysis.md:1–109` | `12–18` | Impact Baseline 的 Requirement Mapping、As-Is Flow、Impact Scope、Constraints、按需 Evidence/Open Items 全在；Entry/Flow/Data/State/Dependency/Extension 定向追踪；Direct/Dependent/Open Impact、Confirmed/Conditional/Unaffected/Open 状态与证据；不先选方案，需求问题回02、技术缺证继续追踪。 |
| `02-solution-design-decision.md:1–127` | `20–28` | Technical Problem、按真实选择保留 Candidate Options、Decision、Rationale、Trade-offs、按需 Open Items 全在。五项取舍维度、相关时补性能安全成本、关键假设先验证；局部惯例可自治，高影响架构迁移等 Confirm，REQ/AC/偏差/风险边界回 Human Decision；不强造多个方案。 |
| `03-detailed-technical-design.md:1–130` | `30–38` | Structure、To-Be Flow、Contracts、Boundary Handling、按需非阻塞 Open Items 全在，章节按复杂度展开。接口/请求响应/事件/Schema/状态/错误/权限、异步并发与失败/重试/幂等/兼容/迁移回滚等边界；不写代码步骤，不另造 Open Issue；核心方案失效回决策。 |
| `04-design-acceptance-convergence.md:1–136` | `40–48` | Requirement Coverage、Consistency Check、Validated Assumptions、按需 Risks/Open Items、Readiness 全在。假设 Validated/Open/Invalid；OI status 与 blocking 正交，Risk 独立；无阻塞且覆盖/一致/证据完整才 Ready，否则 Not Ready。按问题回02或本流程影响/决策/详细设计，只重验受影响链，Ready 才进04。 |

与 `rules/artifacts.md:78、89、110` 组合，`design.md` 或 `shared/` 可承载唯一设计正文；设计 Ready 不代表现状已实现，取代关系与历史证据版本不丢失。

### 04：PASS

源码目录：`docs/workflows/main/04-implementation-planning/`。包：`packages/harness/skills/spec-implementation-planning/SKILL.md`，已读 `1–64`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-implementation-baseline-handoff.md:1–122` | `12–20` | Requirement Baseline、Fixed Decisions、Design Baseline、Constraints、按需 Risks/Open Items 全在。只接 Ready 最终版本、无阻塞；最终/结论/引用优先，Implementation Baseline 不成为新事实源；交接检查不重做验收，缺口回原 Owner。 |
| `02-implementation-task-decomposition.md:1–129` | `22–30` | Candidate Task 的 Requirement、Goal、Trace、Boundary、Coverage、按需 OI 全在。独立实施且独立证明闭环、唯一主 REQ、真正共享实现保主归属和其他 Trace；主/分支/异常/边界/兼容路径按需；Risk 与 OI 分开，独立 OI 目标可成 Task 但仍引原 OI；不提前定依赖/验证/Done/Agent/顺序。 |
| `03-task-definition-and-orchestration.md:1–230` | `32–51` | Formal Task 的 ID、Requirement、Status、Goal、Trace、Boundary、必要 Depends On、Coverage、Verification、Done、按需 OI 全在。初始 Draft，Ready/In Progress/Blocked/Verifying/Done 语义完整。Verification-First、确定性优先、Test-First 按适用；只存真阻塞依赖，不固定运行策略，不新增正式委派契约。 |
| `04-task-set-validation.md:1–188` | `53–64` | Execution Readiness、Coverage/Consistency/Executability/Verifiability、按需 Open Risks；有问题时 Issue/Source/Impact/Recommended Return Point 全在。只读校验，不静默修改上游；主 REQ/TasksOf、覆盖/一致、无循环/缺失依赖、Goal/Coverage/Done/Verification、组合 AC 可证明；修正回源后 Draft→Ready，Ready 不等于 Runnable。 |

`tasks.md` 的统一完整任务集、权威 Status/Primary Requirement、必要详情下钻与跨需求/跨空间依赖保留。Skill `:51` 使用“索引”称呼该承载处，但同一句明确保留核心定义和权威字段，并有 `rules/artifacts.md:110` 明确例外；没有据这个词将 `tasks.md` 判成纯导航、要求把状态迁出。Task Done 也不自动关闭关联 OI。

### 05：BLOCKED（仅 WF-01）

源码目录：`docs/workflows/main/05-development-execution/`。包：`packages/harness/skills/spec-development-execution/SKILL.md`，已读 `1–65`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-ready-task-scheduling.md:1–164` | `12–20` | Execution Dispatch 的 runnable_tasks、scheduling、execution_units 全在，短生命周期而非长期事实源。Ready+依赖满足+无 Blocker+环境可用→Runnable；单写/只读共享/多写隔离/冲突串行，Execution Unit 六组成和必要 Scoped Context；认领后写 In Progress，未调度 Ready 不变；Attempt/能力不足不自动造 Blocked。 |
| `02-autonomous-implementation-and-closure.md:1–174` | `22–32` | Verification-ready Result 的 task、requirement、changes、result、local_evidence、Git 变更时 code_ref、按需 notes 全在。开工最小上下文、Scout 条件、契约内自治/质量、局部自修、能力升级；必要 Local Verification→Task Commit→Verifying，Commit 失败保持 In Progress，不把提交当 Done。 |
| `03-verification-and-exception-convergence.md:1–164` | `34–51` | Verification Result 的 task、requirement、verdict、target_status、evidence、适用 code_ref、按需 findings、阻塞时 blocker/required_action 全在。精确 Commit 为对象、自证仅参考、正式 Gate 优先、Fresh Reviewer 补充；passed→Done、repair_required→In Progress、blocked→Blocked 的目标状态先判后写；归因与四类纠偏/能力问题/Debug 区分完整。 |
| `04-state-commit-and-continuous-progression.md:1–202` | `53–65` | 正式状态写回及 Blocked 的 Reason/Evidence/Affected Contract/Required Action/Decision/Resume From 保留；依赖变化不级联伪造状态；同主 REQ 全 Done→Integration→AC Gate→授权 Push，Sync 仅聚合；新 Runnable 即调度，无固定 Wave；进入06条件保留。Task Graph Update 全部字段名称存在，但 `:63` 的“按需保存”丢失必需/条件区分，见 WF-01。 |

具体未混淆项：正式 Gate 针对 `code_ref` 的实际变更，不针对漂移后的工作区；失败归因可靠时回原 Worker，归因不足才 Debug；Push 失败保留可信 Task 事实；Task Contract 失效才回退重规划；Push 不等于 Merge/Release/Deploy/Verified。`implementation.md` 是底层同步事实的可选承载位置，不能据此认为 Integration/AC Gate/Push 事实也都可选。

### 06：PASS

源码目录：`docs/workflows/main/06-verification-convergence/`。包：`packages/harness/skills/spec-verification-convergence/SKILL.md`，已读 `1–56`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-verification-baseline-establishment.md:1–143` | `12–22` | Scope、Trace、Verification Items（Target/Type/Method/Pass Condition/Evidence）、按需 Review Focus/Human Acceptance、Gates、Environment、按需 OI 全在。Task/需求集成/Push 引用还原 Actual Change，补跨Task/跨REQ/关键链/回归/风险安全缺口；有效证据复用；三类验证职责分开，不固化 Agent 编排。 |
| `02-multi-dimensional-verification-execution.md:1–118` | `24–34` | Verification Results、Evidence、Findings、Suspected Origin、Unverified Items 全在。Pass/Fail/Unverified 明确；只读被测业务对象，测试/Fixture/Mock/验证数据/Harness 修正例外不得改标准或掩盖失败；Reviewer 不替代 Gate；必要 Human Acceptance；能力不足不误报业务 Finding。 |
| `03-verification-finding-triage-and-deviation-convergence.md:1–137` | `36–46` | Finding Resolution 的 Finding、Decision、Authority、Evidence、按需 Invalid Source、Affected Trace、Route、Reverification Scope、按需 Open Item、Status 全在。六类判定及 Resolved/Accepted/Blocked/Open 生命周期分开；上游变化按权限、Accepted 始终 Human；最早源纠正及必要回归；Unresolved 缺决策与需诊断分开，Debug 只回证据。 |
| `04-evidence-closure-and-status-convergence.md:1–119` | `48–56` | Closure 的 Trace、Evidence、Findings（Decision+Status）、Gates、Status、按需非阻断 Open Items 全在。此步只收口，不新验/修复/发布；Required Verification、必要 Gate、Finding 关闭、无 blocking OI、完整 Trace 才 Verified，否则 Blocked；Invalid Finding 仍显式 Resolved，Accepted 不伪装 Pass。 |

最终关闭记录是业务权威结论，证据索引只是引用。跨需求报告可单正文共享，但各关闭记录仍须绑定对应范围及完整证据，不能用目录归档或 Failure Resolved 代替 Verified。

### 07：PASS

源码目录：`docs/workflows/main/07-process-review-improvement/`。包：`packages/harness/skills/spec-process-improvement/SKILL.md`，已读 `1–50`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-evidence-collection.md:1–132` | `12–16` | EV 的 id、time、stage、type、subject、actor、fact、source、related 全在；六类证据、关键事件筛选、只记可观察事实、不先归因、不是全部工具日志晋升；Spec Coding 不默认独立 Spec 产物。 |
| `02-process-reconstruction.md:1–102` | `18–22` | reconstruction.md 的 order/time、stage、event、evidence、result 全在；按 subject/关系串联、关键变化可回 EV，不只保最终状态、不判断合理性或根因。 |
| `03-issue-detection.md:1–126` | `24–28` | issues.md 的 id/title/category/detected_stage/description/impact/evidence/related/status 全在；七类初判、candidate/accepted/ignored/merged/analyzing/closed 全保留；实际影响筛选、排除正常变化与噪声，不提前根因分析。 |
| `04-root-cause-analysis.md:1–152` | `30–34` | root-causes.md 的 id/title/type/description/issues/earliest_stage/escape_reason/failed_mechanism/evidence、可选 confidence 全在；discovery/closure/traceability/execution/verification/workflow-gap/other 七类；最早可拦截点、发生/逃逸区别、多因多问题、低证据降置信不强套。 |
| `05-improvement-design.md:1–133` | `36–42` | improvements.md 的 id/title/root_causes/target/authority/current_state/expected_state/candidates/decision/change/validation_plan/validation_result/status 全在；允许 No Process Change；正确机制 Owner、最小有效变化；行为语义变化 Confirm，弱化强制 Gate/扩权 Human Decision；实施前定义效果及成本验证计划。 |
| `06-implementation-and-validation.md:1–130` | `44–50` | 持续更新原 IMP 的 id/authority/target/change/validation_plan/validation_result/status/related、可选 side_effects；不新增对象。实施前实际满足权限，偏离原决策回判；实际变化→IMP→RC→ISS→EV；下一轮真实运行看 Effect/Cost 决定 Keep/Modify/Remove，不以文字检查冒充有效性证据。 |

该流程修正可复用机制，不直接修业务 REQ/代码来掩盖机制根因。包内补充的维护者回流与禁止热修原发行包，与 `rules/artifacts.md:83、143–149` 的资产身份/归属相容。ISS 的 accepted、IMP 的生命周期字段不被当成 Finding.Accepted 或 Requirement.Verified；源码未规定 IMP 状态枚举，未将包未新增枚举判为缺失。

### Debug：PASS

源码目录：`docs/workflows/exceptions/debug-and-defect-resolution/`。包：`packages/harness/skills/spec-debug/SKILL.md`，已读 `1–54`。

| 完整 Canonical | 包位置 | 字段、完成与边界覆盖 |
|---|---|---|
| `01-failure-intake-and-reproduction.md:1–144` | `12–22` | Failure Baseline 的 Source、Symptom、Expected/Actual、Impact、Context、Reproduction、Repro Status、Evidence、适用 Change Window、按需 OI 全在。已有对象只引用；高影响先保护现场，止损非根因修复；六种 Repro 状态全在，Not Reproduced 不等于无效，安全替代/可靠现场可承接调查。 |
| `02-evidence-collection-and-fault-localization.md:1–208` | `24–32` | Fault Localization 的 Failure、Expected Trace、Observed Trace、Evidence、Hypotheses、Fault Boundary、可选 Candidate Cause/OI 全在。节点 Confirmed/Unknown/Diverged 与假设 Supported/Rejected/Open 区分；边界/差分/变化证据、可证伪循环、反证保存、近期变更非根因；按需 Bisect，不重扫项目，不强求此步最终根因。 |
| `03-root-cause-confirmation-and-correction-routing.md:1–176` | `34–42` | Root Cause Resolution 的 Failure、Root Cause、Evidence、Invalid Source、Affected Trace、Correction Route、Reverification Scope、按需 OI 全在。症状/促因/候选区别、解释首次偏离、排除主要替代；Confirmed/Probable/Unconfirmed 保留，Unconfirmed 回定位，Probable 必须风险可接受且保留不确定；修复绿灯非单独因果证明；回最早源正式纠正。 |
| `04-fix-verification-and-failure-convergence.md:1–168` | `44–54` | Failure Closure 的 Failure、Correction、适用 code_ref、Failure Recheck、Reverification、Trace Status、按需 Residual Risk/Open Items、Status 全在。接管实际纠正、原故障按原复现类型重验、受影响验证复用；必要证据不足 Blocked，原故障消失且验证通过 Resolved；回原 Owner，不代写 Task/Finding/OI/Requirement。 |

触发取自 manifest 的 failure-signal/unexpected-behavior/unreliable-attribution/unresolved-finding，并与 `bootstrap/routes.md:20–24` 组合：可靠局部缺陷走短闭环；仅缺 Human 决策/外部信息的未决项不机械进入诊断。Failure、OI、Finding 可以关联，不自动相互转化或同时关闭。

## 4. 五项共享规则全文与依赖组合

以下规则均已完整读取源码和固定包正文，并逐行比较差异。协作规则仅改包内链接；产物规则仅改第5行 Meta 入口链接；代码质量正文一致；委派第243行把维护者构建链接改为客户端不执行的说明并改接入链接；全局第7行改为包内术语定义入口，其余差异为规则链接重定位。未发现规则正文的状态、权限或执行责任丢失。

| 源码全文 | 固定包全文 | 判定与覆盖 |
|---|---|---|
| `docs/rules/global-contracts.md:1–101` | `packages/harness/rules/global.md:1–101` | PASS。Reuse/Light/Standard/Deep 及提深信号；不能裁剪正确性、Trace、blocking OI、Gate、风险证据、Authority、真实协作 Trigger、纠偏、Git Commit/code_ref。OI 最小字段 id/origin/description/status/blocking/owner_stage/related/resolution，open/resolved/deferred 与阻塞正交；Autonomous/Confirm/Human Decision、已确认不重复请求；运行策略不默认持久化。 |
| `docs/rules/human-agent-collaboration.md:1–163` | `packages/harness/rules/collaboration.md:1–163` | PASS。探索在先、最小共享认知 Goal/Model/State/Delta/Uncertainty/Next/Evidence；六类真实 Trigger；渐进同步、Context/Finding/Uncertainty/Evidence/Recommendation/Impact 的信息要求而非固定表单；Decision Readiness 不升级自治动作；反馈回原源并刷新受影响 Trace，Main 为交互面，不新增审批总账。 |
| `docs/rules/agent-delegation-and-coordination.md:1–253` | `packages/harness/rules/delegation.md:1–253` | PASS。Main 唯一协调及最终责任；Scout/Researcher/Worker/Reviewer/Oracle 边界；委派价值、五维准入、正式 Task/临时工作区别；轻量委派 Goal/Boundary/Context/Authority/Expected Result/Evidence，回传 Result/Evidence/Uncertainty/Risk/Next 加角色结果；最小充分上下文、单写、递归需显式授权；先真实能力发现再证据和路由、能力不等价不得静默 Fallback；候选先验证再写原事实源，Reviewer 不替代 Gate。 |
| `docs/rules/artifact-organization-and-reading.md:1–157` | `packages/harness/rules/artifacts.md:1–157` | PASS。绑定优先、语义等价空间复用、默认目录非强制全建/共享授权；稳定身份/限定跨空间引用；内容字段状态归 Workflow；静态导航优先、动态摘要需来源修订；统一任务集和真实传递依赖；必要权限阻塞异常先有效、索引失效定向回查；原正文→必要证据→直接导航→检查，中断/并发/迁移恢复；固定包/候选/生效范围分离，临时证据晋升和历史保留。 |
| `docs/rules/code-quality.md:1–107` | `packages/harness/rules/code-quality.md:1–107` | PASS。可理解性、信息质量、变更清晰度、一致性四组完整；主路径/状态副作用可见、注释粒度与当前约束、历史归变更事实源、最小完整变更/无关清理限制、惯例与不扩散缺陷；按项目工具和风险执行，不固化语言框架、不新增流程状态。 |

### 依赖装配

以 `packages/harness/manifest.json` 的 `artifacts[].dependencies` 和 `conditional_dependencies`，加 `bootstrap/routes.md:3–5`、各 Skill 前置段核查：

| 流程 | 显式基础依赖 | 条件依赖与正文要求 | 判定 |
|---|---|---|---|
| 01A / 01B / 02 / 03 / 04 / 07 | global + collaboration + artifacts | 委派、隔离、独立审查、能力路由时 delegation；产生代码时 code-quality 由全局路由与条件依赖生效 | PASS |
| 05 / 06 | global + collaboration + artifacts + code-quality | 正文还要求读 delegation；代码质量按实际代码变化适用，独立判断不替代确定性验证 | PASS；05 输出字段问题另列 WF-01 |
| Debug | global + collaboration + artifacts | 正文明确委派时 delegation、写代码时 code-quality；共享路由在相关动作前生效 | PASS |

规则闭包：global→artifacts；collaboration→global/artifacts；delegation→global/collaboration/artifacts；code-quality→global/collaboration/artifacts；artifacts 无声明依赖。相关规则正文中的互相引用不等于要求递归执行或创建新状态机。产物规则独立可读，初始化不依赖尚不存在的空间入口。条件依赖不是“尚未读取即不适用”，路由明确激活前补读及适配。

## 5. 新产物规则与业务语义的交叉检查

| 交叉点 | 具体位置 | 判定 |
|---|---|---|
| 目录不新增状态、Gate 或必需业务产物 | `rules/artifacts.md:3–7、53–59、87`；全部 Skill `:10` | PASS。目录树是承载角色，`implementation.md` 不是新增必需 Artifact；不以全目录建齐判接入或业务完成。 |
| 长期现状与目标方案 | `rules/artifacts.md:75–79、89`；01A `:38–46`；01B `:24–44`；03 `:30–48` | PASS。项目事实与需求/设计目标可区分，设计 Ready 不提前把 To-Be 写为已实现事实。 |
| 普通导航与权威正文的例外 | `rules/artifacts.md:95–110`；04 `:51`；06 `:50–56` | PASS。tasks.md 核心字段权威，轻量 REQ README 正式章节可权威；并非所有 README 都是纯索引，也非所有索引摘要都可判状态。 |
| OI 原身份和生命周期 | `rules/global.md:37–67`；`rules/artifacts.md:77、82、87、117、123、157`；02 `:26`；04 `:30、34`；06 `:40–46`；Debug `:52–54` | PASS。OI 持续同 ID，原源改状态，blocking 不因迁移/归档/Task Done/Failure Resolved 解除。 |
| 统一任务集与跨需求阻塞 | `rules/artifacts.md:19、110–123、135–139`；04 `:51、57–60`；05 `:14、57–61` | PASS。主 REQ 决定 TasksOf，Trace 保其他关系，Depends On 包括跨需求及传递依赖；索引缺失不推定无阻塞，下游 Ready 可以保持但不可 Runnable。输出字段必需性见 WF-01。 |
| 必要契约与最小上下文 | `rules/artifacts.md:7、114–123`；`bootstrap/routes.md:3–5`；05 `:16、24` | PASS。渐进披露只限制无关内容，权限/阻塞/异常及必要契约证据仍在相关动作前有效；当前未激活流程入口保持可达。 |
| 写回、并发与恢复 | `rules/artifacts.md:131–139、153–157`；05 `:55、65`；`rules/delegation.md:125–131` | PASS。Owner/单写，先正文和证据后入口，更新受影响引用；中断回查原状态，临时证据被引用后保留或晋升，不凭 scratch 名称授权删除。 |
| 需求同步与最终验证 | 05 `:59–61`；06 `:14、52–56`；`rules/artifacts.md:59、80–87` | PASS。Integration、AC Gate、Push 各是底层事实，Sync 非第四权威状态；Push 不代替06最终验证；共享报告不复制多个独立事实源。 |
| Debug 关闭及原 Owner 恢复 | Debug `:38–54`；06 `:40–46`；`rules/artifacts.md:82、87` | PASS。根因置信度、Failure Closure.Status、Finding.Decision/Status、OI.status、Requirement.Status 分开；Resolved 回交 Resolution Evidence，原 Owner 决定业务状态。 |
| 07 机制改进与发行包身份 | 07 `:38–50`；`rules/artifacts.md:83、143–149`；`bootstrap/routes.md:26` | PASS。改进回实际 Owner，原固定包不热修，运行时事实不写成永久意图，下一轮真实效果与当前文案完成分开。 |

## 6. Hard Semantics、Guidance、Exception 与路由总裁定

- **Hard Semantics：除 WF-01 外 PASS。**身份连续性、最早权威源、真实证据、权限边界、必要 Gate、Task 状态机、需求级汇合、Finding 分类/生命周期、Failure 独立关闭、最终 Verified 条件均在完整组合中保留。不能用共享“遵守字段”口号弥补某 Skill 自身丢失的必需性。
- **全部产物字段：BLOCKED，定位 WF-01。**其余表中所列字段及源码中的条件性均有包内表达或明确共享字段补足；没有因名词出现就直接认定保真，而是核查含义、Owner、触发条件和写回位置。
- **Guidance：PASS。**01A 启发式非问卷、01B/03 按认知问题选图及按证据下钻、03 真选择才多方案、04 闭环粒度/Verification-First/按需下钻、05 先控冲突/短反馈/事件驱动、06 有效证据复用与风险定深、07 No Process Change 与最小有效改进、Debug 区分性证据/可证伪假设/安全替代均保留；没有把示例、候选工具或建议图表升级成普遍强制步骤。
- **Exception：PASS。**业务异常、实现缺陷、能力问题、边界问题、权限升级分开；未知根因不强归因，未复现不当无效，Probable 不当 Confirmed，Accepted 不当 Pass；修复回原 Owner，重验只针对受影响链和必要回归。
- **路由：PASS。**`bootstrap/routes.md:7–26` 保留01A/01B→02→03→04→05→06及按需07、各阶段最早源纠偏和 Debug 回交；当前动作前有效共享规则与能力要求，无因目录布局改变而失去下游/异常入口。链接存在性结果不被当作运行证明。

## 7. 最终范围声明

覆盖完成：9/9 业务 Skill 全文；38/38 业务 Canonical 全文；5/5 共享规则的源码及包内全文；docs 清单、包清单及业务组合所需 bootstrap 路由/能力/身份说明。结论为 **BLOCKED（WF-01）**，不是阅读不全、环境不可用或未跑行为测试导致的挂起。

本次唯一写入文件为 `.harness-build/v013-package-workflows-review.md`。被审源码和固定包未修改；未调用 Builder、未运行项目/包行为测试、未更改任何业务状态。审查期间另有范围外未跟踪目录出现，本次未读取、修改或清理它，不将其变化计作本次审查产物。
