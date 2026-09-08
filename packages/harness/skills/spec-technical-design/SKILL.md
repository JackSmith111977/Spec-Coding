---
name: spec-technical-design
description: 从已确认需求和 AC 建立影响基线、技术决策、详细设计并判定设计 Ready；用于 Spec Coding 阶段03及设计问题回流。
---

# 03：设计并证明可实施性

先确认[接入](../../bootstrap/BOOTSTRAP.md)就绪，加载[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)，委派时读[委派](../../rules/delegation.md)。输入为已确认 Scope/Rule、AC 和对应项目上下文，深度按风险调整。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 现状与影响

从 Requirement/AC → Business Behavior → System Capability → Technical Entry 映射需求，不直接跳到代码修改点，不重复全项目扫描。复用既有业务/系统/需求上下文，围绕入口定向追踪 Entry、Flow、Data & State、Dependency、可复用/扩展机制。关键结论用代码、配置、Schema、测试或实际行为验证，区分已确认、推断和待验证。

区分直接影响、由数据/接口/状态/调用传播的连带影响、兼容/共享依赖/性能/安全/发布等约束和待确认影响。每关键点记录需求来源和技术证据，标为 Confirmed、Conditional（依赖方案）、Unaffected（证据确认无需改）、Open（证据不足）。这里只回答现在怎样、影响何处和限制，不提前选方案。

固化 Impact Baseline：Requirement Mapping、As-Is Flow、Impact Scope、Constraints、按需 Evidence/Open Items。只留影响技术决策的信息；入口、链路、影响和约束可解释可追溯且无阻塞方案的重大未知才继续。需求歧义/规则冲突回[02](../spec-requirement-clarification/SKILL.md)，纯技术证据不足继续追踪。

## 2. 方案决策

从需求与影响基线提炼当前机制为何不足、需改变的核心行为/性质、必须满足的约束，不从表象跳技术。确有选择空间才列多个方案（同步/异步、复用/新增、接口变化、数据状态架构）；简单明确惯例直接沿用，无需虚构候选。

评估 Requirement Fit、Compatibility、Complexity、Risk、Evolvability，性能/安全/资源成本仅实际相关才补。方案成立所依赖的关键假设先用代码/测试/实验验证。

已有惯例、局部可回退可独立验证可 Autonomous；架构边界、迁移、兼容、安全、显著运维、长期成本或难回滚取舍进入 Confirm。若须改 Requirement/AC、接受偏差或改风险边界，回权威源由 Human Decision，不在设计隐式完成。复用已确认原则；关键决策前按协作程序提供问题、现状影响、主要候选、取舍、证据与推荐，已有共享模型只同步变化。

固化 Solution Decision：Technical Problem、确有选择时 Candidate Options、Decision、Rationale、Trade-offs、按需 Open Items；必要备选及放弃原因可留，不记录一切思考。技术问题、选择依据、需求约束匹配、前提验证及所需确认齐备后展开。

## 3. 详细设计

明确新增/修改/复用模块的职责、边界、协作与保持不变部分，优先既有架构扩展点，避免无必要扩大改造。

沿 Trigger → Input → Processing → Data/State Change → Dependency → Result 设计相关 Interaction/Data/State Flow；异步/事件/并发时明确时序。按需要稳定 API/RPC、Request/Response、Event/Message、数据模型/Schema、状态转换、错误返回、权限校验等跨边界契约，使各模块能独立实现验证，不将关键语义留给编码决定。

补实际影响正确性交付的失败异常、超时重试幂等、并发冲突、旧数据接口兼容、发布迁移回滚、权限安全极端输入；不无限扩张假想异常。

保存 Detailed Technical Design 的 Structure、To-Be Flow、Contracts、Boundary Handling、按需非阻塞 OI 引用；按复杂度展开，不强制所有章节。不下沉具体代码文件、函数拆分或实现步骤。核心方案不成立回方案决策；需求或约束认知错回最早上游。沿用同一 OI，不另造 Open Issue。

## 4. 设计验收

只验证既有设计准入，不偷偷重设计。逐关键 AC 回查 Technical Decision→Detailed Design，确认 Scope/Rules 均承载，无漏项和范围外行为。验证结构边界、调用/数据/状态闭环、契约一致、依赖约束、异步并发状态转换，与影响基线和技术决策一致。

通过代码/配置、Schema/接口、自动化/运行验证、小型 PoC/Spike、相关性能兼容第三方验证证明关键假设；标明 Validated、Open（证据不足但非阻塞）、Invalid（已被推翻）。Risk 是潜在不利影响，OI 是具体未决问题，分别管理。

阻塞 OI 不得进实施：需求规则回02；现状影响错回本Skill第1步；核心决策错回第2步；设计细节缺失冲突回第3步。修复同 OI 状态/resolution，重验受影响 Trace，不重做全部。

输出 Design Acceptance Result：Requirement Coverage、Consistency Check、Validated Assumptions、按需 Risks/Open Items（稳定ID、状态、blocking、owner）、Readiness。只有无阻塞、关键覆盖一致、假设有证据且设计足够稳定时 `Ready`，否则 `Not Ready`。只有 Ready 可作为稳定设计基线进入[实施规划](../spec-implementation-planning/SKILL.md)。
