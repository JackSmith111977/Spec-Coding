# 验证方法纠正

这些记录解释试验设施变化，不改变Canonical、冻结候选或业务正确性标准。

1. Windows PowerShell Transcript不能可靠捕获部分Git原生stdout/stderr。保留原始转录，后续采用subprocess显式捕获两条流及退出码。S03协调者在解除提交故障前实际复核钩子拒绝、确认HEAD未变，并另存`.coordinator/admin-commit-recheck.json`，明确其为设施复核而非Worker原始操作。
2. S08-B设计的函数已经遍历所有命令，但覆盖A夹具文件时意外省略CLI入口，会引入本不属于B的接口故障。在任何行为Agent读取B之前，为场景定义补回相同JSON命令入口，保持B的全部执行及失败汇总逻辑。旧`s08-b-r2`仅完成物化，未执行，弃用；新`s08-b-r2-v2`从修正资料初始化。不得把此夹具修复算为候选包修复或通过证据。
3. 无实际复杂setup的物化脚本原先可能生成看似可投递的目录。工具现对S03/S06/S07合成或故障分支默认拒绝，显式manual标记只得到PENDING_MANUAL_SETUP；实际设施建立并保留证据后才改READY_FOR_EXECUTION。该状态不表示任何Harness或业务已READY。
