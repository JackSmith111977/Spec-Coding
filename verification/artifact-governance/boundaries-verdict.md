# R2 边界与缓存独立行为判定

结论：F01 三子例的既有空间维护、concurrent 的有界并行采集及 Owner 消歧、F08 的文件缓存恢复均 **PASS（仅下述实际范围）**。F01/F08 的 Runtime 接管认证 **BLOCKED（缺加载及行为证据）**，不影响本次授权的文件维护结论。

判定日期：2026-09-09。审查者参与过 F01/F08 夹具物化，未参与其行为执行；未参与 concurrent 物化及执行。本次只读日志、实际文件、初始清单及固定 Canonical，独立重算字节身份和链接；没有重跑行为 Agent、维护脚本或构建。

依据：固定 `8a41958f3feaf08f02dabc5fd67c9b70c7f87604` 的完整 `docs/rules/artifact-organization-and-reading.md`、`docs/rules/agent-delegation-and-coordination.md`、`docs/meta-protocols/project-onboarding.md`、`docs/meta-protocols/harness-adoption-and-adaptation.md`。分别适用既有绑定及共享边界、单写者和候选先于事实源、同身份缓存恢复、用户修改保护及分范围认证要求；未增加额外 Gate。

证据定位：工作区为 `[工作区]`；F01/F08 根分别为 `.harness-staging/v013-r2-remaining/F01`、`F08`；并发根为 `.harness-staging/v013-r2-concurrent`。初始依据为 `.harness-build/v013-oracle/r2-remaining-F01-initial-hashes.json`、`r2-remaining-F08-initial-hashes.json` 和 `.harness-build/v013-r2-concurrent-initial.json`。下文日志行号为各 `coordinator-tools.jsonl` 的物理行号。

七份导出日志的实际 SHA256 均匹配各自 `coordinator-tools.identity.json`，行数依次为 F01 Local/Shared/Repository-native：20/24/24；并发甲/乙/integration：8/10/12；F08：24。结论由调用参数、脚本写目标、返回结果及最终字节共同支持，不以自述或 identity 中的来源声明代替行为证据。导出不是操作系统级完整审计，不外推为宿主所有活动均受监控。

## F01：三个维护子例 PASS

| 子例 | 初始文件实际变化 | 独立核验 |
|---|---|---|
| Local | 仅 `个人资料/流程记录/README.md`；新增限 `records/` | 个人空间原位复用，未复制进项目；私人备注、基线、项目入口、原正文及业务 spec 原字节保留；18 条当前直接导航存在且留在子例根内。 |
| Shared | 仅 `团队资料/流程记录/README.md`；新增限 `records/` | 团队空间原位复用，未进入代码仓库；团队备注、基线、业务 spec 和原正文保留；18 条当前直接导航有效。 |
| Repository-native | 仅 `project/docs/流程记录/README.md`；新增该空间 `harness/README.md` 及 `records/` 文件 | 原仓内空间复用，没有占用业务 spec；24 条直接导航有效，跨项目包/证据链接明确限本夹具布局。 |

三份只读 harness 整树独立重算均为 `3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c`。初始文件无删除；原 adoption、项目说明、需求记录和 `project/spec/` 两份用户文件均与初始清单一致，未产生业务任务或状态推进。Local/Shared 的 Git 初始文件均未变；Repository-native 仅 `.git/index` 字节变化，与日志中的局部 status 检查一致，独立只读核对暂存差异为空，其他初始 Git 文件未变。未见 add/commit、父仓操作、网络或全局修改调用。

实际失败没有被当作通过：Local 日志 17–20 为验证输出尚未生成导致失败后恢复；Shared 21–24 为同类顺序错误后重验；Repository-native 17–24 为 CRLF 导致 diff 检查失败，保存失败输出、恢复本轮入口后以 LF 重跑。最终文件与独立导航核验支持维护完成。此处不证明新会话加载、完整适配、Git 发布生命周期或迁出夹具后的链接可用。

## concurrent：有界并行与冲突消歧 PASS

工具轨迹时间均为 **2026-09-08 UTC**：甲首调用至末返回 `17:35:29.112–17:36:22.410`，乙 `17:35:28.784–17:36:37.250`，工作时段重叠 **53.298 秒**；读取规则的工具区间也重叠约 **2.030 秒**。实际采集记录分别为甲 `17:36:22.3079435`、乙 `17:36:12.1380182`。证明两个 Worker 工作时段并行，不声称两次文件采集同时执行。

