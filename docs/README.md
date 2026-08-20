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
