# Execution R1 独立语义审查

结论：**BLOCKED**。已完整审查分配的 **18/18 份 Canonical 正文**、对应四个 Skill 的全部资源及必要共享依赖。发现 **2 项阻塞语义差异**，均为压缩后新增的强制行为或限制。非阻塞 Finding：0。没有将普通排版、术语中英混用、段落长度或字段展示形式列为阻塞。

## 身份、边界与证据取得

- 仓库：`C:\Users\hp\Documents\ChatGPT\Spec Coding`。
- 固定 Canonical revision：`2f585f0faa8c0ba831161858a2e1418fd2d527e7`。
- 候选：`packages/harness`，版本 `0.12.0`，构建方式 `FULL`。
- 固定 `package_sha256`：`df12bb60ef594c9fb2a324b91b92fe10f4919b1413609f5154fc296cdd6405d1`。
- 首个包校验动作：`python packages/harness/scripts/verify.py`，退出码 0，返回 `integrity=PASS`、`files=23`、上述 revision 与 package hash，均与委派输入一致。
- Canonical 证据直接来自 `git show <固定revision>:<路径>`；候选直接读取磁盘文件。逐文件输出全文及一基行号，按有限批次读取，成功输出均未截断。最初一次控制台编码失败的 05 读取已使用 UTF-8 从头完整重读，不以乱码或失败输出计入覆盖。
- 未读取 Builder 摘要、其他审查报告或他人的语义解释。报告中的判断由本审查者直接比较原文与候选形成。
- 完整读取并比较四个 Skill；目录清单确认这四个目录各只有一份 `SKILL.md`，没有遗漏配套 references、脚本或其他资源。
- 为判定组合行为，完整读取四类共享规则及其 Canonical、Bootstrap/路由/能力要求、接入与项目接入程序及其 Canonical。另完整读取 02/03/04 候选承接入口，仅核查本组异常回流可达及入口契约，不声明这些组的全量 Canonical 已由本报告审查。
- 四组 README 只用于补核导航与入口边界，正文判定仍以固定 revision 的 18 份分配正文为主。
- 本次只新增本报告；未修改候选、Canonical 或其他报告。FULL 首次构建已有用户授权，本审查未增加批准请求，也未执行接入、发布或候选行为试验。

以下所有路径均相对于上述仓库。Canonical 行号以固定 revision 为准；候选行号以固定 package hash 为准。逐文件原始字节 SHA-256 与完整读取行数见末尾读取清单。

## 阻塞 Finding

### EX-R1-01：共享规则将跨阶段承接条件省略，扩大 OI 创建触发

分级：**阻塞 / P2**。类型：新增强制行为、共享规则与局部流程组合冲突。

**Canonical 依据：**

- `docs/rules/global-contracts.md:37-39`：Open Item 是“尚未解决、需要后续阶段或 Workflow 继续承接”的具体问题或决策；`:54-67` 的首次发现、同 ID 复用与状态要求是在该对象定义下成立。
- `docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md:107`：新发现先作为 Finding，只有确实需要跨阶段继续承接时才创建或关联 OI。
- `docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md:35-37`：Finding、Risk、OI 分别管理；只有处置需要跨阶段等待决策、信息或承接时才创建或关联 OI。
- `docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md:84-86`：未复现仍可基于可信现场证据调查；只有证据不足且阻止可靠调查才补证或通过稳定 OI 承接。`:107` 的 OI 字段限定为尚缺且需要跨阶段承接的问题。

**候选位置：**

- `packages/harness/rules/global.md:21` 直接要求“首次发现未决问题时建立稳定 `OI-xxx`”，没有保留需要后续阶段或 Workflow 承接的条件。
- 同文件 `:3` 使该程序成为所有正式主流程与异常流程的前置共享规则。
- `packages/harness/skills/spec-verification-convergence/SKILL.md:18,38` 虽然正确保留局部的按需 OI 条件，仍同时依赖该全局指令；`packages/harness/skills/spec-debug/SKILL.md:18-20` 同样保留局部条件，无法消除全局强制创建的冲突。

