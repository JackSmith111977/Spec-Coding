# 首次 Harness 构建与验证

当前发行版本为 **0.12.0**，原样使用Stage 3 PASS的R2包。[发行记录](publication.md)绑定正式Tag、Release、下载附件与固定内容身份。真实项目仍须完成自身接入及适配验收。

本目录的release-validation.json和release-notes.md保留发布准备时的原始截面及Hash，其中“尚未正式发布”描述的是该历史时点；当前发行生命周期以publication.json及所指向的公开GitHub Release为准，不能修改旧收据来追认发布。

固定源为`2f585f0faa8c0ba831161858a2e1418fd2d527e7`，当前包内容Hash为`4451d39351a32576e99552aada821f98cc69f0c087e041273d294e6bc332db9b`。

- [构建、冻结与可复现命令](build.md)
- [最终发布准备收据与报告Hash](release-validation.json)
- [确定性终检及原始命令](final-checks.json)
- [候选Git字节身份](candidate-identity.json)
- [共享规则与接入R2独立审查](reviews/shared-r2.md)
- [01A—04 R2独立审查](reviews/planning-r2.md)
- [05—07及Debug R2独立审查](reviews/execution-r2.md)
- [独立最终行为裁决与首次阻断历史](behavior-verdict.md)
- [全源覆盖与场景设计](oracle/coverage.md)：设计不等于执行结果。
- [本地转换负控独立语义回查](reviews/local-adaptation-negative-r2.md)：缺陷副本为BLOCKED，不能冒充正常候选。
- [20个案例的原始证据归档身份](evidence-archive.json)
- [发布准备说明与兼容范围](release-notes.md)

本次完整预编译44份Canonical，产出11个Skills、4类共享规则及Bootstrap、路由、能力要求和完整性工具，共23个文件、21个资产。10项工具测试和11个Skills格式检查通过；三份独立语义审查无未解决阻塞；20项行为案例中17项正本挑战通过，3项负控检出缺陷，坏副本自身仍BLOCKED。

CLI跨Fresh恢复初次遗漏原OI/Failure收口，独立评审提出BHV-01并判BLOCKED。Owner追加真实纠正与同ID收敛，Oracle独立复核后关闭Finding；原始失败归档及提交4addbc7保留。本轮验证了含独立审查回流的闭环，不能表述为零提醒一次全过。

行为测试使用包外明确授权的独立项目、固定包副本和Fresh上下文；原始命令、运行记录和目标Git仓库位于`.harness-staging/`。发行包、验证报告及前后两份证据归档通过Release附件提供，文件名与Hash见发行记录。行为执行者禁止读取Canonical、Oracle预期、Builder摘要或其他案例。当前隔离依靠Fresh初始输入及显式工具读写边界，未宣称操作系统向执行者隐藏整个父目录。

当前第二能力环境为禁用原生委派、插件、应用与Hook的Codex CLI；这是同一产品的不同能力配置，不是跨供应商兼容证明。Claude CLI的无工具有界探测45秒超时，未取得可用行为结果，不能列为通过。

当前固定候选的结构、独立全源语义、必要真实行为及validation_focus均已有可复核证据。正式发布应原样使用该候选，并完成发布身份、合并、Tag和Release收敛；任何包修改均产生新身份并重新验证受影响范围。未来真实项目仍须自行完成接入与适配验收。
