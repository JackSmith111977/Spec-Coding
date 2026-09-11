---
name: spec-development-execution
description: 动态调度 Ready Task，在契约内实施、提交、独立验证并完成需求集成与 AC Gate 后同步；用于 Spec Coding 阶段05及实现修复。
---

# 05：实施、验证并持续推进

当前范围[接入](../../bootstrap/BOOTSTRAP.md)有效后读取[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)、[委派](../../rules/delegation.md)；代码变更读[代码质量](../../rules/code-quality.md)。tasks.md 是定义、主 Requirement 与状态的权威源。失败归因不可靠时先进入[Debug](../spec-debug/SKILL.md)取得证据，随后由本流程收敛 Task 状态。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 调度与启动

筛选 Status=Ready、Depends On已满足、无有效Blocker、执行环境可用的任务。Runnable仅运行时视图，不增加 Queued/Runnable/Scheduled 等持久状态。考虑依赖、边界、争用与关键路径，先降冲突再并行：单写任务用当前Workspace，独立只读可共享，多独立写任务用独立Worktree并行，有依赖或高冲突则串行。隔离方式是动态策略，项目硬约束不允许时选择仍满足要求的执行方式，不固化进Task。

构造 Execution Unit：Task Contract + Scoped Context + Agent/Model + Tools + Workspace + Verification Contract。局部上下文含当前Task、引用REQ/AC/Design、直接依赖结果、相关代码、验证要求、有效约束；其余按需检索，产物保持完整。正式任务不另套第二委派契约。

先发现当前实际模型/思考/工具/上下文，再选择最低充分能力；必要机制失效则按[适配](../spec-harness-adoption/SKILL.md)刷新并验证，满足前不启动依赖任务。认领可运行且Execution Unit已就绪任务，Ready→In Progress写回tasks.md；未调度Ready保持原状。启动失败优先作为Attempt问题，仍等价的配置可重试；任务本身无法继续才Blocked，不新增CapabilityBlocked。

短期 Execution Dispatch 记录 runnable_tasks、scheduling、execution_units，不成为长期事实源；Role/Model/Thinking/Fresh/Fork/Workspace/Attempt/Fallback等也不写回核心Task。

## 2. Worker自治闭环

核对Requirement/Goal/Boundary/Coverage/Done、开工所需上下文、依赖结果、正确工作区、验证要求。局部不足Search/Read/Runtime Inspect；明显大缺口才请求Scout/Supervisor，Scout不取得Task Ownership。可正确开工即可，不一次装全信息。

Inspect→Hypothesize→Implement→Run/Observe→Adjust，契约内自主选文件、结构、辅助代码测试调试脚本，按需API/Browser/DB/Logs/Trace证实行为。遵守项目与代码质量约束。可以变策略，不改变Requirement/AC、固定Design、Task Goal/Boundary/Coverage/Verification；需跨界则提供证据影响建议回Main，找到最早事实源并按权限处理，普通实施失败不自动打扰Human。

局部验证优先Typecheck/LSP/Compile/Build、Unit/Focused Integration、API/Contract、DB/状态、Browser/E2E局部、日志Trace。契约内失败由原Worker直接修复重验，保持短回路；能力不足先补Context/Thinking/Model/Tool/策略，契约仍成立不自动Blocked。

局部必要验证通过后形成Task Commit，只提交本Task已局部验证实现及必要测试。业务代码、配置、数据模型等需Git固化变更必须有可追溯Commit code_ref；纯只读无代码可省略。Commit失败/无法稳定引用则保持In Progress，不能进Verifying。Commit不表示Done。

交付 Verification-ready Result：task、requirement、changes、实际result、已执行local_evidence、需要时code_ref、按需notes；不附第二通用Subagent交接或冗长过程。随后In Progress→Verifying。

## 3. 正式独立验证

准备Task/Verification Contract、Worker候选结果、code_ref对应Commit/Patch或无代码实际结果、仅作参考定位的局部证据、适用规则及Gate环境。Worker自证不直接当正式证据，尽可能重新执行独立Gate，存在code_ref时锁定其实际变更，不能验漂移后的工作区。

确定性优先：Build/Compile/Typecheck/Lint、Unit/Integration、API/Contract、DB/MQ/Async、Browser/E2E、架构依赖Schema、安全等。机器难判的复杂UX、语义、代码质量或高风险按需Fresh Reviewer，隔离原Worker实施上下文，能力与复杂度匹配，默认只读找问题；Reviewer不替代Gate。

