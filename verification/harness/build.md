# 首次全量构建记录

用途：维护者构建与验证证据，不是客户端必读层，不替代Canonical或正式发布证明。

- 源分支：refactor/precompiled-harness-architecture，先前已推送的dc70930。
- 构建分支：codex/build-first-harness-package。
- 固定源：2f585f0faa8c0ba831161858a2e1418fd2d527e7，VERSION与docs/manifest.yaml同步0.12.0 candidate。
- 模式：FULL；当前没有可用的既往正式Harness包及可信source_revision基线。
- 输入：manifest schema 5登记34阶段正文、4规则、4异常正文、2元协议，共44份；清单作为构建输入，Governance/Reference不混入正文sources。
- 构建方式：主Builder分批直接读取完整正文，重新编写11个程序Skills及共享规则与消费封装。未用摘要/Clause/IR作为编译输入，未复制Canonical目录作为客户端事实源。
- 自回查：逐阶段检查读取原文中的产物字段、完成条件、权限、状态转换、异常回流和有效引导。独立审查继续直接读原文，不依赖此声明。
- 结构：8主流程+Debug+2meta，4共享规则，Bootstrap/routes/requirements，Plugin封装、完整性脚本、薄manifest。Skills正文保留阶段职责和完成条件，特殊候选授权细节位于接入Skill的references；跨阶段链接用于路由，按当前需求加载。
- 来源映射：流程本体记录对应直接规范来源；共享规则单独记录来源，经dependencies或conditional_dependencies组合；包级路由/要求直接依赖完整语料。元数据/公开格式自身不伪造Canonical来源。
- 外部标准：本轮打开核验 https://agentskills.io/specification 与 https://agent-plugins.org/specification ，采用SKILL.md必要name/description及Agent Plugins 1.0根plugin.json；没有虚构MCP provider或供应商扩展。

## 候选R1

package_sha256：`df12bb60ef594c9fb2a324b91b92fe10f4919b1413609f5154fc296cdd6405d1`。

归档SHA-256：`86802196c47135458f80755348c1a6e8f79020dc817353c088a28a8daad0918c`。

23文件、21资产、11Skills；生成后只读审查与测试。变更产生新候选并重新绑定证据，不把R1结果转贴给新Hash。

R1独立语义审查结论BLOCKED：候选授权省略“未授权”限定；OI建档省略“需后续承接”条件；Debug调查省略“不默认”限定。R1行为记录仅作诊断，不进入R2通过证明。三个问题均属于派生表达失真，回Stage 2 Transform，没有修改Canonical来迁就产物。

## 候选R2

- package_sha256：`4451d39351a32576e99552aada821f98cc69f0c087e041273d294e6bc332db9b`。
- 归档：`.harness-build/spec-coding-harness-0.12.0-candidate-r2.zip`。
- 归档SHA-256：`7f7d5e2c4447231f5bf83afc68a4dba5504097d79a99f9291ee502ced2735a79`。
- 固定源、版本、23文件/21资产/11Skills不变；三项阻塞已回完整来源重读、重新生成并整体回查受影响资产。
- 一并恢复重大收敛同步的Human判断条件、共享认知载体“不要求”的原义，以及大规模规划可按需独立审查的限定。
- 五个正文/资源文件及manifest共六文件改变；共享global/collaboration变化影响全部消费者组合，三分工独立复核新包，不能凭Skill正文未变复用旧组合PASS。
- 候选内容已提交为`02c69747743293847ea21496480b1627742c3030`，逐文件核验Git blob与冻结包原始字节一致，见candidate-identity.json。报告保留原始字节，Git不规范化验证目录行尾；Python缓存不入库。
- 新候选结构及8项工具测试已实际通过；独立语义与行为结论分别见reviews/及后续判定报告。此处不提前宣告Stage 3通过。

## 可复现命令

在仓库根运行：

```powershell
python -m pip install -r tools/requirements.txt
python tools/harness_package.py verify
python -B -m unittest discover -s tools -p 'test_*.py' -v
python tools/harness_package.py archive --output .harness-build/spec-coding-harness-0.12.0-candidate.zip
```

`assemble --source-revision <完整源SHA>`仅重生成薄清单，不是语义编译器，也不证明Builder确实读源。运行前必须完成当前规范的直接生成和回查；未知schema/无法解释范围回FULL。后续增量需按治理比较上一正式Release的源与两侧manifest，工具未宣称自动完成该分析。

结构测试覆盖资源篡改、缺失/新增文件、manifest自身内容身份、非规范来源、依赖循环、路径逃逸/重复JSON键及可复现归档。Hash不证明语义正确；发布必须另有全源独立语义和真实行为证据。

## 本轮验证重点与终检

按首次全量构建计划，validation_focus为：安装前一句接入及实际加载；正常跨Workflow开发和证据固化；验证、提交或推送失败不伪造完成；权限与阻塞项回流；Debug归因及原Owner收敛；恢复、重复接入和环境变化；目标侧转换丢失规则由独立原包/本地组合语义回查阻断；缺少授权、字节损坏或能力语义缺失时拒绝接入。第二种能力配置复测安装和恢复。具体场景设计在执行前形成，见oracle/，最终判定只依据实际执行记录。

final-checks.json保存最终确定性检查：8项包工具测试及2项证据归档测试、全部11个Skills格式检查、Git字节与冻结候选相同、归档可复现。测试使用上面的unittest discover命令，全部检查已实际通过。
