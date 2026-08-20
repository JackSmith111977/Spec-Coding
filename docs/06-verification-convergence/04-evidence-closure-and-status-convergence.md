# 4. Evidence Closure & Status Convergence｜证据闭环与状态收敛

## 4.1 目标

基于已经收敛的 Verification Results、Evidence 与 Finding Resolution，完成最终证据闭环与状态判定。

本步骤回答：

> **当前 Requirement / Change 是否已经具备充分、完整且可追溯的证据，可以正式进入 Verified。**

本步骤不再执行新的验证、修复或发布动作，只负责收口已有事实并完成最终关闭。

---

## 4.2 汇总最终证据

包括：

- Task 级验收 Evidence。
- Deterministic Verification Evidence。
- Independent Review Evidence。
- Human Acceptance Evidence。
- Finding Resolution 与 Re-verification Evidence。
- Accepted Deviation 记录；无则省略。

只建立引用与索引，不复制形成新的测试报告。

---

## 4.3 校验追溯闭环

```text
Requirement
    ↓
Acceptance Criteria
    ↓
Design / Constraints
    ↓
Tasks
    ↓
Actual Changes
    ↓
Verification Items
    ↓
Evidence
    ↓
Finding Resolution
```

重点确认：

- 关键 Acceptance Criteria 均有有效 Evidence。
- 关键 Design / Constraint 得到必要验证。
- Actual Change Set 与验证对象一致。
- 需重验 Finding 已形成 Re-verification Evidence。
- 无未处理关键 Finding 或 Required Verification Gap。

> **Evidence over Claim｜以证据而非完成声明作为关闭依据。**

---

## 4.4 判定最终状态

### Verified

- Required Verification 已完成。
- 必要 Gate 已通过。
- 关键 Finding 已 Resolved、Invalid 或明确 Accepted。
- 不存在阻断性 Open Item。
- Requirement → Evidence 追溯链完整。

### Blocked

任一：Required Verification 未完成；关键 Gate 未通过；有未解决阻断 Finding；关键 Evidence 缺失 / 失效；追溯链无法闭合。

Accepted Deviation 不等于 `Pass`，应保留原始偏差、接受理由、影响与风险记录。

除非存在明确 Governance Constraint，否则不额外增加人工审批 Gate。

---

## 4.5 固化关闭结果

形成 **Verification Closure Record**：

| 字段 | 内容 |
|---|---|
| `Trace` | Requirement → Design → Task → Change → Verification 最终追溯关系。 |
| `Evidence` | 最终有效 Evidence 引用。 |
| `Findings` | Resolved / Invalid / Accepted / Blocked 状态。 |
| `Gates` | 必要质量、安全、风险或治理门禁结果。 |
| `Status` | Verified / Blocked。 |
| `Open Items` | 非阻断遗留项；无则省略。 |

只保存最终关闭真正需要的事实，不重复中间过程与推理。

---

## 4.6 完成标准

Required Verification 已完成或明确阻断原因，Requirement / Design / Task / Change / Evidence Trace 完整，关键 Finding 已处置，Accepted Deviation 有风险记录，无证据缺失 / 状态冲突 / 未处理关键问题，最终状态写入 Closure Record。

最终结果：**Verified** 或 **Blocked**。

```text
Verification Converged
        ↓
1. Final Evidence
        ↓
2. Trace Closure Check
        ↓
3. Final Status Gate
        ↓
4. Closure Record
        ↓
Verified / Blocked
```

> **以 Requirement 到最终 Evidence 的完整追溯闭环作为关闭依据，固化最终验证事实与状态，使完整变更从“实现完成”正式收敛为“证据支持的 Verified”。**