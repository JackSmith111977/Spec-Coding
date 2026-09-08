# 0.13.0 R1 固定候选包共享部分独立语义审查

结论：**PASS**。指定共享部分未发现阻塞性 Finding，无必须先行修正的位置。本结论仅适用于下列固定包及审查范围，不是全包语义通过结论，不证明真实 Runtime 加载或行为试验通过，不构成发布许可。

## 固定身份与独立性

- 日期：2026-09-09。
- 固定 Canonical 源：`36b92f7257a8b69aeb2f93de8f90c40c66e3f402`。
- 候选目录：`[工作区]/packages/harness`。
- 指定及独立实测 `package_sha256`：`e4b84d88ab494b0503837674169bc0fb31814fcdb0a3c5ac7d9636a6f5ea6cd7`，一致。
- 实测 `manifest.json` 文件 SHA-256：`fc50a4361c714280b6c6f00c4c3bfb4c6602dda910dd64916dd642e4d913afa7`。
- 包 Manifest 声明版本 `0.13.0`、构建方式 `FULL`，source_revision 与固定源一致。审查开始及结束的 `git diff 36b92f7257a8b69aeb2f93de8f90c40c66e3f402 -- docs` 均无差异。
- 本轮重新直接读取当前 Canonical 原文与对应包完整文件，不以此前源码 PASS、设计文档、Builder 摘要或其他 Reviewer 结论代替判定；未读取设计或 Builder 报告。
- 哈希检查使用独立只读 PowerShell 实现，按包 README 定义对原始文件字节计算 SHA-256，再按包内 POSIX 路径的序数顺序拼接 `文件hash + 两个空格 + 路径 + LF` 并计算集合 Hash。核对全部 24 个文件、23 个 manifest.files 项及 22 个资产集合 Hash，无缺失、额外文件或 Hash 不符。未执行包内安装程序、验证脚本或构建工具。

## 阅读范围

完整对照五份 `docs/rules/` 正式规则与以下包文件：

- `rules/global.md`
- `rules/collaboration.md`
- `rules/delegation.md`
- `rules/artifacts.md`
- `rules/code-quality.md`

完整读取两份 `docs/meta-protocols/` Canonical 正文，对照：

- `skills/spec-project-onboarding/SKILL.md`
- `skills/spec-harness-adoption/SKILL.md`
- `skills/spec-harness-adoption/references/candidate-validation.md`

完整读取并核对组合入口：`bootstrap/BOOTSTRAP.md`、`bootstrap/routes.md`、`bootstrap/requirements.md`、`README.md`；另核对包 Manifest 和 plugin.json 的身份、依赖及作用域。为核实 README 的发行证据边界，定向读取当前 `docs/governance/harness-build-and-release.md` 的相关原文，未使用构建过程摘要。

其他 Main／Exception Skill 的内部流程语义由另一独立 Reviewer 负责，本报告只评价共享契约及路由接口，不对那些完整程序签发 PASS。对其文件计算 Hash 仅为固定全包身份。

## 逐项审查结果

