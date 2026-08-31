# 1. Requirement Interpretation｜需求解读

## 1.1 目标

基于当前项目入口对应的 Requirement Input Context（需求输入上下文）与 Requirement Materials（需求材料），准确理解**为什么提出本次需求、当前存在什么问题、希望形成什么目标行为，以及当前哪些结论已经明确、哪些仍需澄清**。

`Requirement Input Context` 是对既有上游产物的统一消费视图，不是新增的持久化 Artifact（产物）。Greenfield（新项目）与 Brownfield（存量项目）分别复用各自已经建立的上下文即可。

本步骤只负责形成稳定的需求理解，不补全尚未确认的范围、规则与验收标准，也不提前进入技术方案。

---

## 1.2 建立需求语境

根据项目入口读取对应上下文，不要求两条路径的产物同时存在。

### Greenfield｜新项目

重点读取：

- Project Positioning 中与当前需求相关的项目目标、用户、场景与边界。
- Business Definition 中相关业务能力、对象、场景与规则。
- System Definition 中相关系统职责、链路、数据与约束。
- Requirement Framework 中当前 Requirement Unit（需求单元）、关联需求、Core Flow 与 Open Items。

Greenfield 直接复用 Requirement Framework 已分配的稳定 `REQ-xx`，不得在需求澄清阶段重新编号。

### Brownfield｜存量项目

重点读取：

- Project Overview 中与本需求相关的项目定位与导航信息。
- Business Context 中相关业务能力、对象、场景与规则。
- System Context 中相关组件、链路、数据与约束。
- Requirement Context 中的 Change Points、Business Position、System Position 与 Gaps。

Brownfield 若当前需求尚无稳定 Requirement ID，应在进入本需求澄清链时**分配一次稳定 `REQ-xx` 并持续复用**。Requirement ID 只建立需求身份，不代表范围、规则或 Acceptance Criteria 已经确认。

### 共同输入

同时读取 PRD、补充说明、讨论记录等当前 Requirement Materials。

优先复用已有上下文，只补充当前需求理解真正缺失的信息，不重新执行项目定义或项目认知建立，也不为了统一形式补造另一条入口路径的产物。

---

## 1.3 还原需求意图

将原始需求从“描述了什么”还原成“为什么需要改变或建立这种行为”。

重点明确：

- 谁在什么业务场景下存在问题或目标。
- 当前状态或既有行为是什么；新项目尚无系统行为时，以现有业务 / 用户状态为准。
- 当前状态为什么不能满足目标。
- 希望形成什么新的业务结果或系统可观察行为。

推荐使用：

```text
As-Is / Existing Situation
          ↓
        Problem
          ↓
         To-Be
```

To-Be 只表达目标行为与结果，不提前夹带技术实现。

---

## 1.4 区分理解确定性

对当前需求理解进行轻量分类：

- **Known｜已知**：已有明确需求材料或上下文证据支持。
- **Inference｜推断**：基于上下文形成的合理判断，但尚未被明确确认。
- **Unknown｜未知**：当前信息不足，无法可靠判断。

不要把 Inference 写成事实，也不要为了形成完整叙述而默认填补 Unknown。

---

## 1.5 需求解读产物

形成轻量 Requirement Interpretation：

| 章节 | 内容 |
|---|---|
| `Requirement` | 当前稳定 Requirement ID，如 `REQ-01`；Greenfield 继承上游，Brownfield 首次进入本链时分配。 |
| `Intent` | 需求为什么存在、希望解决什么问题。 |
| `As-Is / Existing Situation` | 与需求直接相关的当前行为或现有状态。 |
| `Problem` | 当前状态与目标之间的核心问题。 |
| `To-Be` | 希望形成的目标行为与结果。 |
| `Known / Inference / Unknown` | 当前理解的确定性边界。 |

只保存相对入口上下文新增的需求理解，不复制完整 Business / System Context 或 Definition。

---

## 1.6 完成标准

当 Human 或 Agent 可以清楚回答以下问题时，本步骤完成：

- 当前需求来自 Greenfield 还是 Brownfield，使用了哪组上游上下文？
- 当前 Requirement 的稳定 `REQ-xx` 是什么？
- 为什么提出本次需求？
- 当前行为或现有状态与问题是什么？
- 希望形成什么目标行为？
- 当前哪些理解已经确认？
- 哪些仍只是推断或未知？
- 是否没有提前补全未确认的范围、规则或技术实现？

---

## 1.7 下游使用约定

```text
Greenfield:
Project / Business / System Definition
              +
      Requirement Framework
              │
              ├─────────────┐
              │             ↓
Brownfield:   │   REQ-xx + Requirement Interpretation
Project / Business / System Context
              +             ↓
      Requirement Context  Ambiguity & Gap Identification
```

两条入口在 Requirement Interpretation 汇合，此后使用同一套稳定 Requirement Identity 与需求澄清流程。

因此，本步骤的最终职责是：

> **基于对应项目入口的既有上下文，建立或继承稳定 Requirement 身份，将原始需求还原为“现状—问题—目标”，明确当前理解的确定性，并形成新项目与存量项目都可稳定消费的统一需求澄清入口。**