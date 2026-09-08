# 0.13.0 公开脱敏修正最终复核

2026-09-09。**PASS：PUB-01已修正，原脱敏阻断解除。** 结论仅绑定下述公开runtime附件及本次限定差异；不替代发布、Tag或后续重新封装材料的最终身份检查。

本次只读对照修正前公开ZIP、修正后ZIP、`pub01-correction.json`和索引，复核四份受影响文件及嵌套内容；其他已验项按字节Hash复用。未修改被审材料或原BLOCKED报告，未重新执行场景、构建或推送。路径均相对于`[工作区]`或ZIP根，不记录真实身份。

## 对象与变更

对象：`spec-coding-harness-0.13.0-runtime-evidence.zip`。

- 修正前公开SHA256：`eb32293d1990b31b39ae091441d2adf28981417c5ddb241dd7fd5c60a2732d83`，与保留的修正前公开ZIP实测一致。
- 修正后公开SHA256：`36d7e7df720a4340a6a7d645cff19b0d815350b9f0bfd84f49ab0a06433b609d`，实测195项、2187892字节。
- 原私有ZIP SHA256仍为`f995c26ce16c291000d720eee74211fea1180032522cdee7d9d0ec42e99b965e`，实测未变。

前后文件集合完全一致，仅以下四份文件及`index.json`发生字节变化；其余190项逐字节一致。

| 受影响文件（相对ZIP根） | 独立核对修正 | 新公开SHA256 |
|---|---|---|
| `v013-r2-adoption/records/probe-A.jsonl` | 机器标识3处、账户2处；含第58行嵌套工具返回 | `f5d69a3b998da4faf6df183bdd6623a673937ab4508475c9386c83669a7f2a0e` |
| `v013-r2-adoption/records/读取-01.txt` | 机器标识3处、账户2处 | `0e1358c5dcfd3e2907c708010414da68be96806d10d3737c2573673d8cca02b9` |
| `v013-r2-adoption/records/读取-02.txt` | 机器标识3处、账户2处 | `2ff3a2db63c31a1d81b3f1cd115b4ab648ff2c9617aedb2d3b351bf9218134fc` |
| `v013-r2-adoption/records/读取-03.txt` | 机器标识3处、账户2处 | `0c09f7ec7f51a6162388de0759958bf893bb01edf977396a33c353110185672e` |

独立用环境实际机器标识作大小写无关匹配，确认共12处替换；机器限定账户共8处替换。四份新文本均严格等于旧公开文本仅施加这两种替换的结果：机器/账户分别变为`[机器标识]`、`[运行账户]`，没有附带正文删改。

## 残留、语义与索引

四份文件的原文、逐行JSONL、递归JSON键值与内嵌字符串、Unicode/十六进制转义、URL/HTML转义，以及可解码Base64的UTF-8/UTF-16候选均已检查；递归检查访问1638个文本节点。未检出原机器标识、原运行账户或本机绝对路径残留。索引也未检出原身份；ZIP没有附加comment/extra元数据。

JSONL前后行数一致，每行仍可解析。PASS/FAIL/BLOCKED/READY/Verified/Resolved/Accepted词项前后计数一致；更强的“仅两类身份替换”全文等价核对同时证明命令、时间、返回内容、失败及限制文字未另改。A读取排除记录的方法失败、transcript字段意义和嵌套返回结构保留，不将失败改为通过。

索引193份保留文件的`public_sha256`全部匹配当前字节；原件Hash和transformed标志均保持，未改四份文件以外的映射。两项省略记录及Git关系摘录清单与前版完全一致，摘录公开Hash匹配。索引新增前版公开归档Hash并追加PUB-01变换说明，未隐去旧公开版本。当前`sanitization-receipt.json`及`public-release-checks.json`所列runtime归档Hash均匹配新ZIP。

## 原判定与未变项保留

公开behavior附件仍为`3962ff8b38d3838a7601f36ccfb8e9f7b586d0c62ba9ba00465115208754eb17`。发行包ZIP与此前已验私有发行包逐字节一致，复用24文件R2身份`3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c`，没有重新解释包语义或重审全部材料。

原审查文件与`verification/artifact-governance/public-sanitization-initial-review.md`逐字节相同，原BLOCKED事实保留。本报告只关闭PUB-01；原报告中已确认的脱敏解释边界继续有效：公开副本不是原始字节归档，省略Git/二进制原件后不证明可独立重演全部原始核验，已有行为PASS也不扩大为完整计划、跨平台或性能通过。

**本次受影响范围内剩余阻断：0。** 后续复制本报告、重生成报告ZIP/SHA及提交发布未在本轮执行或验收；不将其预先标为完成。本报告完成后停止写入。