甲日志 7–8、乙 7–10 的实际脚本仅写自身 `workers/<名>/result.md` 与 `records/<名>/`。独立 Owner 的授权见 integration 日志第 2 行，仅写共享索引和 `records/integration/`；其 9–12 行创建并执行汇总脚本，最终返回 `17:42:18.248`，晚于两 Worker 结束。Owner 重新读取输入、索引、两份提案及证据，没有直接采信提案摘要。

两提案均绑定初始索引 SHA256 `6ae4300ed05d0ba8484fdaaf029bc7fb519f063c7cd60bfb3b787490a3b46be3`，均提议 EV-02。最终索引明确甲为 EV-02、乙为 EV-03，并说明乙 EV-02 是历史候选；未改 Worker 原提案。`records/integration/核验-20260908T174217160Z-51f936b8/索引写前.md` 的哈希与初始索引一致，当前索引完整保留其字节前缀，EV-01 没有重编号或重验冒认；原“协调者”文字明确标为写前历史责任。

独立重读真实输入结果：

| 最终身份 | 实际内容 | UTF-8 原始字节 / U+0020 | SHA256 |
|---|---|---|---|
| EV-02 / 甲 | 你好 世界 | 13 / 1，无 BOM、无换行 | `4ec14dba94b11ab6334bd140750f9fb307ffcdc6c1b7fbb774f8659f5fa9083c` |
| EV-03 / 乙 | 保留 空格 | 13 / 1，无 BOM、无换行 | `4dea664195727613e47d47025fe461e6b0270f0761be2113be64fc58fe3edfc4` |

与甲 `采集结果.json`、乙 `命令结果.json`、工具返回及最终索引一致。独立比较 Owner `核验.json` 保存的 12 份来源原字节及哈希，全部仍与现文件一致；共享索引及两份提案共 19 条 Markdown 链接可达且未越界。相对初始清单只有 `shared/index.md` 被修改，固定包、输入及授权均未变；最终索引 SHA256 为 `faec17c50ff31a2667cb72ff930745d4811de84f27d3774a6751f948d75a2965`。

未测：同时抢写索引、独占锁拒绝、Owner 核验期间源文件再变、崩溃中断恢复。脚本具备相应检查不等于这些异常已触发通过；本轮仅证明真实 EV 提案冲突被单写 Owner 消歧，未推进业务完成状态。

## F08：固定缓存与双范围文件恢复 PASS

日志 13–18 显示先核验原包、确认乙缓存 README 漂移，再保存现场并执行恢复。初始清单没有甲缓存；现在甲缓存 24 个文件、乙缓存及只读 harness 独立整树哈希均等于上述固定 R2，未升级。乙只替换 `缓存/乙包/README.md`；包外 `records/本轮缓存维护/乙缓存修改前README.md` 与初始漂移文件逐字节相同，包含“本机临时缓存备注：待复核。”，备注没有丢失。

相对初始清单，仅修改上述乙 README、`space/harness/README.md`、甲乙各自适配 README 和内容记录（共 6 份）；新增为甲缓存和本轮 records。两模块的本地规则、业务数据、稳定基线、旧 `原管理内容.md` 及全部初始 Git 文件未改。甲用户追加原样保留，当前规则 SHA256 为 `85c176e24664e0b3e9223c80987b6cf9829af00ce188f262428654453d0550e0`，旧快照为 `41d9b14a56d8089af851f6ff6f40b39563167c7062f02ca48defa8baa1fef948`；乙当前及原快照均为 `9ec3c969bb04bc783e032981f6a579d064c015dd8df22eb1417eb44b4f242732`。两份记录分别绑定本模块和本缓存，当前/历史哈希均独立核实；四份修改前 README/JSON 备份均与初始清单相符。

17–18 行首次脚本在缓存恢复后因路径分隔符 KeyError 退出 1；19–20 行接续核对并写范围记录，23–24 行最终检查退出 0。失败保留在真实轨迹及维护证据中。17 条当前导航有效；备份 README 内相对链接保留原位置语境，作为原字节快照，不当成当前导航入口。

**未测试 READY 失效、跨模型、升级回滚或自动回滚**；初始现场本就没有已认证 READY。双范围结论仅限文件绑定、恢复及用户修改保护，不代表两套 Runtime 已安装或加载。真实加载面、候选适配语义及各范围行为认证缺证，因此接管仍 BLOCKED；不把这些后续认证条件升级为本次文件维护的额外 Gate。
