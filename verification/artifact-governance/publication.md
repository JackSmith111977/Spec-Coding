# 0.13.0 发行身份与使用依据

[GitHub Release：0.13.0](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.13.0) · [完整包](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.13.0/spec-coding-harness-0.13.0.zip) · [升级说明](migration.md)

此页在发布前固定交付身份；正式发布事实以对应Tag与非草稿Release为准。Release标题必须逐字为 `0.13.0`。维护者发布后的实际核对另存收据，不修改原包或移动Tag。公开附件均按用户要求脱敏，方法与可复核性限制见[脱敏说明](sanitization.md)。

## 固定对象

| 字段 | 值 |
|---|---|
| 版本 / Tag / Release标题 | `0.13.0` |
| Stage 3候选 | R2，`6f95f43f74c5a134c887db167e123fe9c54498b4` |
| Canonical source_revision | `8a41958f3feaf08f02dabc5fd67c9b70c7f87604` |
| 包内容SHA256 | `3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c` |
| 完整ZIP SHA256 | `3c7908906c9d1a01a09f7038ba242d157661ff9125af1d3dde4745ac00c0cddd` |
| 内容 | 24文件、22资产、11 Skills、5类共享规则，45份Canonical来源 |

Tag包含后续包外验证与发布文档提交；它不冒充构建规范源或最初候选提交。冻结包全部文件与R2逐字节一致，最终来源/依赖映射保存在原包 `manifest.json`。仓库 `docs/manifest.yaml` 的发布状态从candidate更新为released只记录生命周期；未改变规范集合、行为或冻结包Manifest。

## 附件与复核

| 附件 | 用途 |
|---|---|
| `spec-coding-harness-0.13.0.zip` | 完整固定包；解压后从 `harness/bootstrap/BOOTSTRAP.md` 开始。 |
| `spec-coding-harness-0.13.0-manifest.json` | 原包Manifest的原字节副本，便于核对来源。 |
| `spec-coding-harness-0.13.0-verification.zip` | 脱敏后的包外判定、逐项覆盖、迁移说明、初始清单及身份。 |
| `spec-coding-harness-0.13.0-behavior-evidence.zip` | 导航、组织、边界与并发场景的脱敏副本；含无作者的Git关系摘录及失败修正链。 |
| `spec-coding-harness-0.13.0-runtime-evidence.zip` | R1历史及R2接入的脱敏副本、CLI/desktop记录与有限加载对照；R1仅是未发布的失败历史。 |
| `SHA256SUMS` | 上述附件的SHA256，完整清单不计算自身Hash。 |

先核对下载文件与 `SHA256SUMS`，再运行完整包内 `harness/scripts/verify.py`。ZIP Hash与包内容聚合Hash是不同对象，不能互换。结构校验不能代替[Stage 3判定](stage-3.md)及目标侧实际验收。

两份公开证据归档分别含692与195项（含各自index.json），SHA256分别为 `3962ff8b38d3838a7601f36ccfb8e9f7b586d0c62ba9ba00465115208754eb17` 和 `36d7e7df720a4340a6a7d645cff19b0d815350b9f0bfd84f49ab0a06433b609d`。index绑定原件Hash和公开字节Hash，并列出省略项；归档本身不自动判定PASS。

解压公开副本后以各 `v013-*` 目录为场景根。报告中的 `.harness-staging/v013-*` 指相应目录，`.harness-build/*initial*.json` 可从本报告包 `initial-state/` 按[来源映射](initial-state/来源映射.json)查到。公开日志中的本机绝对路径已替换为角色占位；按同一场景相对路径阅读。原始Git数据库仅本地保留，公开摘录不替代完整对象验证。报告中的仓库源码链接在[固定Tag源码](https://github.com/JackSmith111977/Spec-Coding/tree/0.13.0)查阅，客户端执行仍只消费完整包。

测试数据是合成项目，过滤并脱敏后的会话证据保留可公开的外部输入和工具调用/返回；不包含模型推理、系统/开发者消息或其他用户会话。它不是宿主全活动审计，也不证明OS强制隔离。初始状态、真实运行、Reviewer判定与Owner写回各自保留，不能把当前文件反推成首轮就成功。

## 已验证范围与升级

结构与11项工具测试、独立包语义以及本轮必要代表性行为通过；完整依据和失败回流见[最终判定](stage-3.md)。Windows桌面Fresh显式入口只认证本次受控读写，CLI配置的写入限制仍在；未激活能力和其他环境由目标项目实际验收。不是35项扩展矩阵、全五项负控、跨平台、效率或真人审阅全通过，详见[覆盖表](behavior-coverage.md)。

升级优先复用现有空间、权威正文和稳定ID，保护用户修改；按[迁移指南](migration.md)验证新规则实际进入加载链。回退基点是正式 [0.12.0](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.12.0)，其原包和证据未改；回退仍须检查当前布局兼容性，不能只换目录后复用旧READY。
