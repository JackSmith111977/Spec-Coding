# 首次 FULL 候选发行：独立验证设计与覆盖

本文件是验证设计，不是验证结果。尚未读取或冻结构建 agent 的候选包，未执行包验证、行为测试、安装、构建或发布，未授予任何候选通过结论。设计依据为本轮直接分批阅读的 `docs/manifest.yaml` 所登记的全部 44 篇正文，以及 `docs/governance/harness-build-and-release.md`。输出截断批次已重新读取。

清单版本为 `0.12.0`、状态为 `candidate`：34 篇 Main Workflow、4 篇 Exception Workflow、4 篇 Rule、2 篇 Meta Protocol。8 阶段指 01a、01b、02、03、04、05、06、07；01a 与 01b 是不同入口，不能要求同一项目顺序经过两者。Manifest、治理、导航与参考不计入 44 篇正文。下文的核验要求用于审查，不替代 Canonical，也不成为包的长期中间表示。

## 执行者与信息隔离

- 独立语义 Reviewer：直接读取固定源版本的完整 Canonical、对应 Manifest、治理文档和冻结候选。不能用本覆盖表、Builder 摘要、构建回查结论替代原文。
- 行为 Test Agent：新会话，仅得到固定候选、当前单个场景用户请求、物化后的原始 fixture、该轮授权与真实工具。不得访问本文件、`expectations.md`、Canonical、Builder 工作目录或其他场景会话。
- 执行协调者：在冻结候选外物化 fixture、控制分支和故障、保存工具日志及逐步快照；不得将隐藏检查点或正确路由提示写入用户请求。`scenarios.json` 的 `user_request`、fixture 正文和当前轮 `message` 可见；未来轮次不能提前给 agent。
- 隐藏判定者：使用 `expectations.md` 对照真实记录，区分规范偏差、环境不可执行、验证方法缺陷和 fixture 前提不足。隐藏文件需要通过独立文件系统/会话权限隔离；仅分文件不构成隔离。
- 本轮只写 `verification/harness/oracle/`。未来执行者另行在被授权测试根目录建立副本；这些设计不授权修改当前仓库包、全局配置或真实项目。

## 全源审查表

所有路径相对仓库根。每行均须在将来记录：源版本与段落 → 候选实际资产及段落 → 入口/共享依赖可达路径 → 观察到的保真或偏差证据。不得仅凭 `sources` 列出路径认为已覆盖。共享行为可集中承载，但每个适用消费者必须在相关动作前获得它；再反向检查每个生成资产，避免隐藏的新增规范。

