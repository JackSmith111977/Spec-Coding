---
name: spec-verification-convergence
description: 对完整 Requirement/Change 补齐跨任务、回归、风险和人工验收证据，判定 Finding 并收敛 Verified/Blocked；对应 Spec Coding 阶段06。
---

# 06：用完整证据关闭变更

接入当前范围有效，先读[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)、[委派](../../rules/delegation.md)，代码变更读[质量规则](../../rules/code-quality.md)。本阶段不把Task Done或Push当最终Verified。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 建立验证基线

接管Implementation Baseline引用、已完成Task的Boundary/Coverage/Verification/主REQ/状态、有效证据、正式验收Task code_ref及需求集成/Push引用，据此还原最终代码/配置/数据/接口Actual Change Set，读取Integration/AC Gate/Push真实状态、稳定OI及明确治理审批。只引用已有事实，必要才沿Trace回查。

找剩余证明缺口：跨Task组合、AC Gate之外跨Requirement/Change、核心端到端、受影响既有能力回归、高风险安全约束、自动化不能替代的用户/业务确认、OI需验证或决策。有效已有证据复用，风险与影响决定范围，不默认全系统。

建立Critical Flow、Cross-Task/Requirement、Regression、Risk/Security、Runtime Boundary。每项从Source→Target→Type→Method/Requirement→Pass Condition→Evidence推导。确定性工具优先；独立审查尽可能Writer/Verifier分离、默认Fresh、高风险主动找反例、证据优先声明；用户端到端/UI/UX/视觉和业务最终确认不足时安排必要Human Acceptance，执行Agent编排不固化。

Verifier是验证职责，可由工具、Agent或组合承担，不按验证项新建子Agent。工具可判定项目优先确定性检查；相关独立推理项按[委派规则](../../rules/delegation.md)批量审查，仍保持每项Pass Condition、Evidence与独立性。并行只用于真正独立且降低整体成本的工作，不按文件、阶段或可用槽位增加Reviewer。

保存Verification Baseline：Scope、Trace（含code_ref）、Verification Items、按需Review Focus/Human Acceptance、Gates、Environment、OI引用。Finding先作Finding，仅真需跨阶段承接才关联OI；不造新Open Item副本。不写冗长测试计划。

关键AC有验证落点、实际变更可还原、可复用证据与缺口区分、组合/核心/回归/风险无重大遗漏、OI有位置、三类验证边界清晰、关键Pass Condition/Evidence存在且环境可执行，才Verification Ready。

## 2. 只读多维验证

逐项明确对象、方法、环境、通过条件、证据。复用有效证据，跨Task/关键Gate/失效证据/缺口重验。只检查当前Change/Risk相关规则，不机械扩范围。

默认不得修改被验证业务代码、业务配置、数据模型；可修测试/Fixture/Mock/验证数据/Harness等验证资产环境，但不得降低原Pass Condition或掩盖真实失败。业务问题形成Finding，由下一步路由。

先确定性Build/Static、Unit/Integration/Regression、Contract/Permission/Data、Security、Runtime Check，明确Pass/Fail/Unverified并保存可复现证据。需要跨链推理或高风险正确性/回归/安全/边界，按需Fresh Reviewer；仅在能力、上下文容量、隔离或未解决分歧需要时增加Reviewer，真正独立工作可并行，Main汇总。Reviewer只补判断不替代Gate、不直接修被审对象、不用个人风格代替规则。代码质量机器难判处按风险独立审查，项目格式由项目规则/工具处理；模型策略动态且能力充分。

先完成当前环境、廉价前提与受影响确定性检查，前提失败停止依赖试验，候选稳定后批量交独立Reviewer。修复先由实施者自检，再交未参与实现且隔离有效的原Reviewer复核修复及影响；这不是全新盲测。上下文污染、角色转实施者、首次自主行为或新会话/盲测要求时另用Fresh隔离。已验证证据只在对象、相关依赖、环境、范围及独立性仍成立时复用；Hash不变不能独证依赖不变。没有必要覆盖、新对象、新风险或未解问题不重复调用；预算不足保留Unverified，不降低通过条件。

