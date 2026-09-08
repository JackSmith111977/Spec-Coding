# 从这里接入

通过基础文件/网页读取启动，不预设Skill、Plugin或Hook已安装；缺少必要入口访问能力则停止并指出缺口。

1. 阅读[包身份与完整性](../README.md)，定位manifest.json，核验固定发行及通过依据，已有绑定优先复用。Hash不单独证明可信或发布。无正式证明时只有包外维护者授权才可走[候选验证](../skills/spec-harness-adoption/references/candidate-validation.md)，否则BLOCKED。
2. 读取[全局权限段](../rules/global.md)及[人机协作](../rules/collaboration.md)、[产物组织与读取](../rules/artifacts.md)，复用已有意图和授权；一句指令不扩大权限。仅接入无需业务目标，不生成虚构业务产物。
3. 直接读[Harness接入](../skills/spec-harness-adoption/SKILL.md)，调用[项目接入](../skills/spec-project-onboarding/SKILL.md)，确定稳定基线、工作空间入口与01A/01B/Resume。理解程序不依赖安装，不因默认目录缺失而新建平行空间。
4. 加载[全局执行](../rules/global.md)、[完整路由](routes.md)、当前流程及共享依赖和[能力要求](requirements.md)。全局约束/异常触发在依赖动作前生效，正文按需读，暂未激活不代表不适用，不删除后续入口。
5. 发现实际Runtime/项目环境，装配到真实加载面，固定本地候选，对照原包回查语义并验收加载、产物导航/写回与行为。READY仅对已验证Runtime、项目和范围成立，文件存在或安装成功不等于已加载。
6. 正式接入通过后，有既有任务及继续意图则自动继续Workflow；明确仅接入则汇报结果并结束。候选测试只运行授权场景，到停止条件返回。包语义缺失返回维护者，不读浮动源码补缺或重新预编译。

执行中：失败/非预期行为、归因不可靠、未解决Finding按路由诊断；权限/Gate看原授权及证据；包/配置/模型/工具/隔离/Fallback/范围变化在相关动作前重验要求。索引冲突/陈旧回查权威内容；保留原始包和用户资产，不静默覆盖。