| 编号 | Canonical 源 | 独立语义审查要点 | 行为组合 |
|---|---|---|---|
| C01 | `docs/workflows/main/01a-project-definition/01-project-positioning.md` | 从问题、用户、情境、价值建立方向；区分确认/假设；不以功能或技术栈替代定位；启发式不是必答问卷。 | S01 |
| C02 | `docs/workflows/main/01a-project-definition/02-business-definition.md` | 范围、参与者、对象关系、业务场景与规则闭环；不提前设计表/API；不强制简单对象状态图。 | S01 |
| C03 | `docs/workflows/main/01a-project-definition/03-system-definition.md` | 业务能力有系统责任方、数据归属与端到端链；区分约束和设计假设；技术细节留给设计。 | S01 |
| C04 | `docs/workflows/main/01a-project-definition/04-requirement-framework.md` | 稳定唯一 REQ 身份、价值来源、需求关系及最小核心链；不提前冻结详细 AC 或版本范围。 | S01 |
| C05 | `docs/workflows/main/01b-project-understanding/01-project-orientation.md` | 广而浅地图、职责和可核验锚点；文档可能过时，要与结构/配置/入口交叉验证；不复制目录树。 | S02-A |
| C06 | `docs/workflows/main/01b-project-understanding/02-business-understanding.md` | As-Is 与 To-Be 分离；代码只是业务证据之一；只对重要模型变化同步；文本语义与按需图表一致。 | S02-A |
| C07 | `docs/workflows/main/01b-project-understanding/03-system-understanding.md` | 沿业务定位组件、关键 symbol、数据写入方与共享消费者；关键时序/约束有代码或运行证据；不重建全系统。 | S02-A |
| C08 | `docs/workflows/main/01b-project-understanding/04-requirement-positioning.md` | 变化点、业务/系统位置、四类 Gap；Direct/Adjacent 区分；关联影响不自动入范围；不自行解决语义冲突。 | S02-A |
| C09 | `docs/workflows/main/02-requirement-clarification/01-requirement-interpretation.md` | 只消费对应入口；01a 继承 REQ，01b 一次分配；Input Context 是消费视图；Known/Inference/Unknown 不混淆。 | S01、S02-A |
| C10 | `docs/workflows/main/02-requirement-clarification/02-ambiguity-gap-identification.md` | 先查证再问最小关键问题；过滤低价值未知；跨阶段复用同一 OI；deferred 有理由和承接点。 | S02-A/B |
| C11 | `docs/workflows/main/02-requirement-clarification/03-scope-rule-confirmation.md` | 已确认事实可自主整理；新增业务语义/范围/核心规则需 Human Decision；blocking 未解决不得默认补全。 | S01、S02-A |
| C12 | `docs/workflows/main/02-requirement-clarification/04-acceptance-criteria-confirmation.md` | AC 可实际验证、单一主 REQ 归属；缺 REQ 回解读；新正确性需决策，机械转写不重复确认；新歧义回澄清。 | S01、S02-A |
| C13 | `docs/workflows/main/03-technical-design/01-current-state-impact-analysis.md` | 从 AC/行为定位真实入口和链路；Confirmed/Conditional/Unaffected/Open 区分；技术证据缺口与需求缺口分别回流。 | S01、S02-A |
| C14 | `docs/workflows/main/03-technical-design/02-solution-design-decision.md` | 有真实选择才列多方案；关键前提实验；局部可逆自主，高影响架构/迁移 Confirm，改 AC/风险 Human Decision。 | S01、S02-A |
| C15 | `docs/workflows/main/03-technical-design/03-detailed-technical-design.md` | 结构/链路/契约/异常边界足以实施而不变逐文件脚本；OI 引用；方案不成立回决策，语义问题回更早源。 | S01、S02-A/B |
| C16 | `docs/workflows/main/03-technical-design/04-design-acceptance-convergence.md` | AC 覆盖、一致性、关键假设证据；Ready/Not Ready；Risk 与 OI 分开，blocking 不得带入实施。 | S01、S02-B |
| C17 | `docs/workflows/main/04-implementation-planning/01-implementation-baseline-handoff.md` | 只接管最终 Ready 结论、保持引用和 OI；不是新事实源，不静默重设计；上游无效则回流。 | S01、S02-B |
| C18 | `docs/workflows/main/04-implementation-planning/02-implementation-task-decomposition.md` | 独立实施与验证闭环、一个主 REQ；Coverage 按风险；不按目录分层机械拆任务；此步不固定依赖/工具/调度。 | S01、S02-A |
| C19 | `docs/workflows/main/04-implementation-planning/03-task-definition-and-orchestration.md` | tasks.md 权威定义与状态；初始 Draft；Coverage/Verification/Done 对齐；真实依赖；不持久化模型/Wave/第二委派合同。 | S01、S02-B、S03 |
| C20 | `docs/workflows/main/04-implementation-planning/04-task-set-validation.md` | 只读发现覆盖/循环/主归属/契约缺口，回所属步骤修正；通过才 Draft→Ready；Ready 不等于 Runnable。 | S01、S02-B |
| C21 | `docs/workflows/main/05-development-execution/01-ready-task-scheduling.md` | Ready+依赖+无 blocker+能力有效才调度；单写者与串并行隔离；失败先分 Attempt；不新增持久 Runnable 状态。 | S01、S03、S06-A |
| C22 | `docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md` | 契约内自治与局部自修；局部验证→Task Commit→Verifying；commit 失败保持 In Progress；不能由 Worker 宣告 Done。 | S01、S03 |
| C23 | `docs/workflows/main/05-development-execution/03-verification-and-exception-convergence.md` | 正式 gate 绑定实际 code_ref，重跑确定性验证；Reviewer 不能替代；可靠实现缺陷返原 Worker，归因不明进 Debug。 | S03、S04-A |
| C24 | `docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md` | 状态写回、依赖只影响 Runnable；全部主归属 Task Done→集成→REQ AC gate→push；push 失败保留有效 Task；不等于 Verified/发布。 | S01、S03 |
| C25 | `docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md` | 绑定完整变更/code_ref，复用有效证据并补跨任务/回归/风险缺口；确定性、独立、人验边界；OI 不复制。 | S01、S05 |
| C26 | `docs/workflows/main/06-verification-convergence/02-multi-dimensional-verification-execution.md` | 对业务对象只读；可修测试环境但不得降低标准；Pass/Fail/Unverified 有真实证据；模型能力故障不能伪装业务 Finding。 | S05-A/B、S06-A |
| C27 | `docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md` | 分类/权限/最早失效源/重验链；Accepted 永远 Human Decision 且不是 Pass；Unresolved 可进 Debug；Finding/OI/Risk 正交。 | S04、S05-A/B |
| C28 | `docs/workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md` | Required/Gates/Trace 齐备才 Verified，否则 Blocked；Invalid Finding 仍需 Resolved；只汇总证据不修复/发布/另加审批。 | S01、S05-A/B |
| C29 | `docs/workflows/main/07-process-review-improvement/01-evidence-collection.md` | EV 的 source/顺序/subject/actor/related 可追溯；只记录关键事实，无提前根因；不发明独立 Spec 产物。 | S08-A/B |
| C30 | `docs/workflows/main/07-process-review-improvement/02-process-reconstruction.md` | reconstruction.md 由 EV 重建真实变化链，保留返工和纠正；不只记最终状态，不提前评价变化合理性。 | S08-A/B |
| C31 | `docs/workflows/main/07-process-review-improvement/03-issue-detection.md` | 有影响、有复盘价值才 ISS；分类暂定、排除正常演进噪声；issues.md 引用 EV，不提前根因。 | S08-A/B |
| C32 | `docs/workflows/main/07-process-review-improvement/04-root-cause-analysis.md` | 从表象追到发现/闭环/传递/执行/验证/工具机制；区分发生与逃逸，找最早拦截点；不足降低置信度。 | S08-A/B |
| C33 | `docs/workflows/main/07-process-review-improvement/05-improvement-design.md` | 可 No Process Change；改进目标是可复用机制；少量最小改变、先定验证；机制变化 Confirm，弱化 gate/扩权 Human Decision。 | S08-A/B |
| C34 | `docs/workflows/main/07-process-review-improvement/06-implementation-and-validation.md` | 授权后真正修改机制；IMP→RC→ISS→EV；下一轮真实开发验证 Effect/Cost；未运行不得填写有效，后续变更再判权限。 | S08-A/B |
| C35 | `docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md` | 修改前保护现场；复现/可靠观察均可进入；Not Reproduced 非无效；低风险不强加事故流程；不提前猜根因。 | S04-A/B |
| C36 | `docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md` | Expected/Observed Trace 首个偏离、区分性证据和可证伪实验；最近改动非因果；复用基线不全仓扫描。 | S04-A/B |
| C37 | `docs/workflows/exceptions/debug-and-defect-resolution/03-root-cause-confirmation-and-correction-routing.md` | 症状/促因/根因候选分离；Confirmed/Probable/Unconfirmed 有证据门槛；修好不独证根因；错误上游不得下游补丁遮掩。 | S04-A/B |
| C38 | `docs/workflows/exceptions/debug-and-defect-resolution/04-fix-verification-and-failure-convergence.md` | 按原复现状态重验原故障+受影响/known-good；Resolved/Blocked 仅故障结论，回 Owner 才更改 Task/Finding/OI。 | S04-A/B |
| C39 | `docs/rules/global-contracts.md` | 四档裁剪保留 Trace/Gate/Authority/OI/code_ref；严格局部规则优先；不把 workflow Task/Git 合同机械施加到 meta。 | 全部，重点 S01–S05 |
| C40 | `docs/rules/human-agent-collaboration.md` | 自主取证、真实触发才协作；Decision Readiness 与反馈回事实源；既有授权不重复；Main 为人机入口。 | S01、S02、S05、S08 |
| C41 | `docs/rules/agent-delegation-and-coordination.md` | 五角色、Main 责任、候选先验证；单写者、独立上下文、递归需明确授权；能力/边界/权限故障分开；最低充分动态路由。 | S03、S06 |
| C42 | `docs/rules/code-quality.md` | 可理解性/信息质量/聚焦差异/项目一致性；不机械规定语言/框架/注释量；不因局部改动做无关清理。 | S01、S03、S05 |
| C43 | `docs/meta-protocols/project-onboarding.md` | 先发现；Initialize/Reuse/Refresh/Migrate；仅持久意图/绑定/约束；运行事实外置；版本差非必迁移；01a/01b/Resume 正确。 | S01、S02、S06、S07 |
| C44 | `docs/meta-protocols/harness-adoption-and-adaptation.md` | 未安装 bootstrap、同版依赖、完整行为要求与验收；受控候选授权在包外；实际加载/语义回查/只验受影响；旧绑定不默认升级、损坏回维护者、回滚保护用户。 | S01、S06、S07 |

