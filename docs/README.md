# Spec Coding 文档索引

本目录按 Spec Coding 主流程阶段组织当前正式文档。

当前 Canonical Corpus（规范文档集）的机器可读定义见 [`manifest.yaml`](manifest.yaml)。该 Manifest 是判断“哪些阶段文档属于当前版本”的唯一清单；本文件只负责导航和解释。

## 流程

```text
新项目：项目定义建立 ─┐
                    ├→ 需求澄清 → 技术方案设计 → 实施规划 → 开发实施 → 验证收敛 → 流程复盘改进
存量项目：项目认知建立 ─┘
```

## 目录

- `01a-project-definition/`：新项目入口——项目定义建立
- `01b-project-understanding/`：存量项目入口——项目认知建立
- `02-requirement-clarification/`：需求澄清
- `03-technical-design/`：技术方案设计
- `04-implementation-planning/`：实施规划
- `05-development-execution/`：开发实施
- `06-verification-convergence/`：验证收敛
- `07-process-review-improvement/`：流程复盘改进

两种入口在需求澄清阶段汇合；流程复盘改进针对可复用 SDD / Harness（执行框架）规则本身。

## Canonical 规则

- 当前版本共有 34 份正式阶段文档；单次真实流程只消费其中一条入口分支，因此通常执行 30 份阶段规则。
- `README.md`、`manifest.yaml`、`CHANGELOG.md` 等属于治理或导航文件，不计入正式阶段文档数量。
- 正式文件的新增、删除和重命名必须同步更新 `manifest.yaml`。
- 历史版本由 Git 保存，不在 `docs/` 中保留带 `(1)`、`(2)`、`v1`、`old` 等后缀的并行正式副本。

## Open Item Contract｜开放项契约

Open Item（开放项）表示**尚未解决、且需要后续阶段继续承接的具体问题或决策**。它不是新的独立阶段，也不要求单独维护一份全局文件；可以继续存在于当前阶段产物中，但跨阶段追踪时必须保持稳定身份。

最小字段：

| 字段 | 说明 |
|---|---|
| `id` | 稳定唯一标识，使用 `OI-xxx`；首次需要跨阶段跟踪时分配，后续不重新编号。 |
| `origin` | 最初发现该问题的阶段、产物或可追溯来源。 |
| `description` | 当前仍待解决的问题或决策。 |
| `status` | `open` / `resolved` / `deferred`。 |
| `blocking` | 是否阻塞当前准入或后续推进，`true` / `false`。 |
| `owner_stage` | 当前应负责继续处理或完成决策的阶段。 |
| `related` | 相关 Requirement、AC、Design、Task、Finding、Evidence 等引用；无则省略。 |
| `resolution` | `resolved` 时记录最终结论及必要证据；其他状态省略。 |

生命周期遵循：

```text
首次发现
  ↓
OI-xxx / open
  ↓
跨阶段引用同一 ID
  ├─→ resolved
  └─→ deferred
```

- **Reference over Duplication｜引用优先**：下游引用并更新同一个 `OI-xxx`，不复制成新的开放项。
- `blocking = true` 时，不得绕过对应 Gate（门禁）继续推进；解除阻塞后再更新状态或阻塞标记。
- `deferred` 必须保留延期理由与后续承接阶段，不能作为静默丢弃。
- Risk（风险）表示可能发生的不利影响；Finding（验证发现）表示验证中观察到的事实。二者都不自动等同于 Open Item。只有确实存在尚待后续决策或处理的问题时，才创建或关联 `OI-xxx`。
- Open Item 的含义发生实质变化时，应新建 `OI-xxx` 并保留关联，而不是复用旧 ID 表达另一个问题。

## Human / Agent Authority Contract｜人机决策权限契约

Human / Agent Authority（人机决策权限）按**动作是否改变已确认事实源，以及错误决策的影响程度**划分，而不是按阶段固定角色。目标是在保留必要人工控制的同时，避免低风险动作处处等待确认。

| 权限 | 适用边界 | 典型行为 |
|---|---|---|
| `Autonomous`（Agent 自主） | 不改变已确认 Requirement / AC / Design 等语义契约，动作可回退、可验证且处于既定边界内 | 搜索与读取、证据收集、分析、候选方案生成、Task 编排、契约内实现与修复、确定性验证、按既定规则路由 |
| `Confirm`（Agent 提议 + Human 确认） | Agent 可基于证据形成推荐，但决策会产生明显技术、架构、兼容、数据、安全、运维或长期维护影响 | 重大技术取舍、架构边界变化、数据迁移策略、难回滚方案、可复用 SDD / Harness 语义规则调整 |
| `Human Decision`（Human 决策） | 决策直接定义业务意图、正确性标准或风险接受边界 | Requirement 语义、In / Out Scope、核心 Business Rule、Acceptance Criteria 的新增或语义变化、Accepted Deviation（接受偏差）、豁免强制 Gate 或其他明确风险接受 |

升级原则：

```text
既定契约内 + 可验证 + 可回退
        ↓
Autonomous

存在多个合理方案 + 影响显著
        ↓
Confirm

改变业务意图 / 正确性标准 / 风险接受
        ↓
Human Decision
```

- **Evidence before Escalation｜先取证，再升级**：Agent 应先通过代码、文档、运行结果与已有决策缩小问题，再请求必要确认，不把“存在不确定性”直接等同于“询问 Human”。
- Human 已明确确认的规则、策略或约束成为后续执行边界；Agent 在该边界内不重复请求确认。
- Agent 不得通过“技术实现选择”隐式修改 Requirement、AC、已固定 Design Decision 或已明确风险边界。
- `Confirm` 与 `Human Decision` 只约束语义和治理决策；具体工具、仓库或平台的写入授权仍遵循各自权限规则。
- 无法明确判断权限等级时，优先看“该决定失败后是否只需局部返工，还是会改变业务正确性 / 产生难逆影响”；后者应升级。
