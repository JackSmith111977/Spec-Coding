# 能力、适配边界与验收依据

以下ID供manifest定位。必需程度由适用条件决定；Plugin、Hook、模型切换、并行本身不默认必需。实现可变，原包语义和验收预期保持不变；提示不能代替明确隔离或强制Gate。

| ID与适用条件 | 必须保持 | 可变实现与可观察验收 | 无法满足 |
|---|---|---|---|
| read-and-route：全部 | 安装前可读，版本内依赖完整可达，全局权限/异常触发先于动作，正文渐进读 | 基础读取或真实Instructions/Skill/Plugin；新会话实际加载所需程序，新阶段/异常能路由正确资产 | 入口语义缺失返维护者，加载缺口返发现适配 |
| identity-and-scope：全部 | 固定可信发行与通过依据，包/本地候选Hash和真实作用域；测试有包外授权 | 现有校验/配置快照；损坏/额外文件被发现，漂移后旧验收失效，原包未改，正式与候选入口区分 | 阻断接管，不凭自声明通过 |
| authority-and-state：权限/状态动作 | 复用授权，Human边界不越过，单一事实源、稳定ID、blockingOI和必要Gate；Meta不继承Workflow TaskGate | 原生权限、项目审批/状态工具或有证据会话组合；已授权局部动作继续，未授权AC/风险接受停止，blocking不能过Gate | 回权限Owner或修状态机制 |
| trace-and-evidence：正式流程和接入记录 | 引用原事实源，区分事实/推断/未知，证据绑定实际对象，动态事实不进稳定基线 | 原文档/任务/Git索引；新会话可回REQ→Design→Task→Change→Verification；稳定基线与运行证据分离 | 补证或回最早失真源 |
| deterministic-verification：要求确定性验证时 | 真实执行当前契约，证据含命令、环境、对象、结果；不把未运行当Pass、不降标准 | 项目测试/构建/CI/静态/运行；实际通过/失败输入判定正确，局部自证不直接替代正式Gate | 修验证环境/资产，必要Gate不能运行则Blocked |
| independent-review：流程/风险需要独立推理时 | 直接见目标契约证据，尽量隔离Writer推理，能力充分，默认只读，候选结果Main整合，不替代Gate | 真Fresh会话/子Agent/独立审查者；记录实际输入与上下文边界，Finding可复核，能力不足不假称通过 | 补充分机制或阻断依赖范围 |
| scoped-execution：委派/并行写/测试隔离 | 有界权限、最小充分上下文、单写Owner、冲突回Main；实际测试加载限授权作用域 | 单写当前区、独立只读共享、多独立写Worktree或语义等价隔离；可串行，验证无写重叠/用户资产覆盖，子结果不升权 | 重新划分/串行/隔离，必要隔离缺失则阻断 |
| git-lifecycle：Git固化变更或需求同步 | 局部验证→Task Commit/code_ref→正式验证→Done；同REQ全Done后Integration→AC Gate→授权Push；Push非Merge/Release/Deploy/Verified | 实际Git/托管工具及稳定绑定；正式Gate验精确ref；Commit失败保持In Progress，Push失败保留Task事实 | 修环境/绑定/权限，不伪造引用或同步 |
| observe-and-recover：故障或运行变化 | 必要现场先保护，复现或可靠观察、区分性证据、因果状态、最早源纠正、原故障重验、回Owner；环境变化先复核再动作 | 日志/Trace/测试/安全实验；间歇用重复时序、不安全用替代，Fallback不等价则停 | 保留不确定/阻塞，未复现不等于无故障 |

当前路由与依赖→识别要求→本地证据→选既有/原生/组合→固定原包和本地身份→对转换及依赖直接语义回查→真实加载验证→正常、Authority/Gate、异常、必要恢复→范围内READY/BLOCKED，细节以[接入](../skills/spec-harness-adoption/SKILL.md)为准。

可调整方法、路径、环境参数，不能把必要能力改可选或随转换改Pass Condition。未激活流程保留入口要求，激活前补验。原样复用须内容/依赖/作用域及证据仍有效，当前加载行为仍查。记录与授权在包外，不改原始身份。
