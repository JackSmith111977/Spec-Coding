# Rules｜规则

本目录维护持续适用的正式 Rule（规则）。Rule 定义执行过程中需要遵守的原则、约束或质量要求，本身不推进 Workflow（流程）或 Meta Protocol（元协议）状态，也不形成新的阶段。

当前正式规则：

- [`global-contracts.md`](global-contracts.md)：Global Contracts（全局执行契约），定义所有正式 Workflow 默认继承的通用执行规则。
- [`human-agent-collaboration.md`](human-agent-collaboration.md)：Human-Agent Collaboration Rules（人机协作规则），定义共享认知、同步触发、决策就绪与 Human 反馈吸收原则；除正式 Workflow 外，也适用于涉及 Human 意图、权限或关键判断的 Applicable Meta Protocol。
- [`agent-delegation-and-coordination.md`](agent-delegation-and-coordination.md)：Agent Delegation & Coordination Rules（Agent 委派与协调规则），定义 Main Agent / Subagent 职责、委派与协调、运行时能力与模型路由、结果验证与升级原则。
- [`code-quality.md`](code-quality.md)：Code Quality Rules（代码质量规则），定义代码产物的可理解性、信息质量、变更清晰度与一致性原则。

正式 Rule Document 以 [`../manifest.yaml`](../manifest.yaml) 的 `rule_documents` 为机器可读入口。Workflow / Meta Protocol 只引用适用规则，不复制规则正文形成并行事实源。
