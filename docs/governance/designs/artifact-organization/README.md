# 0.13.0 产物组织与渐进读取设计

本设计为维护者版本方案，其规则与协议已在 **0.13.0** 实施并完成本轮必要发行验证。原设计基于仓库提交 `92169e6f1c50cb815972beafbfb4a24d70088926`，实施中的边界澄清以 Manifest 登记的正式规范为准。固定候选与实际验证范围见[构建记录](../../../../verification/artifact-governance/README.md)，本页不证明客户端已经验收。

目标：为目标项目建立统一的产物存储、导航和读取约定，减少 Agent 的无关读取与状态误判，并使 Human 能从短入口进入正文和证据。

阅读导航：本页定义完整方案与实施边界；[验收方案](acceptance.md)定义可观察挑战与通过条件。正式事实源仍以 [Manifest](../../../manifest.yaml) 登记的现有规范为准。本设计不作为预编译输入，不要求目标 Agent 消费它；实施后由正式规则与协议承担行为。

## 1. 分类与责任

新增正式规则为 `docs/rules/artifact-organization-and-reading.md`，中文名“产物组织与读取规则”。这是跨阶段持续成立的组织、可发现性、读取与维护约束，不创建新的阶段或业务状态机。

| 层次 | 职责 |
|---|---|
| 新增 Rule | 产物放置原则、默认布局、入口契约、按需读取、索引一致性、拆分与维护约束 |
| Project Onboarding | 发现已有产物，确定 Spec Workspace 与共享边界，建立或迁移稳定目录映射 |
| Harness Adoption & Adaptation | 绑定真实加载入口，管理发行包与本地适配记录，验收读取行为及恢复能力 |
| 各 Workflow | 继续定义产物语义、必需字段、状态、Gate、追溯及关闭条件 |
| 仓库 Governance | 新规则登记、构建范围、预编译验证、版本与发布 |

规则适用于创建、读取、修改和维护正式产物的 Main / Exception Workflow，以及两个 Meta Protocol 的相关动作。不能仅依靠 Workflow 全局继承而漏掉安装前的接入动作。

## 2. 现状与必须保持的契约

| 已有来源 | 当前契约 | 本设计的处理 |
|---|---|---|
| [项目接入 §3.2–3.4](../../../meta-protocols/project-onboarding.md) | Spec Workspace 可与代码仓库分离；Local / Shared / Repository-native；Baseline 只存稳定意图与绑定 | 目录默认值不能扩大共享范围；在原 Baseline 中绑定布局，不创建第二份基线 |
| [Harness 接入 §2.1、§5–7](../../../meta-protocols/harness-adoption-and-adaptation.md) | 包内渐进读取、原包不变、记录固定适配候选、真实验收、相关变化重验 | 增加目标产物入口，保留来源与候选分离及失效判断 |
| [任务规划 §3.3、§3.7](../../../workflows/main/04-implementation-planning/03-task-definition-and-orchestration.md) | tasks.md 保存完整任务集及权威状态；复杂任务可下钻 | 不按需求拆成独立任务集，不把 tasks.md 降格为纯索引 |
| [开发写回 §4.2–4.7](../../../workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md) | Task 状态、code_ref、底层集成/AC/Push 事实；Requirement Sync 只是聚合视图 | 索引不得新建第四个同步状态；运行时 Runnable 不作为长期 Task 状态 |
| [全局执行契约](../../../rules/global-contracts.md) | 同一 OI ID 跨阶段复用；Task 完成不等于 OI 关闭 | 不强制迁移所有 OI 到新总表，不复制开放项权威记录 |
| [验证关闭](../../../workflows/main/06-verification-convergence/04-evidence-closure-and-status-convergence.md) | Verified / Blocked 由 Gate 与完整证据决定 | 目录归档、索引标记、Task Done 都不能替代 Verified |
| [委派协调](../../../rules/agent-delegation-and-coordination.md) | 完整产物、最小上下文、单写入者边界 | 分层读取与写入串行化复用现有规则，不固化 Worker/模型策略 |
| [复盘证据](../../../workflows/main/07-process-review-improvement/01-evidence-collection.md) | 关键事件才成为 EV；不保存所有工具调用 | 原始证据与 EV 记录分开；不要求为每个日志新增 EV |

