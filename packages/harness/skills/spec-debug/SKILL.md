---
name: spec-debug
description: 将失败信号、异常行为或无法可靠归因的 Finding 转为复现、故障边界、根因与纠正回流证据；Spec Coding 全阶段 Debug 异常流程。
---

# Debug：定位原因，回接原流程

失败、非预期行为、归因不可靠或未解决Finding触发时，从[路由](../../bootstrap/routes.md)进入；可靠可归因的局部实现缺陷保持最短原Worker修复路径。读取[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)，委派时读[委派](../../rules/delegation.md)，写代码时读[质量](../../rules/code-quality.md)。当前所需环境能力须[验收](../spec-harness-adoption/SKILL.md)。本流程提供Resolution Evidence，不拥有Task/Finding/OI/Requirement最终状态。

## 1. 异常接管与复现

归一Source（用户/测试/CI/运行/监控/Finding）、Expected、Actual、Context（时间环境输入状态）、Impact，已有Finding/OI/缺陷单直接引用。不先猜根因或改上游定义。

持续数据错误、不可用、安全等高影响时，修改/重启前保存会消失的现场证据，按权限用必要可回退动作止损；止损不表示根因修复。普通低风险开发/测试失败直接复现，不额外铺事故响应。

建立最小充分复现：Environment/关键依赖、Version/code_ref（可知时）、Input/Data、Precondition、Trigger/Steps、Expected/Actual；回归按需Last Known Good/First Known Bad。不强制完全最小样例。

按实际记录Repro Status：Reproduced（稳定）、Intermittent（再次出现不稳定）、Observed（不能主动重现但有可靠现场）、Not Reproduced（尝试未再现）、Unsafe to Reproduce、Insufficient Evidence。未重现不等于无效，有可靠证据可继续；只有缺证阻止可靠调查才补证或稳定OI承接。

Failure Baseline保存Source、Symptom、Expected/Actual、Impact、Context、Reproduction、Repro Status、Evidence引用、适用Change Window、按需OI。不复制日志、不写未证实根因。上下文与影响明确、现场保护、可靠复现/观察成立即可定位；否则明确缺口阻塞，入口不要求先知道根因。

## 2. 证据与定位

复用System Context、AC、Impact Baseline、Design/To-Be/Contracts、Task Coverage/Verification、code_ref及既有证据建Expected Trace，结合Runtime重建Observed Trace，找First Divergence，关键点标Confirmed/Unknown/Diverged。已有基线不足时沿代码、配置、运行时定向下钻，不默认重新扫描整个项目；已有基线不可用可直接从Failure Baseline/System Context/Runtime调查。

优先区分性证据：边界哪侧、失败与已知正常对照、代码配置依赖数据环境的前后变化。Recent Change仅线索，不是原因。按需Code/Logs/Trace/Metrics/DB/MQ/Runtime/Test/Git/Config。

Observation→Hypothesis→Predicted Evidence→Inspect/Experiment→Support/Reject，问“若假设成立还应看到什么”。可增Debug日志/测试/脚本/观测点以取证，不作无依据修复。保留关键反证，已可靠排除无新证据不反复查。

逐步从系统/子系统/服务/组件/路径缩到Fault Boundary；回归按需Good/Bad和Git Bisect。输出Fault Localization Result：Failure引用、Expected Trace、Observed Trace、Evidence、Hypotheses及Supported/Rejected/Open、Fault Boundary、可选Candidate Cause/OI；只保存因果确认所需事实。明确偏离点、假设状态和可继续确认的范围；不能推进则说明缺证/阻塞，不强求此步最终根因。

## 3. 因果确认与纠正路由

区分症状、促成但不能单独解释的因素、能解释首次偏离及主要异常的根因候选，不停在错误消息。检查是否解释Failure/Observed Trace/Divergence、证据是否足、主要替代原因是否排除，允许时以干预/对照/重复检验Cause Present→Failure、Cause Controlled→Failure Removed。不能安全干预时用一致多源证据，不机械定数量；修复后通过单独不能证明原猜想是根因。

根因Confirmed=足以解释并排除主要替代；Probable=高度支持但现场/竞态等无法强确认，只有风险可接受且显式不确定才继续，风险接受仍按权限；Unconfirmed回定位补证。

沿Trace找最早失效源：REQ/AC→[02](../spec-requirement-clarification/SKILL.md)，Design→[03](../spec-technical-design/SKILL.md)，Task→[04](../spec-implementation-planning/SKILL.md)，Implementation→[05](../spec-development-execution/SKILL.md)，Verification Asset→[06](../spec-verification-convergence/SKILL.md)，Environment/Dependency→对应运行/依赖治理。下游忠实实现错误上游时继续上溯，不打补丁掩盖。

明确受影响REQ/AC/Design/Task/Change、失效Evidence、纠正位置与重验范围，不重做完整流程。Root Cause Resolution保存Failure、Root Cause及Confirmed/Probable、Evidence、Invalid Source、Affected Trace、Correction Route、Reverification Scope、按需OI。证据与风险匹配后交Owner正式纠正，本步骤不替代Owner修改。

## 4. 修复验证与回接

接管Root Cause/Route/Trace/重验范围，确认最早源已修、下游对齐、实际Change与处置一致、新风险OI已记录，不凭“已修复”声明。

优先复用原Failure Baseline：Reproduced重跑原场景，Intermittent用重复/压力/时序降低偶然，Observed用运行Trace/监控再观察，Unsafe用安全替代。证明原异常不再成立，不只看一测试绿。

依据受影响Trace复用Task Verification、AC Gate、确定性、独立Review或06能力；必要补相关Contract/Boundary/Known-good/Regression，不建立第二验证流程。

原故障消失且必要受影响验证通过才Failure Closure.Status=Resolved；修复/验证/证据不足为Blocked。非阻断不确定以Residual Risk或稳定OI保留，不添中间关闭状态。Closure保存Failure、Correction及源、适用code_ref、Failure Recheck、Reverification证据、Trace Status、按需Residual Risk/OI、Status。

将Closure和重验证据回原Owner，由主流程写Task/Finding/OI状态、重算依赖和继续验证；Debug不直接代写权威状态，不复制主流程状态。Resolved不等于REQ Verified，最终仍须对应Gate与完整Trace。
