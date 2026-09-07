# Spec Coding

**让 Coding Agent 按一套清晰的流程，把你的想法推进到有验证依据的交付。**

Spec Coding 提供开发流程与规则的发行包（Harness）。你在自己的项目中给 Agent 一条接入指令，它就从包内入口开始，结合当前项目和工具完成适配，再按任务需要推进需求、方案、实现与验证。

[当前正式版本：0.12.0](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.12.0) · [下载完整包](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.12.0/spec-coding-harness-0.12.0.zip) · [查看完整流程](docs/overview.md)

## 快速开始

### 1. 在 Coding Agent 中打开你的项目

可以是已有代码仓库，也可以是准备开始的新项目目录。Agent 需要能读取发行包和项目文件，并执行当前任务所需的命令。

### 2. 复制这段指令，把最后一行换成你的目标

```text
请在当前项目中接入 Spec Coding。
使用固定发行：https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.12.0
获取完整 Harness 包和包外验证依据，核验发行身份与完整性。
从包内 bootstrap/BOOTSTRAP.md 开始，按当前 Agent 和项目环境完成接入、适配与验收，然后继续下面的任务。

我的目标：为现有列表增加按来源筛选的能力，并验证旧数据仍能正常使用。
```

首次接入时，Agent 会了解你的使用意图、项目现状和可用工具，建立项目内的流程入口。需要你决定需求边界、方案取舍或操作权限时，它会说明依据和待决定事项。

接入完成后，直接告诉它下一项任务即可，例如“继续上次未完成的任务”或“排查这次测试失败”。已有绑定与有效证据会被复用，环境变化时重新核验受影响部分。

<details>
<summary>Agent 无法自行下载？手动提供发行包</summary>

从[0.12.0 发行页](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.12.0)下载以下附件，放到 Agent 能读取的位置：

- `spec-coding-harness-0.12.0.zip`：完整流程与规则包。
- `spec-coding-harness-0.12.0-verification.zip`：发行身份和包外验证报告。
- `SHA256SUMS`：附件校验清单。

保留下载的 ZIP，并解压前两个文件。完整包解压后，入口为 `harness/bootstrap/BOOTSTRAP.md`。把下面的路径和任务替换为实际内容，再交给 Agent：

```text
请使用我提供的 Spec Coding 0.12.0 完整包、验证报告和 SHA256SUMS，核验固定发行身份与完整性。
入口文件：<解压目录的绝对路径>/harness/bootstrap/BOOTSTRAP.md
从这个入口接入当前项目，按当前 Agent 和项目环境完成适配与验收，然后继续任务。

我的目标：<描述你要完成的事情>
```

保持包的完整目录结构，流程正文会引用共享规则和支持文件。无需先手动安装每个 Skill，Agent 可以直接读取 Bootstrap 开始接入。

</details>

## 接入后，怎么交给它任务？

用自然语言描述目标，并提供你已有的代码、文档或错误信息。

| 场景 | 可以这样说 |
|---|---|
| 开始新项目 | 我想做一个个人阅读清单工具，先帮我明确第一版范围，再推进实现。 |
| 修改已有项目 | 给现有列表增加来源筛选，保持旧数据兼容，完成后说明验证结果。 |
| 排查故障 | 这条测试失败了，请定位原因、修复并重验原失败场景：…… |
| 继续已有工作 | 继续上次未完成的任务，先核对当前状态和未解决事项。 |

## Agent 会怎样推进？

```text
理解项目与目标 → 澄清需求 → 设计方案 → 拆分任务 → 开发实施 → 验证交付
```

Agent 根据新项目、存量项目或已有状态选择入口，并按任务风险和现有证据调整执行深度。执行中会：

- 把需求、方案、任务、代码变化和验证结果关联起来，方便你复核，也方便下一次接管。
- 在已授权范围内推进实现，用实际测试和检查结果判断是否完成。
- 遇到失败、未解决的阻塞项或权限缺口时，保留事实并回到对应环节处理。
- 在需要时复盘流程，根据实际问题决定是否改进。

你主要参与目标、取舍和权限决策；交付时可以沿着记录检查“做了什么、为什么这样做、怎样验证”。

## 适用范围

当前正式发行包含 **11个 Skills、4类共享规则，以及接入入口、流程路由、能力要求和完整性工具**。稳定流程已经预编译，目标 Agent 从发行包按需读取，并适配当前环境。

0.12.0 已完成结构、独立语义和行为验证；实测范围为 Windows 下的 Codex 基础工具与独立 CLI 配置，确认 Python 3.13.7 可运行包内校验器。其他 Agent 或环境需要实际接入验收，格式兼容本身不代表已经验证可用。完整范围与限制见[发行记录](verification/harness/publication.md)。

## 了解设计或参与维护

| 我想…… | 从这里开始 |
|---|---|
| 理解完整开发流程 | [流程概要](docs/overview.md) |
| 查看当前发行身份、校验方式和证据 | [发行记录](verification/harness/publication.md) |
| 查看接入程序具体做什么 | [包内 Bootstrap](packages/harness/bootstrap/BOOTSTRAP.md) |
| 阅读流程与协作规则 | [Workflow](docs/workflows/README.md) · [Rules](docs/rules/README.md) |
| 查看规范来源与登记 | [文档入口](docs/README.md) · [Manifest](docs/manifest.yaml) |
| 修改规范、构建或发布 Harness | [仓库维护规则](docs/governance/repository-governance.md) · [构建与发布流程](docs/governance/harness-build-and-release.md) |
| 了解版本变化 | [CHANGELOG](CHANGELOG.md) |

维护者负责将规范构建、验证并发布为固定版本的 Harness；使用方从正式发行包接入，在自己的项目中完成环境适配和验收。

## 许可

除非另有说明，本仓库的文档、规范、图示及其他非软件内容采用 [Creative Commons Attribution 4.0 International](LICENSE)（CC BY 4.0）许可。
