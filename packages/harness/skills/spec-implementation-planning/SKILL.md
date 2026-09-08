---
name: spec-implementation-planning
description: 接管 Ready 设计，拆解独立可验证任务，定义契约和依赖并执行 Draft→Ready 规划准入；对应 Spec Coding 阶段04。
---

# 04：把设计交给可验证任务

确认[接入](../../bootstrap/BOOTSTRAP.md)当前范围有效；读[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)，涉及委派时读[委派](../../rules/delegation.md)。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 接管实施基线

仅接管 Design Acceptance Result 的 Readiness=Ready、无阻塞规划实施OI、已收敛最终需求设计版本。Not Ready 或上游冲突/缺口返回其Owner，不自行补全。接管 Scope/Rules/AC、Solution Decision及取舍约束、Detailed Design的结构/To-Be/契约/边界、Design Acceptance的已验证假设/风险/OI/Readiness。

最终结论优先于已取代历史，已确认结论优先原始材料推测，引用优先复制；不清或冲突才回查原文/代码/证据。开放OI保留原ID状态blocking及owner，不在消费视图造新事实源。

只查交接完整性与可追溯性，不重做设计验收、不提前拆任务/测试。需求规则缺口回02；技术决策冲突回03决策；设计细节缺失回03详细设计；验收失效回03验收。修复后仅接管受影响结论。

Implementation Baseline 保存 Requirement Baseline、Fixed Decisions、Design Baseline、Constraints、按需 Risks/Open Items，尽量只引用上游，必要摘要降低理解成本。确认无过时、冲突、不可追溯或阻塞后继续。

## 2. 候选拆解

围绕行为与端到端闭环组织变化，不按文件、Controller/Service/DAO、前后端层级、行数或开发时长机械拆分。跨页面/接口/服务/数据组合才有意义的行为先视为一闭环，再按复杂度下钻。

“能独立完成且独立证明正确”作为粒度。目标不单一、边界大、不能独立验证、上下文失控说明过粗；无独立价值、必须两任务一起才能验、仅文件/函数切分说明过细。每项一个主 REQ；无法归属先查边界，真共享实现选主要闭环归属，其他关系放 Trace。

从 AC、To-Be、Contracts、Boundary Handling、Risk/Constraint 推导 Coverage，按实际需要选择主路径、合法分支、错误、空极值/重复/并发/超时/重试等边界、旧数据调用方行为兼容，不强制每项全有。这里只确定必须验什么，下一步决定怎么验。

影响策略的 Risk 绑定 Coverage/后续验证；实施需关注OI引用同ID；OI本身为独立可验证目标可建Task并Trace原OI；blocking影响拆解或设计成立则回owner/最早失真源，不默认关闭。保存 Candidate Task Set：Requirement、Goal、Trace、Boundary、Coverage、按需OI；此时不正式定 Depends On、Verification、Done、Agent或执行顺序。

## 3. 正式定义与编排

继承候选边界，补稳定唯一 ID、初始 Status=Draft、必要 Depends On、Verification、Done，形成 Goal/Boundary/Coverage/Verification/Done 的 Task Contract。一个主Requirement用于 TasksOf(REQ)和需求Gate/Git汇合，Trace可多源。Task完成不自动关闭OI，原事实源只有问题实解才更新。Task不写成文件函数逐行修改脚本；粒度不合返回拆解。

| 状态 | 语义 |
|---|---|
| Draft | 定义完成，任务集未验收 |
| Ready | 规划准入通过，依赖满足后才可执行 |
| In Progress | 正在实施 |
| Blocked | 当前任务存在真实阻塞 |
| Verifying | 实施与必要局部验证完成；有代码变更时已Task Commit并有code_ref，正执行正式验证 |
| Done | 正式Verification通过 |

生命周期 Draft→Ready→In Progress→Verifying→Done，In Progress/Verifying 与 Blocked 按开发流程恢复；此步骤只初始化Draft，下一步决定Ready。

Verification优先确定性：逻辑/规则/状态机用Unit/Property；API用API/Contract；DB/MQ/异步用Integration；Build/Type/Static用构建类型检查Lint；关键用户交互用Browser/E2E；视觉体验用Browser+Human Review。Verification说如何证明，Done说何种结果完成。每Task Verification-First，适合时Test-First，不默认把测试实施拆成独立Task。

仅记录真阻塞依赖（数据、契约、能力、验证），不按层级/习惯排固定顺序。独立、上下文可隔离、可验证时可在运行时委派，否则Main顺序推进；并行只是额外收益，上下文隔离是核心。Execution Unit已有正式委派输入，不另建Delegation Contract。

默认在已绑定 Spec Workspace 的 tasks.md（或稳定映射的等价既有位置）保留完整任务集及权威状态、主REQ，不按需求拆出独立核心状态；跨范围依赖用限定引用。单项上下文大、跨会话长生命周期、多人Agent独立负责或证据多时可下钻 tasks/Txx.md，但索引仍留核心定义、主REQ、依赖、状态、引用。上下文从Trace按需读取，不复制完整上游。不持久化Agent、Role、Model、Thinking、Fresh/Fork、Workspace、Attempt、Wave，运行时推导策略。

## 4. 任务集只读验收

整体确认，不静默改 Requirement、Design 或Task。小Feature可Main检查；规模较大时可按需使用Fresh Reviewer等按覆盖/一致/依赖/验证维度只读检查，Main汇总，独立检查本身不添新Gate或状态。

- Coverage：In Scope、AC、结构/链路/契约、重要边界、风险/OI都有实施承接；每Task唯一主REQ、TasksOf可计算。发现未覆盖需求/设计/边界、无归属任务或OI。
- Consistency：不超Scope、不改Fixed Decisions，主REQ与AC/Trace一致，Task间契约状态规则一致，无重复、矛盾、无来源任务。
- Executability：无循环依赖，真实阻塞依赖明确，上下文可得，无未定义中间契约/基础能力或遗漏blockingOI。
- Verifiability：Goal→Coverage→Done→Verification能真实证明行为，重要兼容异常边界有证据路径，同REQ任务汇合可覆盖其AC。

问题输出 Issue、Source、Impact、Recommended Return Point：需求规则回02，设计回03，Task边界回拆解，定义/依赖回本步3；持续未决复用OI，修复后只验受影响链。

无未处理阻塞、四维通过后记录 Execution Readiness: Ready 与 Coverage/Consistency/Executability/Verifiability: Pass，按需Open Risks；通过任务 Draft→Ready。Ready仅规划准入，非立即Runnable。进入[开发实施](../spec-development-execution/SKILL.md)。
