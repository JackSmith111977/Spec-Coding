# 构建范围与候选记录

## 来源与范围

- 上一正式发行：0.12.0，Tag 对应的原包 Manifest source_revision 为 `2f585f0faa8c0ba831161858a2e1418fd2d527e7`。
- 本次固定规范源：`36b92f7257a8b69aeb2f93de8f90c40c66e3f402`，VERSION 与 Manifest 均为 0.13.0，源状态 candidate。
- 输入：34 Main、5 Rule、4 Exception、2 Meta，共45份完整Canonical；Manifest是集合与依赖输入，不冒充正文Source。
- 模式：FULL。新规则对全部流程及两个Meta的产物动作适用，global/collaboration/delegation与接入/写回链同时变化，包级依赖与加载行为均需重审；本次不宣称已完成可缩小范围的增量构建演练。
- 变化：新增产物规则；明确工作空间/加载入口、适配记录与仅接入结束；统一任务与原OI、共享设计/验证、索引漂移、写回/迁移恢复；原有业务状态及Authority/Gate保持。
- 输出：11 Skills、5共享Rules、Bootstrap/routes/requirements及Plugin/完整性封装；全部消费者依赖新规则。工具显式登记新来源与artifact-navigation能力，并拒绝入口/Skill漏掉该依赖。

主Builder按完整当前Canonical分批直接读取各流程和规则，沿现有阶段表达核对完整产物、状态、权限、异常及有效指导，重新装配消费者和新共享依赖。共享规则从完整原文转为同包链接；阶段程序保留回查有效的表达，并接通新产物导航及写回契约。未以Source Diff或其他Agent摘要替代原文；设计文件不计入预编译Source Trace。

## 候选 R1

- 候选提交：`20b48366745db166fedbef83037e9d10189f8a3e`。
- package_sha256：`e4b84d88ab494b0503837674169bc0fb31814fcdb0a3c5ac7d9636a6f5ea6cd7`。
- 24文件，22资产，11 Skills，45规范来源。
- ZIP：`spec-coding-harness-0.13.0-candidate-r1.zip`。
- ZIP SHA-256：`af78ab8dd4990dd010960f3c7c07740aa347b26f3157e568952598e2bb348936`。
- 已执行结构/完整性与11项工具测试，通过；这不证明独立语义、实际行为或发布已经通过。

## 复现

在相应候选提交运行：

```powershell
python -B -X utf8 tools/harness_package.py verify
python -B -X utf8 -m unittest discover -s tools -p 'test_*.py' -v
python -B -X utf8 tools/harness_package.py archive --output .harness-build/reproduce-0.13.0.zip
```

`assemble --source-revision <固定源>`仅重生成包清单，必须先完成完整源驱动的资产构建与回查。更改包内容产生新候选，全部结论必须回指实际验证对象。

## 验证边界

独立源码审查与包语义审查分开；行为执行者只消费固定包、测试项目和包外授权，不读取Canonical、设计、Oracle或Builder过程。Fresh上下文和显式读写范围不等于操作系统隐藏父目录。记录实际加载、工具与文件证据，不用目录存在或自述代替验收。

测试候选授权只适用于各隔离项目，不迁移到正式项目。读取效率、Human审阅与不同Runtime兼容性仅按实际证据报告，不从格式或单次运行外推。
