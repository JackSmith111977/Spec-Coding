# 0.13.1 Builder 来源回查与交接

本报告是本轮唯一 Builder 的 Stage 2 来源生成与自回查记录，不是独立 Review，不是 Stage 3 PASS，不证明 Runtime 行为已经通过，也不构成正式发布依据。

固定来源：6ef35782bf836a7795687a6b5919ccb74359c81b。基线：0.13.0，source_revision 为 8a41958f3feaf08f02dabc5fd67c9b70c7f87604。目标为用户指定的 0.13.1 candidate。

## 执行范围与方法

实际逐组直读了旧 prepared/manifest.json 精确 sources 的全部45份当前 Canonical：34份主流程、4份异常流程、5份规则、2份元协议；同时读取当前 docs/manifest.yaml、构建治理 Stage 2 及相关验证边界、包外 scope.json。没有使用 Git Diff 生成正文，没有依赖其他 Agent 的来源摘要，没有递归委派。治理、manifest、scope 是构建输入，不计入45份 Canonical sources。

生成前已完整读取11个 Skill 正文、candidate-validation 支持资源及各 Envelope。以当前完整来源检查每个流程的进入、步骤、输出、Gate、失败回流和完成边界，保留原紧凑流程表达；同字节消费者是完整来源回查后的保留结果。委派规则继续使用既有规则正文承载方式，将当前来源完整行为转为包内引用；没有将紧凑 Skills 扩成源码转储，也没有添加包内 IR 或新结构。

生成后以本轮已直读的完整原文上下文逐组回查，并重新读取全部来源文件内容、核对其 Git blob 与固定源提交一致；Hash/Blob 检查仅证明来源身份，不代替语义回查。对重点变化来源另作直接回查。最终小幅修正了入口“需要独立推理时”的条件和无Git变更任务的Commit例外，避免新增无条件独立审查Gate或提交要求。

## 实际读取的精确来源

下面按旧资产绑定列出全部45份原始来源，每项均已完整直接读取。共享规则按当前 manifest 的适用关系组合：所有Skills消费适用的全局/协作/产物规则；委派、隔离、独立审查或能力路由成立时消费当前委派规则；05/06及其他实际代码变更动作消费代码质量规则。这些共享原文也已直接读取，不只读取对应派生规则。

### rule-global

- docs/rules/global-contracts.md

### rule-collaboration

- docs/rules/human-agent-collaboration.md

### rule-delegation

- docs/rules/agent-delegation-and-coordination.md

### rule-artifacts

- docs/rules/artifact-organization-and-reading.md

### rule-code-quality

- docs/rules/code-quality.md

### spec-project-definition

- docs/workflows/main/01a-project-definition/01-project-positioning.md
- docs/workflows/main/01a-project-definition/02-business-definition.md
- docs/workflows/main/01a-project-definition/03-system-definition.md
- docs/workflows/main/01a-project-definition/04-requirement-framework.md

### spec-project-understanding

- docs/workflows/main/01b-project-understanding/01-project-orientation.md
- docs/workflows/main/01b-project-understanding/02-business-understanding.md
- docs/workflows/main/01b-project-understanding/03-system-understanding.md
- docs/workflows/main/01b-project-understanding/04-requirement-positioning.md

### spec-requirement-clarification

- docs/workflows/main/02-requirement-clarification/01-requirement-interpretation.md
- docs/workflows/main/02-requirement-clarification/02-ambiguity-gap-identification.md
- docs/workflows/main/02-requirement-clarification/03-scope-rule-confirmation.md
- docs/workflows/main/02-requirement-clarification/04-acceptance-criteria-confirmation.md

### spec-technical-design

- docs/workflows/main/03-technical-design/01-current-state-impact-analysis.md
- docs/workflows/main/03-technical-design/02-solution-design-decision.md
- docs/workflows/main/03-technical-design/03-detailed-technical-design.md
- docs/workflows/main/03-technical-design/04-design-acceptance-convergence.md

### spec-implementation-planning

- docs/workflows/main/04-implementation-planning/01-implementation-baseline-handoff.md
- docs/workflows/main/04-implementation-planning/02-implementation-task-decomposition.md
- docs/workflows/main/04-implementation-planning/03-task-definition-and-orchestration.md
- docs/workflows/main/04-implementation-planning/04-task-set-validation.md

### spec-development-execution

- docs/workflows/main/05-development-execution/01-ready-task-scheduling.md
- docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md
- docs/workflows/main/05-development-execution/03-verification-and-exception-convergence.md
- docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md

