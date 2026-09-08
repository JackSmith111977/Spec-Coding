---
name: spec-project-onboarding
description: 建立、复用、刷新或迁移 Spec Coding 的目标项目接入基线；用于接入缺失、稳定意图或绑定变化，由 Harness 接入程序调用。
---

# 建立稳定接入关系

先读[权限](../../rules/global.md)的权限段和[协作](../../rules/collaboration.md)。本程序只持久化长期意图、绑定、硬约束，不推进业务阶段、不建立项目认知、不构建 Harness。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 触发与解析

没有有效基线；Target/Scope/仓库绑定变化；Human 改变协作、发布等长期意图；稳定权限/约束改变；规范语义影响接入；旧基线冲突、缺失、不可验证；或 Human 要求重接入时执行。普通需求、Bug、Task、代码变化不自动触发。

先从当前Runtime已授权入口与已有绑定定向发现，再检查必要仓库、Git、配置和代表性产物；未看到spec/不能推定不存在空间。同名目录先检查所有权，不覆盖。确定 Target 是单仓、Monorepo、Workspace、模块或多仓边界，发现既有 Adoption Baseline 与 Spec Workspace。判定 Initialize/Reuse/Refresh/Migrate 及变化来源。Target Scope 是管理变化的边界，不等同 Harness 放置范围。Greenfield 未建仓时可用 provisional 绑定，建仓后轻量刷新。

## 使用契约

先确定共享意图，再派生落点。可发现的事实自行调查，只询问无法安全推导的真实意图、歧义与权限，复用已有授权。

| 模式 | 状态共享边界 |
|---|---|
| Local | 当前 Human + Agent，不进入目标项目共享边界 |
| Shared | 团队共享，不要求进入代码仓库 |
| Repository-native | 流程产物作为正式资产进入目标仓库 |

解析 Working Language、需跨会话保存的 Workflow Artifact、Publication Boundary。Spec Workspace 承载需求/设计/任务/证据/基线，可与代码分离，但稳定绑定 Target。Workflow 决定什么是事实源，这里只决定保存在哪里和谁可见。

新建Repository-native默认项目根spec/，Local/Shared服从原共享意图，不扩大公开边界。已有等价空间或外部系统优先映射；原Baseline绑定空间根、管理范围及必要角色位置，默认布局不逐文件重复登记。Monorepo/多仓按管理范围绑定、跨范围引用带身份，不切断任务依赖。最小接入只建立必要总入口、基线及Harness记录，不造虚构REQ或空任务集。真实加载目录与READY属于适配记录。

已有仓库只记录必要稳定事实：Repository/Remote Identity、Base/Development Branch、fork/upstream/origin 的 Push/PR Target、Branch Isolation/PR 要求、Push/Merge Authority、禁止额外工作区等硬限制。Git 时机由开发实施定义，具体 Worktree/工具/并行不进入这里。

记录长期 Harness 共享与所有权边界、现有资产必须保留等约束。不把 Runtime、Loader、Model/Thinking、Tool/Subagent、包管理器、CI 命令、已有 Harness 清单、临时上下文或具体适配设计放入基线。

## 对齐与固化

只处理 Target、Usage、Spec Coding 或稳定集成相关 Delta；找到最早失效的接入事实，只刷新/迁移其受影响链路，判断包和 Workflow 影响。版本数字不同不自动迁移，要看版本、清单、变更记录和必要差异的真实语义影响。动态能力变化交回 Harness 环境发现；只有稳定意图/绑定受影响才改基线。

基线仅含 Declared Intent、Resolved Binding、Overrides/Constraints 三类内容。固化前检查完整性（后续不猜意图绑定）、一致性（协作发布仓库权限不冲突）、权限安全（不弱化规范/项目更严格约束/安全）、最小性（删冗余字段）。按 Spec Workspace 共享边界保存；Reuse 无变化不重写。已有事实源可引用，不复制项目结构、需求、设计、Task 或 Harness 状态。

需要布局迁移时在原Initialize/Reuse/Refresh/Migrate中检查权限、用户修改、对象身份和入站引用；确定复用、只补导航或迁移范围。先保留恢复依据，核对迁移正文，再更新引用/入口，最后清理本次确认无用的旧管理副本。中断以原绑定和确认记录定位，不按修改时间盲选新旧副本；冲突先消歧，保护原证据。普通任务不全量重整，布局完成不证明Harness生效。

## 移交

选择最终路由：Greenfield 无有效流程状态进入[01A](../spec-project-definition/SKILL.md)；Brownfield 项目认知不足进入[01B](../spec-project-understanding/SKILL.md)；已有有效权威产物/状态则恢复最早仍有效 Owner Stage。

向[Harness 接入](../spec-harness-adoption/SKILL.md)移交有效最小基线、最终路由和兼容的固定发行包。此时基线稳定不代表 Runtime 已验收。受控候选测试只在外部授权边界内建立明确标为测试的基线并移交固定候选；不建立真实项目正式发行绑定，不迁移测试 READY。

完成标准：Target 稳定可识别，原接入已发现或确认不存在，变化归属明确；无需猜测工作空间、发布、仓库或权限；Relevant Delta 已收敛，基线最小有效、路由明确。无需固定问卷或全量业务扫描。

移交前确认基线与总入口互相可定位、权威记录可达、迁移或必需写回缺口已明确；只读可继续阅读但不能假称持久写回完成。明确仅接入时无需业务目标，Route只保留后续入口，适配验收后按请求结束；有明确启动新业务工作或继续既有工作的意图则进入或恢复适当Workflow，不要求已有Task。

仅接入限定当前请求，不作为永久禁止业务推进的接入意图；后续新需求复用有效绑定，按项目事实选择01A、01B或适当Owner，先验收新增激活能力。