| 项目 | 原文依据与包内位置 | 判断 |
|---|---|---|
| 五类规则完整性 | 五份 Canonical Rule；包 `rules/*.md` | PASS。逐份直接阅读并进行 no-index 差异核对。artifacts、collaboration 仅改包内链接；delegation 另将维护者构建链接改为客户端不执行的说明；global 将外置术语导航改为包内定义定位；code-quality 无正文差异。未删减 Authority、OI、裁剪、协作触发、单写入者、委派结果性质、能力路由或质量要求。 |
| 新产物规则 | Canonical 产物规则 §1–5；`rules/artifacts.md` §1–5 | PASS。默认布局、既有空间复用、跨空间身份／依赖、轻量权威章节、统一任务集及原 OI、共享唯一正文、来源修订、定向恢复、正文先于导航、并发及迁移恢复、原包身份与证据保留均完整进入包。implementation.md 仍非新增必需产物，未创建第二套状态。 |
| Meta 的必要 scope 限定 | Canonical 人机协作 §5；`rules/collaboration.md` §5；`bootstrap/routes.md:3`；`bootstrap/requirements.md:3`、`:10` | PASS。Manifest 中对 global 的依赖表示读取关系，包正文明确 Meta 只复用适用权限／协作／委派／产物约束，不继承 Workflow 特有 Task／Gate。能力表明确必需程度由适用条件决定；independent-review、scoped-execution、git-lifecycle 等不是无条件安装要求，未把枚举的能力全部升级为仅接入前置。 |
| 稳定接入与迁移 | Canonical Project Onboarding §1–3.4；`spec-project-onboarding/SKILL.md` 全文 | PASS。触发、先发现后询问、三种共享模式、三类持久信息及动态事实排除、provisional Target、相关变化处理、权限与用户修改保护、双向入口、只读写回缺口和受控候选移交均保持。目录变化不推定状态变化或 Harness 生效。 |
| 仅接入结束与继续分支 | Canonical 两 Meta 的入口／移交／结论；`BOOTSTRAP.md:6`、`:10`；`routes.md:9`；两 Meta Skill 的移交和结论；README 示例 | PASS。明确仅接入不要求业务目标、不造虚构 REQ 或空任务集，必要适配验收后汇报结束。有既有任务及继续意图时自动继续；Route 保留后续入口但不扩大本轮授权。候选测试只执行授权场景并按停止条件返回。 |
| 安装前入口与完整路由 | Canonical Harness 接入 §2–3；Bootstrap、routes、requirements、README | PASS。基础文件／网页读取可启动，不先依赖已安装 Skill／Plugin／Hook；入口无法访问有停止条件。相关动作之前使约束及异常触发有效；当前正文与依赖按需加载，未激活程序仍可达。包缺失语义返回维护者，不读浮动 Canonical 补洞或要求客户端重新预编译。 |
| 真实加载与行为验收契约 | Canonical Harness 接入 §4–6；`spec-harness-adoption/SKILL.md:22–56`；`BOOTSTRAP.md:9`；requirements | PASS。区分环境发现、装配、固定候选、原包语义回查、真实加载及行为验收；记录目录／文件存在／安装成功不能证明已加载。重载／新会话条件明确；验收预期不随适配改写，行为 Agent 不借未部署／未路由的知识补缺，语义评审与行为执行分离。 |
| 读写、索引失效与恢复 | Canonical 产物规则 §3–5；`rules/artifacts.md` 对应节；Harness Skill §4–5；requirements 的 artifact-navigation | PASS。摘要不取代权威状态，来源不符时不能用于状态判断；缺失、陈旧、冲突或无检索结果须回原文定向恢复。当前必需阻塞不能藏入日志；写回先正文／证据后直接入口。中断、跨需求共享、迁移及证据失效不改变原权威归属。 |
| 多范围 READY 与变化处理 | Canonical Harness 接入 §5.3、§6.3、§7；Harness Skill §3–5；产物规则 §5 | PASS。原包、候选及实际范围分离，多 Runtime／范围分别绑定证据；旧证据按相关变化失效，未激活未验能力不宣称 READY。缓存恢复核验同身份而非自动升级；回滚保护用户修改，不回滚业务事实或借旧 READY 掩盖兼容性。 |
| 候选例外与发行证明 | Canonical Harness 接入 §3.1、§6–8；candidate-validation 全文；README 身份部分 | PASS。包外授权只替换正式发行／发布通过证明前置，其他边界不放宽。测试配置和真实加载限授权范围，测试结果不自动发布、不迁移正式基线。README 要求固定身份及通过依据，明确 Hash、版本号或目录本身不构成发布证明；没有将当前候选自声明为正式发行。 |

## Finding 与修正位置

**阻塞 Finding：0。必要修正位置：无。**

已专门检查两处容易被误读的组合关系：

1. `manifest.requires` 是能力引用，实际必需条件来自 `bootstrap/requirements.md` 的条件列及当前流程契约；不能脱离该列解释为所有能力都必须启用。当前包已具备此限定，不构成新增强制规范。
2. Harness Skill 中 Fresh 导航验收提及任务／依赖，但同文件仅接入条款及完整产物规则已禁止制造虚构业务产物。空项目应按真实适用范围验证接入入口与记录，不能为满足导航场景强造任务；这一点仍须由后续真实场景验证，本文未执行或宣称其通过。

范围内 12 份 Markdown 的 60 个本地 Markdown 链接目标均存在。此检查仅证明静态目标可定位，不证明 Runtime 自动加载、相应程序执行正确或外部证据有效。

仅写入本报告，未修改 Canonical、包或工具。后续候选内容变化须重新固定 Hash 并审查受影响部分；本 PASS 不能转用于其他包身份，也不能替代另一 Reviewer 的流程语义审查、独立行为试验或真实目标侧验收。

## R1 补充边界核查与收口

本次补充仍审查上述 R1 原对象。再次直接计算全包 Hash 得到 `e4b84d88ab494b0503837674169bc0fb31814fcdb0a3c5ac7d9636a6f5ea6cd7`，与原身份一致；当前 docs 相对固定源仍无差异。未将未来 R2 内容混入此报告，未修改对象，也未扩展到 Oracle 计划。

