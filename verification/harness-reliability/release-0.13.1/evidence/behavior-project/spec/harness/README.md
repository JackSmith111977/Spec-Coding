# 本次受控加载记录

原包：`<repo>/.harness-build/patch-0.13.1/frozen-r1`；版本 `0.13.1`；source_revision `6ef35782bf836a7795687a6b5919ccb74359c81b`；package_sha256 `34ade88a97f78926f5cb2cc7d5daec005c165ad8710972db40900e0ca3d24b4a`。

本次采用会话内基础文件读取：用户指定 bootstrap/BOOTSTRAP.md 为实际入口，已实际读取其接入、全局规则、路由、能力要求及当前队列必要程序，不安装或转换包。当前会话为 Codex，工具为 functions.exec → exec_command / apply_patch；环境探测为 PowerShell 7.6.5、Python 3.13.7，Python 路径 `<python>`。应用具体构建版本未探测，不用于证明额外能力。

包完整性校验与指定 Hash 一致。该事实仅证明固定对象完整性。会话内读取适用规则是当前加载证据；本目录只是记录入口，不声明自动加载或新会话生效。原包全路由由其 bootstrap/routes.md 保持可达，未激活流程在使用前补读与验收。

稳定基线见 [接入基线](../adoption.md)，队列见 [queue.json](../../queue.json)，本轮结果及原始证据见 [behavior-result.md](../../../behavior-result.md)。不转换源码语义；依据原包直接消费，新增文件只承载绑定与导航。

本地记录身份以本轮结果中的文件 SHA-256 快照固定。范围仅当前会话与此合成项目的 A 检查及 B/C/D 安排。包、工具、对象、依赖、范围、上下文或权限变化时，先复核受影响要求；当前证据不继承为其他 runtime、首次恢复或正式项目 READY。

没有既有 spec/，本轮初始化最小测试空间。路由停留受控队列入口；01A/01B 不激活，不伪造项目业务状态或 Task；不存在可恢复的既有流程状态。无需安装或恢复原配置，本轮新增记录保留，不清理用户原资产。