**行为与影响：**

例如，一个可在当前验证步骤直接分类并关闭的 Finding，或当前 Debug 取证循环内即能消除的未决问题，Canonical 允许保留为局部 Finding/调查信息。候选全局程序却在首次发现时即要求建立稳定 OI，增加长期对象、状态维护及 owner/related 等承接负担，并使跨阶段持久化边界不再明确。四个分配 Skill 都加载该共享规则，因此影响并不限于单一局部句子。这里改变的是对象创建的适用条件，属于语义增量。

**需要修正的内容：**在全局 OI 程序中恢复原对象定义及创建前提，仅对需要后续阶段或 Workflow 承接的具体未决问题建立或关联稳定 OI；保留同 ID、blocking、resolution、deferred 等既有约束。复核局部可闭环 Finding、当前调查未知与真正跨阶段问题三类路径。

### EX-R1-02：Debug 将默认避免全量重扫压缩为无条件扫描限制

分级：**阻塞 / P2**。类型：有效 Guidance 的条件丢失、新增禁止性限制。

**Canonical 依据：**

- `docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md:17-26` 要求优先复用有效基线。
- 同文件 `:44` 原文为“已有基线不足时，再沿代码、配置与运行时定向下钻，**不默认重新扫描整个项目**”。它规定默认调查策略，并保留按证据和缺口扩大调查的余地。
- 同文件 `:99-119,151` 要求逐步收敛故障边界，已有基线不可用时可直接依据 Failure Baseline、System Context 与 Runtime Evidence 调查。

**候选位置：**

- `packages/harness/skills/spec-debug/SKILL.md:24` 在说明基线不可用时如何调查后，以“**不全量扫项目**”结束，省略“默认”，将偏好的调查策略写成无条件限制。
- 同文件 `:26-30` 列出取证工具与收敛步骤，但没有恢复该限制的条件；已读取的全局、路由、能力和委派资源亦未为 Debug 的这项限制提供相应例外。

**行为与影响：**

当既有基线失效、入口或跨组件影响尚不清楚，且证据证明较广的代码/配置盘点是必要调查手段时，Canonical 允许基于缺口调整调查范围；候选文字会禁止涉及整个项目的盘点，即使其由当前故障证据驱动。该差异缩小了允许的取证手段，可能使故障边界无法充分定位。问题在于默认条件被删除，并非要求日常 Debug 执行全量扫描。

**需要修正的内容：**恢复“优先复用、缺口驱动定向下钻、不默认全量重扫”的条件性指导，保持范围由实际证据与故障边界决定。复核有效基线的局部故障与基线失效的跨组件故障两种路径。

## 逐源反查覆盖

下表“已核对”表示该源从首行至末行的硬规则、状态、Gate、Authority、触发、异常、程序、产物与有效 Guidance 均已直接比较；不代表所在组合已通过。EX-R1-01 是四组共同加载的依赖问题，EX-R1-02 是 Debug 第二步的局部问题。

