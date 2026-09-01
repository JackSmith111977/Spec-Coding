# Harness Compiler V2 Semantic Review Scenarios

这些场景供独立 Reviewer 使用；它们不伪装成可由结构校验器判断的自然语言真值。

| Scenario | 变化 | 预期 Verdict |
|---|---|---|
| Trigger-driven Human Collaboration | 触发式同步被改为每阶段人工审批 | strengthening / fail |
| Constraint strength | `MUST` 被改为 `SHOULD` | weakening / fail |
| Reviewer boundary | Reviewer 被写成确定性验证的替代品 | misinterpretation / fail |
| Delegation boundary | Formal Task 被复制为平行 Delegation Contract | unjustified addition / fail |
