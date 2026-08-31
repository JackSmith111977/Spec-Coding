# 4. Requirement Framework｜需求框架

## 4.1 目标

基于 Project Positioning、Business Definition 与 System Definition，将项目能力转化为**结构化的需求空间**，明确核心需求领域、可独立讨论的需求单元及其关系，为后续 Requirement Clarification 提供清晰输入。

需求框架只回答“**有哪些需求需要被进一步定义，它们彼此如何组织**”，不在本阶段提前确定详细范围、业务规则、交互细节或验收标准。

---

## 4.2 识别需求领域

```text
Business Capability
        +
System Responsibility
        ↓
Requirement Area
```

重点明确：

- 哪些核心业务能力需要形成独立需求领域。
- 每个需求领域主要承载什么用户目标或业务结果。
- 哪些需求领域属于核心，哪些属于支撑或扩展。
- 是否存在尚未被需求承载的关键业务能力。

> 需求领域用于组织需求空间，不直接等同于页面、接口或技术模块。

### 启发式引导

- 为了承载核心业务能力，需要哪些可以独立讨论的需求主题？
- 哪些需求缺失后，核心业务闭环将无法成立？
- 当前讨论的是需求主题，还是已经进入详细功能设计？

---

## 4.3 建立需求单元

将需求领域拆分为可独立进入 Requirement Clarification 的 Requirement Unit（需求单元）。

每个 Requirement Unit 分配稳定、唯一的 Requirement ID（需求标识），推荐使用 `REQ-xx`。该 ID 从需求框架开始沿后续需求澄清、设计、任务、实现与验证持续复用，不因文档调整或状态变化重新编号。

```text
REQ-01
Actor
  ↓
Scenario
  ↓
Expected Capability / Result
```

重点保证：

- 单元具有稳定 `REQ-xx` 标识。
- 单元具有明确的业务目的。
- 粒度足以独立讨论和澄清。
- 不提前拆解为接口、数据库、类或具体实现任务。
- 不过早进入字段、文案、交互细节等低层设计。

> 需求单元的目标是成为后续需求澄清的基本对象，而不是提前形成完整规格。

---

## 4.4 建立需求关系

围绕核心业务场景，组织需求单元之间的前后置、依赖与支撑关系。

重点识别：

- 哪些需求构成核心业务链。
- 哪些需求依赖其他需求才能成立。
- 哪些属于主流程，哪些属于支撑或扩展。
- 是否存在需求之间的明显断链。

优先识别能够支撑项目核心价值的最小端到端链路：

```text
REQ-01
  ↓
REQ-02
  ↓
REQ-03
  ↓
Business Result
```

该链路可作为 Walking Skeleton（行走骨架），帮助确认项目最核心的需求骨架，但不在本阶段最终确定详细版本范围。

---

## 4.5 校验并固化需求框架

### 1. 上游可追溯

```text
Project Value
    ↓
Business Capability
    ↓
System Responsibility
    ↓
Requirement Unit
```

无法解释其价值来源的需求，应重新判断其必要性。

### 2. 需求完整性

重点检查核心业务能力与场景是否有对应需求承载、是否存在无价值来源需求、需求单元间是否有缺口或重复，以及是否提前进入后续澄清 / 技术方案内容。

### 3. 保留开放项

对于当前无法确认、但会影响后续需求定义的问题，显式记录为 Open Item，由 Requirement Clarification 继续处理。

---

## 4.6 结构化产物

| 章节 | 内容 |
|---|---|
| `Requirement Map` | 核心需求领域及其关系。 |
| `Requirement Units` | 带稳定 `REQ-xx` ID、可独立进入需求澄清的需求单元。 |
| `Core Flow` | 支撑项目核心价值的端到端需求链。 |
| `Open Items` | 尚需在后续需求澄清中确认的问题；无则省略。 |

---

## 4.7 完成标准

需求框架不以“完成详细需求规格”为完成标准。

当新的 Human 或 Agent 能仅依赖 Requirement Framework 说明核心需求领域、稳定 `REQ-xx` 需求单元、核心业务链、关键依赖、业务能力覆盖和开放项时，本阶段完成。

---

## 4.8 下游使用约定

Requirement Framework 是新建项目定义阶段的**需求组织层产物**。

后续 Requirement Clarification 应以带稳定 `REQ-xx` 的 Requirement Unit 为基本对象，进一步完成需求解读、歧义与缺口识别、范围与规则确认以及验收标准确认，不重新从项目定位或系统模型推导需求空间，也不重新分配需求身份。

```text
System Definition
        ↓
Requirement Framework
        ↓
REQ-xx
        ↓
Requirement Clarification
        ↓
Technical Design
```

因此，Requirement Framework 的最终职责是：

> **将项目价值、业务能力与系统职责组织为清晰、可追溯且具有稳定身份的需求地图，使后续需求能够被逐项澄清，而不提前完成需求本身。**