本版本不新增业务需求、任务、Finding、Failure 或接入验收状态，不改变权限和 Git 门禁。统一组织不等于所有产物必须保存为独立 Markdown 文件。

## 3. 目录与绑定

### 3.1 根目录解析

1. 优先读取当前 Agent 已授权的入口与既有 Adoption Binding；再定向发现已绑定的 Spec Workspace，不能因为没看到 `spec/` 就新建一套。
2. 已有有效空间优先复用。新建 Repository-native 空间默认使用项目根 `spec/`；Local / Shared 使用符合既有意图的独立空间。不因默认目录推定用户同意共享。
3. 目标已有同名目录、外部文档系统或团队约定时，先判定所有权与语义等价性；满足契约则映射复用，否则在授权边界内补入口或迁移。
4. 在原 Adoption Baseline 中记录空间根、Target Scope 及必要角色到位置的映射；采用默认布局时不重复登记每个文件。映射只保存长期位置与边界，不保存 Runtime 清单、当前任务或适配 READY 状态。
5. 当前 Runtime 的真实入口保存最短可用定位信息，并链接工作空间总入口；初次建立空间时从包内规则启动，不能依赖尚不存在的工作空间索引。

Monorepo 按稳定管理范围绑定空间，不能默认每个子目录各建一套。多仓空间引用代码时带 Repository Identity 与 code_ref；不同空间的同名 REQ / Task 通过空间身份消歧。一个统一任务集覆盖一个明确的管理范围；拆分空间不能切断既有依赖，跨空间依赖使用限定引用。

### 3.2 默认布局

```text
<Spec Workspace>/
├── README.md                     # 总入口：范围、分类、当前工作链接
├── adoption.md                   # 原有稳定接入基线
├── harness/
│   ├── README.md                 # 原包及按范围生效的适配入口
│   └── adaptations/
│       └── <适配标识>/
│           ├── README.md         # 身份、映射、验收结果与失效条件
│           └── evidence/         # 此适配的验证证据
├── project/
│   ├── README.md                 # 长期项目上下文入口
│   └── …                         # 定位、业务、系统、需求框架或已有文档引用
├── requirements/
│   ├── README.md                 # REQ 导航
│   └── REQ-01/
│       ├── README.md             # 对象摘要及正文导航
│       ├── requirement.md        # 需求、范围、规则、AC
│       ├── design.md             # 影响、决策、详细设计与设计验收
│       ├── implementation.md     # 按需保存的集成、AC Gate、Push 事实
│       └── verification.md       # 验证基线、发现及最终关闭
├── tasks.md                      # 完整任务集及权威核心字段
├── tasks/                        # 按需扩展 T07.md 等
├── shared/                       # 真正跨需求的设计、约束或验证正文
├── failures/                     # 故障基线、定位、根因及关闭
├── reviews/                      # 流程复盘与改进记录
├── evidence/                     # 业务执行证据及外部证据入口
└── scratch/                      # 临时探索内容
```

树表示可用角色，不要求接入时生成所有目录和空文件。最小接入建立可用总入口、基线及实际需要的 Harness 记录，不创建虚构 REQ 或空任务集。单个简单需求可以先在其对象入口中承载正式章节，增长后拆出正文；必须标明哪些章节是权威记录、哪些只是摘要。

目录与文件名使用稳定身份，描述性标题写入正文；复用现有 REQ / Task / Failure 等身份，不建立另一套统一业务 ID。没有规范 ID 的适配或证据运行目录只使用局部唯一定位符，不赋予业务状态含义。移动目录不改变对象身份。

同一管理范围分配新 ID 前检查已有记录；并发分配由当前写入者协调，发现冲突先消歧再集成，不重编号已有对象。关键跨文件引用使用稳定章节标识，标题润色不能无意破坏引用。仅有外部系统 ID 时保留原身份，并明确与 Workflow 所需身份的关联。

`shared/` 仅在真正共享时创建：跨需求设计有一个正文，所有需求引用它；跨需求验收有一个对应范围的报告，各需求关闭记录引用同一报告。`implementation.md` 不是新增必需 Artifact，仅为已有集成/AC/Push 事实的默认承载位置；已有系统能可靠提供时直接引用。

### 3.3 引用与外部资产

工作空间内优先相对路径与稳定章节锚点；代码引用携带相对于已绑定仓库的路径及必要版本，不把本机绝对路径作为团队通用引用。跨根位置由绑定解析，需 Human 审阅的外部系统记录提供可访问定位方式。

