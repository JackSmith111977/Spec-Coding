# Patch发行包构建

本机制属于维护者构建治理，不是客户端新协议。Patch是版本语义，Incremental是构建方式；最终输出仍是可独立安装的完整包，不发布依赖旧安装顺序的二进制差分包。

## 1. 资格与基线

按仓库版本治理，Patch只用于不改变Canonical语义的Harness修复、拼写、链接、格式或纯文档修正。新增规则、治理能力或语义演进按MINOR等实际范围处理，不能因Diff小就发Patch。本机制自身属于新增维护能力，不据此自动将当前未提交的规则变化定为0.13.1。

维护者先核验上一正式Release、Tag、发布收据和包身份，保存完整旧包及其从可信记录取得的Hash。工具只验证指定包与Hash一致及其来源结构，不联网认证发布资格；不得把刚对任意本地包计算的Hash当正式可信来源证明。目标版本为同一主次版本的下一修订号，固定源提交中的VERSION与规范Manifest一致。

## 2. 构建路线

1. 维护者确认Patch语义资格及可信基线；绑定候选源提交，记录修复原因。工具不自动判断规范语义。
2. 执行 `harness_patch.py plan`：比较两侧完整规范和Manifest，反查来源到资产，再传播依赖。Canonical未变的包缺陷用 `--defect` 显式声明资产。条件依赖缺少精确消费者映射时保守覆盖所有Skill及入口。
3. Builder读取受影响资产的完整当前来源，重建整个资产，直接回查。不能只拿Diff在旧包上修几句。未受影响资产保持原字节，Envelope逐轮刷新；在包外暂存目录准备完整候选。
4. 使用 `harness_package.py assemble --package` 装配暂存目录并绑定已提交来源；不会自动生成正文或补版本文案。
5. 执行 `harness_patch.py build`：重新计算范围、核验候选身份及范围外内容、复制到全新输出目录，标记INCREMENTAL与旧包身份，输出固定候选Hash。范围报告留包外。此时只是结构候选，不是发行PASS。
6. 按构建治理完成一次受影响范围的批量独立语义审查、必要行为挑战及共享集成验证。原Reviewer可以定向复核，真正盲测保留Fresh；复用证据需证明来源、对象、依赖、环境、范围及独立性仍适用。
7. 用 `harness_package.py archive --package` 生成完整可复现ZIP；记录最终包与ZIP Hash、验证对象、证据复用关系。必要发布门槛通过后才推送、打Tag及创建Release，标题使用Tag，公开证据先脱敏。

示意命令中的参数均须替换为已核验身份，PowerShell变量名为调用者自行设置：

```powershell
python tools/harness_patch.py plan --baseline $patchBase --baseline-sha256 $patchBaseHash --source-revision $patchSource --defect spec-development-execution
python tools/harness_package.py assemble --package $patchPrepared --source-revision $patchSource
python tools/harness_patch.py build --baseline $patchBase --baseline-sha256 $patchBaseHash --source-revision $patchSource --candidate $patchPrepared --output $patchFrozen --defect spec-development-execution
python tools/harness_package.py archive --package $patchFrozen --output $patchZip
```

`plan`和`build`输出JSON可按现有运行机制保存，不要求客户端读取。`build`接受Builder准备并装配好的完整候选，不在冻结旧发行目录内原地升级。输出存在、路径嵌套、基线Hash不符、版本不符、未声明范围外变更均阻断。

## 3. 保守退出与验证边界

Manifest除版本和发布状态之外发生变化，或资产集合、映射、依赖及条件路由改变时，工具拒绝Patch快捷路径。按常规范围治理分析，无法可靠解释时Full Build；不能绕过拒绝手工改成PASS。该保守限制可以多做验证，但不允许漏掉新增/删除消费者。

所有包都全量执行结构检查。共享规则、Bootstrap、Routing及组合变化必须保留包级挑战；Patch不保证每次只需测试一项，也不承诺固定子Agent次数。工具的 `reusable_artifacts` 只是未受影响的资产候选，不是自动复用行为证据的批准。

版本升级本身不能认证语义未变，测试通过不能替代Patch资格审查。纯工具修复但没有包或来源缺陷时不生成空Harness Patch；以仓库实际发布范围处理。

## 4. 客户端与回滚

客户端仍从新Release取完整包，核验身份后在独立位置适配，按受影响范围验收；保留旧固定包及有效绑定。失败时在授权范围内恢复旧绑定，不覆盖用户修改，不将新包READY沿用给旧环境或其他Runtime。此机制不引入客户端安装器、自动更新器或补丁链。

## 5. 实现验证范围

2026-09-12：原有11项维护工具回归通过，新增9项Patch测试通过。使用真实包副本，目标Patch源身份与部分差异通过隔离fixture模拟；指定暂存目录的装配测试读取真实基线提交。覆盖固定Hash、版本拒绝、条件依赖传播、清单关系变化、范围外修改、Envelope运行变化、顶层入口变化、嵌套/已有输出、候选身份、旧包保护及归档可复现性。新增装配测试最初因fixture切换工作目录导致Git定位失败，修复测试隔离后复跑通过，不记作产品构建成功。

一名独立Reviewer批量审查，发现Envelope运行变化与包级入口字段两项范围遗漏；修复并补回归后由原Reviewer定向复核关闭。没有运行客户端Agent行为认证，没有创建实际Patch Release，也没有证明真实发布耗时已下降。
