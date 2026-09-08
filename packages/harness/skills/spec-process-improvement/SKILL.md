---
name: spec-process-improvement
description: 从真实执行证据重建过程、识别问题、分析机制根因并经权限门禁改进可复用流程；用于 Spec Coding 阶段07。
---

# 07：复盘并验证机制改进

读取[全局](../../rules/global.md)、[协作](../../rules/collaboration.md)，委派时读[委派](../../rules/delegation.md)。当前[接入](../../bootstrap/BOOTSTRAP.md)范围须有效。这里改进可复用 Workflow/Rule/Meta Protocol/Harness，不将具体项目REQ/AC/Design/Task/Change/Verification或业务代码当改进对象。业务故障走[Debug](../spec-debug/SKILL.md)和其Owner。

产物读写前使[产物组织与读取](../../rules/artifacts.md)有效：从已绑定工作空间入口定位当前权威正文，按需沿依赖读必要状态/证据，写回原事实源后同步直接导航；不复制状态、不全文读取无关历史。

## 1. 收集关键事实

按需收原需求及评论补充变更、澄清/设计关键会话中的确认假设决策纠正、正式REQ/AC/Design/Task/Change/Verification及必要版本、执行日志关键行为/Diff/Commit/测试工具输出、验证评审偏差反馈、返工修正重验证据。Spec Coding不是默认独立Spec产物；真实Technical Contract/Executable Specification按实际名称引用。

只将影响理解、决策、产物契约、实施、偏差、返工、验证的可观察事件晋升Evidence，不保存每次工具读取；先记发生什么，不判断归属根因。每条唯一EV-xxx，字段id、time（时间/可排序顺序）、stage、type（question/decision/implementation/feedback/correction/verification等）、subject、actor、fact、source、related。比如浏览器发现来源字段不能搜索，关联原会话/验证记录及REQ/TASK，不在fact提前写原因。

## 2. 过程重建

按subject或明确关系串EV，还原需求明确、AC/Design变化、Task/Change后置修改、首次偏差、重新澄清返工和验证闭环。每关键事件可回EV，保留关键变化而非只保最终状态，不复制原日志，不提前评价合理性或根因。

在reconstruction.md统一Process Timeline，字段order/time、stage、event、evidence、result。例如“确认展示→设计存传→实施→验证发现不能搜索→补充搜索需求确认→修正→重验”，只陈述顺序事实，不能倒推最初需求必然包含搜索。

## 3. 问题筛选

从时间线识别有实际影响且可追溯的重新澄清、需求/AC/Design/Task/Change后置修改、返工重复开发、Verification/Review失败、Human纠正、明显重复无效高成本工作、反复问题、未出事但高风险缺口。排除正常变化和轻微低价值噪声，至少有一项真实影响才通常晋升正式Issue。

在issues.md记录ISS-xxx：id、title、初步category（requirement-gap/design-gap/task-gap/implementation-gap/verification-gap/agent-behavior/process-friction）、detected_stage、客观description、impact、evidence、related、status（candidate/accepted/ignored/merged/analyzing/closed）。分类可被后续证据修正，此时不深挖原因。

## 4. 根因到机制

问为什么流程没更早阻止/发现/纠正，不停在写错/漏做/Agent没想到。检查：早期本可发现未发现(discovery-gap)；问题已提但没闭环(closure-gap)；REQ→AC→Design→Task→Change→Verification传递丢失(traceability-gap)；既定契约未执行(execution-gap)；测试/验证遗漏(verification-gap)；上下文/Skill/Rule/Tool/Workflow缺失失效(workflow-gap)；有证据且不属前述才other。

找最早可拦截点并区分发现阶段与逃逸原因；允许一因多Issue、一Issue多因。证据不足继续追溯或降低confidence，不强塞分类。root-causes.md记录RC-xxx：id、title、type、description（失效机制）、issues、earliest_stage、escape_reason、failed_mechanism、evidence、按需confidence=high/medium/low。

## 5. 最小有效改进

看影响、重复性、风险、既有机制效果，允许No Process Change，不为复盘加规则。落点选最直接的权威机制：跨阶段持续约束→Rule，状态推进→Workflow，接入装配转换→Meta Protocol，项目执行保障→Harness；可以是清单Gate/Skill/AGENTS/Template/Tooling自动化，不在下游项目产物掩盖根因。

Current State→Expected State→真实Candidate Solutions→Smallest Effective Change→Decision；可增改删合并自动化。证据整理、映射、候选、影响分析及不变语义的文案格式可Autonomous；可复用行为、权限、状态、准入、自动化策略改变需Confirm；弱化强制验证、安全风险Gate或扩大业务语义/偏差接受权限需Human Decision。确认前呈现行为变化、RC/EV、收益与新增成本风险，不要求Human从全Diff猜影响。

实施前按expected_state定validation_plan：原问题是否减少消失、能否更早发现拦截、是否增明显成本。improvements.md记录IMP-xxx：id、title、root_causes、target、authority、current_state、expected_state、candidates、decision、change、validation_plan、后续运行填写validation_result、status。

## 6. 实施与后续真实确认

先核对authority已满足再改对应机制；Confirm/Human Decision未完成不写正式机制。实作偏离decision、扩权、弱Gate或新高影响行为则回改进设计重判权限，不能沿旧授权继续。实际变化→IMP→RC→ISS→EV可反向追溯，实际与方案明显差异更新同IMP。

下一轮真实Spec Coding按原计划观察Effect和Cost，判断保留、调整、删除/回滚，更新validation_result/status；未运行就明确待验证，不把文档检查当效果证明。机制不再解决问题、被替代、副作用明显或成本超收益可重调；既有机制不意味着后来语义变更自动获权。

持续更新同一improvements.md的id、authority、target、change、validation_plan/result、status、related（机制/文件/提交）、可选side_effects，不新增追踪对象。维护者规范或发行资产的变化移交维护者重新构建发布；目标侧不得热修原始发行包。完成边界是真实后续效果证据支持Keep/Modify/Remove，而非只把改进写下。
