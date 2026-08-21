# Spec Coding

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）流程与规则文档仓库。

本仓库维护 Spec Coding 的 Canonical Documentation（规范文档集），并使用 Git 进行版本治理。

## 当前状态

- 当前版本：见 [`VERSION`](VERSION)。
- 当前状态：见 [`docs/manifest.yaml`](docs/manifest.yaml) 中的 `status`。
- `main` 是当前 Canonical Source of Truth（规范事实源）；未合入 `main` 的分支内容仅代表候选变更。
- 当前 Canonical Corpus（规范文档集）由 [`docs/manifest.yaml`](docs/manifest.yaml) 唯一定义。
- 当前共有 34 份正式阶段文档；治理、导航和术语文件不计入该数量。

`0.x` 表示体系仍处于审核、场景验证与 Pilot（试运行）阶段；达到稳定发布门槛后再进入 `1.0.0`。

## 流程

```text
新项目：项目定义建立 ─┐
                    ├→ 需求澄清 → 技术方案设计 → 实施规划 → 开发实施 → 验证收敛 → 流程复盘改进
存量项目：项目认知建立 ─┘
```

## 文档入口

- [`docs/README.md`](docs/README.md)：面向 Human / Agent 的流程导航与全局执行契约。
- [`docs/manifest.yaml`](docs/manifest.yaml)：机器可读的正式文档清单、版本与阶段结构。
- [`docs/glossary.md`](docs/glossary.md)：Canonical Terminology（规范术语）与统一中文解释。
- [`CHANGELOG.md`](CHANGELOG.md)：版本级语义变化记录。
- [`VERSION`](VERSION)：当前规范版本号。

## 仓库维护规则

1. **Canonical Only｜只维护一个当前正式版本**：`main` 上每份正式文档只保留一个当前路径，不使用 `foo-v1.md`、`foo-v2.md`、`old`、`backup` 等并行副本保存历史。
2. **Branch First｜先分支后修改**：功能、修复、审核与规则演进应从 `main` 创建独立分支，在分支完成后再合入 `main`。
3. **Affected Trace Only｜只改受影响链路**：规则调整只修改真实受影响的定义点、消费者和治理文件，不顺手重写无关阶段。
4. **Manifest 同步**：新增、删除、移动或重命名正式阶段文档时，必须在同一变更中更新 `docs/manifest.yaml`；正式文档数量变化也同步维护。
5. **Glossary 同步**：新增核心英文术语、修改规范译法或改变术语语义时，必须更新 `docs/glossary.md` 并检查关键定义点。
6. **Global Contract 同步**：影响全部阶段的通用规则优先维护在 `docs/README.md`，避免复制到 34 份阶段文档形成重复事实源。
7. **Changelog 同步**：会改变流程语义、Artifact Contract（产物契约）、状态、Gate（门禁）、Authority（决策权限）或下游消费方式的变更必须进入 `CHANGELOG.md`。
8. **Git Owns History｜历史交给 Git**：删除内容、旧版本和重命名关系通过 Commit / PR / Changelog 保留，不在当前文档目录继续维护废弃副本。
9. **No Silent Semantic Change｜禁止静默语义变化**：纯措辞优化不得顺带改变 Requirement、Design、Task、Verification 等契约；如确需改变，按版本级语义变更处理。

## 版本管理

版本遵循 Semantic Versioning（语义化版本）：

| 类型 | 适用情况 |
|---|---|
| `MAJOR` | 进入稳定版本后，对核心阶段、Artifact Contract、状态模型、Gate 或消费者行为产生不兼容变化。 |
| `MINOR` | 新增或增强兼容能力、规则、治理、验证或自动化机制；`0.x` 阶段的主要语义演进通常使用 MINOR。 |
| `PATCH` | 不改变流程语义的拼写、链接、格式、说明或纯文档修复。 |

版本治理遵循以下规则：

- 普通分支提交不必每次修改 `VERSION`；版本号在一次版本级收敛时统一更新。
- 未发布的版本级变化先记录在 `CHANGELOG.md` 的 `Unreleased`。
- 形成版本时，应在同一收敛变更中同步更新：
  - `VERSION`
  - `docs/manifest.yaml` 的 `spec_coding_version` 与 `status`
  - `CHANGELOG.md`
- 若该版本同时改变正式文档集合、术语或全局 Contract，还应同步更新 `manifest.yaml`、`glossary.md` 或 `docs/README.md`。
- Git Tag 可用于稳定里程碑或需要长期引用的版本快照，但 Tag 不替代 `VERSION + manifest + CHANGELOG` 的 Canonical 判定。

## 标准变更流程

```text
main
  ↓
独立分支
  ↓
修改受影响规则 / 文档
  ↓
Cross-Artifact Check（跨产物一致性检查）
  ↓
同步 Manifest / Glossary / Changelog / VERSION（按需）
  ↓
Review / Verification
  ↓
Merge to main
  ↓
main 成为新的 Canonical Source of Truth
```

合入前至少确认：

- 上下游术语、状态和 Artifact Contract 一致。
- 没有引入并行事实源或废弃副本。
- 受影响 Trace 可追溯。
- 新规则没有静默削弱 Verification、Evidence、Gate 或 Human / Agent Authority。

## Agent 消费顺序

Agent 不应通过搜索结果自行猜测“最新版”，推荐按以下顺序读取：

```text
VERSION
  ↓
docs/manifest.yaml
  ↓
docs/README.md
  ↓
docs/glossary.md
  ↓
当前阶段文档 + 必要上游引用
```

## 1.0 稳定发布门槛

进入 `1.0.0` 前，至少应完成：

- 静态审核中的 P0 / P1 问题清零，核心 Artifact / State / Terminology 契约一致。
- 典型 Scenario Stress Test（场景压力测试）。
- Fresh-Agent Blind Run（新 Agent 盲跑），验证规则在无历史会话上下文时仍可被正确消费。
- 2–3 个真实项目 Pilot，未出现重大 Trace 逃逸、静默假设或无法解释的人工救场。

在达到以上门槛前，`main` 仍是当前规范事实源，但版本状态保持 `0.x / candidate`。