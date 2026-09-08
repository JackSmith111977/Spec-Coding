# 0.13.0 Stage 3 最终判定

判定：**PASS**。本次固定R2满足结构、独立语义及必要行为验证要求，可进入Stage 4原样发布。桌面接入结果写回已获独立复核PASS，阻塞Finding为0；本判定不代替正式Tag/Release事实或目标项目验收。

公开分发使用[脱敏副本](sanitization.md)，原审查与Hash仍绑定本地原件；公开Hash另列。只改变包外证据的展示，不改变固定包与行为判定。

## 对象与来源

本轮版本为0.13.0，固定候选R2提交 `6f95f43f74c5a134c887db167e123fe9c54498b4`，来源 `8a41958f3feaf08f02dabc5fd67c9b70c7f87604`。包24文件的 `package_sha256` 为 `3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c`；原样发行ZIP的SHA256为 `3c7908906c9d1a01a09f7038ba242d157661ff9125af1d3dde4745ac00c0cddd`。后续包外报告、仓库发布状态和Tag提交不替换这两个身份。

上一正式0.12.0的规范源为 `2f585f0faa8c0ba831161858a2e1418fd2d527e7`；本轮因共享规则和接入链广泛变化按FULL构建。45份Canonical、全部入口及消费者的来源与依赖见[构建记录](build.md)和[candidate-identity.json](candidate-identity.json)。结构与完整性复核通过，11项工具测试全部通过。

## 独立语义与行为依据

共享规则、两Meta和包级入口的[独立语义审查](semantic-shared.md)及[业务流程审查](semantic-workflows.md)均PASS，阻塞Finding为0。Reviewer直接读取固定规范原文；行为执行者使用Fresh上下文和固定包，不读取Canonical。实际工具轨迹、初始清单、项目文件及Git对象由独立Reviewer核对，不以执行者自述或脚本断言数量代替判定。

| 必要类别及本轮重点 | 实际依据与结论范围 |
|---|---|
| 正常跨流程、共享设计和最终验收 | F05/F07真实检查、精确代码、本机Push、06收口PASS；保留Accepted偏差及未决项。见[本机闭环判定](closure-verdict.md)。 |
| 空间与共享边界、身份及迁移 | F01三种既有空间维护、F02双仓同名ID迁移检查点、中文空格路径PASS；不是所有模式Runtime认证。见[首次组织判定中的F02](organization-initial-verdict.md)及[边界判定](boundaries-verdict.md)。 |
| 权威、Gate及渐进读取 | tasks权威、详情冲突、跨需求传递阻塞、陈旧摘要、只读与缺证检测PASS；被测需求保持Blocked可以是正确结果。见[导航判定](navigation-verdict.md)。 |
| 异常与证据生命周期 | F07真实故障修复、原始失败证据保留与晋升、Finding/OI独立归属及LEGACY缺证不关闭；首次状态错误与纠正完整保留。见[组织纠正](organization-correction-verdict.md)及[本机闭环](closure-verdict.md)。 |
| 并发写回和适配身份 | 真实并行采集后单Owner消歧，旧ID保留；缓存同身份恢复、双范围及用户修改保护PASS，限定文件维护。见[边界判定](boundaries-verdict.md)。 |
| 未安装起点的接入、实际读取与写回 | R2 Bootstrap建立基线和入口，随后固定本地适配并独立审查；新Fresh显式读取桌面入口，真实写正文、导航及回读，有限失效窗口PASS。见[桌面判定](desktop-verdict.md)及[结果收口复核](desktop-closure-verdict.md)。 |

当前必要挑战覆盖normal、boundary、authority/gate、exception/routing及本轮共享产物、索引、写回、迁移、缓存和接入组合风险。扩展设计矩阵并非全部完成，逐项实际范围见[行为覆盖表](behavior-coverage.md)。本次汇总不以未测试的场景提供通过依据，也不把扩展效率计划当作已完成实验。

## 失败及回流

1. R1被独立语义审查阻断：05必需字段被整体弱化为按需输出。回到构建层修正，重新固定R2及重新验证；R1未发布，其报告保留。
2. R2的F05/F07首次豁免必要Push而提前Verified，独立判定BLOCKED。外部提醒后Owner撤回状态，纠正判定PASS但需求仍Blocked。随后新增明确本机同步授权，由两个新的Fresh执行者真实Push与06复核，独立判定才通过。不声称首次无人提醒全过。
3. CLI A误读排除的旧记录，方法失败；A2限定输入重跑通过。CLI W真实写入被底层只读策略拒绝，旧BLOCKED及原始stderr保留。另用桌面实际可用工具验证显式入口范围，没有绕过或改写CLI策略。
4. 本地接入结果写回保留已验身份快照，单独复核结果变化，不以旧聚合Hash冒充当前文件身份；不修改固定包。

## 兼容性与证据限制

实测为Windows、PowerShell、Python 3.13.7及本轮Codex工具环境。桌面通过仅指本次Fresh显式项目入口和受控读写；精确桌面宿主及模型部署版本未知，不借CLI版本补填。CLI 0.144.1的特定隔离配置只提供有限加载/只读证据，不能宣称可写或完整READY。目标项目仍需按真实Runtime、权限和作用域验收，未来未激活能力与配置变化需核验受影响部分。

未完成POSIX、跨模型与多Runtime普适认证、远程HTTP/CI服务、完整升级失败回滚、真实进程崩溃、全套五项负控、效率对照或真人审阅；不宣称这些已通过或已经提高效率。Fresh上下文和显式权限边界不等于OS隐藏所有父目录，过滤轨迹也不是宿主全活动审计。

汇总范围及失败回流另经[独立发布解释审查](release-review.md)确认；该报告当时等待的desktop前置现由[收口独立复核](desktop-closure-verdict.md)满足。[被审草稿](stage-3-reviewed-draft.md)原样保留，不把历史待验状态改写为当时已通过。

维护者签署汇总日期：2026-09-09。附件检索、Hash及使用方式见[发行记录](publication.md)；只有Git Tag/正式Release实际存在后才提供正式发行身份。
