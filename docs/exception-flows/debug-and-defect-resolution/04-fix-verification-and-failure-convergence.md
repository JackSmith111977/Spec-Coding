# 4. Fix Verification & Failure Convergence｜修复验证与异常收敛

## 4.1 目标

基于 Root Cause Resolution（根因处置结果），接管已完成的纠正结果，重新验证原始异常与受影响链路，并形成可回交主流程的 Failure Closure（故障关闭结果）。

本步骤重点回答：

> **纠正是否真正解决了原始异常，以及当前故障是否具备关闭并返回主流程继续推进的条件。**

本步骤不重新决定修复方案，也不重复建立独立验证体系；具体 Verification（验证）优先复用既有主流程能力。

---

## 4.2 纠正结果接管

接管 Root Cause、Correction Route、Affected Trace 与 Reverification Scope，并确认对应主流程阶段已经完成必要纠正。

重点确认：

- 最早失效事实源已被修正。
- 受影响下游产物已完成必要对齐。
- 实际 Change 与 Root Cause Resolution 一致。
- 新产生的风险或 Open Item 已得到记录。

只验证实际纠正结果，不以“已经修复”的声明作为完成依据。

> **Verify the Correction｜验证实际纠正结果。**

---

## 4.3 原始故障回归验证

优先复用 Failure Baseline 中的 Reproduction、Repro Status 与 Evidence，重新验证原始异常：

```text
Before Fix
    ↓
Failure

After Fix
    ↓
Expected Behavior
```

根据原复现状态选择适当方式：

- `Reproduced`：重新执行原复现场景。
- `Intermittent`：通过重复、压力或时序验证降低偶然性。
- `Observed`：通过运行时 Evidence、Trace 或 Monitoring 重新观察。
- `Unsafe to Reproduce`：采用安全替代验证。

重点证明原始 Failure 已不再成立，而不是只确认某个测试通过。

> **Reverify the Original Failure｜优先重新验证原始异常。**

---

## 4.4 受影响链路重新验证

依据 Affected Trace 与 Reverification Scope，只重新验证因纠正而可能失效的链路。

```text
Invalid Source
      ↓
Correction
      ↓
Affected Trace
      ↓
Existing Verification
      ↓
Reverification Evidence
```

优先复用已有 Task Verification、Acceptance Criteria Gate、Deterministic Verification、Independent Review 或其他 Stage 6 验证能力，不重新定义重复验证流程。

必要时补充与修复直接相关的 Contract、Boundary、Known-good Case 或 Regression 检查。

> **Affected Trace Only｜只重新验证受影响链路。**

---

## 4.5 异常关闭与流程回接

综合纠正结果、原始故障回归与受影响链路验证，形成当前 Failure 的关闭结论：

| 状态 | 含义 |
|---|---|
| `Resolved` | 原始异常已消失，必要受影响验证通过，当前故障具备关闭条件。 |
| `Blocked` | 修复、验证或必要 Evidence 仍不足，当前故障无法可靠关闭。 |

仍存在非阻断不确定性时，通过 Residual Risk（残余风险）或稳定 `OI-xxx` 保留，不额外引入中间关闭状态。

Failure Closure 只关闭当前异常，不直接修改或替代主流程中的 Task、Finding、Open Item、Verification 等权威状态。关闭结果与 Reverification Evidence 应回交对应 Owner Stage，由主流程按其既有规则完成状态写回、依赖重算、Finding / Open Item 收敛或后续 Verification。

```text
Failure Closure
      ↓
Resolution Evidence
      ↓
Owner Stage
      ↓
Main-flow State Update
      ↓
Main Flow Continues
```

`Resolved` 不等于 Requirement 已 `Verified`；主流程最终状态仍由对应阶段 Gate 与完整 Evidence Trace 决定。

> **Close the Failure, Restore the Flow｜关闭当前异常，回接既有流程。**

---

## 4.6 产物

形成 **Failure Closure｜故障关闭结果**：

| 字段 | 内容 |
|---|---|
| `Failure` | Failure Baseline 引用。 |
| `Correction` | 已完成的纠正及对应事实源。 |
| `code_ref` | 相关实现引用；适用时记录。 |
| `Failure Recheck` | 原始异常重新验证结果。 |
| `Reverification` | 受影响链路的关键 Evidence。 |
| `Trace Status` | 受影响链路是否已经重新对齐。 |
| `Residual Risk` | 剩余风险；无则省略。 |
| `Open Items` | 尚需承接的问题；无则省略。 |
| `Status` | `Resolved` 或 `Blocked`。 |

只保存关闭所需的最终事实与证据引用，不复制完整修复、调试或验证过程，也不复制主流程自身状态。

---

## 4.7 完成标准

最早失效事实源已完成纠正，原始 Failure 已重新验证，Affected Trace 中必要 Verification 已通过或明确阻断原因，关键 Evidence 可追溯，剩余风险与 Open Item 已得到承接。

满足关闭条件时形成 `Resolved` 的 Failure Closure，并将结论与 Evidence 回交对应 Owner Stage；否则保持 `Blocked`。

本步骤结束只代表当前 Failure 已关闭或明确阻断，不替代主流程的 Task、Finding、Requirement 或 Verification 最终状态判定。

---

## 4.8 下游使用约定

```text
Root Cause Resolution
        ↓
纠正结果接管
        ↓
原始故障回归验证
        ↓
受影响链路重新验证
        ↓
异常关闭与流程回接
        ↓
Failure Closure
        ↓
Resolution Evidence
        ↓
Owner Stage
        ↓
Main Flow Continues
```

因此，本步骤的最终职责是：

> **以原始故障回归与受影响链路证据确认纠正结果，关闭当前异常并将可信结论回交主流程，使后续状态继续由既有权威事实源收敛和推进。**