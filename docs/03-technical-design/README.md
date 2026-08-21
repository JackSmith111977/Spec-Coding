# 3. 技术方案设计

将已经澄清的需求转化为**可实施、可解释、可验证的技术方案**。

## 阶段流程

```text
现状与影响分析 → 方案构思与决策 → 方案详细设计 → 方案验收与收敛
```

| 步骤 | 主要做什么 |
|---|---|
| 现状与影响分析 | 找到真实变更面、依赖、约束与风险。 |
| 方案构思与决策 | 识别关键技术问题，完成必要方案取舍。 |
| 方案详细设计 | 明确结构、链路、接口 / 数据 / 状态等实施契约。 |
| 方案验收与收敛 | 检查需求覆盖、一致性与关键假设，确认是否 Ready。 |

## 输入

已确认的 Requirement、Scope / Rules、Acceptance Criteria，以及必要的项目 / 系统上下文。

## 输出

Impact Analysis、Technical Decisions、Detailed Technical Design、Design Acceptance Result。

## 完成条件

关键需求与 AC 均有设计覆盖，关键假设有证据，阻塞问题已收敛，设计可以作为实施基线。

## 详细规则

1. [现状与影响分析](01-current-state-impact-analysis.md)
2. [方案构思与决策](02-solution-design-decision.md)
3. [方案详细设计](03-detailed-technical-design.md)
4. [方案验收与收敛](04-design-acceptance-convergence.md)

下一步：[`实施规划`](../04-implementation-planning/README.md)。
