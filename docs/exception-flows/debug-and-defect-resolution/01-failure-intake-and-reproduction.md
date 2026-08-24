# 1. Failure Intake & Reproduction｜异常接管与复现

## 1.1 目标

基于来自开发、验证、运行时、用户反馈或监控等来源的异常信号，建立可信的 **Failure Baseline（故障基线）**，为后续证据采集与故障定位提供稳定起点。

本步骤回答：

> **到底发生了什么、在什么条件下发生，以及当前是否具备继续调查的可靠基础。**

只负责异常归一、影响判断、现场保护与复现，不提前判断根因，也不直接修改 Requirement、Design、Task 等上游事实源。

---

## 1.2 异常归一与接管

首先将原始异常整理为可调查事实，至少明确：

- **Source**：User、Test、CI、Runtime、Monitoring、Finding 等来源。
- **Expected**：原本应当发生的行为。
- **Actual**：实际观察到的异常行为。
- **Context**：时间、环境、输入、状态及相关运行上下文。
- **Impact**：当前已知影响范围；低风险局部问题可简化。

已有 Finding、Open Item 或外部缺陷单时直接引用原对象，不重复建立新的事实源。

> **Normalize before Diagnose｜先明确问题，再开始诊断。**

---

## 1.3 影响判定与现场保护

判断异常是否仍在持续造成显著影响。

若存在持续数据错误、服务不可用、安全风险或其他高影响信号：

1. 优先保存可能随修改、重启或时间流逝而消失的关键 Evidence。
2. 必要时先通过可回退方式稳定系统或限制影响。
3. 稳定动作只用于止损，不视为 Root Cause（根因）修复。

普通开发缺陷或低风险测试失败无需额外展开 Incident Response（事故响应），直接继续复现。

任何高影响操作继续遵循全局 Human / Agent Authority。

> **Preserve before Mutation｜修改前先保护现场。**

---

## 1.4 复现基线建立

围绕原始异常建立最小充分的复现条件，优先确认：

- **Environment**：运行环境及关键依赖。
- **Version / `code_ref`**：相关版本或代码引用，可确定时记录。
- **Input / Data**：关键输入与数据状态。
- **Precondition**：异常发生前必须满足的状态。
- **Trigger / Steps**：触发方式或操作步骤。
- **Expected / Actual**：复现时应比较的关键行为。

对于 Regression（回归问题），可补充：

- **Last Known Good**：最后已知正常版本。
- **First Known Bad**：最早已知异常版本。

优先缩小到稳定、低成本的复现场景，但不强制构造完全最小化样例。

> **Minimal where Practical｜条件允许时尽量缩小复现范围。**

---

## 1.5 可复现性判定

根据实际观察明确当前复现状态：

| 状态 | 含义 |
|---|---|
| `Reproduced` | 在已知条件下能够稳定重现。 |
| `Intermittent` | 能够再次观察，但触发不稳定。 |
| `Observed` | 当前无法主动重现，但已有可靠现场 Evidence。 |
| `Not Reproduced` | 已尝试复现，但当前尚未再次观察。 |
| `Unsafe to Reproduce` | 主动重现可能造成不可接受影响。 |
| `Insufficient Evidence` | 当前既无法可靠观察，也缺少继续定位所需证据。 |

`Not Reproduced` 不代表异常无效。已有可信现场 Evidence 时，可继续进入后续故障定位。

只有 `Insufficient Evidence` 且缺失信息会阻止可靠调查时，才应补充证据或通过稳定 `OI-xxx` 承接。

> **Reproduce or Reliably Observe｜稳定复现或可靠观察。**

---

## 1.6 产物

形成轻量 **Failure Baseline｜故障基线**：

| 字段 | 内容 |
|---|---|
| `Source` | 异常来源及已有 Finding / Open Item / Issue 引用。 |
| `Symptom` | 已确认的异常现象。 |
| `Expected / Actual` | 期望行为与实际行为。 |
| `Impact` | 已知影响；无显著影响时可简化。 |
| `Context` | 环境、版本、数据及关键前置状态。 |
| `Reproduction` | 已确认的复现条件、步骤或现场观察方式。 |
| `Repro Status` | 当前可复现性状态。 |
| `Evidence` | 日志、Trace、请求、状态快照等关键原始证据引用。 |
| `Change Window` | Last Known Good / First Known Bad；适用时记录。 |
| `Open Items` | 尚缺失且需要跨阶段承接的 `OI-xxx`；无则省略。 |

只保留后续定位真正需要的事实与证据引用，不复制完整日志，也不记录未经验证的根因猜测。

---

## 1.7 完成标准

异常的 Expected / Actual 已明确，关键运行上下文与影响已知；必要现场 Evidence 已在修改前保存；已建立可复用的复现条件或可靠观察依据，并明确 Repro Status。

当前信息足以支持下一阶段开始故障定位，或证据不足的问题已明确阻塞并得到承接。

本步骤结束时**不要求已经知道根因**。

---

## 1.8 下游使用约定

```text
Failure Signal
      ↓
异常归一与接管
      ↓
影响判定与现场保护
      ↓
复现基线建立
      ↓
可复现性判定
      ↓
Failure Baseline
      ↓
Evidence Collection & Fault Localization
证据采集与故障定位
```

后续阶段以 Failure Baseline 为调查起点，通过运行证据逐步缩小故障边界，不应将 Error Message、初始猜测或临时修复直接视为 Root Cause。

> **将模糊异常转化为具有明确现象、上下文、复现状态和原始证据的可信故障基线，使后续定位建立在事实而非猜测之上。**