## 治理附加检查 G01–G08（不计入 44 源）

| 检查 | 执行设计与必要证据 |
|---|---|
| G01 首次 FULL 范围 | 核对无可信前发行时采用 FULL；完整 44 源及 Rule 当前适用关系均有承载。Manifest 不混入 artifacts.sources。不能用 HEAD~1 冒充发行基线。 |
| G02 内容身份与结构 | 确定性核查实际格式、路径、引用、assets/references、目录文件清单与 hash 范围、重复/悬空/旧版残留；包内 bootstrap 安装前可读取；全量检查包 envelope。 |
| G03 来源与派生 | source_revision 可解析并与源码快照、Manifest 绑定；sources 为确切实际直接依赖正文，不是目录/摘要；引用的哈希与内容一致。无法由最终包独立证明 Builder 确实读过原文，须另查直接读取记录，不能猜测。 |
| G04 双向语义审查 | 44 源→所有适用承载，再所有生成资产→原文；检查硬语义、程序、有效 Guidance、无新增规范和共享规则组合。不是比较长度或仅搜索 MUST。 |
| G05 受控候选隔离 | 固定身份、来源、测试范围、副作用、停止条件明确写在候选外。Test Agent 只有包+场景；不得伪造发布依据或读取 Canonical 补洞。 |
| G06 修改使证据失效 | 将来在独立副本分别改变资产、Build Manifest、Envelope，记录前后身份；旧 Stage 3 记录不能复用到新候选。此为故障注入，不得改正本。本轮未创建这些副本。 |
| G07 失败回流 | Canonical 语义错误→源；范围遗漏→Stage 1；表达缺陷→Stage 2 Transform；装配缺陷→Stage 2 Assembly；方法失效→Stage 3。Reviewer 只阻断/归因，不能自行热修后宣布通过。 |
| G08 发布边界 | 将来核对 VERSION/Manifest/Build Manifest/发布身份/验证记录一致，Stage 4 原样发布；受控 READY 不代表发布资格。本轮不执行合并、tag、release。后续变化重新进入构建链，旧版仅通过 Git/Release 管理。 |

