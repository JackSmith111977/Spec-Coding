# 6. Implementation & Validation｜实施和验证

## 6.1 目标

将上一阶段形成的 `IMP-xxx` 真正实施到对应的 Spec Coding / SDD 规则或 Harness 组件中，并通过后续真实开发验证改进是否有效。

> **实施对象是可复用规则与 Harness 机制，不是某个具体项目的 Requirement、Acceptance Criteria、Design、Task、Change、Verification 或代码等项目产物。**

---

## 6.2 实施改进

根据 `IMP-xxx.target` 和 `IMP-xxx.change` 修改对应规则或 Harness 组件。

实施前先检查 `IMP-xxx.authority`：

- `Autonomous`：可直接按既定改进实施。
- `Confirm`：只有 Human 已确认方案后才能写入 Canonical Rule（规范规则）。
- `Human Decision`：只有对应人工决策完成后才能实施；不得通过实现过程绕过该决策。

如果实施过程中出现会实质改变原 `decision`、扩大权限、弱化强制 Verification / Gate 或引入新的高影响行为，应停止按原授权继续，返回 Improvement Design 重新判定 Authority（权限）。

实施后应建立：

```text
实际规则改动
  ↓
IMP-xxx
  ↓
RC-xxx
  ↓
ISS-xxx
  ↓
EV-xxx
```

保证未来可以追溯：

> **为什么这条规则存在，以及它最初解决了什么问题。**

如果实际实施与原方案明显变化，应同步更新 `IMP-xxx`。

---

## 6.3 后续验证

在下一轮真实 Spec Coding 中，根据 `IMP-xxx.validation_plan` 观察实际结果。

```text
Effect
是否改善原问题

Cost
是否引入新的明显流程成本
```

根据结果判断：

- 保留
- 调整
- 删除 / 回滚

并更新 `validation_result` 与 `status`。

---

## 6.4 持续跟踪

规则出现以下情况时可以重新调整：

- 已不再解决实际问题。
- 被其他机制替代。
- 持续产生明显副作用。
- 成本高于收益。

Harness 演进既包括新增，也包括修改和删除；语义变化仍需重新经过对应 Authority Gate（权限门禁），不能因规则已经存在而默认获得后续修改权限。

---

## 6.5 持续跟踪产物

本阶段不新增独立对象，持续更新已有 `IMP-xxx`：

| 字段 | 说明 |
|---|---|
| `id` | 沿用 `IMP-xxx`。 |
| `authority` | 当前实施所依据的 Autonomous / Confirm / Human Decision。 |
| `target` | 实际改进落点。 |
| `change` | 最终实施内容。 |
| `validation_plan` | 既定验证方案。 |
| `validation_result` | 实际验证结果。 |
| `status` | 当前状态。 |
| `related` | 相关规则、文件、提交或其他位置。 |
| `side_effects` | 可选，副作用或额外成本。 |

仍统一维护在：

```text
improvements.md
```

---

## 6.6 闭环关系

```text
EV-xxx
  ↓
ISS-xxx
  ↓
RC-xxx
  ↓
IMP-xxx
  ↓
Authority Gate
  ↓
实施规则改进
  ↓
下一轮 Spec Coding
  ↓
验证效果
  ↓
Keep / Modify / Remove
  ↓
Evolved Harness
```

因此，Implementation & Validation 的最终职责是：

> **在既定人机权限边界内将改进真正落入可复用规则，并通过后续真实开发持续验证其效果，使 Spec Coding / SDD Harness 在实践中可控地演进。**