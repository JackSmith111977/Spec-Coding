# Spec Coding Harness 0.13.0

本包提供11个预编译 Skills、5类共享规则、安装前入口、路由及适配验收要求。它是版本绑定的派生产物，目标 Agent 不需要重新读取规范源码。

一句指令：

> 从这份固定 Spec Coding 发行包的 bootstrap/BOOTSTRAP.md 接入当前项目，按当前 Agent 与项目环境适配 Harness，建立适配的完整Harness，完成适配与验收后汇报结果，本次指令到此结束。

打开[Bootstrap](bootstrap/BOOTSTRAP.md)，无需先安装插件。保持整个包结构；只复制SKILL.md会丢失依赖。支持Agent Plugins 1.0的客户端可读plugin.json发现skills/；其他客户端按包内要求绑定真实加载面。安装成功不代表接入及能力验收成功。

## 身份与完整性

manifest.json记录版本、完整source_revision、入口、资产来源/适用/依赖/能力及逐文件SHA-256。原始包保持不变，目标配置及转换放授权的本地范围。

有Python 3可在包根运行 `python scripts/verify.py .`，或传包绝对路径，得到package_sha256。没有Python时用可用机制实现同等检查；必要完整性不能证明则阻断。

Hash算法：对范围内文件按包内POSIX路径排序，每行UTF-8为 `sha256原始文件字节 + 两个空格 + 相对路径 + 换行`，对所有行再取SHA-256。资产Hash覆盖其文件/目录下全部文件；manifest.files覆盖除manifest.json自身外全部文件；package_sha256覆盖包含manifest.json的整个包。哈希不写回自身。

正式消费还须从可信发行入口取得固定Tag/Release、归档SHA-256及包外验证报告，确认报告绑定同一package_sha256、version、source_revision，结构、独立语义和行为全部通过。目录、版本号、Hash或候选测试记录本身不构成正式发布证明。尚未发布时，仅凭包外维护者授权可进行受控候选试验。

授权、验证报告、兼容实测和发布元数据在维护者仓库verification/harness/中，不进入冻结包。发行入口无可信通过依据则正式接入BLOCKED。客户端执行语义全部在包内，报告不补缺失行为。

## 使用与变化

完整[路由](bootstrap/routes.md)保持可达，当前流程正文按需读；[能力要求](bootstrap/requirements.md)说明适配边界和可观察预期。包不固定供应商、模型、Hook、隔离方式或CI命令，不能从格式推断Runtime已通过。

0.13.0新增[产物组织与读取](rules/artifacts.md)，统一空间入口、权威正文与按需导航，并支持仅接入结束。已有绑定不默认升级；相关环境变化重验受影响机制，候选测试不代替真实项目验收。历史版本用Git/Release，不在包内维护副本。
