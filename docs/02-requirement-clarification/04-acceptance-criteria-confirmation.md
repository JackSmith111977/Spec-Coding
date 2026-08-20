# 4. Acceptance Criteria Confirmation｜验收标准确认

## 4.1 目标

基于已确认的 Scope & Rule Definition，将关键需求行为转化为**明确、可验证、与需求一致的验收标准**，定义本次需求“什么算做对了”。

本步骤只定义正确结果与可验证行为，不展开具体技术实现，也不替代后续完整测试设计。

---

## 4.2 提取关键行为

当前 Requirement（需求）必须具有稳定 `REQ-xx` 标识。Greenfield（新项目）直接继承 Requirement Framework 中的 Requirement Unit ID；Brownfield（存量项目）若尚无稳定标识，应在进入当前需求澄清链时分配一次并持续复用。

重点关注：

- **Core Flow｜核心路径**：正常场景下需求应如何成立。
- **Boundary｜关键边界**：已明确的重要条件与限制。
- **Exception｜关键异常**：会影响需求正确性的异常行为。
- **Result｜期望结果**：用户或系统最终应感知到什么结果。

只提取影响需求正确性的关键行为，不机械覆盖所有细节。

---

## 4.3 转化为可验证标准

推荐使用 Given / When / Then：

```text
Given  前置条件
When   发生行为
Then   期望结果
```

例如：

```text
Given 用户选择一个受支持的文件
When 文件上传成功
Then 页面应确认文件已上传
And 后续处理不阻塞上传结果返回
```

形式不是重点，核心要求是：

> **每条验收标准都应能够被实际验证，并产生明确判断。**

避免“体验良好”“正确处理”“合理展示”等无法直接验证的描述。

Agent 可基于已经确认的 Scope、Rule 与 Decision 自主起草、检查和补全表达形式；若新增 AC、改变 AC 语义或重新定义“什么算正确”，应进入 Human Decision（Human 决策）。已经由上游明确确认、只是被机械转写为可验证表达的内容不重复请求确认。

---

## 4.4 检查覆盖与一致性

重点确认：

- 每条 Acceptance Criteria（验收标准）都明确归属于一个 `REQ-xx`。
- 是否覆盖核心路径。
- 是否覆盖已明确的重要边界与异常。
- 是否遗漏关键 Business Rules 或 Decisions。
- 是否引入 Scope 之外的新需求。
- 是否存在无法明确验证的描述。

如果编写验收标准时发现新的需求歧义或规则缺口，应返回前序澄清步骤，而不是在本步骤自行补全。

---

## 4.5 验收标准产物

| 字段 | 内容 |
|---|---|
| `ID` | 验收标准唯一标识，如 `AC-01`。 |
| `Requirement` | 当前验收标准所属的稳定 Requirement，如 `REQ-01`。 |
| `Scenario` | 需要验证的关键场景。 |
| `Given` | 前置条件。 |
| `When` | 触发行为。 |
| `Then` | 期望结果。 |
| `Trace` | 必要时关联对应 Scope、Rule 或 Decision。 |

一条 AC 只设一个主 Requirement 归属；若需要引用其他需求关系，通过 `Trace` 保留，不复制或改变主归属。

只保留能够证明需求成立的关键标准，不展开为完整测试用例集。

---

## 4.6 完成标准

当 Human 或 Agent 能确认每条 AC 都有稳定 Requirement 归属、核心需求行为都有明确验收标准、关键边界和异常得到必要覆盖、每条标准可以明确判断 Pass / Fail、与范围和业务规则一致且没有引入新需求或实现约束；其中涉及正确性语义新增或变化的部分已完成必要 Human Decision 时，本步骤完成。

---

## 4.7 下游使用约定

```text
REQ-xx
  +
Scope & Rule Definition
          ↓
Acceptance Criteria Confirmation
          ↓
Acceptance Criteria
          ↓
Technical Design
```

因此，本步骤的最终职责是：

> **将已确认的需求范围与业务规则转化为具有稳定 Requirement 归属、可验证且权限边界明确的正确性标准，为技术方案设计、任务编排与后续验证提供稳定依据。**