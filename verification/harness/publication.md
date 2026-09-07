# Spec Coding 0.12.0 正式发行记录

本次发行原样采用Stage 3 PASS的R2包。正式发布身份以[GitHub Release 0.12.0](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.12.0)的公开状态、Tag指向与附件实物为准；本文件或本地版本号本身不能替代远端发布证明。

| 对象 | 固定身份 |
|---|---|
| 版本与Tag | 0.12.0 |
| Canonical源提交 | 2f585f0faa8c0ba831161858a2e1418fd2d527e7 |
| R2候选内容提交 | 02c69747743293847ea21496480b1627742c3030 |
| 最终验证记录提交 | cee74135d3c98169c3478f8555912b3c69038dfb |
| package_sha256 | 4451d39351a32576e99552aada821f98cc69f0c087e041273d294e6bc332db9b |
| 发行ZIP SHA-256 | 7f7d5e2c4447231f5bf83afc68a4dba5504097d79a99f9291ee502ced2735a79 |

发行附件`spec-coding-harness-0.12.0.zip`与原`spec-coding-harness-0.12.0-candidate-r2.zip`逐字节相同，只使用正式下载文件名。包内manifest及source_revision均未变；源提交中的candidate状态属于构建历史，当前仓库manifest仅把发行状态更新为released，规范正文、登记、适用和路由保持不变。

## 下载与验证

- [完整Harness包](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.12.0/spec-coding-harness-0.12.0.zip)：包含11个Skills、4类共享规则、Bootstrap、路由、能力要求与完整性校验器。
- [验证报告归档](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.12.0/spec-coding-harness-0.12.0-verification.zip)：完整包外报告与机器可读收据。
- [初次行为证据](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.12.0/spec-coding-harness-0.12.0-r2-evidence.zip)：保留初次BLOCKED，SHA-256为`28a91e498523b24b760985284f8ff1b11fdd3eb0afba31013fc654256ec000a9`。
- [纠正后完整行为证据](https://github.com/JackSmith111977/Spec-Coding/releases/download/0.12.0/spec-coding-harness-0.12.0-r2-evidence-after-correction.zip)：包含追加收敛及完整案例，SHA-256为`5780bd6ca7a95d2826bb14e2ac70ed5bc2925c46b7d6bc126b6e52853cf40868`。
- Release同时附带`manifest.json`、`release-validation.json`、`publication.json`与`SHA256SUMS`。先核对固定Tag、ZIP摘要及包外PASS，再解压并运行`python harness/scripts/verify.py harness`，核对package_sha256。

取得可信固定发行后，可给目标Agent以下指令：

> 从这份固定Spec Coding发行包的bootstrap/BOOTSTRAP.md接入当前项目，按当前Agent与项目环境适配Harness，并继续当前任务。

保持完整目录结构；真实项目需要自己的授权、能力发现、适配语义回查和实际加载/行为验收，不能继承候选测试READY。

## 通过范围与历史边界

结构检查、10项工具测试、11个Skills格式检查及三份覆盖44份Canonical的独立语义审查通过。20项行为挑战中17项正本挑战通过，3项负控检出缺陷；坏副本自身仍BLOCKED。

CLI跨Fresh恢复首次遗漏原OI/Failure收口。独立评审提出BHV-01，Owner追加真实纠正后独立复核通过；原始BLOCKED提交4addbc7及归档保留，不能表述为无提醒一次全过。详见[最终行为裁决](behavior-verdict.md)和[发布准备收据](release-validation.json)。这些历史收据保持原字节，不改写过去的发布状态。

实测范围为Windows、PowerShell、Git及Python 3.13.7下的Codex基础工具与独立CLI能力配置。同供应商的不同配置不等于所有Runtime兼容；未认证所有客户端的原生插件安装、Hook或并行隔离。Claude CLI探测未取得可用结果，更低Python版本未认证。具体隔离、夹具、语义负控及证据捕获限制见原始报告。

本次为首次正式Harness包，先前0.10.0规范发行不能作为同形Harness的等价回滚包；如需撤回本发行，应明确撤回可用性并重新进入构建验证链，不能宣称存在未经验证的等价回滚包。后续包修改必须形成新候选并重新验证受影响范围。
