# Environment Discovery V3

Environment Discovery 是 Harness Compilation V3 的第二阶段工具层。它消费已发布 / Pilot Semantic IR 与有效 Adoption Context，建立后续 Harness Adapt 所需的当前环境事实。

它只回答：

> **当前 Runtime、Project 与 Existing Harness 实际提供什么，以及缺少能力时可以去哪里查找 Provider？**

它不回答“应该生成什么 Harness”。

## Flow

```text
Semantic IR + Adoption Context
        ↓
prepare
        ↓
Per-Clause Discovery Seed
        ↓
Agent derives environment questions
        ↓
Runtime / Project / Existing Harness evidence discovery
        ↓
Capability + Provider Surface normalization
        ↓
validate
        ↓
Environment Model
```

## `prepare`

```bash
python -m tools.environment_discovery prepare \
  --semantic-ir semantic/pilot/clauses.json \
  --adoption /path/to/adoption.json \
  --output /tmp/discovery-seed.json
```

`prepare` 不用关键词或硬编码规则猜测 Clause 需要什么 Runtime Capability。它为每条 Clause 生成不可跳过的 `derive_environment_dependencies` 工作项，并附加五类核心发现问题：

1. Runtime Identity；
2. Loader Surface；
3. Provider Surfaces；
4. Project Mechanisms；
5. Existing Harness。

Agent 随后将 Clause 工作项收敛成 `discovery-plan.schema.json`。每条 Clause 必须明确为：

- `discover`：需要一个或多个环境问题；
- `no_environment_dependency`：该 Clause 不依赖环境适配，并说明理由。

## Environment Model

Environment Model 只保存短生命周期当前事实：

```text
Observed Fact + Evidence
        ↓
Normalized Capability / Provider Surface / Existing Mechanism / Constraint
```

Capability Support：

- `native`
- `composable`
- `external`
- `unavailable`
- `unknown`

Provider Surface 表示后续出现真实 Capability Gap 时可以按需查询的来源，例如 Runtime Package、Plugin / Extension Registry、MCP Registry 或 Project Package Manager。

它只记录 `query_mechanism / install_mechanism / trust_scope / fact_refs` 与 `reachable / unavailable / unknown`，**不枚举整个市场内容**。

已确认事实必须有当前证据。任何非 `unknown` Capability，以及任何已解析 Provider Surface，都必须回指至少一个 `confirmed` Fact。

Environment Model 不允许表达 Harness 设计决策，例如：

- 应创建 AGENTS.md；
- 应创建 Skill；
- 应安装某个 Plugin；
- 应使用 Reviewer Subagent；
- 某 Clause 应标记为 HARNESS_REQUIRED。

这些属于下一阶段 Harness Adapt。

## `validate`

```bash
python -m tools.environment_discovery validate \
  --semantic-ir semantic/pilot/clauses.json \
  --adoption /path/to/adoption.json \
  --discovery /tmp/discovery.json \
  --environment /tmp/environment.json \
  --output /tmp/environment-validation.json
```

验证重点：

1. Semantic IR / Adoption fingerprint 一致；
2. 每条 Clause 恰好有一个 Discovery Disposition；
3. 五类核心问题均已处理；
4. `discover` Clause 能追溯到真实 Discovery Question；
5. Confirmed Question 能追溯到 Confirmed Fact；
6. Confirmed Fact 有 Evidence；
7. 已解析 Capability 有 Confirmed Fact 支撑；
8. 已解析 Provider Surface 有 Confirmed Fact 支撑；
9. Blocking Unknown 为零。

工具通过只表示 **Environment Handoff 足够可靠**，不表示 Harness 已经设计、生成或接管 Runtime。

## Evidence Priority

```text
Local executable / runtime metadata
        ↓
Local config / repository evidence
        ↓
Version-matched official documentation
        ↓
Official repository / release / registry
        ↓
External evidence
```

Reference 只帮助发现，不替代当前事实。
