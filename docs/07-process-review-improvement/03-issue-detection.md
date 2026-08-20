# 3. Issue Detection｜问题识别

## 3.1 目标

基于重建后的 Process Timeline，从真实开发过程里识别具有实际影响和复盘价值的异常信号，将其标准化为 `ISS-xxx`，为后续 Root Cause Analysis 提供高质量输入。

本阶段负责识别“**哪里表现异常以及造成什么影响**”，不提前深入解释根因。

---

## 3.2 识别异常信号

重点关注：

- 需求在后续阶段重新澄清。
- Requirement / Design / Spec / Plan / Task 后置修改。
- 实现返工或重复开发。
- Verification / Review 失败。
- Human 需要纠正 Agent。
- 明显重复、无效或高成本工作。
- 同类问题重复出现。
- 虽未造成故障但暴露高风险流程缺口。

---

## 3.3 初步分类

可使用：

- `requirement-gap`
- `design-gap`
- `spec-gap`
- `implementation-gap`
- `verification-gap`
- `agent-behavior`
- `process-friction`

问题分类只是初步判断，Root Cause Analysis 可根据进一步证据修正。

---

## 3.4 问题筛选原则

一个异常信号通常至少满足一项才晋升正式 Issue：

- 导致重新澄清。
- 导致 Requirement / Design / Spec / Plan / Task 后置修改。
- 导致代码或方案返工。
- 导致 Verification / Review 失败。
- 需要人工介入或纠正 Agent。
- 导致明显重复或无效工作。
- 同类问题重复出现。
- 暴露明显高风险缺口。

优先保留**有实际影响、可追溯、值得进一步分析**的问题，避免所有轻微异常进入正式复盘。

---

## 3.5 问题产物

统一维护：

```text
issues.md
```

| 字段 | 说明 |
|---|---|
| `id` | 唯一 `ISS-xxx`。 |
| `title` | 问题短标题。 |
| `category` | 初步分类。 |
| `detected_stage` | 实际发现阶段。 |
| `description` | 事实描述，不深入根因。 |
| `impact` | 重新澄清、Spec 修改、代码返工、重复测试、人工介入、上线风险等。 |
| `evidence` | 一个或多个 `EV-xxx`。 |
| `related` | `REQ-xx`、`DESIGN-xx`、`SPEC-xx`、`TASK-xx`、其他 `ISS-xx` 等。 |
| `status` | candidate / accepted / ignored / merged / analyzing / closed。 |

### 示例

```yaml
id: ISS-003
title: 合同来源搜索能力在实施后才确认
category: requirement-gap
detected_stage: verification
description: >
  需求澄清阶段曾讨论合同来源是否支持搜索，但没有形成明确结论。
  初始实现完成后，在验证阶段重新确认需要支持搜索，随后修改 Spec 并补充搜索链路。
impact:
  - requirement-reclarification
  - spec-change
  - implementation-rework
  - re-verification
evidence:
  - EV-007
  - EV-018
  - EV-052
  - EV-054
  - EV-057
related:
  - REQ-07
  - SPEC-04
  - TASK-12
status: accepted
```

---

## 3.6 下游使用约定

```text
EV-xxx
  ↓
Process Timeline
  ↓
Issue Candidate
  ↓
ISS-xxx
  ↓
RC-xxx
  ↓
IMP-xxx
```

因此，Issue Detection 的最终职责是：

> **从重建后的真实开发过程里识别异常信号，排除正常变化和低价值噪声，将具有实际影响和复盘价值的问题标准化为 `ISS-xxx`，为后续 SDD 根因分析提供高质量输入。**