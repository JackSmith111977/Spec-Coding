# Harness Compilation Protocol｜Harness 编译协议

本协议属于 Meta Protocol（元协议），定义如何将 Spec Coding 的 Applicable Workflow（适用流程）、Rules（规则）与当前有效 Adoption Baseline（接入基线）稳定转换为目标项目可执行的最小 Harness（执行框架）。Workflow 包括当前适用的 Main Workflow（主流程）以及由实际异常触发的 Exception Workflow（异常流程）。

Harness Compilation 不是项目接入协议。若当前 Target 不存在有效 Adoption Baseline，或 Baseline 已发生冲突 / 失效，应先执行 [`Project Onboarding Protocol`](project-onboarding.md)，不得在 Harness 编译阶段自行猜测接入范围、共享方式、Artifact Publication 或 Authority。

对使用者仍可保持单一意图入口，例如：

```text
按照 Spec Coding 接入当前项目并继续开发。
```

Agent 内部按需执行：

```text
Project Onboarding（若需要）
        ↓
Adoption Baseline
        ↓
Harness Compilation
        ↓
Harness Ready
        ↓
Enter / Resume Workflow
```

读取、推导、组合与验证由 Agent 内部完成，不要求 Human 手工执行额外转换步骤。

---

## 1. 核心原则

- **Adoption before Compilation｜先接入，再编译**：Harness 编译只消费已收敛的 Adoption Context；接入意图未解决时先回到 Project Onboarding。
- **Local First｜本地优先**：优先取得 Spec Coding 规范仓库与目标项目仓库 / Workspace 的一致视图；已有本地工作区时同步并确认基线，不重复拉取。远程接口主要用于获取、同步、版本确认与必要补充。
- **Process as Cognition｜流程用于认知**：流程规定 Agent 如何理解、判断和推进，不强制把中间认知全部结构化。
- **Artifact as Contract｜产物用于对齐**：只对需要稳定交接与验证的结果明确约束，减少重复对齐成本。
- **Reuse before Add｜复用优先**：优先复用 Agent 原生能力、项目已有工具与既有 Harness，仅补齐真实缺口。
- **Minimum Sufficient Harness｜最小充分 Harness**：以最低复杂度可靠满足当前流程、规则与 Adoption 约束，避免重复包装与过度设计。
- **Constraint Preservation｜约束保持**：Harness 不得弱化原流程、规则或 Adoption Baseline 语义，也不应无依据增强约束。
- **Deterministic First｜确定性优先**：可由脚本、测试、Hook、Gate 等确定性机制保障的要求，不依赖模型自觉记忆。

---

## 2. 输入模型

Harness Compilation 同时消费三类上下文：

```text
Normative Context
= Applicable Workflow + Applicable Rules

Adoption Context
= Adoption Baseline + Final Workflow Route

Execution Context
= Current Target Environment + Existing Harness + Agent Capability
```

职责边界：

- Workflow / Rules 定义“必须做什么、什么必须持续成立”；
- Adoption Baseline 定义“Spec Coding 在这个 Target 中如何使用、共享和受约束”；
- Current Target Environment 提供当前工具、CI、配置、Agent 能力等动态事实；
- Harness Compilation 只负责把三者转换为最小充分执行机制。

Adoption Baseline 中不应复制技术栈、CI 命令或 Harness 组件清单；这些动态事实继续在本协议中按需发现。

---

## 3. 转换流程

```text
Read
  ↓
Derive
  ↓
Compose
  ↓
Verify
  ↓
Harness Ready
```

### 3.1 Read｜基线接管与认知建立

先确认当前 Target 的 Adoption Baseline 有效，并取得 Spec Coding 规范仓库、Spec Workspace 与目标项目的可用一致视图。

若出现以下情况，停止编译并回到 Project Onboarding：

