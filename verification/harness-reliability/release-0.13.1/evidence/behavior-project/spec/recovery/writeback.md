# 写回核验

本文件仅记录当前执行者的确定性写回自检，不是独立审查或整体验收。

方法：用 PowerShell 读取本次恢复目录内五个明确文件的 Markdown 链接，以文件所在目录解析目标，仅检查目标为文件；不遍历旧报告。另核对原总入口仍包含恢复导航链接、权威表保留 T1 阻塞及 E1，T2 为依赖阻塞。根 README 链接检查对象未修改，故不重复运行原检查。

检查命令核心：`[regex]::Matches($正文, '\]\(([^)]+)\)')`，逐项以 `Join-Path` 和 `Test-Path -PathType Leaf` 判定。对象哈希使用 `Get-FileHash -Algorithm SHA256`。
恢复文件链接数：11；缺失数：0；权威状态与总入口检查：True
- `tasks.md`：`89ba90b372565af5cab5046dc2d7da187c467c5455dcf80256169c78fd96430d`
- `summary.md`：`d39c921f57366b365ff91802f82e7785ed012c655eb1af0946f6e860df40995c`
- `result.md`：`35a49b752323b9e9f731815eb0d43cb3392dd787a896ab48270fbecf1d2c281a`
- `evidence.md`：`90202266a75f6b4fa7bacb4f3fc437451abf5621046b7136b1b4aa14c2e0f58f`
本次写回自检完成；命令成功退出。
