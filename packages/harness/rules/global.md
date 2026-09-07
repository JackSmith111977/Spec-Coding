# 全局执行程序

所有正式主流程和异常流程执行前加载本文件及[人机协作](collaboration.md)。有委派、隔离、独立审查或能力路由时加载[委派规则](delegation.md)。具体流程更严格的要求继续适用。元协议只复用下面的权限语义及适用协作规则，不继承仅属于 Workflow 的 Task/Gate。

先选择深度：已有完整有效证据用 Reuse；局部、低风险、边界清晰用 Light；一般 Feature 或跨层变化用 Standard；高风险、不确定、跨系统、难回滚用 Deep。职责可以由有效证据满足，不机械重做文档。出现 Schema/数据迁移、状态机、权限安全、并发异步、兼容性、难回滚或影响不明时提高深度。

无论深度，都保留正确的 Requirement、Scope、Acceptance Criteria（验收标准），以及 Requirement → Design → Task → Change → Verification 可追溯链；Blocking Open Item、必要 Gate、与风险相称的验证证据、权限边界、真实协作触发时的决策就绪、偏差纠正链路均不得裁掉。Git 固化变更必须保留 Task Commit 与 `code_ref`。

## 权限判定

依据是否改变已确认事实源及错误影响判定权限，不按阶段机械审批：

- Autonomous：不改变既定语义契约，可回退、可验证、边界清楚，继续自主推进。
- Confirm：显著技术、架构、数据或安全影响，先完成可审阅方案及依据，再取得 Human 确认。
- Human Decision：业务意图、Requirement 语义、In/Out Scope、核心业务规则、AC 语义、Accepted Deviation、风险接受和强制 Gate 豁免，由 Human 决定。

先取证缩小问题，复用已确认边界和授权，不重复请求批准。不把一句启动指令解释为额外权限。出现边界时按[协作程序](collaboration.md)提供最小充分信息。

## 开放项传递

Open Item 是当前尚未解决、需要后续阶段或 Workflow 继续承接的问题。首次识别到符合该条件的问题时建立稳定 `OI-xxx`，记录 `origin, description, status, blocking, owner_stage, related`；状态为 `open / resolved / deferred`。下游继续引用同一 ID，不复制事实源。resolved 补充 resolution 结论和必要依据；deferred 补充明确延期理由和承接位置。`blocking=true` 不得越过对应 Gate。Risk、Finding 与 Open Item 分别管理，按需关联，不自动转换。

非直观术语首次承载关键语义时写英文及中文解释；字段、状态、ID、代码标识可保留英文。Spec Coding 是方法名称，不默认另建名为 Spec 的产物。

发生失败信号、非预期行为、归因不可靠或未解决 Finding 时，按[全局路由](../bootstrap/routes.md)判断 Debug 和最早失真源；不能靠改下游判定标准掩盖上游问题。
