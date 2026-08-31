# Meta Protocols｜元协议

本目录维护 Spec Coding 自身的 Meta Protocol（元协议）：它们不推进业务开发阶段，而是定义 Spec Coding 如何被项目接入、解释、装配或转换为可执行机制。

当前正式 Meta Protocol：

- [`harness-compilation.md`](harness-compilation.md)：Harness Compilation Protocol（Harness 编译协议），将 Applicable Workflow + Rules 与目标项目现有能力组合成最小充分 Harness。

Meta Protocol 与 Workflow / Rules 的职责不同：Workflow 规定“怎么推进”，Rules 规定“什么必须持续成立”，Meta Protocol 规定“如何让这些规范在具体项目中被正确接入和执行”。生成出的 Harness 是项目侧运行机制，不替代 Spec Coding 的规范事实源。

后续若新增 Project Onboarding Protocol（项目接入初始化协议）等 Meta Protocol，应在完成正式设计后登记到 [`../manifest.yaml`](../manifest.yaml)；不以空文档或占位协议提前形成事实源。