路径只能在已绑定和已授权范围内解析。链接、符号链接或目录联接指向其他范围时重新核对作用域，不能把“在索引中”视为读取或公开授权。验证时考虑大小写差异、中文与空格路径、Windows / POSIX 分隔符及锚点变化。

远程记录访问失败时明确不可核验项；不得将链接存在当成证据存在。无需为导航下载全部附件。若关键依据将过期，应在授权的存储范围内保留可复核版本或更新引用；无法保留时说明缺口对依赖结论的影响。

## 4. 全流程产物落位与状态归属

| 产生位置 | 现有内容 | 默认承载与读取入口 |
|---|---|---|
| Project Onboarding | 声明意图、稳定绑定、硬约束 | adoption.md；总入口引用，动态事实不进入 |
| Harness Adoption | 原包身份、环境证据、候选映射、验收、恢复依据 | harness/；原包可在外部固定缓存，记录定位与完整身份 |
| 01A | Project Positioning、Business Definition、System Definition、Requirement Framework | project/；按需分文件，继承已分配 REQ 身份 |
| 01B | Project Overview、Business Context、System Context、Requirement Context | project/；优先引用已有权威文档，不另造平行 01A 副本 |
| 02 | Requirement Interpretation、Scope / Rule、AC、OI | requirements/REQ-xx/；OI 保留原事实源；Input Context 仍是消费视图 |
| 03 | Impact Baseline、Solution Decision、Detailed Design、Design Acceptance | 需求 design.md 或 shared/ 唯一正文；记录有效设计及已取代关系 |
| 04 | Implementation Baseline、候选任务、Formal / Executable Task Set | 上游基线仍是引用视图；正式任务在 tasks.md，必要详情下钻 |
| 05 | Verification Result、Task 状态、code_ref、集成/AC/Push、Task Graph Update | tasks.md + 任务详情/证据；需求底层同步事实按需在 implementation.md；聚合视图不复制权威状态 |
| 06 | Verification Baseline、Items / Results、Finding Resolution、Closure Record | verification.md；大报告按需拆目录；跨需求结果放 shared/，不复制报告 |
| Exception | Failure Baseline、Fault Localization、Root Cause Resolution、Failure Closure | failures/ 下同一故障记录及引用；Resolved 只关闭故障，不代写 Task/OI/Requirement 状态 |
| 07 | EV、Process Timeline、ISS、RC、IMP、实施与验证结果 | reviews/ 按复盘范围组织，引用原证据；规则改进按实际所有者回流维护者或本地适配 |
| Human 协作 | 意图、决策、偏差接受、关键反馈 | 写回承担该事实的原产物；不建立第二份长期审批总账 |
| 临时委派 / 探索 | 草稿、假设、工具输出、临时执行信息 | scratch/ 或现有临时机制；确认结论回原事实源，重要原始证据晋升后再清理 |

目录不承担生命周期推导：Task Done 不等于 Requirement Verified，Failure Resolved 不等于 OI resolved，失效证据不得因对象被放入“历史”区域而脱离追溯。

项目长期上下文区分现状、目标模型与假设：01A保留目标和定义，01B及As-Is模型依据已验证现状。需求与设计可以描述目标状态。设计通过不代表代码已实现；项目现状更新要依据实际变更和验证，不能提前把拟议方案写成当前系统行为。取代旧正文时保留版本与替代关系，历史验证仍绑定当时的代码/产物身份；普通导航读取当前正文，复核历史结论读取其对应版本。

## 5. 渐进披露契约

### 5.1 入口的最小信息

总入口只提供：管理范围、接入基线位置、Harness 入口、分类用途、当前工作定位以及读取顺序。不复制完整任务表、日志、全局规则或每个对象的状态。多个并行工作以范围链接列出，不强制全项目只有一个“当前任务”。

分类/对象入口提供以下必要信息，可使用普通 Markdown 表格或章节，不引入强制数据库或双份 YAML 索引：

| 信息 | 要求 |
|---|---|
| 身份与范围 | 复用对象 ID；注明适用项目、需求或验证范围 |
| 内容用途 | 一句话说明正文内容与何时读取 |
| 权威位置 | 文件/记录及稳定章节；不得仅靠文件名猜测 |
| 状态与限制 | 如展示则标明为派生摘要并链接原状态；当前有关阻塞、待决策、失效信号可见 |
| 关联入口 | 直接依赖、相关规则、OI、验证与证据定位 |
| 摘要依据 | 显示动态状态时绑定其来源修订或内容指纹；不能只用时间戳证明同步 |