- 没有与当前 Target 匹配的 Adoption Baseline；
- Target Identity / Scope 无法稳定解析；
- Collaboration / Publication / Authority 等关键 Adoption Fact 冲突或缺失；
- Relevant Delta 已使当前 Baseline 失效。

Baseline 有效后，以本地确定性搜索和文件读取为主，建立生成 Harness 所需的最小完整认知，重点识别：

- 当前有效的 `VERSION`、`manifest.yaml`、Applicable Rules 与 Final Workflow Route 对应的 Main Workflow 文档；
- `manifest.yaml` 中已登记的 Exception Workflow，以及当前 Failure / Finding 是否触发其中某一流程；
- Adoption Baseline 中与 Harness 直接相关的 Target Scope、Spec Workspace、Publication Boundary、Repository / Authority Constraint 与 Integration Constraint；
- 当前任务需要的关键上游引用；
- Gate、Verification、Traceability、Human / Agent Authority、Human-Agent Collaboration、Code Quality 等持续约束；
- 目标项目已有 Harness、规则、工具、脚本、CI 与 Agent 原生能力。

Applicable Rules 以 `manifest.yaml` 中的 `rule_documents` 为机器可读入口；其中 Human-Agent Collaboration 在需要 Human Interaction 的正式 Workflow / Meta Protocol 中适用，其他专项规则按其 `applies_to` 加载。Exception Workflow 以 `exception_workflows` 为机器可读入口，仅在 Trigger 成立时加载对应正式文档，不要求常驻全部异常流程。

```text
Applicable Workflow
=
Current Main Workflow
+
Triggered Exception Workflow（若有）
```

**完成条件**

Agent 已能明确判断：当前 Harness 必须保障哪些 Workflow / Rules / Adoption 约束、是否存在已触发的 Exception Workflow，以及哪些要求已经被现有环境可靠覆盖。

---

### 3.2 Derive｜Harness 需求推导

对照 Applicable Workflow / Rules / Adoption Baseline 与现有能力，识别真正需要 Harness 补齐的缺口。

重点关注：

- MUST / MUST NOT；
- Gate 与 Blocking Condition；
- Verification；
- Human / Agent Authority；
- Cognitive Sync / Decision Readiness 等 Human-Agent Collaboration 要求；
- Traceability；
- Artifact Publication / Spec Workspace / Repository Constraint；
- 持续适用的质量与执行规则；
- 明确的上下文与执行约束。

优先判断现有能力是否已经可靠覆盖，避免将流程章节、规则条目或 Adoption 字段机械映射成 Skill、Agent 或其他 Harness 组件。尤其不应把 Human-Agent Collaboration 机械转换为每阶段人工审批；只有真实 Sync Trigger 或 Authority Boundary 成立时才需要 Human Interaction。

同时区分：

- **Capability Gap｜能力缺口**：当前 Agent 或项目环境缺少完成要求所需的能力；
- **Reliability Gap｜可靠性缺口**：能力已经存在，但无法稳定保证要求被执行。

根据要求强度选择保障级别：

```text
指导性要求
→ Rule / Skill

需要稳定执行
→ Workflow / Checklist / Verifier

不可绕过
→ Script / Hook / Permission / Gate
```

**完成条件**

每一个待新增 Harness 都能回答：

1. 它对应什么真实 Workflow、Rule 或 Adoption 要求？
2. 当前能力为什么不能可靠覆盖？
3. 如果不补充，是否会影响流程正确性、接入边界、代码质量或可靠性？

---

### 3.3 Compose｜Harness 组合生成

将已确认的缺口转换为最小可用 Harness。

组合顺序遵循：

```text
Reuse
  ↓
Compose
  ↓
Create
```

优先级依次为：

1. 复用已有 Harness；
2. 复用 Agent 原生能力；
3. 复用项目已有工具、脚本与 CI；
4. 组合已有能力；
5. 仅在确有缺口时新增 Harness。

组件按问题性质选择，而不是按流程章节、规则文件或 Adoption 字段创建：

