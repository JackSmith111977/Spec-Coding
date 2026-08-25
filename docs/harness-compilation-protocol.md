# Harness Compilation Protocol｜Harness 编译协议

本协议定义如何将 Spec Coding 流程稳定转换为当前项目可执行的最小 Harness（执行框架）。

对使用者保持单一入口，例如：

```text
Build Harness
```

读取、推导、组合与验证由 Agent 内部完成，不要求 Human 手工执行额外转换步骤。

---

## 1. 核心原则

- **Local First｜本地优先**：优先取得 Spec Coding 规范仓库与目标项目仓库的本地一致视图；已有本地工作区时同步并确认基线，不重复拉取。远程接口主要用于获取、同步、版本确认与必要补充。
- **Process as Cognition｜流程用于认知**：流程规定 Agent 如何理解、判断和推进，不强制把中间认知全部结构化。
- **Artifact as Contract｜产物用于对齐**：只对需要稳定交接与验证的结果明确约束，减少重复对齐成本。
- **Reuse before Add｜复用优先**：优先复用 Agent 原生能力、项目已有工具与既有 Harness，仅补齐真实缺口。
- **Minimum Sufficient Harness｜最小充分 Harness**：以最低复杂度可靠满足当前流程要求，避免重复包装与过度设计。
- **Constraint Preservation｜约束保持**：Harness 不得弱化原流程语义，也不应无依据增强约束。
- **Deterministic First｜确定性优先**：可由脚本、测试、Hook、Gate 等确定性机制保障的要求，不依赖模型自觉记忆。

---

## 2. 转换流程

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

### 2.1 Read｜基线接管与认知建立

先取得 Spec Coding 规范仓库与目标项目仓库的本地一致视图，确认版本、分支 / Commit 与工作区状态。

随后以本地确定性搜索和文件读取为主，建立生成 Harness 所需的最小完整认知，重点识别：

- 当前有效的 `VERSION`、`manifest.yaml`、Global Contracts（全局契约）与适用阶段文档；
- 当前任务适用的异常流程与关键上游引用；
- Gate、Verification、Traceability、Human / Agent Authority 等流程不变量；
- 目标项目已有 Harness、工具、脚本、CI 与 Agent 原生能力。

**完成条件**

Agent 已能明确判断：当前 Harness 必须保障哪些流程要求，以及哪些要求已经被现有环境可靠覆盖。

---

### 2.2 Derive｜Harness 需求推导

对照流程要求与现有能力，识别真正需要 Harness 补齐的缺口。

重点关注：

- MUST / MUST NOT；
- Gate 与 Blocking Condition；
- Verification；
- Human / Agent Authority；
- Traceability；
- 明确的上下文与执行约束。

优先判断现有能力是否已经可靠覆盖，避免将流程章节机械映射成 Skill、Agent 或其他 Harness 组件。

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

1. 它对应什么真实流程要求？
2. 当前能力为什么不能可靠覆盖？
3. 如果不补充，是否会影响流程正确性或可靠性？

---

### 2.3 Compose｜Harness 组合生成

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

组件按问题性质选择，而不是按流程章节创建：

| 需求性质 | 常见 Harness 机制 |
|---|---|
| 持续遵守的原则 | Rule / Instruction |
| 可复用的复杂方法 | Skill |
| 外部执行能力 | Tool / MCP |
| 独立上下文或角色隔离 | Subagent |
| 确定性检查 | Script / Hook / CI |
| 不可绕过的流程边界 | Gate / Permission |
| 固定多步协调逻辑 | Workflow |

所选机制的执行强度不得低于原流程要求。生成完成后执行一次 Simplify Pass（简化检查），删除重复、无必要或可由现有能力替代的组件。

**产物**

必要时可形成轻量 **Harness Plan**，仅说明：

- `Reuse`：复用了什么；
- `Add`：新增了什么；
- `Reason`：为什么需要。

随后生成实际 Harness。Harness Plan 默认不是长期事实源，只有在确需跨 Agent / 跨会话解释转换决策时才持久化。

---

### 2.4 Verify｜转换验证与收敛

验证重点不是“配置是否能加载”，而是生成的 Harness 是否忠实承载了 Spec Coding。

#### Coverage｜覆盖完整

关键流程要求均得到可靠保障，尤其是 MUST / MUST NOT、Gate、Verification、Human / Agent Authority、Blocking Condition 与 Traceability。

不要求每条规则都生成独立文件，只要求其语义被可靠满足。

#### Fidelity｜语义忠实

不得发生约束弱化或无依据增强，例如：

```text
MUST      → SHOULD
MUST NOT  → “注意避免”
Human Decision → Agent 自主决定
不可绕过 Gate → 可跳过 Checklist
```

#### Minimality｜最小充分

逐项反查新增组件：

- 为什么存在？
- 对应哪个真实缺口？
- 删除后是否降低流程可靠性？

删除后无实质影响的组件应移除。

#### Executability｜实际可用

确认：

- 文件与引用路径正确；
- Skill / Rule 可被 Agent 发现；
- Tool / Hook / Script 实际存在且可执行；
- 配置语法有效；
- 依赖与权限满足运行条件。

**失败处理**

```text
Verify Fail
    ↓
定位最早失真点
    ↓
Read / Derive / Compose 修正
    ↓
重新 Verify
```

避免在下游通过临时补丁掩盖上游理解或推导错误。

**完成条件**

```text
Coverage      Pass
Fidelity      Pass
Minimality    Pass
Executability Pass

Result        Ready
```

---

## 3. 最终约束

Harness 编译不要求将 Spec Coding 完全形式化，也不要求引入复杂 DSL、IR 或额外人工步骤。

Agent 可以在内部自由完成理解与推理，但最终结果必须满足：

> **完整承载必要流程语义，只补真实缺口，并以最低复杂度形成可执行、可验证的 Harness。**
