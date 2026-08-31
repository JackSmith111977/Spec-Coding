# Exception Workflows｜异常流程

Exception Workflow（异常流程）用于承接无法沿 Main Workflow（主流程）直接推进的跨阶段异常，例如故障、缺陷或无法可靠归因的问题。

它不是新的 Happy Path 阶段，而是在需要时从当前流程进入，完成调查、纠正与验证后，再将可信结论回交对应 Owner Stage（承接阶段）继续推进。

```text
Main Workflow
      ↓
Failure / Unexpected Behavior
      ↓
Exception Workflow
      ↓
Correction / Resolution Evidence
      ↓
Owner Stage
      ↓
Main Workflow Continues
```

## 当前异常流程

- [`debug-and-defect-resolution/`](debug-and-defect-resolution/)：Debug & Defect Resolution（调试与缺陷解决），处理异常接管、证据定位、根因确认、纠正路由与故障关闭。

## 使用原则

- **Triggered Only｜按需触发**：只有当前异常无法由既有阶段局部闭环可靠处理时才进入对应异常流程。
- **Reuse Existing Baseline｜优先复用已有基线**：复用 Requirement、Design、Task、Verification、Evidence 与 System Context，不重新建立并行事实源。
- **Correct the Earliest Invalid Source｜修正最早失效的事实源**：根因确认后返回真正失效的权威位置纠正。
- **Affected Trace Only｜只处理受影响链路**：只重新对齐和验证真实受影响部分。
- **Return to Owner Stage｜回交承接阶段**：异常流程形成 Resolution Evidence，不替代主流程自身的 Task、Finding、Open Item 或 Verification 状态管理。

正式 Exception Workflow 文档清单以 [`../../manifest.yaml`](../../manifest.yaml) 的 `exception_workflows` 为机器可读事实源。