| 分配 Canonical 正文 | 全文行范围 | 对应候选位置 | 核对的关键语义及结果 |
|---|---:|---|---|
| `docs/workflows/main/05-development-execution/01-ready-task-scheduling.md` | 1-164 | `packages/harness/skills/spec-development-execution/SKILL.md:10-18`，共享委派规则 | 已核对 Ready/Runnable 区分、依赖/Blocker/环境、串并行与单写边界、最小 Execution Unit、能力发现、认领与 Attempt 异常；局部未发现差异。 |
| `docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md` | 1-174 | `packages/harness/skills/spec-development-execution/SKILL.md:20-30` | 已核对接管、局部检索/Scout、契约内自治、权限升级、确定性局部修复、Task Commit/code_ref、提交失败留 In Progress、送 Verifying 产物；局部未发现差异。 |
| `docs/workflows/main/05-development-execution/03-verification-and-exception-convergence.md` | 1-164 | `packages/harness/skills/spec-development-execution/SKILL.md:32-49` | 已核对精确提交对象、独立 Gate、按需 Fresh Reviewer、先归因再分流、能力问题与业务缺陷区分、Debug 回 Owner、三类 verdict 和目标状态；局部未发现差异。 |
| `docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md` | 1-202 | `packages/harness/skills/spec-development-execution/SKILL.md:51-61` | 已核对 tasks.md 权威性、Blocked 五项信息、阻塞不伪造下游状态、REQ 全 Done 后 Integration/AC Gate/Push、Sync 非第四权威源、失败保留 Task 事实与事件驱动调度；局部未发现差异。 |
| `docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md` | 1-143 | `packages/harness/skills/spec-verification-convergence/SKILL.md:10-20` | 已核对完整 Change/code_ref/Sync 接管、跨任务跨需求/回归/安全/人工缺口、有效证据复用、风险范围、三类验证及 Verification Ready；局部 OI 条件正确，共享组合受 EX-R1-01 影响。 |
| `docs/workflows/main/06-verification-convergence/02-multi-dimensional-verification-execution.md` | 1-118 | `packages/harness/skills/spec-verification-convergence/SKILL.md:22-32` | 已核对只读业务对象、可修验证资产但不降标准、Pass/Fail/Unverified、独立推理用途、Human Acceptance 决策就绪、能力失败不误报业务 Finding；局部未发现差异。 |
| `docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md` | 1-137 | `packages/harness/skills/spec-verification-convergence/SKILL.md:34-44` | 已核对六种判定、实际 Authority、Accepted 必须 Human Decision、最早失效层、Unresolved 的诊断/决策分支、受影响重验、OI 及 Finding 正交状态；局部 OI 条件正确，共享组合受 EX-R1-01 影响。 |
| `docs/workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md` | 1-119 | `packages/harness/skills/spec-verification-convergence/SKILL.md:46-54` | 已核对只做事实收口、完整 Trace、Required Verification/Gate/OI 门禁、Invalid 的 Resolved、Accepted 不等于 Pass、Verified/Blocked、无治理约束不新增审批；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/01-evidence-collection.md` | 1-132 | `packages/harness/skills/spec-process-improvement/SKILL.md:10-14` | 已核对六类证据、关键事件筛选、客观事实不提前归因、EV 字段与原始来源、Spec 非默认独立产物；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/02-process-reconstruction.md` | 1-102 | `packages/harness/skills/spec-process-improvement/SKILL.md:16-20` | 已核对 subject/关联串链、保留演变、每节点可回 EV、不提前评价、统一 reconstruction.md 及字段；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/03-issue-detection.md` | 1-126 | `packages/harness/skills/spec-process-improvement/SKILL.md:22-26` | 已核对异常信号、实际影响筛选、排除正常变化、初步类别可修正、ISS 字段与六个生命周期状态；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/04-root-cause-analysis.md` | 1-152 | `packages/harness/skills/spec-process-improvement/SKILL.md:28-32` | 已核对机制根因、六类缺口及 other、最早拦截点、发现与逃逸区分、多对多、缺证追溯/降低置信度、RC 产物；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/05-improvement-design.md` | 1-133 | `packages/harness/skills/spec-process-improvement/SKILL.md:34-40` | 已核对可复用机制范围、No Process Change、权威落点、最小有效改动、Autonomous/Confirm/Human Decision、Behavior Delta、实施前 validation_plan、IMP 字段；局部未发现差异。 |
| `docs/workflows/main/07-process-review-improvement/06-implementation-and-validation.md` | 1-130 | `packages/harness/skills/spec-process-improvement/SKILL.md:42-48` | 已核对实施前授权、偏离 decision 重新判权、反向追溯、真实下一轮 Effect/Cost、保留/调整/删除、同 IMP 持续跟踪及既有机制不自动授新权；局部未发现差异。 |
| `docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md` | 1-144 | `packages/harness/skills/spec-debug/SKILL.md:10-20` | 已核对异常归一、引用已有对象、先保护现场再按权止损、普通缺陷不铺事故流程、最小充分复现、六种复现状态、未复现不等于无效；局部 OI 条件正确，共享组合受 EX-R1-01 影响。 |
| `docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md` | 1-208 | `packages/harness/skills/spec-debug/SKILL.md:22-30` | 已核对 Expected/Observed/First Divergence、区分性证据、Recent Change 非原因、可证伪假设、保留反证、定位产物与假设状态；扫描范围 Guidance 存在 EX-R1-02。 |
| `docs/workflows/exceptions/debug-and-defect-resolution/03-root-cause-confirmation-and-correction-routing.md` | 1-176 | `packages/harness/skills/spec-debug/SKILL.md:32-40` | 已核对症状/促成因素/根因、排除替代原因、干预与安全多源证据、Confirmed/Probable/Unconfirmed、风险与不确定性、六类最早源及 Owner 路由；局部未发现差异。 |
| `docs/workflows/exceptions/debug-and-defect-resolution/04-fix-verification-and-failure-convergence.md` | 1-168 | `packages/harness/skills/spec-debug/SKILL.md:42-52` | 已核对实际纠正接管、按原复现状态重验、受影响链路复用验证、Resolved/Blocked、残余风险/OI、不创造中间关闭状态、回 Owner 维护主流程状态且 Resolved 非 Verified；局部未发现差异。 |

## sources、dependencies 与共享承载

四组 `manifest.artifacts[].sources` 经固定 revision 目录清单反查，分别准确包含 4、4、6、4 份编号正文，集合完全相等，无错配或遗漏。位置为 `packages/harness/manifest.json:206-211,232-237,256-263,281-286`。四组自己的文件/目录均存在，全部声明依赖 ID 均可解析。

- `rule-global` 与 `rule-collaboration`：四组均在清单与正文入口声明；分别完整读取并对照 `docs/rules/global-contracts.md`、`docs/rules/human-agent-collaboration.md`。权限、共享认知、真实协作触发和反馈回权威源已承载；OI 创建条件见 EX-R1-01。
- `rule-delegation`：`manifest.json:9-12` 的条件依赖、`rules/global.md:3`、`bootstrap/routes.md:3`，以及 05/06 入口、07/Debug 条件引用，共同保证委派、隔离、独立审查和能力路由前加载。其未重复出现在四组每一个静态 dependencies 数组中，不构成本次遗漏：条件加载与正文语义均实际存在。角色权限、单写边界、临时委派、能力路由、回传候选和失败分流已直接对照完整原规则。
- `rule-code-quality`：05/06 静态声明并在代码变更时消费，Debug/07 代码产物由条件依赖与全局路由补齐。四类质量原则、注释有效性、最小完整变更和项目惯例均承载，未因个人风格增加 Gate。
- 确定性验证、独立审查、观察恢复等能力还由 `bootstrap/requirements.md:3,7-15,17-19` 按适用条件定义，并由当前流程正文和接入程序识别。因此没有仅凭 06/Debug 的 `requires` 较短就认定必要能力被移除。
- 02/03/04 是跨阶段返回入口；完整读取其候选，确认需求语义、设计修正、Task 契约失效均有对应程序与准入门禁。`bootstrap/routes.md:5` 明确跨阶段链接是路由，不要求一开始同时加载全部正文，故没有把所有路由目标机械当作静态共享依赖。
- Bootstrap、接入、项目接入、恢复及候选测试资源已全部读取；对照两个固定 Canonical 元协议，确认当前范围就绪、能力变化前重验、原包不可热修、授权复用与候选测试范围边界。这里对必要依赖的读取用于本组执行语义判断，不代表其他审查分工或全包发布已通过。
- 另按 README 定义独立复算所有清单资产树 hash，未发现不一致；包内 Markdown 文件链接检查未发现缺失目标。这些是辅助结构证据，不代替上述语义比较。

## 结论与复核要求

本次 18 份正文的完整读取与逐源审查已完成；**BLOCKED 的原因是两个未解决语义差异，不是读取不足或环境访问失败**。需要由候选维护者修正并形成新固定候选，然后对 EX-R1-01 的共享组合影响及 EX-R1-02 的 Debug 路径重新审查。候选内容一旦变化，本报告所绑定 hash 的结论不能移用于新候选。

本报告仅判定本分配范围的 Canonical→候选语义保真度，未宣称整个包语义、目标 Runtime 行为、接入验收或正式发布通过。

## 实际完整读取清单与固定文件 hash

以下清单由实际已读文件集合生成；Canonical hash 取固定 revision 的 Git blob 原始字节，候选 hash 取固定包的磁盘原始字节。行范围覆盖每份文件全文。导航文件和辅助依赖单列，未混入 18 份分配正文的完成计数。

### 分配 Canonical 正文（18 份）

| 文件 | 全文行范围 | SHA-256 |
|---|---:|---|
| `docs/workflows/main/05-development-execution/01-ready-task-scheduling.md` | 1-164 | `2b58d385b0a3700e3d06b7db2fc5392cffb776688918dc931459ab88d13bc270` |
| `docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md` | 1-174 | `ffb93ef64817d1b7659c23ff8da544712899c32220aae3cdf43a2aac0f129a24` |
| `docs/workflows/main/05-development-execution/03-verification-and-exception-convergence.md` | 1-164 | `8d8b9fc519106999a700a5e4f578e8f0dbed3bdc9a7333d3705869a804096f43` |
| `docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md` | 1-202 | `2cf0ea8917ee8c6a8de2b60e37b6d50e89dc7bd99707d8badfafb5c240372365` |
| `docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md` | 1-143 | `61bcf438f0a9623237c808c1c6872b87169e75f120e5c2157362b9fcf30225a5` |
| `docs/workflows/main/06-verification-convergence/02-multi-dimensional-verification-execution.md` | 1-118 | `721077252d87056c44f91ca57f59860d455ae0d6acf39ae686a66f4515e27f43` |
| `docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md` | 1-137 | `6be7688cd7380e05d944354d4973cf31c18b98ea405ea7dfe09957bee46b2e19` |
| `docs/workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md` | 1-119 | `67769aba7827104662c0a2a2e7ec1b7eded7f4863ce601a02f7b3958d8b15bc3` |
| `docs/workflows/main/07-process-review-improvement/01-evidence-collection.md` | 1-132 | `b630a6bb451770da9fcbd8aa50e4af0986b360c1f5925217288f9f7bb3e49bd5` |
| `docs/workflows/main/07-process-review-improvement/02-process-reconstruction.md` | 1-102 | `62ba04ca68af60a62bb6bf1fa426d71d0672385b2124749eca0029b94bb2a571` |
| `docs/workflows/main/07-process-review-improvement/03-issue-detection.md` | 1-126 | `252df87d349293c6936f2d2c5467b50a2d7272b40761fba50d9e7f8d7ba376bb` |
| `docs/workflows/main/07-process-review-improvement/04-root-cause-analysis.md` | 1-152 | `787629a5483ae380e5bd15ad49705276d622cfb4125f22ef3f92039d2cbbb7da` |
| `docs/workflows/main/07-process-review-improvement/05-improvement-design.md` | 1-133 | `ecba970433df48275d61ba7b125ab73f7b7141c2b6c488afa0b92df8fe83a992` |
| `docs/workflows/main/07-process-review-improvement/06-implementation-and-validation.md` | 1-130 | `f33bb644397f2d22b2152fc8fe05ec40995a9403c4b46e8359f3fc0198179102` |
| `docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md` | 1-144 | `e148dca5a56d6a9319f1261e4129b1ae971da0c8727cf2ed5e67c5f42a7d5084` |
| `docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md` | 1-208 | `5224405d1837d8c36c1781669b7dc526b624a9493ea7cab98f00ac4f1d8fb003` |
| `docs/workflows/exceptions/debug-and-defect-resolution/03-root-cause-confirmation-and-correction-routing.md` | 1-176 | `fe1dd070b36bb56e4f62fee08faf7c0a9c47f255b79bda1222c95b827eb582b3` |
| `docs/workflows/exceptions/debug-and-defect-resolution/04-fix-verification-and-failure-convergence.md` | 1-168 | `8982ee10c1742f4af5910b983b5415c78df56cfebe1ccb36f063f50d66155648` |

### 必要 Canonical 共享依赖（6 份）

| 文件 | 全文行范围 | SHA-256 |
|---|---:|---|
| `docs/rules/global-contracts.md` | 1-97 | `6bd268abbf1cd96a4fa154d42c26fae59f07e180d9f85e03103209af668d49fc` |
| `docs/rules/human-agent-collaboration.md` | 1-159 | `3a48c58f0ae1eb1d5cd51a548df61e840c77a1198277e5e20167dc94972175a5` |
| `docs/rules/agent-delegation-and-coordination.md` | 1-249 | `1b53932178d3647877bfb95c4b5da2132a48d88a8f506044ae7bd33c7bc2f610` |
| `docs/rules/code-quality.md` | 1-107 | `d3cff36ad0bdc285fd76a0ae9d3aa69d3906b1aafd928c84ddf0948a9af68389` |
| `docs/meta-protocols/harness-adoption-and-adaptation.md` | 1-211 | `dd6cfbc4c05ccacbc1ee3898bf49a70ee72c0b086eca2b7b211a0eb174158d5b` |
| `docs/meta-protocols/project-onboarding.md` | 1-216 | `fa64d6c41bd33a0d9ffc2abf771ca2ed796b0f91a2b2df9ef0ccf0a209b58d81` |

### 补充导航（4 份）

| 文件 | 全文行范围 | SHA-256 |
|---|---:|---|
| `docs/workflows/main/05-development-execution/README.md` | 1-39 | `c843354d109464b1100a1b1b22460a6b0e6ee18760a5bc99e1fb249eed961a41` |
| `docs/workflows/main/06-verification-convergence/README.md` | 1-39 | `5594e6bad7684c847f2df92902b0fab6c4ff75ea4a5926b56d8043fae7552ac1` |
| `docs/workflows/main/07-process-review-improvement/README.md` | 1-43 | `966754ebb4c1ecfc5b0f60fe62a60eca6c1a128abf0ae21f24a25a39b7da78fc` |
| `docs/workflows/exceptions/debug-and-defect-resolution/README.md` | 1-63 | `26416d7f3a3f22267c967fa5febea9e034134ed35d04cfcf689c9c13b4dd51a9` |

### 候选完整读取资源（21 份）

| 文件 | 全文行范围 | SHA-256 |
|---|---:|---|
| `packages/harness/README.md` | 1-27 | `66e31f7e58e74b01c731e40f1f5830d06f25980b5654eb3108099a9c7e7c21f9` |
| `packages/harness/manifest.json` | 1-558 | `2f724f19b206a7a1cfb1e2e9b2d9f9fdef5c7000ca374c1a89de908d924d11ec` |
| `packages/harness/plugin.json` | 1-7 | `5ce1881e1359dfb7657c041c8cdb9826db14335cfc8f01eb95450bae4a2c6c80` |
| `packages/harness/scripts/verify.py` | 1-72 | `62812b7c380421b2dbfb62aa84a72b1543b0efc50c5bf7ca3b7066bbd0b1c6bc` |
| `packages/harness/bootstrap/BOOTSTRAP.md` | 1-12 | `40784682fa52df74b9006d3f7b11f410fad2a385028c51c86a40bf2969f550e2` |
| `packages/harness/bootstrap/routes.md` | 1-26 | `704704864ffd62ab555df40b0ce718a205bfe34b8db0581d0192fa58dc5778d8` |
| `packages/harness/bootstrap/requirements.md` | 1-19 | `ab68478fe5e106bfbc1a5d8fb1a701d8d9f1856e8fb7022d85704bf0da638c66` |
| `packages/harness/rules/global.md` | 1-25 | `9d54f65df575f74aa0137341086d6e1a89f4e02a1f327c269079d14573cb7c46` |
| `packages/harness/rules/collaboration.md` | 1-13 | `96905bb872961d07599bb42c8fc90ea506f2041b5d5ff6077ff76fcd8674f91b` |
| `packages/harness/rules/delegation.md` | 1-45 | `8a70b666b2fbcb4cfdbe042f5fd52cb7334ace01cae165878f26ea7057baf20e` |
| `packages/harness/rules/code-quality.md` | 1-8 | `7f6b0e5d05f8a79778dda950844ce3f0bf0aeccd3d9c0666eb307f1c9b3cae89` |
| `packages/harness/skills/spec-development-execution/SKILL.md` | 1-61 | `91c74ffb3c020db1468d2abe19eaa281a8278b3deef72577433099293e821147` |
| `packages/harness/skills/spec-verification-convergence/SKILL.md` | 1-54 | `b6458519f2f62d44499644186b9ba5366042e9008ef641aae6535f23a1f2fad9` |
| `packages/harness/skills/spec-process-improvement/SKILL.md` | 1-48 | `b9d3fc13208c4090a1cc3d436ae9bfd9710374d9f37f62e157939f433e8db123` |
| `packages/harness/skills/spec-debug/SKILL.md` | 1-52 | `e17f520ad266409c3089ead00473f6157e25d3a6db565f396711fd0455f94f97` |
| `packages/harness/skills/spec-harness-adoption/SKILL.md` | 1-54 | `5db3edf416e284ac1b2f62248a61ec327091d3478ed7b4e6c99883543767c664` |
| `packages/harness/skills/spec-harness-adoption/references/candidate-validation.md` | 1-9 | `2084d8ca66cea4b3ce9c87bfa85fa484ca98d8eb8003e1a235bcd776fc0b0114` |
| `packages/harness/skills/spec-project-onboarding/SKILL.md` | 1-44 | `3abbd8c7b6dc765111a9d9c58b055db6d5b131d86a5ac1696ff77267dc4713ab` |
| `packages/harness/skills/spec-requirement-clarification/SKILL.md` | 1-42 | `3bed21544cc133281660e51d483b6d9406b6d233484169d6cdb85c71f71c09c8` |
| `packages/harness/skills/spec-technical-design/SKILL.md` | 1-46 | `8d61c6eb2d5a4b61ee789cb67145fe2c67023d3b78b8af334147adbe647dbec7` |
| `packages/harness/skills/spec-implementation-planning/SKILL.md` | 1-62 | `5ee2af5c3389679fec96b0405c27f0733750b29a224a8f6abe88ee258fd1916f` |

### 收尾复核

写报告时再次运行包校验，退出码 0，结果与首次一致：

```json
{"version": "0.12.0", "source_revision": "2f585f0faa8c0ba831161858a2e1418fd2d527e7", "files": 23, "package_sha256": "df12bb60ef594c9fb2a324b91b92fe10f4919b1413609f5154fc296cdd6405d1", "integrity": "PASS"}
```

已检查所读 Canonical 工作区文件与固定 revision 无差异；语义判定始终使用 Git 固定正文。包校验的 PASS 仅表示完整性通过，本次语义审查仍为 BLOCKED。