### spec-verification-convergence

- docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md
- docs/workflows/main/06-verification-convergence/02-multi-dimensional-verification-execution.md
- docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md
- docs/workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md

### spec-process-improvement

- docs/workflows/main/07-process-review-improvement/01-evidence-collection.md
- docs/workflows/main/07-process-review-improvement/02-process-reconstruction.md
- docs/workflows/main/07-process-review-improvement/03-issue-detection.md
- docs/workflows/main/07-process-review-improvement/04-root-cause-analysis.md
- docs/workflows/main/07-process-review-improvement/05-improvement-design.md
- docs/workflows/main/07-process-review-improvement/06-implementation-and-validation.md

### spec-debug

- docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md
- docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md
- docs/workflows/exceptions/debug-and-defect-resolution/03-root-cause-confirmation-and-correction-routing.md
- docs/workflows/exceptions/debug-and-defect-resolution/04-fix-verification-and-failure-convergence.md

### spec-project-onboarding

- docs/meta-protocols/project-onboarding.md

### spec-harness-adoption

- docs/meta-protocols/harness-adoption-and-adaptation.md

Envelope 实际依据：entry/readme 基于两个元协议，并直接消费委派规则以同步前置触发和验证说明；routes/requirements 基于上述全部45份来源与当前规范清单的适用关系；integrity 基于 Harness Adoption 的固定身份及完整性要求，完整回查后保持既有代码字节；plugin 没有 Canonical 正文 sources，仅按目标版本刷新元数据。candidate-validation 是 spec-harness-adoption 的包内支持资源，依据该元协议 §3.1、§6 与共享委派规则生成。

装配交接时，来源记录应区分资产自身正文来源与已实际读取的共享依赖；本报告给出本轮真实读取范围，不将治理、scope 或本报告登记为 Canonical sources。Builder 未生成或修改 manifest。

## 修改资产（11个文件）

- rules/delegation.md：完整承载当前批量审查、原Reviewer复核、必要Fresh、主Agent工具检查、证据复用、预算与停止条件；保留原角色、权限、单写、能力路由、失败升级和结果状态边界。
- skills/spec-development-execution/SKILL.md：Verifier是职责；正式独立Gate与Worker自检区分；相关任务批量审查仍分别绑定对象/Coverage/结果，不绕Depends On；修复、新Commit、原Reviewer复核与Fresh例外明确。
- skills/spec-verification-convergence/SKILL.md：每项Pass Condition/Evidence保持；先环境及确定性检查，再按需批量独立审查；修复复核及证据复用边界保持，不减少必要Human Acceptance或Gate。
- skills/spec-harness-adoption/SKILL.md：环境结构先行；批量与定向复核；首次加载、新会话恢复及盲测的隔离；未激活能力不提前验证；证据复用保留原身份并关联新对象。
- skills/spec-harness-adoption/references/candidate-validation.md：授权始终包外；固定候选变更不继承旧整体PASS；受影响证据失效，未受影响证据有条件复用；判定者与盲测执行者分开；测试READY不转正式接入。
- skills/spec-project-onboarding/SKILL.md：直接入口补齐委派/隔离/独立审查/能力路由成立时读取共享规则，未增加新阶段或审批。
- bootstrap/BOOTSTRAP.md：安装前即可获得委派触发与验证入口；需要独立推理时批量送审，必要Fresh保留。
- bootstrap/routes.md：统一工具检查、批量审查/复核、Fresh及证据条件，保留完整主流程与Debug回流。
- bootstrap/requirements.md：independent-review实际上下文边界及可观察验收；补充工具优先、临时委派信息和证据复用条件，不以能力名称代替行为。
- README.md：标题0.13.1；去除旧版本专属维护者记录路径，说明可信发行与验证依据须从包外取得；候选不自称Release已发布。
- plugin.json：version改为0.13.1；既有标准schema及repository元数据保留，它们不是运行时语义依赖链接。

## 同字节保留资产（12个载荷文件）

以下文件均已与旧manifest.files的SHA-256核对一致；其中四条未经影响规则严格保留原字节。共享委派依赖变化仍影响相关消费者后续独立审查范围，正文Hash不变不表示可免除该范围。

- rules/artifacts.md
- rules/code-quality.md
- rules/collaboration.md
- rules/global.md
- scripts/verify.py
- skills/spec-debug/SKILL.md
- skills/spec-implementation-planning/SKILL.md
- skills/spec-process-improvement/SKILL.md
- skills/spec-project-definition/SKILL.md
- skills/spec-project-understanding/SKILL.md
- skills/spec-requirement-clarification/SKILL.md
- skills/spec-technical-design/SKILL.md

