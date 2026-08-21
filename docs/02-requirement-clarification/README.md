# 2. 需求澄清

将原始需求收敛为**明确、可验证、可供技术设计直接消费的需求基线**。

## 阶段流程

```text
需求解读 → 歧义与缺口识别 → 范围与规则确认 → 验收标准确认
```

| 步骤 | 主要做什么 |
|---|---|
| 需求解读 | 还原需求意图，明确现状 / 问题 / 目标。 |
| 歧义与缺口识别 | 找出会影响后续决策的不确定项。 |
| 范围与规则确认 | 明确做什么、不做什么以及关键业务规则。 |
| 验收标准确认 | 将正确结果转化为可明确 Pass / Fail 的 Acceptance Criteria。 |

## 输入

对应项目入口形成的 Requirement Input Context，以及 PRD、讨论记录等 Requirement Materials。

## 输出

Requirement Interpretation、Scope & Rule Definition、Acceptance Criteria，以及必要的 `OI-xxx`。

## 完成条件

需求意图、范围、关键规则与验收标准已经明确；不存在会阻塞技术设计的关键未知。

## 详细规则

1. [需求解读](01-requirement-interpretation.md)
2. [歧义与缺口识别](02-ambiguity-gap-identification.md)
3. [范围与规则确认](03-scope-rule-confirmation.md)
4. [验收标准确认](04-acceptance-criteria-confirmation.md)

下一步：[`技术方案设计`](../03-technical-design/README.md)。