默认优先静态导航与指向原状态的链接，降低摘要漂移成本。无需为每个普通文档计算 Hash；仅当保留跨文件动态摘要并要复用其有效性时，使用可核验的来源修订。不能可靠证明同步的摘要只用于定位。

`tasks.md` 的核心字段和状态仍是权威正文，任务详情不能另存可独立修改的 Status / Primary Requirement。需求入口在轻量模式中承载正式正文时，应标明对应权威章节，不把整份 README 一概视为非权威。

### 5.2 读取路径

1. 读取当前 Runtime 已生效的全局约束及产物入口；按已有稳定绑定定位空间，核对作用域。
2. 沿对象 ID / 当前任务进入相关分类，确认入口指向权威内容；不从目录排序推断最新版。
3. 加载当前动作必需的正式契约、相关状态与共享依赖。已有上下文仅在对象和来源仍有效时复用；不要求每次重新读取完整正文。
4. 调度时从统一任务集解析真实 Depends On、Primary Requirement 及相关 OI；跨需求或传递阻塞继续沿必要依赖定位，不能只读取当前需求目录。
5. 验证、诊断、决策证据不足或结论冲突时，读取相关证据和上游正文；满足当前动作所需的完整约束及证据后停止扩展。
6. 新阶段、异常触发、环境或上游事实变化时扩展受影响上下文。全流程入口始终可达，不因当前未读取而移除。

渐进披露限制的是无关内容进入上下文，不限制必要发现。默认不递归全文扫描全部产物；索引缺失、陈旧、冲突或检索无结果时，先在绑定范围内按 ID / 引用定向搜索，再按问题扩大。无法判定权威来源时只阻断依赖该事实的动作，保留可独立推进的工作。

阻塞、权限、异常触发和证据有效性不能藏在深层日志中：由原产物保存明确信号，相关入口链接或同步摘要提示。索引损坏不代表“没有阻塞”。

### 5.3 Human 审阅

对象入口首先回答：是什么、现在到哪、发生了什么重要变化、有哪些待决定事项、结论与依据在哪里。详细推理过程不进入入口；正式决策依据与尚未解决的不确定性不能被摘要省略。

长文件先按职责和独立消费边界拆分，不设强制行数/Token 阈值。普通任务保持集中，复杂任务遵循原有 tasks/ 下钻条件。分类规模增长时可分页或按稳定主题分索引，但保留完整可检索入口及任务依赖，不以“只显示最近项目”隐藏未完成工作。

## 6. 写回、一致性与并发

写入顺序：核对当前权威内容与所有权 → 写入原产物与必要证据 → 更新直接受影响入口 → 检查引用与摘要依据 → 才报告此次写回完成。验证结论仍由原 Workflow 判定；导航检查不是新的业务审批 Gate。

同一可变产物同一时刻只有一个写入者。Worker 修改分配范围，Main Agent 或当前 Owner 汇总 tasks.md 和共享索引；这属于当前运行安排，不写入永久任务字段。集成其他分支前重新核对事实与依赖，不用简单保留一侧文本解决状态冲突。

多文件更新不假设文件系统事务：入口最后更新；并发环境采用实际可用的隔离/锁/修订冲突检查。动态摘要未完成同步或来源不符时不能供状态判断。中断恢复先核对权威正文与引用，修复受影响导航，再继续依赖动作；无需另建长期事务状态机。

新增、拆分、移动和合并文件都保留对象身份、权威归属、直接依赖和入站引用。只更新有影响的索引，不要求每次写回重建整棵树。当前布局与索引可以由工具生成，但工具输出仍需满足同一规则，手工 Markdown 路径也应可用。

## 7. Harness 资产与过程材料

`harness/README.md` 是管理导航，不是 Runtime 默认加载全部内容的目录。发行包身份、适配候选身份、实际生效范围必须区分；同一项目可有多个 Runtime/作用域适配，不能设置一个不带范围的全局 READY。

原始包保持固定内容，记录版本、source_revision、包 Hash、可信发布及验证依据、可取得位置。可复用外部缓存，不在每个适配目录复制整包；缓存不可用时重新获取并核验同一身份，不自动升级。