| 需求性质 | 常见 Harness 机制 |
|---|---|
| 持续遵守的原则 | Rule / Instruction |
| 可复用的复杂方法 | Skill |
| 外部执行能力 | Tool / MCP |
| 独立上下文或角色隔离 | Subagent |
| 确定性检查 | Script / Hook / CI |
| 不可绕过的流程边界 | Gate / Permission |
| 固定多步协调逻辑 | Workflow |

Harness 的共享 / 放置方式不得越过 Adoption Baseline 的 Integration / Publication Boundary。Local Adoption 不应无依据把个人 Harness 写入目标 Repository；Repository-native Adoption 则应遵守适用项目约定。

Human-Agent Collaboration 可按项目能力映射为轻量 Summary、Decision Packet、Checkpoint、UI 提示或共享状态，但不得要求 Human 持续跟踪 Agent 全部 Working Context，也不得无依据增加强制 Gate。

生成完成后执行一次 Simplify Pass（简化检查），删除重复、无必要或可由现有能力替代的组件。

**产物**

必要时可形成轻量 **Harness Plan**，仅说明：

- `Reuse`：复用了什么；
- `Add`：新增了什么；
- `Reason`：为什么需要。

Harness Plan 默认不是长期事实源，只有在确需跨 Agent / 跨会话解释转换决策时才持久化。

---

### 3.4 Verify｜转换验证与收敛

验证重点不是“配置是否能加载”，而是生成的 Harness 是否忠实承载了当前 Spec Coding + Adoption Context。

#### Coverage｜覆盖完整

关键 Workflow、Rules 与 Adoption 约束均得到可靠保障，尤其是 MUST / MUST NOT、Gate、Verification、Human / Agent Authority、必要 Cognitive Sync / Decision Readiness、Blocking Condition、Traceability、Publication / Repository Boundary 与适用质量规则；存在已触发 Exception Workflow 时，其必要语义同样必须被覆盖。

不要求每条规则或异常流程步骤都生成独立文件，只要求其语义被可靠满足。

#### Fidelity｜语义忠实

不得发生约束弱化或无依据增强，例如：

```text
MUST      → SHOULD
MUST NOT  → “注意避免”
Human Decision → Agent 自主决定
Trigger-driven Sync → 每阶段强制 Human Review
不可绕过 Gate → 可跳过 Checklist
Local Publication Boundary → 自动写入目标 Repository
```

#### Minimality｜最小充分

逐项反查新增组件：

- 为什么存在？
- 对应哪个真实 Workflow / Rule / Adoption Gap？
- 删除后是否降低流程或规则执行可靠性？

删除后无实质影响的组件应移除。

#### Executability｜实际可用

确认：

- 文件与引用路径正确；
- Skill / Rule 可被 Agent 发现；
- Tool / Hook / Script 实际存在且可执行；
- 配置语法有效；
- 依赖与权限满足运行条件；
- Harness 放置与共享方式符合 Adoption Baseline。

**失败处理**

```text
Verify Fail
    ↓
定位最早失真点
    ├─ Adoption Fact 失效 → Project Onboarding
    └─ Read / Derive / Compose 失真 → 对应步骤修正
    ↓
重新 Verify
```

避免在下游通过临时补丁掩盖上游接入、理解或推导错误。

**完成条件**

```text
Coverage      Pass
Fidelity      Pass
Minimality    Pass
Executability Pass

Result        Ready
```

---

## 4. 最终约束

Harness 编译不要求将 Spec Coding 完全形式化，也不要求引入复杂 DSL、IR 或额外人工步骤。

Agent 可以在内部自由完成理解与推理，但最终结果必须满足：

> **基于有效 Adoption Baseline，完整承载当前 Applicable Workflow 与 Rules，只补真实缺口，并以最低复杂度形成可执行、可验证的 Harness；需要 Human 判断时保持 Decision Readiness，不需要 Human 时保持契约内自治。**
