# 4. Design Acceptance & Convergence｜方案验收与收敛

## 4.1 目标

基于已完成的 Detailed Technical Design，对技术方案进行最终闭环验证，确认其是否完整覆盖需求、在现有系统中保持一致、关键假设是否成立，并收敛剩余风险与未决问题。

本步骤重点回答：

> **这套设计是否真的满足需求、能够在系统中成立，并已经足够稳定地进入实施。**

本步骤不重新设计方案，而是验证已有设计是否具备进入任务拆解与实现的条件。

---

## 4.2 需求覆盖验证

重点确认：

- 每个关键 Acceptance Criteria 是否都有对应设计。
- Scope & Rule Definition 中的关键规则是否得到遵守。
- 是否存在已确认需求但未被设计覆盖的部分。
- 是否出现超出需求范围的额外设计或行为。

```text
Requirement
    ↓
Acceptance Criteria
    ↓
Technical Decision
    ↓
Detailed Design
```

核心目标是确保需求与设计之间不存在明显断点。

---

## 4.3 技术一致性校验

重点确认结构是否符合现有架构与模块边界、调用链 / 数据流 / 状态流是否闭环、接口 / 数据 / 状态契约是否一致、依赖和约束是否成立、异步 / 并发 / 状态转换是否遗漏，以及设计是否与影响范围和技术决策一致。

---

## 4.4 关键假设验证

会直接影响方案成立或可实施性的关键技术假设，应按需通过代码 / 配置检查、Schema / 接口确认、自动化测试或运行验证、小型 PoC / Spike、性能 / 兼容性 / 第三方能力验证。

关键结论区分：

- **Validated｜已验证**：已有足够证据支撑。
- **Open｜待验证**：证据仍不足，但暂不阻塞。
- **Invalid｜不成立**：假设被推翻，需要回到上游纠正。

---

## 4.5 结果收敛

对仍需后续处理的具体问题沿用 Open Item（开放项）契约，不重新生成新的“Open Issue”副本：

- `status = open`：尚未解决，继续由 `owner_stage` 承接。
- `status = resolved`：已完成修正或确认，记录必要 Resolution / Evidence。
- `status = deferred`：明确延期且已有后续承接位置。
- `blocking = true`：当前问题会影响方案正确性或可实施性，必须先处理；它与生命周期 `status` 分开记录。

若存在 `blocking = true` 的 Open Item，应沿追溯链返回：

```text
需求或规则问题
    → 需求澄清

现状或影响判断错误
    → 现状与影响分析

核心技术决策错误
    → 方案构思与决策

设计细节缺失或不一致
    → 方案详细设计
```

修正后更新同一 `OI-xxx` 并重新验证受影响链路，而不是从头重复全部流程。

Risk（风险）与 Open Item 分开维护：Risk 描述可能发生的不利影响；只有存在尚待处理的具体问题或决策时才关联 `OI-xxx`。

---

## 4.6 验收与收敛产物

| 内容 | 说明 |
|---|---|
| `Requirement Coverage` | 需求、规则与验收标准的设计覆盖情况。 |
| `Consistency Check` | 结构、链路与契约的一致性结论。 |
| `Validated Assumptions` | 已验证的关键技术假设。 |
| `Risks` | 已知风险；无则省略。 |
| `Open Items` | 仍需后续承接的稳定 `OI-xxx` 引用及其状态 / 阻塞信息；无则省略。 |
| `Readiness` | 当前设计是否可以进入实施。 |

最终只给出明确准入结论：

- `Ready`：不存在阻塞问题，可以进入任务规划与实施。
- `Not Ready`：仍存在 `blocking = true` 的问题，需要回到对应上游阶段纠正。

---

## 4.7 完成标准

当 Human 或 Agent 能确认关键需求 / 规则 / AC 均有设计覆盖，结构 / 链路 / 契约闭环一致，关键假设有证据，阻塞风险已收敛，Open Item 均保持稳定 ID 且有明确承接位置，设计足以作为实施基线时，本步骤完成。

---

## 4.8 下游使用约定

只有 Readiness 为 `Ready` 时，下游才应将当前技术方案视为稳定设计基线。

```text
Detailed Technical Design
           ↓
Requirement Coverage
           ↓
Consistency Check
           ↓
Assumption Validation
           ↓
Open Item Convergence
           ↓
        Ready?
       ↙      ↘
     No        Yes
     ↓          ↓
Upstream Fix   Task Planning /
               Implementation
```

因此，本步骤的最终职责是：

> **以需求覆盖、一致性与关键证据验证技术方案，收敛阻塞问题，并以稳定 Open Item 引用承接剩余未决事项，确认设计是否已经具备进入实施的条件。**
