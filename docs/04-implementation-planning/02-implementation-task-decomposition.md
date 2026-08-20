# 2. Implementation Task Decomposition｜实施任务拆解

## 2.1 目标

基于 Implementation Baseline，将已确认的需求与设计拆解为**可独立实施、可独立验证的候选任务闭环**，形成 Candidate Task Set，为后续任务定型与编排提供稳定粒度。

本步骤只确定“需要哪些实施单元以及每个单元必须覆盖什么”，不提前固定 Agent、Wave、Worktree 或具体验证工具。

---

## 2.2 识别实施关注点

从以下基线信息识别需要被实际承接的变化：

```text
Requirement Baseline
+
Fixed Decisions
+
Design Baseline
+
Constraints
+
Risks / Open Issues
```

优先围绕业务 / 系统行为和端到端实现闭环组织，而不是按文件、Controller / Service / DAO、前后端层级或目录结构机械拆分。

---

## 2.3 形成实施单元

将相关变化聚合为具有明确目标和边界的 Implementation Unit。一个单元应尽量能够独立完成某个行为闭环，而不是只完成一个中间技术动作。

例如跨前端、接口、服务、数据的一个用户行为，如果这些变化只有组合后才具备独立意义，通常应优先视为一个实施闭环，再根据复杂度继续下钻。

---

## 2.4 收敛候选 Task 粒度

核心原则：

> **能独立做完 + 能独立证明做对 = 一个 Task。**

不以文件数量、代码行数、技术层或固定开发时长作为通用任务粒度标准。

Task 过粗的信号包括：目标不单一、边界过大、无法独立验证、执行上下文长期失控；Task 过细的信号包括：单独完成没有可观察价值、必须与另一个 Task 同时完成才能验证、只是文件或函数级机械切分。

---

## 2.5 识别关键覆盖路径

为了证明实施闭环成立，从以下信息推导 Coverage：

```text
Acceptance Criteria
+
To-Be Flow
+
Contracts
+
Boundary Handling
+
Risks / Constraints
```

按实际行为选择必要路径：

- **Main Path｜主路径**：正常执行并得到预期结果。
- **Branch Path｜分支路径**：不同合法条件、状态或业务分支。
- **Error Path｜异常路径**：失败、异常返回或错误状态。
- **Boundary Path｜边界路径**：空值、极值、重复、并发、超时、重试等。
- **Compatibility Path｜兼容路径**：历史数据、旧调用方或既有行为保持。

不要求每个 Task 固定覆盖所有类型，只保留真正影响正确性的路径。

本步骤只确定 **What must be verified**，具体采用何种验证方式留给下一步。

---

## 2.6 承接 Risks / Open Issues

| 情况 | 处理方式 |
|---|---|
| 不影响任务边界，但实施时需关注 | 绑定到相关候选 Task 的 Coverage 或后续验证要求。 |
| 本身形成独立、可验证的实施目标 | 形成单独候选 Task。 |
| 已实际阻塞任务拆解或使设计无法成立 | 触发纠偏，返回对应上游阶段。 |

不得为了继续拆 Task 而通过默认假设强行关闭仍然有效的 Open Issue。

---

## 2.7 候选任务产物

形成 Candidate Task Set。候选 Task 只保留最小必要信息：

| 字段 | 内容 |
|---|---|
| `Goal` | 当前候选 Task 要达成的单一实施结果。 |
| `Trace` | 对应的 Requirement / Acceptance Criteria / Design 来源。 |
| `Boundary` | 当前 Task 覆盖与不覆盖的实施边界。 |
| `Coverage` | 为证明该实施闭环成立必须覆盖的关键路径。 |
| `Open Items` | 实施 / 验证中仍需承接的问题；无则省略。 |

本步骤不正式定义 `Depends On`、Verification Method、Done、Agent 或执行顺序。

---

## 2.8 完成标准

当 Candidate Task Set 能完整承接 Implementation Baseline，任务粒度均能形成独立实施 / 验证闭环，关键路径有 Coverage，风险和开放项有明确承接位置，且没有通过文件 / 技术层机械切分时，本步骤完成。

---

## 2.9 下游使用约定

Candidate Task Set 是 Task Definition & Orchestration 的直接输入。下一步为每个候选任务建立稳定 ID、验证契约、Done、必要依赖与可执行组织方式，而不重新改变已收敛的任务边界。

> **将设计基线拆解为最小可验证实施闭环，为后续正式任务定义建立稳定粒度。**