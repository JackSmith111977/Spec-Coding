---
name: spec-project-understanding
description: 围绕存量项目当前需求建立可验证的项目地图、As-Is 业务与系统认知及变化定位；对应 Spec Coding 01B，认知不足时启用。
---

# 01B：定向认识现有项目

前置：[Bootstrap](../../bootstrap/BOOTSTRAP.md)完成当前范围接入；加载[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)，有委派时加载[委派](../../rules/delegation.md)。复用有效上下文，按风险深入，不扫描全部实现。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 导览

广而浅建立地图与入口，不在这里深入规则、完整调用链、数据模型或影响分析。先项目文档（可能过时），再仓库结构、Manifest/Build Config、应用/路由入口；信息不足或冲突才深入代码验证。

确认名称、定位职责、用户、问题、仓库类型（单仓/Monorepo/多仓）和技术形态。建立一句话业务领域地图；前后端、数据库、中间件、服务、外部依赖的顶层系统地图；仓库核心目录/模块与业务系统的职责映射，不复制完整目录树。

定位前后端入口/路由页面/主要服务、业务模块、迁移/Schema/数据访问、中间件/任务/外部集成、文档/测试/配置/脚本。导航采用“概念/模块 + 一句话职责 + 入口”，例如 DB Migrations → 数据结构演进入口 → db/migrations/，不枚举 API/DTO/表/类。

固化 Project Overview：Identity、Domain Map、System Map、Repository Map、Navigation Anchors、按需 Open/Conflicting Information。保留稳定高复用导航信息，结论可回原仓库文档核实。新读者能定位项目、顶层组成和模块探索起点即可继续。

## 2. 业务理解

沿当前需求从项目→业务域→核心能力→直接关联能力收敛，明确直接相关、背景和暂不深入的范围；As-Is（现状）与目标行为分开，不提前把 To-Be 合并为事实。

识别参与者目标/职责与可做、不可做、条件受限的业务行为；只谈业务权限，不分析鉴权实现。识别必要对象、包含/归属/依赖/产生关系、重要业务属性和容易混淆的术语，不展开数据库/技术实体。

多角色职责/权限需对齐时用用例图（参与者、行为、关系），对象多且关系影响理解时用领域模型（对象、关系语义、必要基数）；不在业务图塞 Controller/Service/DTO/API/表/技术状态码。

每核心场景明确 Actor/Trigger → Business Action → Object/State Change → Next Action/Business Result。围绕场景保存会改变路径/状态/结果的规则、权限、前置、异常。活动图为核心场景默认视图，状态生命周期复杂才补状态图，原则上一活动图对应一个场景、一状态图对应一个对象；按认知问题选图，不机械全生成。

用系统、文档、AC、测试、代码交叉验证高影响事实；代码行为只是证据之一，不自动等于正确业务规则。区分事实/推断/未知。先自主探索，再在重要模型建立或变化时按协作规则请求必要业务语义校正。

固化 Business Context 的 Business Scope、Business Model、Business Scenarios。证据与重要未知附着对应章节，避免重复。文本承载规范语义、图作结构视图，优先 Mermaid/PlantUML 等可版本化 DSL，同一事实只有一个权威位置。新读者能解释范围、角色、对象、场景状态及规则异常即完成。

## 3. 系统理解

将已确认业务映射为 System/Service/Module 的核心、直接和外围依赖范围。识别前后端、数据库、缓存、MQ、任务、文件存储、外部服务等实际组件的一句话职责与边界；HTTP/RPC/MQ/任务/数据库等交互、方向与同步异步边界，不维护全 API 清单。

将业务对象映射到系统表示与数据归属：创建、修改、存储、消费方；证据确认历史兼容、共享消费者、唯一写入方等重要不变量。组件图保持系统/服务/模块/存储粒度，呈现职责依赖与外部边界，不下沉方法/DTO/字段。

按业务场景追踪系统入口、控制流、数据流、状态、同步异步、关键分支失败和结果。通常到组件/模块→关键入口→关键 Symbol 即可，需要证明再回源码/配置/日志/数据，不复制私有调用链和实现。复杂链路按需时序、数据流或状态图。

固化 System Context：System Scope、System Model、System Flows；高影响结论先验证，分清确定性，证据/OI附在模型链路，文本精确、图表示结构、单一事实源。新读者能解释业务承载、协作、链路、数据状态和约束后继续。

## 4. 需求定位

提取新增/修改/扩展/限制/移除的业务 Change Points，每项一个独立意图，表达 As-Is → Change Intent，不补未知目标、不转换成实现清单。

定位业务的参与者、对象、场景阶段动作、状态/规则/前置/权限/分支；定位系统的入口、核心组件、System Flow、关键数据存储消费、跨服务/同步异步/外部边界。区分 Direct Impact 与 Adjacent Impact；关联上下游是澄清验证线索，不默认入 Scope。复杂时使用变化点—业务位置—系统位置轻量映射。

识别 Existing Capability、Missing Capability、Semantic Mismatch、Boundary Conflict。这里只发现定位 Gap，不决定目标语义或修法。优先验证影响范围与澄清方向的定位，区分直接、关联、潜在影响；需求和现状冲突不默认任一方正确，找到系统落点不表示设计已确定。

固化 Requirement Context：Change Points、Business Position、System Position、Gaps；只保存相对业务/系统模型新增定位，引用原模型链路。新读者能说清变什么、在哪里、直接/关联和缺口时完成01B，进入[需求澄清](../spec-requirement-clarification/SKILL.md)。
