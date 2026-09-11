# 0.13.1 发行验证材料

本目录保存冻结候选的包外验证及公开副本。[Stage 3最终判定](stage-3.md)为PASS；正式发布事实须核对[GitHub Release](https://github.com/JackSmith111977/Spec-Coding/releases/tag/0.13.1)与发布后收据。

版本 `0.13.1`，规范源 `6ef35782bf836a7795687a6b5919ccb74359c81b`；包 SHA256 为 `34ade88a97f78926f5cb2cc7d5daec005c165ad8710972db40900e0ca3d24b4a`；完整 ZIP SHA256 为 `d2f4d6677c99d1886becc58ad4101f0802f261dbc733d6341fe86ecc42e9f7df`。正式 ZIP 与候选 ZIP 仅文件名不同，字节不变。

## 阅读顺序

- 构建范围：[scope](evidence/scope.json)、[来源清单](evidence/source-inventory.json)、[结构收据](evidence/build-r1.json)。
- 独立判定：[语义审查](evidence/semantic-review.md)、[行为判读](evidence/behavior-verdict.md)。
- 实际记录：[执行记录](evidence/behavior-result.md)、[事先固定的 Oracle](evidence/behavior-oracle.json)、[合成项目](evidence/behavior-project/README.md)。
- 真实输入及工具记录：[首次会话轨迹](evidence/traces/01a09179-1d4d-79d2-9677-2ff3bc94bb0d.json)、[首次接入补证判定](evidence/stage3-initial-trace-review.md)。
- 独立新会话恢复：[轨迹](evidence/traces/01a091c2-2fa5-7c40-8fa8-f39dd937aa40.json)、[执行结果](evidence/behavior-project/spec/recovery/result.md)、[事先 Oracle](evidence/recovery-oracle.json)。恢复入口与状态为维护者添加的合成夹具，初始正文和后续执行写回在证据中分别保留。
- 原件与公开字节关系：[脱敏索引](sanitization-index.json)。

报告中的 `<repo>` 表示仓库根，`<python>` 表示实际 Python 可执行程序位置。`.harness-build/patch-0.13.1/` 下报告及合成项目在本目录 `evidence/` 中按相同相对路径提供；`frozen-r1/` 对应完整发行包的 `harness/`。历史版本材料可从各自固定 Tag 读取，不把旧 PASS 转成新候选 PASS。

公开副本去除了本机绝对路径、主机标识及邮箱，保留原件 SHA256 和公开 SHA256。原始文件仅本地留存；不上传 Git 数据库、模型推理、系统消息或完整宿主会话。索引证明字节对应关系，不自动证明行为通过。

原始受控测试期间的“不发布”和“非发行 PASS”是当时的生命周期或局部验证范围，原样保留。用户后来授权本次推送及发布，公开的是经过脱敏的副本，冻结包不变。

已记录的 A 为真实链接检查，B/C/D 为情境判断。首次报告只有工具摘录，后续导出对应会话的可见输入及完整工具调用/返回，独立 Reviewer 已据此补强有限范围隔离与接入证据；不宣称 OS 强制隔离或全宿主活动审计。没有完成全 Runtime 认证、跨会话业务闭环或效率对照，不宣称实际成本下降。目标项目仍须按包内程序执行实际加载、适配及验收。