### 1. 项目上下文 As-Is 与 01A 目标模型

直接依据：Canonical 产物规则及包 `rules/artifacts.md:5`、`:75`、`:76`、`:89`；Canonical `01a-project-definition/01-project-positioning.md` §1.4–1.5、`03-system-definition.md` §3.1–3.8；包 `spec-project-definition/SKILL.md` §1–4，并对照 01B 的 As-Is 表达。

第 89 行“项目长期上下文描述已确认的当前事实”不能单独解释为 project/ 只允许保存已实现行为。第 5 行明确由 Workflow 决定内容，第 75 行将 01A 的四类 Definition 放入 project/；01A 正文仍明确要求 Goals、预期业务模型、系统职责、System Flows 和可调整的 Design Assumption。01B 则承担实际项目的 As-Is 认知。因此，已确认目标／定义及尚未实施模型可以作为 01A 正式产物保存，但必须与“当前系统已如此运行”区分；不得因 As-Is 概括句删除目标模型，也不得凭定义通过声称代码已实现。

判断：**未发现包独有的语义弱化或阻塞遗漏**。存在一处非阻塞措辞风险：Canonical 与包第 89 行均采用较宽的“项目长期上下文”表述。若后续澄清，宜在 `docs/rules/artifact-organization-and-reading.md:89` 明确区分“描述现状的项目上下文”和“01A 已确认目标定义”，再派生包 `rules/artifacts.md:89`，不在包中自行修正规范。现有具体产物契约足以判定边界，本次不据此新增阻塞 Finding。

### 2. 仅接入结束后收到新需求

直接依据：Canonical Project Onboarding 第 50、201 行，Harness 接入第 74、159、207、211 行；包 `spec-project-onboarding/SKILL.md:14`、`:52`，Harness Skill §1、§4–5，`bootstrap/routes.md:5`、`:9–14`，以及包 01A／01B 入口和 02 解读与身份原文。

“仅接入后结束”限定当次接入请求，未形成永久禁止后续开发的状态。随后用户提出新的业务请求时，该请求建立当前工作意图：复用仍有效的接入基线和已验范围，按项目事实选择 01A、01B 或 02／有效 Owner；新增激活范围所需能力先补验。普通需求不会单独触发全量 Onboarding，也不要求事先存在 Formal Task／Txx 才能进入 01A 或 02——Formal Task 本来由后续规划形成。路线表保留了这些直接入口，没有把每次新需求都限定为恢复旧任务。

判断：**PASS，无阻塞 Finding**。若执行器把“有既有任务及继续意图”推广成所有未来业务请求的永久准入条件，属于错误消费；当前原文将其放在“正式接入通过后”的移交语境中，未作该推广。本次仅核对语义，未模拟新会话行为。

### 3. 只读场景的导航修复权限

直接依据：Canonical 与包产物规则第 7、121、133–137 行；Canonical Project Onboarding 第 193 行；包 `spec-project-onboarding/SKILL.md:52`、Harness Skill §3、`bootstrap/requirements.md:8`；原 Authority 契约。

“修复受影响导航，再继续依赖动作”是已授权写回／恢复的顺序约束，不是新增写权限。只读授权下可定向读取权威正文、确认实际来源并报告导航缺口；不得为了同步入口而修改任何只读对象，也不得宣称已保存修复。确实依赖持久修复的动作保持受阻，交回有权限的 Owner 或按已有权限规则处理；不依赖该修复且证据充分的只读工作仍可继续。只读文件系统能力与用户明确只读授权都不能被导航维护要求覆盖。

判断：**PASS，无阻塞 Finding**。权限先于动作、仅阻断受影响动作、只读可继续阅读及不得假称写回完成，均已有直接原文约束。可将“在写权限内修复”作为未来措辞澄清，但不是本次必须通过包补入的新权限机制。

### R1 最终结论及外部交接

**R1 本 Reviewer 的共享范围结论：PASS；本次新增阻塞 Finding：0。** 上述非阻塞措辞风险留在原身份报告中，不以潜在未来修正替代当前判断。

用户告知业务 Reviewer 已发现 05 Task Graph Update 必需字段被整体按需弱化，并将形成 R2。该项作为外部交接信息记录，不冒充本 Reviewer 已独立复核的 Finding；本报告的共享范围 PASS 不能覆盖、撤销或抵消该业务阻塞。不得以本报告宣称 R1 全包语义通过。

R1 审查至此落盘完成。R2 尚未由本 Reviewer 审查；后续应以其实际固定来源、包 Hash 和变更对象重新独立核查，不能复用 R1 身份签发 R2 结论。
