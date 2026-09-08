# Harness维护工具

`harness_package.py`只装配已由Builder直接读规范后编写的程序、核验结构身份和生成可复现ZIP，不生成Workflow语义，不是客户端编译器。

Python 3.10或更新版本，维护者依赖见requirements.txt；包内完整性脚本只用标准库。

```powershell
python -m pip install -r tools/requirements.txt
python tools/harness_package.py assemble --source-revision <完整规范源提交SHA>
python tools/harness_package.py verify
python -B -m unittest discover -s tools -p 'test_*.py' -v
python tools/harness_package.py archive --output .harness-build/spec-coding-harness-0.13.0-candidate.zip
```

先同步并提交版本源，再直接生成/回查全部受影响资产，然后assemble并冻结Hash。验证记录留在包外。任何候选修改都必须重新装配/固定并重验受影响范围；校验PASS只表示结构完整，不表示独立语义、行为或发行通过。

当前映射在工具中显式列出11个流程及5规则，包含产物组织与读取规则。登记改变时维护者先解释影响，不自动猜测新来源。后续增量范围仍按治理从上一正式Release的source_revision比较两侧正文和Manifest并传播依赖；本工具不声称实现自动语义增量编译。

`prepare_harness_scenario.py <场景> <分支> <全新目录名>`物化Oracle提供的原始项目资料、固定包副本和包外授权。目录只能在.harness-staging下且必须不存在。复杂故障、动态环境或合成发行场景默认拒绝；协调者读完setup后显式传`--allow-manual-setup`只能建立未就绪资料，补齐真实前提后才能投递。只将AUTHORIZATION.md、包及目标项目提供给行为Agent；coordinator-input.json、.coordinator/和Oracle期待不得投递。

S03物化后运行`prepare_harness_git_faults.py <目录名>`：先在独立探针仓库实际验证提交/接收拒绝及恢复，再安装场景钩子。动态回合中由协调者在观察到真实失败后解除对应标记，不能让执行者绕过钩子。

全部被选试验结束后，`export_harness_evidence.py <目录名...> --output <包外ZIP路径>`保存原始记录、实际消费的Harness副本与项目Git快照，绑定每份文件Hash；故障副本也原样保留，不能用正常包替代。归档不自动判定PASS；0.12.0独立判定报告保留在verification/harness/，0.13.0记录在verification/artifact-governance/。归档过程中发现已枚举文件变更即失败，不用于并发运行中的最终证据冻结。

现有prepare脚本绑定0.12.0场景资料，不能仅改版本号就用作0.13.0产物治理覆盖证明。新场景应按本轮独立验收方案单独物化，保留候选身份、初始文件清单、授权和实际操作证据。

Fresh上下文隔离与文件读写授权不等于操作系统隐藏父目录。本地测试需如实记录实际可见输入、读取轨迹和沙箱范围；不得将仅口头声明独立或文件存在当作真实加载证据。更强隔离要求无法满足时记为限制或阻断。
