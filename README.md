# Spec Coding

Spec Coding / SDD（Specification-Driven Development，规格驱动开发）流程与规则文档仓库。

本仓库维护 Spec Coding 的 Canonical Documentation（规范文档集），并使用 Git 进行版本治理。

## 当前版本

当前规范版本见 [`VERSION`](VERSION)。

当前唯一正式文档集合由 [`docs/manifest.yaml`](docs/manifest.yaml) 定义；未列入 Manifest（清单）的文档不属于当前 Canonical Corpus（规范文档集）。

## 文档入口

- [`docs/README.md`](docs/README.md)：面向 Human / Agent 的流程导航与全局执行契约。
- [`docs/manifest.yaml`](docs/manifest.yaml)：机器可读的正式文档清单与阶段结构。
- [`docs/glossary.md`](docs/glossary.md)：Canonical Terminology（规范术语）与统一中文解释。
- [`CHANGELOG.md`](CHANGELOG.md)：版本级语义变化记录。

## 版本治理原则

1. `main` 作为当前稳定 Canonical Source of Truth（规范事实源）。
2. 功能、修复与审核改动在独立分支完成，再进入稳定版本。
3. 当前正式文档只保留一个文件路径，不通过 `foo-v1.md`、`foo-v2.md` 等副本保存历史。
4. 历史版本、删除内容与重命名关系由 Git Commit / Tag / Changelog 保存。
5. 新增、删除或重命名正式阶段文档时，必须在同一变更中同步更新 `docs/manifest.yaml`。
6. Agent 消费规则时应优先读取 `VERSION` 与 `docs/manifest.yaml`，不得通过搜索结果自行猜测“最新版”。
7. 核心英文术语及中文解释以 `docs/glossary.md` 为准；术语变化若改变流程语义，应按语义变更治理。

> `0.x` 表示该体系仍处于审核、场景验证与 Pilot（试运行）阶段；达到稳定发布门槛后再进入 `1.0.0`。