## 预期最小测试矩阵

以下是计划数量，不是已执行次数。每个分支使用独立初始副本；同一分支中的多轮用于观察失败及恢复，不能只执行恢复后半段。

| 组合 | 必选分支 | 数量 | 必须实际产生的证据 |
|---|---|---:|---|
| S01 新项目完整链 | A：未安装→接入→01a→02→03→04→05→06 | 1 | Runtime 真实加载、产物写盘、代码/测试、commit、独立 gate、本地 bare remote push、最终 trace |
| S02 存量与规划边界 | A：01b+歧义+高影响提案；B：Not Ready/循环依赖/缺 Coverage | 2 | 读真实源码和测试、OI 与反馈写回、设计提案；只读核查差异与回流记录 |
| S03 恢复调度与 Git | A：阻塞依赖、无依据 Worker 声明、commit 失败恢复、push 失败恢复 | 1 | 状态快照、被拒绝及成功命令、确切 code_ref 独立验证、远程 ref |
| S04 Debug | A：稳定复现/对照/修复/回交；B：历史观察可用、当前未复现 | 2 | 原故障和 known-good 运行、原始现场与反证、Failure/Owner 分离 |
| S05 最终验证 | A：业务缺陷+接受偏差边界；B：错误验证资产 | 2 | 只读对象前后 hash、执行退出码、Finding 分类/状态、人类决策及门禁区分 |
| S06 Runtime 与转换 | A：加载未生效/执行中能力变化；B：本地转换丢语义；C：用户改动与失败回退 | 3 | 新会话加载与能力探测、原包↔本地语义回查、配置快照/回退、证据失效 |
| S07 包消费生命周期 | A：旧基线复用；B：无候选授权；C：损坏/缺引用；D：完整但语义缺失 | 4 | 绑定/包/文件 hashes、读取轨迹、写入范围、缺陷归因；不能靠对话模拟包损坏 |
| S08 流程复盘 | A：机制改进并下一轮开发验证；B：正常演进无机制修改 | 2 | 原始日志、EV→ISS→RC→IMP、授权后机制 diff、下一轮真实测试与成本记录 |
| 小计 | 一种真实可隔离 Runtime 的全部组合 | 17 | 任一未执行分支保留待执行/限制，不得推断 |
| 可移植退化补充 | 在确实无原生 subagent/hook、但具基础读写/命令及独立会话的环境重跑 S01-A、S06-A | 2 | 等价机制成立或如实阻断；不可把 rich Runtime 的配置标签改名充数 |
| 最小行为计划 | 17+2；全源语义和 G01–G08 另行全量执行 | 19 | 不要求穷举所有模型/Runtime；第二环境不可提供则仍为覆盖缺口 |

