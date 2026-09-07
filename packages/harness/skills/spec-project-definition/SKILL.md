---
name: spec-project-definition
description: 为没有存量项目的 Greenfield 建立项目定位、业务定义、系统定义和带稳定需求 ID 的需求框架；对应 Spec Coding 01A。
---

# 01A：从想法建立可复用定义

前置：[Bootstrap](../../bootstrap/BOOTSTRAP.md)接入与当前范围验收完成；读[全局规则](../../rules/global.md)及[协作](../../rules/collaboration.md)。有委派时读[委派](../../rules/delegation.md)。按风险裁剪，复用已有有效定义；保持以下四项职责及其边界。

## 1. 项目定位

从最初想法回溯问题，不以功能、产品形态或技术手段代替问题。确定核心问题/未满足需要、直接受影响者、发生情境、现行解决方式和不足、值得独立立项的理由。信息模糊时可用“不做项目会怎样解决”“只能解决一个问题选哪个”“这是问题还是预设方案”帮助收敛；不是固定问卷。

将问题落实为 User/Role → Context/Problem → User Goal；用户场景太宽时先聚焦最能代表核心价值的一类。识别核心用户和主要关系，暂不展开详细权限组织职责。描述真实场景目标，不列功能。

用 Before → Project → After 表达用户关键变化，确定最核心价值、项目级整体能力和基本职责/不做边界，不以接口、模块、技术栈表达目标。未知边界显式保留，详细 In/Out Scope 留阶段02。

固化 Project Positioning：Identity、Problem、Users & Scenarios、Value、Goals、Boundaries，按需 Assumptions/Open Items。分清已确认、推断和待确认，影响项目成立的关键未验证判断不隐藏。不提前做业务、系统或需求细化。

完成检查：新读者仅靠定位即可说明项目是什么/为什么、为谁解决什么、典型场景、价值变化、目标能力、边界和重要未知。下一步直接继承，不重新猜项目方向。

## 2. 业务定义

基于定位按 Project → Business Domain → Core/Related Capability 划分业务范围，分核心、关联辅助和范围外；能力表达业务做什么，不等同页面、功能或模块。可用“完成目标必须发生哪些行为”“缺哪项核心价值不成立”检查必要性。

建立参与者及主要业务职责、核心对象、创建/使用/影响者、对象关系与变化、影响理解的统一术语；暂不设计详细权限、组织、数据表、DTO 或 Schema。

对核心场景按 Actor/Trigger → Business Action → Object/State Change → Business Result 描述起点、行为、对象流转、结果、关键规则分支和异常。先保证核心闭环；对象生命周期复杂时才补状态机。

回查 Core Problem → User Goal → Business Capability 的价值来源；检查角色缺失、对象一致性、起止结果、状态闭环、跨场景规则冲突和范围无意识扩大。未知而影响设计的判断显式留 Assumption/OI。

固化 Business Definition：Business Scope、Business Model、Business Scenarios、按需 Assumptions/Open Items。新读者应能解释能力、参与者职责、对象关系、场景从触发到结果、变化、规则边界和未知；不以穷尽细节为完成。向系统定义移交已确认模型。

## 3. 系统定义

将业务能力映射到 System/Service/Module，区分内部承载与外部依赖，明确职责/不负责边界，避免用技术栈或代码结构代替职责。逐项检查“谁承载、是否必须内部实现、是否已越界讨论实现”。

定义组件协作、调用方向、同步/异步与外部交互关系，保持系统/服务/主要模块粒度，不写完整 API。对业务对象明确谁创建、修改、持有/持久化、消费及关键流转，不设计表字段。区分必守 Constraint 和仍可调整的 Design Assumption。

沿 Business Scenario → System Entry → Control Flow → Data/State Change → Sync/Async Boundary → System Result 形成核心端到端链路。复杂处按需时序/数据流/状态图，简单场景不强制。

检查 Business Capability → System Responsibility → System Flow 全覆盖、职责重叠/缺口、数据归属、状态责任方、循环依赖、同步异步/外部边界和核心闭环。具体框架基础设施、API 请求协议、表字段索引、类函数组织和部署拓扑留技术设计，已有明确硬约束除外。

固化 System Definition：System Scope、System Model、System Flows、按需 Assumptions/Open Items。新读者能解释上述边界、承载、数据、链路、约束即可进入需求框架。

## 4. 需求框架

结合业务能力与系统职责识别 Requirement Area，按用户目标/业务结果区分核心、支撑、扩展，检查是否有关键能力无人承载。不以页面/API/技术模块组织需求，不提前定义详细规则范围。

拆成可独立讨论澄清的 Requirement Unit，一次分配稳定唯一 `REQ-xx`，跨澄清、设计、Task、实现、验证复用，文档/状态变化不重编号。每单元说明 Actor → Scenario → Expected Capability/Result，保持业务目的和合适粒度，不提前拆接口、数据库、类或实现任务，也不下沉字段文案交互。

组织前后置、依赖、支撑、主流程/扩展关系，找最小端到端需求链作为 Walking Skeleton（行走骨架）；不是最终版本范围。检查 Project Value → Business Capability → System Responsibility → Requirement Unit 追溯，核心能力场景覆盖、无价值来源需求、重复/缺口和过早设计。待澄清问题复用稳定 OI。

固化 Requirement Framework：Requirement Map、Requirement Units、Core Flow、按需 Open Items。新读者能解释领域、稳定 ID、业务链、依赖、覆盖与未知时完成01A；按共享规则同步必要认知，进入[需求澄清](../spec-requirement-clarification/SKILL.md)，继承 ID 与上下文，不重新推导需求空间。
