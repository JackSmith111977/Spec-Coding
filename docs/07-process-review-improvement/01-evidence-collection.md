# 1. Evidence Collection｜证据收集

## 1.1 目标

收集 Spec Coding 全流程中的关键事实，为后续的**过程重建、问题识别与根因分析**提供可追溯的证据基础。

证据收集阶段只记录**发生了什么**，不提前判断问题归属或分析根因。

---

## 1.2 证据分类

### 1. 需求证据

- 原始 PRD。
- PRD 评论与补充说明。
- 后续需求变更或补充。

### 2. 会话证据

- 需求澄清、技术方案设计中的关键会话。
- 对需求、设计、实现产生实际影响的确认、假设、决策与纠正记录。

### 3. 流程产物证据

围绕当前正式产物链，按需保留：

- Requirement（需求）及 Acceptance Criteria（验收标准）。
- Design（设计）。
- Task（任务）。
- Change（变更 / 实现结果）。
- Verification（验证）相关结果。
- 必要时保留关键版本变化。

> `Spec Coding` 是整套流程与方法的名称，不默认对应一个独立 `Spec` 产物。若具体项目存在 Technical Contract（技术契约）或 Executable Specification（可执行规格）等真实产物，应按其实际名称记录。

### 4. 执行证据

- Agent 执行日志中的关键行为。
- 文件修改、Git Diff、Commit。
- 测试执行及结果。
- 其他能证明实际实现行为和结果的工具输出。

### 5. 反馈证据

- Verification、Review 等环节发现的实际偏差。
- 因偏差触发的重新澄清、需求确认或设计调整记录。

### 6. 修正证据

- 针对已发现偏差进行的 Requirement、Acceptance Criteria、Design、Task、Change 或 Verification 修正。
- 返工与修复记录。
- 修正后的重新验证结果。

---

## 1.3 证据筛选原则

不是每一次 Agent 操作、工具调用、文件读取或日志输出都需要形成 Evidence。

只有真正影响以下内容的关键事件才晋升为正式证据：

- 理解
- 决策
- 产物 / 契约
- 实现
- 偏差
- 返工
- 验证

Evidence 保持客观，只描述可观察事实，不在本阶段加入根因判断。

---

## 1.4 证据产物

每条 Evidence 使用唯一编号 `EV-xxx`。

| 字段 | 说明 |
|---|---|
| `id` | 证据唯一编号。 |
| `time` | 事件发生时间或可排序顺序。 |
| `stage` | 事件发生的 SDD 阶段。 |
| `type` | 事件性质，如 question、decision、implementation、feedback、correction、verification。 |
| `subject` | 事件涉及主题 / 对象，用于串联同一主题。 |
| `actor` | human、agent、tool、system 等直接产生者。 |
| `fact` | 一句话客观事实描述。 |
| `source` | PRD、会话、Git Commit、Diff、测试 / 验证记录等原始来源。 |
| `related` | 相关 EV、Requirement、Acceptance Criteria、Design、Task、Change、Verification 等引用。 |

### 示例

```yaml
id: EV-023
time: 2026-08-17T15:10:00+08:00
stage: verification
type: feedback
subject: contract_source
actor: human
fact: >
  浏览器验证发现合同来源字段无法作为搜索条件使用。
source:
  - conversation/session-08#msg-32
  - verification/run-04
related:
  - REQ-07
  - TASK-12
```

---

## 1.5 下游使用约定

```text
IMP-xxx
  ↓
RC-xxx
  ↓
ISS-xxx
  ↓
EV-xxx
  ↓
source
```

因此，Evidence Collection 的最终职责是：

> **从 Spec Coding 全流程原始材料中筛选关键事实，将其标准化为可排序、可关联、可追溯的 `EV-xxx` 证据，为后续过程重建提供可信事实基础。**