S07-A 使用双重标注的合成旧发行 fixture，只证明旧绑定选择/不自动升级，不提供真实历史发行认证。S06-B/S07-C/D 是故障对照副本；其行为不能与正本候选混算。S08 修改的是测试项目自有的可复用工具，不是被冻结的 Harness Package。

## 不可用问答替代的证据与限制

必须实际执行：包 inventory/hash/引用校验；bootstrap 到真实加载面；新会话行为；fixture 读写；业务测试和失败重跑；Git commit/push 及失败；只读验证前后内容对照；独立上下文边界；Runtime 能力变化探测；本地转换与原包回查；用户资产保护与恢复；下一轮开发中的机制效果。答出“应该阻断”“会运行测试”只算表述，不能证明行为。

可以通过结构化审查证明：Guidance 是否可达、状态责任及 Authority 是否保真、没有新 Gate、源到全部消费者的映射；但结构和口述仍不能证明真实加载或门禁实际工作。运行能力不足、身份占位未绑定、原始记录不足均由执行协调者报告验证限制，不能让 agent 编造证据。

源快照附录只记录设计读源的内容身份，不是候选 Build Manifest，不证明发行源版本与当前工作树完全相同。若构建期间 Canonical/Manifest 变化，后续 Reviewer 必须对固定候选绑定的源版本重读受影响原文并更新设计适用性。


## 设计读源后的身份快照

记录时仓库 HEAD：`2f585f0faa8c0ba831161858a2e1418fd2d527e7`。以下为设计读源完成后的工作树字节 SHA-256；不是对候选 source_revision 的认证。