适配记录继续保存原协议要求的来源资产、要求到实现映射、管理文件/配置与内容身份、当前环境证据、验收范围、结果、限制、失效条件和恢复依据。实际 Skills、规则、配置使用 Runtime 真实加载位置；总入口只做必要引用，不伪装某一供应商目录为通用标准。

记录中的模型/工具/环境快照只用于绑定当次验收与失效判断，不能把它们当作永久配置意图。候选变更或环境变化先使相关旧证据不再适用，再验证新对象；失败候选不覆盖有效适配。回滚只作用于本次管理且获授权的变化，并核对当前用户修改与项目兼容性。

过程材料按用途处理：

- 正式结论与其必要证据留在所属产物或 evidence/，原始失败与后续修复证据分别保存；重跑不覆盖旧运行记录。
- scratch/ 默认不在正常读取路径内；草稿不能直接充当已确认的设计或验收结果。
- 被正式结论引用的临时文件在清理前移入稳定位置并修复引用，或绑定满足保留要求的外部证据。目录名称不能作为删除授权。
- 非持久 Workspace、团队空间、Git、CI 附件均沿既有 Publication Boundary 管理。被忽略文件不等于保密；提交或发布之前检查真实载荷和范围。
- 本版本不新增按天自动清理器、向量数据库或全量工具日志归档。完成对象默认原地保留，从活跃导航退出，但仍有历史入口；未关闭 OI/依赖不得随之消失。

## 8. 接入、迁移与恢复

Project Onboarding 在原有 Initialize / Reuse / Refresh / Migrate 中处理布局，不新增独立迁移协议：

1. 发现现有空间、入口、产物权威性和实际访问/写入权限；只读取接入所需结构与代表性记录，不提前执行完整业务认知。
2. 形成角色到既有位置的映射，确定哪些直接复用、哪些只补导航、哪些确需迁移。外部 Issue/设计系统可作为原事实源，不强制导出为平行 Markdown。
3. 在原 Baseline 中登记稳定绑定；真实缺失的共享意图或权限按既有协作规则处理，不机械加确认步骤。
4. 需要迁移时先检查范围、现有用户修改和引用，保留可回退依据；目标正文核对后更新引用与入口，最后清理本次已确认不再需要的旧管理副本。
5. 中断时以已确认权威内容恢复；新旧位置均存在不能自动认定较新者有效。发现重复身份或不同内容冲突时停止相关替换，先定位原来源。
6. 无相关变化时 Reuse 不生成无意义文件改动；普通业务任务不触发全量目录重整。

Harness Adoption 的验收需证明真实入口能到达产物，Fresh Agent 能定位当前状态、完整任务依赖和必要证据，且不会读取无关历史。仅生成 README 或安装 Skill 不构成通过。只读空间可复用阅读，但不能声称已满足需要写回的工作；具体缺口按实际能力和权限返回。

用户仅要求建立 Harness 时，允许在接入、适配、验收并汇报后结束，不要求填写业务目标或创建业务产物。明确要求启动新业务或继续既有工作时按适当路由接管，不以已有Task为条件；明确仅接入则止于本次请求边界，不形成永久业务禁令。Canonical、Bootstrap 与 README 示例同步保持此边界。

从 0.12.0 升级时先按既有绑定和正式发行规则确定是否采用新版，再由新版接入程序解释布局。只补目录不能使旧包自动获得新行为。工作空间迁移完成与新 Harness 生效分别验证；回滚 Harness 时核对它能否理解迁移后的入口，必要时恢复本次导航映射，不回滚已确认业务事实或误用旧验收结果。

## 9. 正式实施影响清单

