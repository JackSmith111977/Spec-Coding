# 1. Current State & Impact Analysis｜现状与影响分析

## 1.1 目标

基于已确认的 Scope & Rule Definition、Acceptance Criteria 与既有项目认知，将需求映射到真实系统，明确**当前实现如何运转、需求会影响哪些系统职责，以及存在哪些依赖与约束**，为后续方案构思与决策提供稳定的事实基础。

本步骤只回答“**现在怎么做、会影响哪里、受什么限制**”，不提前选择技术方案或设计具体实现。

---

## 1.2 需求映射

```text
Requirement / Acceptance Criteria
              ↓
       Business Behavior
              ↓
       System Capability
              ↓
       Technical Entry
```

重点确认需求涉及哪些现有业务行为与系统职责、哪些行为 / 状态 / 数据需要变化、对应系统入口和关键技术锚点在哪里。

优先复用既有 Business Context、System Context 与 Requirement Context，不从需求描述直接跳到代码修改点，也不重复扫描整个项目。

---

## 1.3 追踪现有实现

围绕已定位技术入口定向下钻，重点追踪：

- **Entry｜入口**：页面、接口、任务、事件或其他触发点。
- **Flow｜处理链路**：关键调用、处理职责及上下游关系。
- **Data & State｜数据与状态**：关键数据读写与状态流转。
- **Dependency｜依赖**：外部服务、中间件、共享能力或其他模块。
- **Extension｜既有能力**：当前可直接复用或扩展的机制。

关键结论尽量由代码、配置、Schema、测试或实际运行行为验证，并显式区分已确认事实、合理推断与待验证信息。

---

## 1.4 识别影响与约束

- **Direct Impact｜直接影响**：需求明确触达的系统职责。
- **Dependent Impact｜连带影响**：由数据、接口、状态或调用关系传播产生的影响。
- **Constraint｜约束**：兼容性、共享依赖、性能、安全、发布或其他限制方案选择的条件。
- **Open Impact｜待确认影响**：当前证据不足、需要继续验证的影响点。

只确认“哪里可能需要变化以及为什么”，不决定具体如何修改。

---

## 1.5 收敛影响边界

| 状态 | 含义 |
|---|---|
| `Confirmed` | 已有证据确认属于本次需求影响范围。 |
| `Conditional` | 是否变化取决于后续方案选择。 |
| `Unaffected` | 虽然相关，但已确认无需因本需求变化。 |
| `Open` | 当前证据不足，暂不能形成结论。 |

对每个关键影响点保留必要的需求来源与技术证据，使结论能够回溯到对应 Requirement / Acceptance Criteria 与现有实现。

---

## 1.6 现状与影响分析产物

形成 **Impact Baseline（影响基线）**：

| 章节 | 内容 |
|---|---|
| `Requirement Mapping` | 关键需求行为与现有系统能力的映射。 |
| `As-Is Flow` | 与需求直接相关的现有实现链路。 |
| `Impact Scope` | 已确认、条件性及待确认的技术影响。 |
| `Constraints` | 会限制后续方案选择的重要依赖与约束。 |
| `Evidence / Open Items` | 关键证据及仍需继续验证的问题；无则省略。 |

只保留影响后续技术决策的信息，不复制完整项目认知、需求材料或低价值代码细节。

---

## 1.7 完成标准

当 Human 或 Agent 能说明每个关键需求行为在现有系统中的能力与入口、As-Is 链路、确认 / 条件影响、重要依赖约束，且关键结论有证据、无阻塞方案设计的重大未知时，本步骤完成。

若发现新的需求歧义或规则冲突，应回到需求澄清；若只是技术证据不足，则继续补充实现追踪。

---

## 1.8 下游使用约定

```text
Scope & Rule Definition
          +
Acceptance Criteria
          +
Project / System Context
          ↓
Current State & Impact Analysis
          ↓
     Impact Baseline
          ↓
Solution Design & Decision
```

因此，本步骤的最终职责是：

> **将已澄清的需求准确映射到真实系统，以可验证的现状、影响范围与约束建立 Impact Baseline，为后续方案决策提供可靠边界。**