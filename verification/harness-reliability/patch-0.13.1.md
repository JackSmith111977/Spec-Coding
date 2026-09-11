# 0.13.1 增量候选构建

本报告保留首次候选构建时点的事实；其后补证及正式发布判定见[0.13.1发行材料](release-0.13.1/README.md)。以下“未发布”等为当时状态，不作为当前Release事实。日期：2026-09-12。

## 版本与范围

用户明确要求以Patch方式构建新版本。本次使用0.13.1修订号；变更包含新增维护治理/工具能力，按原版本规则通常属于MINOR，已在CHANGELOG记录本次版本选择例外，不宣称全部变更语义不变。此记录不批准其他版本沿用例外。

| 对象 | 身份 |
|---|---|
| 旧正式版本 | 0.13.0 |
| 旧source_revision | `8a41958f3feaf08f02dabc5fd67c9b70c7f87604` |
| 旧包SHA256 | `3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c` |
| 新source_revision | `6ef35782bf836a7795687a6b5919ccb74359c81b` |
| R1包SHA256 | `34ade88a97f78926f5cb2cc7d5daec005c165ad8710972db40900e0ca3d24b4a` |
| R1 ZIP SHA256 | `d2f4d6677c99d1886becc58ad4101f0802f261dbc733d6341fe86ecc42e9f7df` |

旧包以[正式发行身份](../artifact-governance/publication.md)记录核验；本轮没有重新联网认证Release状态。新源提交仅在本地创建，不推送、不创建Tag或Release。

4份Canonical正文发生变化；依共享/条件依赖保守传播，17个资产回查，另刷新Plugin元数据。Builder一次批量读取45份当前原文并回查；11个载荷文件改变、12个保持原字节，Manifest另行装配。最终保持24文件、22资产、11 Skills、5规则，无新客户端目录层或差分安装链。

## 构建与验证边界

工具从可信基线身份与固定源计算范围，Builder完成来源驱动生成，再在独立目录冻结INCREMENTAL候选。全量结构验证通过，ZIP逐文件与冻结目录字节一致；旧包保留。此前21项工具测试是工具级证据，不替代本候选语义与行为验收。

本轮角色：一名Builder、一名独立语义Reviewer、一名Fresh行为执行者。Reviewer不依赖Builder回查报告作为语义依据；行为执行者只读取冻结包、合成项目及场景，不读取Canonical或Oracle。局部问题优先由原Reviewer复核，不默认扩展多轮Fresh矩阵。

行为范围为一次Fresh中的四项相关场景：A实际执行文档链接检查，B/C/D对局部修复复核、Fresh污染和Commit门槛作情境决策。B/C/D不是实际跨会话或完整业务生命周期测试；不声称自动加载、所有Runtime、性能提升或完整端到端业务通过。

本地完整证据保存于 `.harness-build/patch-0.13.1/`，包括scope、源Hash清单、Builder回查、构建收据、语义/行为记录、ZIP与SHA256SUMS。原始记录仅本地留存；后续若公开须先按既定脱敏要求处理。固定候选未发布，正常客户端不能把该包当已有正式Release；受控使用须绑定包外授权与本次Hash。

## 本轮结论

- 结构：全量包验证通过，归档逐文件与冻结包一致，仓库 `packages/harness/` 已同步为相同内容Hash；基线副本Hash未变。
- 独立语义：Reviewer直接读取四份变化Canonical与必要未改原文，核对共享组合和复用身份，限定范围PASS，无可操作Finding；未重新全审未变历史语义。
- 受控行为：同一Reviewer依据事先固定的Oracle判定限定范围PASS。A记录实际检查1个链接、0个缺失；B允许合格原Reviewer定向复核，C拒绝以知情执行者证明Fresh恢复，D拒绝缺必要Commit时假Done/假通过。
- 证据限制：A工具输出以执行记录中的摘录保存；读包范围及未读Canonical属于执行者自报，没有完整宿主轨迹，不能认证全程无提醒或无污染。执行者曾修正自建导航检查的局部错误，不将整个接入描述为零修正首次成功。
- 行为判读沿用原语义Reviewer，不另建判定者；本轮三个子Agent分别承担Builder、独立Reviewer和Fresh执行，未递归委派。没有测量实际成本下降，也没有执行完整跨会话业务闭环。

可交付文件为 `spec-coding-harness-0.13.1-candidate.zip`、独立Manifest副本及SHA256SUMS。后续若要求正式发行，应先收敛必要Release验证范围和公开证据，不直接把本报告的限定通过改写为全量发行PASS。
