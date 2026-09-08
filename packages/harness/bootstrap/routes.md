# 全局流程路由

正式Workflow前使[全局](../rules/global.md)和[协作](../rules/collaboration.md)有效；委派/隔离/独立审查/能力路由前读[委派](../rules/delegation.md)。代码产物遵守[质量](../rules/code-quality.md)，05/06主要消费。所有相关产物动作使[产物规则](../rules/artifacts.md)有效，从空间入口定位权威内容与必要依赖。Meta只复用适用权限/协作/委派/产物约束，不继承Workflow特有Task/Gate。

执行当前步骤前读完整Skill与适用资源，按manifest.dependencies读共享依赖；跨阶段链接是路由，不要求同时加载全部。未激活程序保持可达，激活前补齐[能力](requirements.md)适配与验收。

| 触发 | 程序 | 移交 |
|---|---|---|
| 首次接入或相关变化 | [Harness接入](../skills/spec-harness-adoption/SKILL.md) | 基线、发现、适配、验收；仅接入则结束，有明确启动新业务工作或继续既有工作的意图则进入或恢复适当Workflow，不要求已有Task |
| 基线缺失/稳定意图或绑定失效/显式重接入 | [Project Onboarding](../skills/spec-project-onboarding/SKILL.md) | 回Harness接入，不直接宣称READY |
| Greenfield且无有效流程状态 | [01A](../skills/spec-project-definition/SKILL.md) | 02 |
| Brownfield且项目认知不足 | [01B](../skills/spec-project-understanding/SKILL.md) | 02 |
| 已有有效权威产物/状态 | Resume最早仍有效Owner | 复用有效证据并履行该职责 |
| 需求含义/范围/规则/AC待明确 | [02](../skills/spec-requirement-clarification/SKILL.md) | 03 |
| 需求已明确、设计或设计纠偏 | [03](../skills/spec-technical-design/SKILL.md) | 设计Ready后04 |
| 设计Ready、任务拆解或契约纠偏 | [04](../skills/spec-implementation-planning/SKILL.md) | 规划准入Draft→Ready后05 |
| 已Ready任务或实现修复 | [05](../skills/spec-development-execution/SKILL.md) | Required Task Done及Integration/AC Gate/Push完成后06 |
| 完整Change最终验证/Finding收敛 | [06](../skills/spec-verification-convergence/SKILL.md) | Verified/Blocked，按需07 |
| 真实执行后的可复用机制改进 | [07](../skills/spec-process-improvement/SKILL.md) | 权限确认、实施、下一轮真实效果验证 |
| 失败信号/非预期行为/归因不可靠/未解决Finding | [Debug](../skills/spec-debug/SKILL.md) | 原Owner凭Resolution Evidence写状态 |

可靠归因的局部实现问题返回原Worker短闭环；需跨层、缺证或无法判断边界根因时Debug。未决只缺人类决策/外部信息时保留Finding/OI承接，不机械诊断。

最早失真源路由：REQ/AC→02，Design→03，Task→04，实现→05，验证资产/环境→相应验证或运行治理。只刷新受影响Trace重验。Debug只关闭Failure，Task/Finding/OI/Requirement由Owner写回；Task Done、Push、Failure Resolved不替代06 Verified。

运行时工具/模型/权限/隔离/Fallback变化须在依赖动作前回发现/适配/验收，不重编译或沿旧READY。稳定意图/绑定变才Onboarding。权限、blockingOI、必要Gate不可裁剪；已确认边界不重复请求。