| 源文件 | SHA-256 |
|---|---|
| `docs/manifest.yaml` | `caafbb32d1862c5140ab9d4fb64eef646482ce1da99fca5c2781326f9fac5cec` |
| `docs/governance/harness-build-and-release.md` | `601264626a23a0297a5bf205ee6d74af4fa0eb2577eb666ec59733a3776f6da7` |
| `docs/workflows/main/01a-project-definition/01-project-positioning.md` | `f8228a9a5ff6d87037939cadd1d3a3a9822afca7d8195d3b8472c57fdbdb6d03` |
| `docs/workflows/main/01a-project-definition/02-business-definition.md` | `63360d74251e0a1bedaa6525f878f07f602c05e08df6470eddd4388f16c75683` |
| `docs/workflows/main/01a-project-definition/03-system-definition.md` | `34f991239312da9234f842e56c6e80120f9d58d1f83641beca415c8f08813bd1` |
| `docs/workflows/main/01a-project-definition/04-requirement-framework.md` | `1b0ec6767cc983a428d5f98bd24ed24a546ad43a25a03454601e21b72ab3756d` |
| `docs/workflows/main/01b-project-understanding/01-project-orientation.md` | `59e4050ad7b21f3392a93d368a6e140fac8ed56c4fc08e5719c6ad8b00b9e320` |
| `docs/workflows/main/01b-project-understanding/02-business-understanding.md` | `43f175279c4143ef88778c3f44690376b015ccb3470c4b39a0bb6f3df41d48a6` |
| `docs/workflows/main/01b-project-understanding/03-system-understanding.md` | `7d33b7de59cda0fceeecf74fa1f26fc742f04ec9b344f8abc071715f3e80d7ce` |
| `docs/workflows/main/01b-project-understanding/04-requirement-positioning.md` | `356fa6b0aea910a9fd916cd12da8765704e51e0945dc7bf9df5739fa750b10c5` |
| `docs/workflows/main/02-requirement-clarification/01-requirement-interpretation.md` | `013b08ae82497af9e527475cbc9ac4035aad035c6d82c38543841e3cef103928` |
| `docs/workflows/main/02-requirement-clarification/02-ambiguity-gap-identification.md` | `fd9aaeea2681e9cb06959b791a4b936224983765a517b0c52476b0b36d95a8bf` |
| `docs/workflows/main/02-requirement-clarification/03-scope-rule-confirmation.md` | `003eb42d912420f5b43ec354947fef42fdae39484fc262a37ea01091ed949e60` |
| `docs/workflows/main/02-requirement-clarification/04-acceptance-criteria-confirmation.md` | `5a025b39753d465ea37cfd61a5b33c02b9a8508763c6606822b76f84f8a24fa9` |
| `docs/workflows/main/03-technical-design/01-current-state-impact-analysis.md` | `5699a8658124a743e6753404c22276affe9f40d27d32be7990308e8a5d393271` |
| `docs/workflows/main/03-technical-design/02-solution-design-decision.md` | `294628df1d818478653ea39e8ced2cf07ee4fef06847a429447b64b3d36499a8` |
| `docs/workflows/main/03-technical-design/03-detailed-technical-design.md` | `061b34a181575df92db76103910c0dd96082d0ee72b13352c98a053b6100ae84` |
| `docs/workflows/main/03-technical-design/04-design-acceptance-convergence.md` | `f5fb9a9b8cca8925366e46d009a72919dc8158dd8ea111a463a9af178e303fd9` |
| `docs/workflows/main/04-implementation-planning/01-implementation-baseline-handoff.md` | `c5fa9b2b847b7b8f749444414dc37911e2dc07bc37dec7d236ca36b8ecf2c090` |
| `docs/workflows/main/04-implementation-planning/02-implementation-task-decomposition.md` | `0ba955af09361e4b174ef70da48d84754247d1939d353a351dac35accbc61bd1` |
| `docs/workflows/main/04-implementation-planning/03-task-definition-and-orchestration.md` | `2d6f6b5e9ee1222b3a1a113d44b0ccda100746ce35076697adacb81b5ec09115` |
| `docs/workflows/main/04-implementation-planning/04-task-set-validation.md` | `b414dea09dd4c6ef35fd2fa7cc58489ad9af6d7fa6c3afb1646417b5f2e7ad8d` |
| `docs/workflows/main/05-development-execution/01-ready-task-scheduling.md` | `efe74845a90bea42afd97b18626c308f8de4d16dd453847f45b6697cc3b223e7` |
| `docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md` | `9e033cad5750f4712c569aa116c55e4e94d40b76cf7558af56d0a1d7d23fb497` |
| `docs/workflows/main/05-development-execution/03-verification-and-exception-convergence.md` | `1042e4c538a62fb2e7878f688c551dce6bb7b2329eb92f7a945e8e72126bd405` |
| `docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md` | `1801774a835315b8ae832018745ae26bc24543fb2f883d9e313710310ff36f06` |
| `docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md` | `2d19dd6fd9082cc263786353499563364529e60fe8bce3233d8acf41b28eb6a0` |
| `docs/workflows/main/06-verification-convergence/02-multi-dimensional-verification-execution.md` | `7424a1a322894b70bf027a0c7081287f6490f5a01c54d481ab0f6f2c8b40d2e2` |
| `docs/workflows/main/06-verification-convergence/03-verification-finding-triage-and-deviation-convergence.md` | `05588904f65dac503a6d349ede9932342d229199cf091197d1dc3c424da34ec6` |
| `docs/workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md` | `4a2a3c7bcfbac6773b8c034f84ecc4051b31c1e2540dc2ec7f0864a1bf3a4389` |
| `docs/workflows/main/07-process-review-improvement/01-evidence-collection.md` | `054652f9375465c65f0a7670ed9f0d7e1a42562dcaba99c34001e34ca9e7c6e2` |
| `docs/workflows/main/07-process-review-improvement/02-process-reconstruction.md` | `75acc08672dbaed7193bc285e51f4fb9951ff51139f0a44175589a04002ee8aa` |
| `docs/workflows/main/07-process-review-improvement/03-issue-detection.md` | `172c3ca2ab3d30ce0537ef55c95fd4ed789487315b9a54b98449097c18ce4d30` |
| `docs/workflows/main/07-process-review-improvement/04-root-cause-analysis.md` | `9aeeab12c107ce40e98a1aff0b4daeb9b1009ae50cd9ad101e524da91b1b3694` |
| `docs/workflows/main/07-process-review-improvement/05-improvement-design.md` | `3b71f3cdcf3a642ade8c3f5401baa0527ddfa68b9aad1a1c56973feb6cb7ff13` |
| `docs/workflows/main/07-process-review-improvement/06-implementation-and-validation.md` | `92249724e65fdbbb0cafd8d6f3640026f83a5bcf43ac5e913fc55e5f009927fe` |
| `docs/workflows/exceptions/debug-and-defect-resolution/01-failure-intake-and-reproduction.md` | `75e22616e4f01147e1907355eeeaca011f980421fe0dc29877356b3cf7461a00` |
| `docs/workflows/exceptions/debug-and-defect-resolution/02-evidence-collection-and-fault-localization.md` | `37f0d18993589b6ff5a81ce948b458e946edbf5b2d39996fe0b79c7e1b935d20` |
| `docs/workflows/exceptions/debug-and-defect-resolution/03-root-cause-confirmation-and-correction-routing.md` | `266f9a6103fd86a21e954a88facc4b724a2cd0a1358dbe76b6ed286c0fd24c2b` |
| `docs/workflows/exceptions/debug-and-defect-resolution/04-fix-verification-and-failure-convergence.md` | `232c94aac6c15d34946f0cc3dd4faf761b6b79c2bde4371597324be8b83f2bd9` |
| `docs/rules/global-contracts.md` | `aae6dc15f2359a0d2fba8095efd08d88221c99511930301758cb4a07924954ee` |
| `docs/rules/human-agent-collaboration.md` | `c1a0a81dc5992f912dc20c0fd4d0ad155f4b92df6678543a11f53b9676b6b96f` |
| `docs/rules/agent-delegation-and-coordination.md` | `d643210545d0b1275d439f9b17292c01c745263e594c8028cae0317af760f596` |
| `docs/rules/code-quality.md` | `58965492f8767ff6ecadb66934f3625fdf55929bfe7cd403911aaaa15363d1cd` |
| `docs/meta-protocols/project-onboarding.md` | `42647895ac599a39dc8e0a9f6e0c040d6d0535919a9b55f9385e3f72ebc34906` |
| `docs/meta-protocols/harness-adoption-and-adaptation.md` | `dd6cfbc4c05ccacbc1ee3898bf49a70ee72c0b086eca2b7b211a0eb174158d5b` |