Verifier是正式验证职责，不等于每Task新建子Agent。结构、引用、Hash、格式等可确定检查优先由Main调用工具；正式Gate仍走满足本步骤独立性的执行路径，Worker自检不能改称独立通过。先检查环境与廉价前提，失败时停止依赖的昂贵验证；无依赖且无共享可变状态的检查可并行。

需要独立推理时，先完成自检及受影响确定性检查，再按[委派规则](../../rules/delegation.md)将稳定候选和相关问题批量送审，不按文件/Task数量机械建Reviewer或默认双人审查。每Task仍分别绑定实际对象、Coverage与结果，不绕Depends On、不改变状态归属。修复先由原Worker自检，存在Git固化变更时形成新Commit，再由未参与实施且隔离仍成立的原Reviewer定向复核；污染、转为实施者或首次自主行为/新会话/盲测需要时另用Fresh上下文，原Reviewer复核不称全新盲测。仅在对象、依赖、环境、范围及独立性仍适用时复用证据，Hash不变单独不能证明依赖不变；影响不明扩大必要验证，预算不足明确未验证范围，不降低Gate。

先证据归因再分流：

| 问题 | 返回与状态 |
|---|---|
| 可可靠归因实现缺陷（含代码质量） | 原Worker，Verifying→In Progress，修复后局部验证、新Commit、再正式验证 |
| 集成/环境/验证设施异常 | 修复运行条件重验，必要时阻塞 |
| Task Boundary/Coverage/依赖/Verification失效 | Blocked，回[规划](../spec-implementation-planning/SKILL.md) |
| 需求歧义/设计不成立/上游冲突 | Blocked，回[02](../spec-requirement-clarification/SKILL.md)/[03](../spec-technical-design/SKILL.md)最早失真源 |
| 无法可靠归因、需跨层诊断 | [Debug](../spec-debug/SKILL.md)，取得Root Cause/Correction/Closure后回Owner |
| 验证Agent/Model/Tool能力问题 | 调整配置后执行同一契约，不误报实现缺陷或权限升级 |

形成 Verification Result：task、requirement、verdict、target_status、evidence、实际验过的code_ref、按需findings、阻塞时blocker/required_action。passed→Done；repair_required→In Progress；blocked→Blocked。这里判定目标状态，下一步写回。模型/Attempt等仅其差异影响证据解释时才需保留。

## 4. 写回与需求汇合

只固化确认Result/Evidence/Code Reference/主REQ/Blocker/相关Finding，不保存调试过程。根据正式结果写tasks.md：Verifying→Done/In Progress，真实阻塞则Verifying或In Progress→Blocked；Blocked记录Reason、Evidence、Affected Contract、Required Action/Decision、Resume From。

重算依赖与Runnable：T01 Blocked且T02依赖它时，T02仍Ready但不可运行；不要级联伪造Blocked。只有上游修正使下游契约本身失效才改状态并重规划验收。

每次Task变化后重算TasksOf(主REQ)。全部Done才汇合其已正式验收code_ref，解决集成冲突，执行该REQ所属AC的组合Gate（不机械重跑所有TaskGate），通过后按既有Push权限同步远程开发分支。Requirement Sync只聚合Integration/AC Gate/Push及必要code_ref，不成为第四权威状态。Push不等于Merge、Release、Deploy或06的Verified；权限不足不虚报已Push。任一步失败保留可信Task事实，记同步状态并走最短修复，只有契约失效才退Task。

新Runnable立即调度，不等固定Wave。没有Runnable时：全部Required需求Task Done且Integration/AC Gate/Push完成才进入[验证收敛](../spec-verification-convergence/SKILL.md)；Required Blocked等待纠偏/外部恢复；需求同步未完继续处理对应环节；Task契约改变重新规划有效性确认。

Task Graph Update保存task、requirement、status、result、evidence、dependency_updates、runnable_updates、next_action；无依赖或可执行条件变化时明确无变化。code_ref保存本次正式验证的代码引用，无则省略；Blocked时保存blocker，包括原因、证据、受影响契约、所需动作/决策与恢复点；requirement_sync在触发后保存当前REQ的task completion、integration、AC gate、push及必要代码引用，尚未触发可省略。它仍是既有事实及必要运行时结论的输出视图，不建立第二份任务状态。确认状态证据已写回、可执行条件重算、需求边界结果明确和下一动作后继续循环。

写回与恢复遵循产物规则：先固定必要证据，再更新权威产物与直接入口，检查引用及摘要依据；共享写入单一Owner，中断先核对原状态，被正式结论引用的临时证据先晋升/保留再清理。