另有 manifest.json 保留旧0.13.0基线内容，等待主Agent装配，不算本轮重生成资产。

## 完整来源语义回查结论

- 01A：定位→业务→系统→需求框架及稳定REQ身份完整；目标模型/假设不伪装现状，不提前设计实现或确认详细范围。
- 01B：项目导航→As-Is业务→系统→需求定位完整；事实/推断/未知及Direct/Adjacent区分，保留必要图表与定向取证指导。
- 02：入口上下文和身份→歧义→Scope/Rule→AC完整；业务含义与正确性Human权限、OI阻塞和回流保持。
- 03：影响→方案决策→详细设计→Ready验收完整；高影响Confirm、上游Human Decision、关键假设证据和最早失真源回流保持。
- 04：上游Ready→候选闭环→正式Task→只读任务集验收完整；统一任务核心状态、单主REQ、必要依赖和Draft→Ready保持；批量审查不形成新增Gate。
- 05：Runnable推导→自治实现/Local Check→需要时Task Commit→正式验证→事实写回→需求集成/AC/授权Push完整；自检不冒充独立验收，能力失败不误作实现缺陷，Task Done/Push不等于Verified。
- 06：完整变更基线→只读多维验证→Finding判定/纠偏→证据关闭完整；不修改被验业务实现、不降Pass Condition；Accepted Deviation仍由Human决定且不伪装Pass；阻断OI与必要Gate保留。
- 07：EV→过程→ISS→RC→IMP→权限→下一轮真实效果完整；不把项目业务修复当可复用机制改进，不把文档检查当真实效果。
- Debug：现场保护/复现状态→区分性证据/假设→根因因果与最早源→原故障回归/Owner回接完整；未复现不代表无效，修复通过不单独证明根因，Failure不代写Task/Finding/OI/REQ状态。
- Project Onboarding：稳定意图/绑定/硬约束和Initialize/Reuse/Refresh/Migrate保留；动态Runtime不写永久Baseline；仅接入不虚构业务目标，有明确业务意图不要求先存在Task。
- Harness Adoption：固定来源→基线→需求驱动发现→等价适配/固定→原包语义回查/真实加载及行为→范围READY/BLOCKED→失效恢复完整；测试授权不自授、不迁移正式状态；原包语义与未部署行为不能由测试者额外知识补齐。
- 共享规则及组合：主Agent承担最终责任；子Agent有界，普通检查优先工具；需要独立推理才批量审查；修复原Reviewer定向复核，污染/实施角色转换/必要首次自主与新会话使用Fresh；无新Finding不等于审查无价值；不以预算降低通过条件。临时预算、用途、重跑原因不变成每Task长期必填字段。
- 原四规则：权限/全局不变量、人机协作触发、产物权威导航、代码质量各自职责继续由既有包内规则承载，无字节修改。
- Envelope：完整路由、条件依赖、适配要求及安装前入口一致；不新增流程、状态、逐次审批或私有组件层。

## 已完成的结构自检及边界

prepared 共24文件：23个载荷文件加旧manifest。未新增包内文件或目录。142处Markdown链接均解析到存在的包内目标，无包外运行语义链接。plugin版本及README标题已核对为0.13.1。全部45份来源与固定提交的Git blob一致。

上述链接/数量检查完成后，仅对三处现有文字增加“需要独立推理时”及“存在Git固化变更时”条件，不改变链接目标、文件集合或版本。没有额外运行测试。

本轮只写 prepared 和本报告；没有装配manifest、运行assemble、Git提交、改tools或正式docs，没有运行行为试验，也没有新增Agent。

## 未解决问题与主流程交接

Builder来源与表达回查未发现尚未处理的语义偏差，无写入或来源阻塞。prepared 已可供主Agent装配固定候选。

尚未完成且明确由主流程承担：刷新manifest版本/source_revision/实际source trace/Hash，装配并固定候选，执行全量结构验证、受影响独立语义Review及必要共享集成/行为挑战。当前prepared保留旧manifest，故尚不是完整性自洽的最终候选；本轮没有把旧包PASS转给它，也未运行会因旧manifest必然失败的包验证来伪造PASS。

版本例外仅在包外记录：用户明确指定Patch修订号0.13.1；本轮不据此宣称变化天然符合通常Patch语义资格，也不改变Canonical。版本治理例外与发布资格由主Agent在包外记录并收敛；包内不加入版本豁免规范或发布自证。