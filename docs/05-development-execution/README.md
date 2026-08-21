# 5. 开发实施

让 Agent 在既定 Task Contract 内完成实现，并通过任务级与需求级边界持续推进直到开发收敛。

## 阶段流程

```text
就绪任务调度 → 自治实施与闭环 → 验收与异常收敛 → 状态提交与持续推进
```

| 步骤 | 主要做什么 |
|---|---|
| 就绪任务调度 | 从 Task Graph 中选择当前可执行 Task，并准备最小上下文。 |
| 自治实施与闭环 | 在契约内实现、局部验证、修复并形成 Task Commit。 |
| 验收与异常收敛 | 独立验证 Task 结果，失败时路由修复 / 纠偏。 |
| 状态提交与持续推进 | 固化状态与证据，重算 Runnable；Requirement 完成时进行 Integration、AC Gate 与 Push。 |

## 输入

Execution Ready 的 Task Set、Task Graph、Implementation Baseline 与必要运行环境。

## 输出

Task Commit / `code_ref`、Verification Result、可信 Task 状态，以及 Requirement Integration / AC Gate / Push 状态。

## 完成条件

Required Requirement 下的 Task 均已完成，需求级 Integration、AC Gate、Push 已完成或明确阻断，并可进入最终验证。

> Requirement Push 只是同步到远程开发分支，不代表最终 Verified、Merge、Release 或 Deploy。

## 详细规则

1. [就绪任务调度](01-ready-task-scheduling.md)
2. [自治实施与闭环](02-autonomous-implementation-and-closure.md)
3. [验收与异常收敛](03-verification-and-exception-convergence.md)
4. [状态提交与持续推进](04-state-commit-and-continuous-progression.md)

下一步：[`验证收敛`](../06-verification-convergence/README.md)。
