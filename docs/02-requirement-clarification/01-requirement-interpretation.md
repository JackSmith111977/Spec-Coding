# 1. Requirement Interpretation｜需求解读

## 1.1 目标

基于已有 Project Overview、Business Context、System Context、Requirement Context 与 Requirement Materials，准确理解**为什么提出本次需求、当前存在什么问题、希望改变什么，以及当前哪些结论已经明确、哪些仍需澄清**。

本步骤只负责形成稳定的需求理解，不补全尚未确认的范围、规则与验收标准，也不提前进入技术方案。

---

## 1.2 建立需求语境

优先复用既有项目认知，而不是从原始需求重新猜测业务与系统背景。

重点读取：

- Project Overview 中与本需求相关的项目定位与导航信息。
- Business Context 中相关业务能力、对象、场景与规则。
- System Context 中相关组件、链路、数据与约束。
- Requirement Context 中的 Change Points、Business Position、System Position 与 Gaps。
- PRD、补充说明、讨论记录等当前 Requirement Materials。

只补充当前需求理解真正缺失的信息，不重复执行完整项目认知建立。

---

## 1.3 还原需求意图

将原始需求从“描述了什么”还原成“为什么要改变”。

重点明确：

- 谁在什么业务场景下遇到问题。
- 当前行为是什么。
- 当前行为为什么不能满足目标。
- 希望形成什么新的业务结果或系统可观察行为。

推荐使用：

```text
As-Is
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
| `Intent` | 需求为什么存在、希望解决什么问题。 |
| `As-Is` | 与需求直接相关的当前行为。 |
| `Problem` | 当前行为与目标之间的核心问题。 |
| `To-Be` | 希望形成的目标行为与结果。 |
| `Known / Inference / Unknown` | 当前理解的确定性边界。 |

只保存相对既有上下文新增的需求理解，不复制完整 Business / System Context。

---

## 1.6 完成标准

当 Human 或 Agent 可以清楚回答以下问题时，本步骤完成：

- 为什么提出本次需求？
- 当前行为与问题是什么？
- 希望改变成什么目标行为？
- 当前哪些理解已经确认？
- 哪些仍只是推断或未知？
- 是否没有提前补全未确认的范围、规则或技术实现？

---

## 1.7 下游使用约定

```text
Project / Business / System / Requirement Context
                +
        Requirement Materials
                ↓
     Requirement Interpretation
                ↓
     Ambiguity & Gap Identification
```

因此，本步骤的最终职责是：

> **在既有项目认知基础上，将原始需求还原为“现状—问题—目标”，并明确当前理解的确定性，为后续需求澄清提供最小充分、可追溯的需求理解。**