必要Human Acceptance前给REQ/AC、实际Change、确定性结果、已知Finding和真正待判问题，不让Human重建全部上下文。不存在治理约束不额外造审批。

将Item→Result→Evidence→Finding关联。失败/争议记录现象、复现、证据、影响严重性、Suspected Origin（仅线索）；能力不足先调配置执行原契约，不误报业务Finding或权限升级。输出Verification Results、Evidence、Findings、Suspected Origin、Unverified Items；要求已完成或明确无法执行、必要审查验收完成、失败可复核且未改业务对象时进入判定。

## 3. Finding判定与纠偏

依据证据区分 Invalid Finding（误报/证据不足/验证资产问题）、Verification Issue、Implementation Defect、Upstream Deviation、Accepted Deviation、Unresolved。证据明确且不改语义的前三类可自主分类路由重验；疑似上游偏差可提来源/Trace/建议，但使REQ/AC/固定Design失效或变化需相应Confirm/Human Decision。Accepted Deviation永远Human Decision，不能降标准、跳强制Gate或标Pass。证据冲突/不足/高风险先补证据，别强行分类。

重要判断前按协作程序说明Expected/Actual、证据、影响风险、Trace、推荐；旧认知失效先修共享模型。Finding是观察与处置，OI是需继续承接的未决问题，Risk是潜在影响，分别管理。已有OI继续同ID。Unresolved可可靠观察但缺故障边界/根因时进入[Debug](../spec-debug/SKILL.md)；仅缺人类决策/外部信息则保留Finding与需决策内容。

定位最早失效层：验证资产/环境回第2步，实施回[05](../spec-development-execution/SKILL.md)，Task回[04](../spec-implementation-planning/SKILL.md)，Design回[03](../spec-technical-design/SKILL.md)，Requirement回[02](../spec-requirement-clarification/SKILL.md)。此处只判定路由，不在验证上下文隐式修上游；不是07的方法机制根因分析。

纠正源→受影响Trace→刷新验证基线→受影响验证+必要回归。仍失败带新证据再判，通过关闭Finding；关联OI只有未决问题实解且有结论才resolved。Debug Closure只是Resolution Evidence，Finding生命周期仍由本阶段判为Resolved/Accepted/Blocked/Open。Accepted保留偏差、接受理由、影响风险、后续动作，不伪装Pass。

保存Finding Resolution：Finding引用、Decision、实际Authority、Evidence、按需Invalid Source、Affected Trace、Route、Reverification Scope、按需OI、Status。必要判定/上游修正/重验完成且无未处理关键Finding则Verification Converged，否则Verification Blocked。

## 4. 证据收口与最终状态

这里只索引最终事实，不做新验证、修复或发布。汇总Task/确定性/独立/Human证据、Finding Resolution/重验、接受偏差记录，不复制新测试报告。

核对REQ→AC→Design/Constraint→Task→Actual Changes→Verification Items→Evidence→Finding Resolution完整；关键AC有有效证据、设计约束必要验证、实际变更等于被验对象、需重验有证据、无Required Gap和未处理关键Finding。

Required Verification完成、必要Gate通过、关键Finding Status为Resolved或Accepted（Invalid Finding也明确Resolved）、无阻塞OI、追溯完整，才Verified。任何必要验证未完、Gate失败、阻断Finding未解、关键证据缺失失效或Trace不闭合则Blocked。Accepted不是Pass，仍保留原偏差和风险，不能自动豁免Gate。

写Verification Closure Record：Trace、Evidence引用、Findings的Decision与Status两个独立维度、Gates、Status=Verified/Blocked、按需非阻断Open Items。明确阻断时将原因写清，不隐藏为普通遗留。后续需改进流程时进入[07](../spec-process-improvement/SKILL.md)。
