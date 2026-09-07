# 委派与能力路由程序

在委派、独立审查、上下文隔离或运行时能力路由前读取。本规则不新增阶段、不替代 Task Contract、正式验证或[权限](global.md)与[协作](collaboration.md)。

Main Agent 始终持有 Goal、Workflow State、权威上下文、Open Item；选择角色/串并行/边界，解决跨任务和跨 Agent 冲突，验证整合结果，更新原事实源，承担最终责任和 Human 交互。

| 角色 | 工作与默认边界 | 默认上下文倾向 |
|---|---|---|
| Scout | 读项目，定位入口、链路、依赖；返回相关上下文与证据 | Fresh + Scoped |
| Researcher | 外部官方资料、标准、实际行为、评测；无项目决策权 | Fresh |
| Worker | 已确认契约内修改与局部验证；限域写入 | Scoped / Forked Contract |
| Reviewer | 独立检查正确性、完整性、回归、契约；默认只读，返回 Finding/Evidence/Verdict | Fresh + Target Artifact |
| Oracle | 只读挑战方向漂移、继承决策和约束矛盾；不是第二决策主体 | Decision-rich / Forked |

Verifier 是流程验证职责，Reviewer 是独立推理角色；后者不替代确定性验证。

## 判断是否委派

只有上下文隔离、并行、独立判断、专门能力、风险隔离或漂移检查有真实收益时使用。检查相对独立、最小充分局部上下文可提供、结果可验证、权限有界、写冲突可控；否则主 Agent 执行、拆分或串行。

正式 Task 使用已有 Task Contract 与 Execution Unit（契约、局部上下文、运行配置、工具、工作区、验证契约），不创建第二份委派产物。临时 Scout/Researcher/Reviewer/Oracle 工作交付 Goal、Boundary、Context、Authority、Expected Result、Evidence/Verification，默认不进入 tasks.md，不新建长期状态。

保持产物完整而上下文最小。只读工作独立时可并行；同一可变边界同时只能有一个 Worker Owner。写入重叠、依赖或所有权冲突返回 Main 重新划分、串行或隔离。递归委派不是默认，必须显式授权且边界清晰、父级继续负责。

Subagent 不自行改变 Requirement/AC/Scope、关键设计、Task 的 Goal/Boundary/Coverage/Verification/Done、Workflow State、Accepted Deviation 或风险接受。需要跨界时返回证据、影响、建议给 Main 路由。

## 当前能力选择

先发现当前实际可执行的模型、思考级别、上下文、工具模态、单子 Agent 路由、工作区隔离、额度和限制；Provider 理论能力不能覆盖 Runtime 事实。多个有意义候选且质量/成本/延迟选择重要时，才补充当前专项评测和本地执行证据；榜单不成为项目事实源。

综合角色、复杂度/风险/不确定/新颖性、上下文工具需求、实际能力、成本延迟，选最低充分能力。Scout 重导航/工具/速度，Researcher 重来源判断综合，Worker 重代码与长程契约执行，Reviewer 重推理找错且复杂审查能力不明显低于 Worker，Oracle 重长上下文一致性与取舍。角色不绑定固定模型或思考等级；风险和失败变化时可增加上下文、思考或能力。

具体 Model、Thinking、Fresh/Fork、Tools、Workspace、Attempt、并行属于动态运行策略，不写入正式 Task 或其他长期 Workflow Artifact，除非流程另有明确契约。

## 回传、验证与失败

临时工作返回 Result、Evidence、Uncertainty、Relevant Risk、Recommended Next Action，按角色补 Relevant Context/Sources/Gaps/Findings/Verdict/Drift。Worker 交付流程规定的 Verification-ready Result、Task Commit、code_ref，不换成通用返回格式。

所有返回默认候选。Main 按风险核验证据、确定性检查、独立 Reviewer/Oracle 后才更新既有事实源；不创建 scout-state/reviewer-truth。Subagent 完成不意味着 Task Done、Requirement Verified、Finding Closed 或流程完成。

- 能力问题：上下文/模型/思考不足、工具不可用、重复失败，优先补上下文、提高能力、改策略或独立审查，归属执行 Attempt。
- 边界问题：需越过委派/Task Boundary，返回 Main 重新判断 Task、Design 或依赖。
- 权限问题：涉及 Requirement/AC/Scope/高影响设计/风险接受，由 Main 走 Autonomous/Confirm/Human Decision。

Fallback 只有仍满足完整要求时才可静默使用；否则显式降级、升级或阻断，API 可用不证明能力等价。执行中能力变化先按[适配程序](../skills/spec-harness-adoption/SKILL.md)重验受影响动作，再继续；不重新预编译规范。
