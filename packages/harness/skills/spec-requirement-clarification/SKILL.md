---
name: spec-requirement-clarification
description: 将新项目或存量项目需求收敛为稳定 REQ、范围、业务规则与可验证 AC；用于 Spec Coding 阶段02及需求语义失真回流。
---

# 02：确认需求含义与正确性标准

当前范围通过[接入](../../bootstrap/BOOTSTRAP.md)后，读取[全局](../../rules/global.md)和[协作](../../rules/collaboration.md)，委派时读[委派](../../rules/delegation.md)。不能靠推断填正式需求；已明确确认的事实可自主整理，不重复审批。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 解读与身份

Requirement Input Context 是已有上游产物的消费视图，不新建持久层。Greenfield 读取相关 Project Positioning、Business/System Definition、Requirement Framework 中需求单元、关联/Core Flow/OI，继承原 REQ，不重编号。Brownfield 读取 Project Overview、Business/System Context 和 Requirement Context 的变化/定位/缺口，若缺 ID，在进入本链时只分配一次稳定 `REQ-xx`。身份不代表范围规则AC已确认。两条路径无需同时存在，不补造另一套产物；结合 PRD、补充说明、讨论等材料，只补真正缺失上下文，不重做01。

还原谁在什么场景下的目标，As-Is/Existing Situation → Problem → To-Be。新项目无系统现状时用业务/用户状态；To-Be 是可观察行为/结果，不夹实现。

以 Known（材料/证据支持）、Inference（合理但未确认）、Unknown 分类，不将推断当事实。保存轻量 Requirement Interpretation：Requirement、Intent、As-Is/Existing Situation、Problem、To-Be、Known/Inference/Unknown，只保存新增理解。检查入口上下文、ID、原因、现状问题、目标、确定性清楚且未补范围规则技术，再继续。

## 2. 关键歧义与缺口

从 Inference/Unknown/Problem/To-Be 检查 Ambiguity（多解）、Gap（缺条件规则场景）、Conflict（材料与现状矛盾）、Assumption（未确认前提）。仅保留会影响需求正确性、范围、规则或技术决策的关键不确定；低价值细节不为完整性强行澄清或造OI。

先用项目证据缩小问题，再形成明确场景、单一未知、可回答问题，按需附当前理解、候选和影响；不转交未完成研究，不提前讨论实现。例如重新上传已知替换生效内容、保留历史未定义时，说明其数据保留/验收影响，再问覆盖还是留历史。

跨阶段跟踪复用稳定 OI，按全局字段并附 Issue、Impact、Question、Status、Blocking、Owner Stage、已解决 Resolution；deferred 要有明确后移理由和承接位置。问题可判断且排除低价值未知后交下一步，同ID不复制事实源。

## 3. 范围与规则

根据已确认解读和澄清结论，按业务结果写 In Scope、Out of Scope、Boundary，不用页面/API/文件列表代替范围。按需确认 Trigger、Behavior、State（允许/禁止）、Data（业务语义）、Exception（失败/回退），保持需求层级，不设计字段组件MQ。

固化歧义解释、范围取舍、核心行为规则决策和非阻塞OI。Agent 可整理已确认内容；仍待决定 Requirement 意义、范围、核心规则、关键目标由 Human Decision，提供证据、候选解释、影响，必要时先恢复决策就绪。不通过默认假设关闭未知。

保存 Scope & Rule Definition：In Scope、Out of Scope、Boundaries、Business Rules、Decisions、按需 Open Items。若关键未知仍影响目标/范围/规则，回歧义步骤；必要 Human 决策已完成且不阻塞 AC/Design 才移交。

## 4. 验收标准

必须已具稳定 REQ；缺身份回解读修正，不在这里重新分配。由已确认范围规则提取核心路径、重要边界异常、用户或系统期望结果，不机械覆盖一切细节。

可用 Given/When/Then，例如受支持文件上传成功后确认已上传且后续处理不阻塞结果返回。形式可调，但每条必须真实可验证、可明确 Pass/Fail，不用“体验良好”“合理展示”。Agent 可机械转写已确认含义；新增 AC、改变其意义或重新定义正确性由 Human Decision，已有确认不重问；写AC发现新歧义/规则缺口回前序，不自行补全。

AC 保存 ID（如AC-01）、唯一主 Requirement、Scenario、Given、When、Then、按需 Trace 到 Scope/Rule/Decision。跨需求关系放 Trace，不复制主归属。只保留证明需求成立的关键标准，不扩成完整测试设计。

检查核心、已明边界异常、规则决策全覆盖，稳定归属正确，无 Scope 外需求、含糊判定或实现约束，涉及新增正确性语义的必要决策完成。输出 REQ + Scope/Rule + AC 进入[技术设计](../spec-technical-design/SKILL.md)。
