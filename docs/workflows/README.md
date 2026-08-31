# Workflows｜流程

本目录维护 Spec Coding 的正式 Workflow（流程）。Workflow 负责定义活动如何推进、状态如何收敛以及异常如何回接，不承担跨阶段 Rule 或项目接入 / 装配协议的职责。

## Main Workflow｜主流程

```text
01A / 01B → 02 → 03 → 04 → 05 → 06 → 07
```

- [`main/01a-project-definition/`](main/01a-project-definition/)：Project Definition（项目定义建立），Greenfield（新项目）入口。
- [`main/01b-project-understanding/`](main/01b-project-understanding/)：Project Understanding（项目认知建立），Brownfield（存量项目）入口。
- [`main/02-requirement-clarification/`](main/02-requirement-clarification/)：Requirement Clarification（需求澄清）。
- [`main/03-technical-design/`](main/03-technical-design/)：Technical Design（技术方案设计）。
- [`main/04-implementation-planning/`](main/04-implementation-planning/)：Implementation Planning（实施规划）。
- [`main/05-development-execution/`](main/05-development-execution/)：Development Execution（开发实施）。
- [`main/06-verification-convergence/`](main/06-verification-convergence/)：Verification Convergence（验证收敛）。
- [`main/07-process-review-improvement/`](main/07-process-review-improvement/)：Process Review & Improvement（流程复盘改进）。

## Exception Workflows｜异常流程

异常流程只在 Trigger 成立时按需加载，不作为新的 Main Workflow 阶段。

- [`exceptions/`](exceptions/)：Exception Workflow 总入口。
- [`exceptions/debug-and-defect-resolution/`](exceptions/debug-and-defect-resolution/)：Debug & Defect Resolution（调试与缺陷解决）。

正式 Workflow 清单以 [`../manifest.yaml`](../manifest.yaml) 的 `stages` 与 `exception_workflows` 为机器可读事实源。
