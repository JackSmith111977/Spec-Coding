# Meta Protocols｜元协议

本目录维护 Spec Coding 的 Meta Protocol（元协议）：它们不推进业务开发阶段，而是定义 Spec Coding 如何与项目建立接入关系，并如何转换为当前环境中的执行 Harness。

当前正式 Meta Protocol：

1. [`project-onboarding.md`](project-onboarding.md)：建立、复用、刷新或迁移稳定的 Adoption Baseline，只持久化长期意图与稳定绑定。
2. [`harness-compilation.md`](harness-compilation.md)：消费 Adoption Baseline 与已发布 Semantic IR，按 `Environment Discover → Harness Adapt → Verify & Accept` 将稳定语义适配为目标 Runtime 的最小充分 Harness。

规范侧在版本发布时先执行 [`Semantic Compilation`](../governance/semantic-compilation.md)：Canonical Workflow / Rules / Exception Workflow / Meta Protocol 被一次性编译为 Semantic IR。目标项目不再重新从完整 prose 中发现规范语义。

```text
Canonical Corpus
      ↓
Semantic Compile（发布侧）
      ↓
Semantic IR

Target / Intent
      ↓
Project Onboarding（按需）
      ↓
Adoption Baseline
      ↓
Environment Discover
      ↓
Harness Adapt
      ↓
Verify & Accept
      ↓
Harness Ready
      ↓
Enter / Resume Workflow
```

职责边界：

- Workflow：怎么推进；
- Rules：什么必须持续成立；
- Project Onboarding：当前 Target 如何使用 Spec Coding；
- Semantic Compilation：规范语义如何无损进入稳定 IR；
- Environment Discover：当前 Runtime / Project / Existing Harness 实际提供什么，以及去哪里按需寻找 Provider；
- Harness Adapt：如何为 Clause 选择可靠 Provider 并生成内容绑定的最小 Harness Candidate；
- Verify & Accept：如何证明 Candidate 被真实 Runtime 接管，并由 Independent Fresh Agent 验收行为。

确定性支持工具：

```text
tools/semantic_compiler/
tools/environment_discovery/
tools/harness_adapt/
tools/harness_acceptance/
```

`Harness Verify & Accept` 属于 Meta Protocol 编译验收，不等于 Main Workflow Stage 6 Verification Convergence：前者验证 Harness，后者验证 Requirement / Change Set。

[`../reference/harness-primitives.md`](../reference/harness-primitives.md) 与 [`../reference/coding-agent-runtimes.md`](../reference/coding-agent-runtimes.md) 继续作为非规范 Reference，只提供共同语言、架构不变量与官方事实入口；Current Environment Evidence 始终优先。

Adoption Baseline、Semantic IR、Environment Model、Adaptation Plan、Harness Candidate 与 Acceptance Evidence 各自承担不同生命周期，不互相复制为平行事实源。