| 位置 | 计划变化与检查 |
|---|---|
| docs/rules/artifact-organization-and-reading.md（新增） | 承载本设计中必要的持续规则；不直接复制维护者设计和验收表 |
| docs/rules/global-contracts.md | 声明 Workflow 适用新规则，保留 OI 与状态归属 |
| docs/rules/agent-delegation-and-coordination.md | 将上下文最小化和共享产物写入连接到新规则；不复制全文 |
| docs/rules/human-agent-collaboration.md | 将审阅入口及反馈写回连接到新规则，复用 Decision Readiness |
| docs/meta-protocols/project-onboarding.md | 补空间/布局发现、绑定、复用与迁移，保留 Baseline 三类信息边界 |
| docs/meta-protocols/harness-adoption-and-adaptation.md | 补入口装配、适配记录位置、读取验收和仅接入请求边界 |
| docs/workflows/main/04-implementation-planning/03-task-definition-and-orchestration.md | 明确 tasks.md 相对于所绑定空间定位，保留核心权威字段与按需下钻 |
| docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md | 补原产物写回与直接导航同步，保留 Requirement Sync 与底层事实分离 |
| 01A / 01B / 02 / 03 / 06 / 07 与 Exception | 逐份检查产物映射及读取链；依靠共享规则足够时不机械添加模板，仅修冲突与缺失消费者 |
| docs/manifest.yaml | 正式落地时 rule_documents 新增条目，规则数 4→5、Corpus 合计 44→45；明确 Main/Exception/Meta Protocol 适用，不凭 applies_to: all 推定完整覆盖 |
| docs/README.md、rules/README.md、meta-protocols/README.md、overview.md | 同步职责与导航，不让设计文档成为 Canonical 入口 |
| docs/reference/glossary.md | 必要时定义产物入口、权威正文、派生导航及空间映射，避免引入与既有 Artifact 冲突的术语 |
| README.md、CHANGELOG.md、VERSION、发布元数据 | 按实际里程碑更新；接入示例不要求业务目标；兼容性仅按实测宣称 |
| packages/harness/、tools/、verification/harness/ | 走正式构建链生成受影响资产，按实际需要扩展结构检查与行为证据，不手改旧包追认 |

不因设计文档新增而立即修改正式 Manifest 计数。正式规则提交后再同步其登记；实施来源 Commit 与最终 Package source_revision 必须一致。

## 10. 版本、构建与交付路线

这是新增跨阶段组织/消费约束，符合当前 0.x 的 MINOR 规则，目标为 **0.13.0**。设计阶段只在 Unreleased 标注方案与状态；VERSION、正式 Manifest 和当前发行身份仍保持 0.12.0。进入实施候选时按治理流程同步预期版本及候选状态，最终冻结之前统一 Candidate 元数据。

| 顺序 | 工作 | 完成依据 |
|---|---|---|
| 1 | 本设计、验收矩阵和语义冲突检查 | 全流程落位、权威归属、迁移及读写边界可审阅 |
| 2 | 正式 Rule、两个协议及必要消费者落地 | 新规则登记和旧语义保持；设计未落地项显式追踪 |
| 3 | 构建范围判定 | 从上一发行 Manifest 的 source_revision 识别真实 Delta，建立新规则来源映射 |
| 4 | 预编译与 Builder 回查 | 直接读取完整 Canonical，更新规则/接入/流程消费者及完整 Envelope |
| 5 | 固定候选结构、独立语义和行为验证 | 执行[验收方案](acceptance.md)，记录失败与修正，固定对象通过 |
| 6 | 合入与发布 | 同一通过对象发布；Tag 与 Release 标题均为 0.13.0；提供迁移说明和实际兼容范围 |

上一正式包 Manifest 的构建基线是 `2f585f0faa8c0ba831161858a2e1418fd2d527e7`，不是当前设计分支 HEAD。实施时重新从上一正式发行解析，不把此值当作未来永久常量。

新增规则为共享依赖，且两份接入协议和读写链变化，预计验证至少覆盖所有 11 个 Skill 的消费路径、5 类共享规则及包级组合。实际重建范围由新旧 Manifest、精确来源映射及依赖判定；无法证明缩小范围时 Full Build，不能只新增一个规则文件并改计数。

## 11. 设计自查与剩余验证

已在设计中处理：跨需求任务集、共享设计/验收、原位置 OI、状态摘要漂移、索引缺失、并发与中断、外部空间与加载目录分离、原包不可变、证据清理、无业务目标接入、版本与候选身份。

实现选择已给默认值：Markdown 入口、spec/ 默认根、原位历史、按需拆分、静态链接优先、复用原协议。具体项目已有目录与共享边界由接入时发现，不能在可移植规则中固定本机路径或单一 Runtime。

设计未声称实现已完成、读取效率已提高或 0.13.0 已发布。性能收益、Fresh 恢复、真实加载与 Human 审阅效果必须由下一阶段证据支持；验收结果与不足按下页记录要求报告。
