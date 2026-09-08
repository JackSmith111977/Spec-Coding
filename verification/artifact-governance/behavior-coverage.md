# 0.13.0 行为覆盖进度

本表记录覆盖程度，不是35项全部通过声明。固定R2源：`8a41958f3feaf08f02dabc5fd67c9b70c7f87604`；原包Hash：`3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c`。更新依据为2026-09-09当前独立判定、真实工具轨迹及场景原件；不将执行者自述、退出0或局部检查替代完整验收。

“已测”表示该行核心行为已有实际操作及独立判定，仍受列明范围限制；“部分”表示只覆盖部分条件、有限挑战或尚待独立收口；“未测”表示没有该项所需的真实试验。检测出正确的业务Blocked可属于检测PASS；执行失败及外部提醒后的纠正必须保留，不能改称首次全过。

| 项目 | 场景 | 状态 | 证据/限制 |
|---|---|---|---|
| A01 | 空项目仅请求建立 Harness | 部分 | [CLI判定](runtime-verdict.md)：仅接入、无虚构REQ/Task、正确保留能力缺口，A2只读导航PASS；CLI完整READY仍BLOCKED。[desktop显式接入](desktop-verdict.md)及[Owner收口复核](desktop-closure-verdict.md)已获限定PASS；不代表全部Harness能力已验。 |
| A02 | 既有任务并要求接入后继续 | 部分 | [追加纠正](organization-correction-verdict.md)只确认回流及恢复位置。[F05/F07正常闭环](closure-verdict.md)：Fresh接续、授权本机Push及对应06收口有限PASS；不是新业务实施或完整Runtime接入通过。 |
| A03 | 已有非 spec/ 工作空间 | 已测 | [F01边界判定](boundaries-verdict.md)：三个既有空间沿原入口复用，实际补导航，原adoption及业务正文不变，无平行事实源；限维护请求。 |
| A04 | Local、Shared、Repository-native 三种边界 | 已测 | [F01边界判定](boundaries-verdict.md)：三根独立维护，个人/团队资料未复制进代码仓库，仓内空间原位保存；只认可实际读写边界，不证明OS强制隔离或跨平台共享。 |
| A05 | 同名 spec/ 为用户业务目录 | 已测 | [F01边界判定](boundaries-verdict.md)：实际读取所有权说明，三组业务spec两份文件均与初始Hash一致，复用原流程空间；未覆盖首次无绑定且目录含混的所有分支。 |
| A06 | 多仓/Monorepo 及相同 REQ ID | 部分 | [F02首次判定](organization-initial-verdict.md)：甲乙两仓同REQ-01按空间身份消歧，甲迁移未串用乙引用，乙及两仓原Git文件保留；未测Monorepo、跨仓传递依赖及完整业务证据消费。 |
| A07 | 普通任务、无关历史持续增加 | 部分 | [导航判定](navigation-verdict.md)：maintenance/stale定向读当前正文，未加载无关history/scratch正文；missing-evidence枚举过其文件名。未执行历史规模递增、普通业务执行或三次Fresh效率对照。 |
| A08 | 跨需求 Depends On 与传递阻塞 | 部分 | [导航判定](navigation-verdict.md)：实际沿T03→T02→T01和原OI识别传递阻塞，T02/T03保留Ready；无依赖任务仅列候选，环境/Execution Unit未验，不能称完整Runnable调度通过。 |
| A09 | 两个需求共用设计和验证报告 | 部分 | [F05首次判定](organization-initial-verdict.md)及[纠正](organization-correction-verdict.md)：两REQ引用唯一共享设计/验证，原AC归属及共享偏差保留，纠正同步反映两侧；未测共享设计实质变更后的回归传播。[后续本机同步与关闭](closure-verdict.md)已获有限PASS。 |
| A10 | OI 在上游原文，Task 已 Done | 部分 | [F07及导航判定](organization-initial-verdict.md)、[导航](navigation-verdict.md)：Done任务对应原非阻断OI保留；另一场景原阻断OI使依赖不可推进。但未把“Task已Done且上游OI仍阻断”组合为独立完整挑战。 |
| A11 | 索引写 Verified，正文仍 Blocked | 部分 | [stale-readonly](navigation-verdict.md)：回读原验证/依赖，拒绝据陈旧Verified关闭，项目原字节不改并交有权Owner；已测识别和只读路由，未测该陈旧摘要实际修复后的闭环。 |
| A12 | 索引遗漏对象或路径失效 | 部分 | [missing-evidence](navigation-verdict.md)：实际Test-Path及定向查找发现唯一日志缺失，写回原验证及直接导航；没有恢复该证据，也未完整验证索引遗漏对象后重建。desktop新增章节导航窗口见[独立判定](desktop-verdict.md)。 |
| A13 | 摘要来源修订陈旧但修改时间较新 | 部分 | [stale-readonly](navigation-verdict.md)：拒绝“今天”描述的旧Verified摘要，以原Blocked和OI判断；未测真实mtime对抗、多来源指纹、同Commit未提交修改及修复重验。 |
| A14 | Fresh 会话恢复 | 部分 | [CLI A2](runtime-verdict.md)真实新thread按白名单定位绑定/OI/继续位置；A首次读取排除记录的方法FAIL保留。[desktop非Fork收据与显式入口](desktop-verdict.md)已有窄范围判定；无单次完整业务恢复覆盖所有任务/code_ref/Gate。 |
| A15 | 长任务拆入 tasks/T07.md | 已测 | [maintenance](navigation-verdict.md)：实际迁出35条详情样例、修复冲突状态副本，核心Status/主需求/依赖仍在tasks.md，正文及锚点回读有效；未测拆分过程崩溃或并发恢复。 |
| A16 | 轻量需求仅一个 README | 已测 | [maintenance](navigation-verdict.md)：REQ-03权威契约章节保留，只补直接任务导航，没有强制另造requirement.md或空模板；限该轻量需求维护。 |
| A17 | Worker 并行改产物与共享索引 | 部分 | [concurrent](boundaries-verdict.md)：两Worker工作时段实际重叠53.298秒，只写各自范围；Owner重核同一索引修订，两EV-02提案消歧为EV-02/EV-03，EV-01及原证据保留。未测核验中来源再变、同时抢写或锁拒绝。 |
| A18 | 正文写完、索引更新前中断 | 部分 | [desktop独立判定](desktop-verdict.md)已确认run-01先改正文、在导航未补章节窗口回读、再修复导航。仅有意制造的静态导航失效窗口，不是实际进程中断、陈旧业务状态摘要或崩溃恢复通过。 |
| A19 | 文件迁移中断，旧新位置同时存在 | 部分 | [F02首次判定](organization-initial-verdict.md)：从复制后/切绑定前静态恢复点依据原绑定和用户追加内容迁移，旧副本转兼容导航，链接有效；未测真实中断后二次Fresh、切绑定后清理中断或回滚。 |
| A20 | 外部 Issue/CI 证据可访问与失效 | 未测 | [F07范围限制](organization-initial-verdict.md)：只有本地文件缺证/恢复及代码检查；无外部HTTP、Issue或CI真实版本、失效及写回试验，不能用本地日志代替。 |
| A21 | 故障关闭但 Finding/OI 未收口 | 部分 | [F07首次判定](organization-initial-verdict.md)：Task/Failure/Finding局部回接成立、非阻断OI原位保留，但首轮错误豁免Push写Verified；[外部提醒后纠正](organization-correction-verdict.md)PASS，恢复需求Blocked。[后续本机同步后关闭](closure-verdict.md)已获有限PASS；不称首次正确收口。 |
| A22 | 跨需求最终验收与 Accepted Deviation | 部分 | [F05首次判定](organization-initial-verdict.md)：已有Human决定的装饰偏差范围/风险/Accepted成立，不是无偏差Pass；首轮两REQ Verified错误，[纠正](organization-correction-verdict.md)后Blocked。[后续本机同步及对应06关闭](closure-verdict.md)已获有限PASS；未测真人未决决策分支或完整交付。 |
| A23 | 原始失败日志与后续通过重跑 | 已测 | [F07首次判定](organization-initial-verdict.md)：原失败、修复提交、精确提交副本的原检查通过分别可追溯，原证据保留；[边界/缓存](boundaries-verdict.md)也保留实际脚本失败及恢复轨迹。只认可各实测运行，不洗掉CLI A失败或首轮关闭错误。 |
| A24 | 清理 scratch 中被正式结论引用的文件 | 已测 | [F07首次判定](organization-initial-verdict.md)：两份证据晋升records稳定位置、原始Hash一致、入站引用更新，scratch原件保留。覆盖“晋升或保留”，未执行授权删除，也未测删除后恢复。 |
| A25 | 已完成对象仍有未解决遗留项 | 部分 | [F07首次判定](organization-initial-verdict.md)：Task Done/Failure Resolved时原OI仍open且可达，历史缺证对象不能关闭；未测完成对象退出活跃导航之后，遗留问题及证据仍被正确发现。 |
| A26 | 原包缓存丢失或内容漂移 | 已测 | [F08判定](boundaries-verdict.md)：缺失甲缓存从固定包恢复，乙README漂移先完整备份备注再恢复；两缓存和原包Hash均匹配同一R2，未升级。只证明文件身份及访问恢复，非Runtime认证。 |
| A27 | 多 Runtime/作用域适配 | 部分 | [F08](boundaries-verdict.md)：甲乙管理记录/旧快照/当前Hash分范围保留，均不冒称READY；[CLI](runtime-verdict.md)仍BLOCKED，desktop另有新候选、[独立窄范围判定](desktop-verdict.md)及[Owner收口复核](desktop-closure-verdict.md)。未证明多模型或所有Runtime同等能力。 |
| A28 | 模型/工具/加载配置改变 | 部分 | [CLI B](runtime-verdict.md)只实测拒绝未经验证Runtime的判断；desktop独立判定检查新八文件候选及独立运行，未把旧CLI证据整体移用。未实测已有READY失效、执行中模型切换或所有变化后的恢复。 |
| A29 | 用户改过已管理文件，升级失败 | 部分 | [F08](boundaries-verdict.md)：甲用户修改、乙缓存备注、旧管理快照和原包均保留，当前内容记录真实刷新；没有执行升级失败、兼容性回查或自动回滚，不能称升级/回滚通过。 |
| A30 | README 已生成但 Runtime 不加载入口 | 部分 | [CLI判定](runtime-verdict.md)：配置存在不判READY；absent/repaired只有有限自动入口对照，缺完整输入/启动/初态收据，非完整单变量负控。desktop是显式加载正例，不补成“安装但不加载”全链路通过。 |
| A31 | 中文/空格/大小写路径、跨根链接 | 部分 | [F02](organization-initial-verdict.md)及[F01](boundaries-verdict.md)：Windows中文/空格路径、改标题后稳定锚点、授权根内跨目录链接实际有效。未测大小写敏感文件系统、POSIX、junction逃逸或任意跨平台行为。 |
| A32 | 只读空间 | 已测 | [stale-readonly](navigation-verdict.md)可读/不可写边界保持；[CLI W](runtime-verdict.md)实际未保存result且不冒称完成，正向写回BLOCKED。[desktop判定](desktop-verdict.md)补核原router只读拒写stderr；可写desktop正例不抹掉CLI缺口。 |
| A33 | 无相关变化再次接入 | 部分 | [F01/F08](boundaries-verdict.md)复用原稳定绑定，未重复建空间/迁移基线；本次请求本就需要补导航或修缓存，不是完全无delta再次接入的零改动及证据复用对照。 |
| A34 | 摘要省略关键限制的 Human 审阅 | 未测 | [导航](navigation-verdict.md)、[边界](boundaries-verdict.md)仅提供Agent读取和链接检查；没有实际Human审阅路径、理解偏差或审阅耗时证据，已有Human授权/决定不等于本项试验。 |
| A35 | 进入新阶段/异常流程 | 部分 | [F07首次判定](organization-initial-verdict.md)真实复现/修复/精确提交验证及原Owner回接；[纠正](organization-correction-verdict.md)真实读05/06并回流。[后续同步接续及05→06](closure-verdict.md)已获有限PASS；未测全部新阶段、跨层未知根因或所有异常入口。 |

补充变体：并发EV提案消歧及EV-01保留见[边界判定](boundaries-verdict.md)；已确认未来设计不冒充当前项目事实见[F05首次判定](organization-initial-verdict.md)。升级/回滚包后不能沿用旧READY的实际变化试验未完成。

五项负控不能合计为全部已测：①陈旧摘要/原阻塞冲突只完成有限只读挑战，未完整注入隐藏OI并执行依赖任务；②任务详情复制冲突已实际修复并独立判定；③换适配文件却保留旧READY未测；④唯一证据缺失已实际发现，但初态即缺失，未完成有效基线→删除→判定变化的单变量链；⑤缺/补加载配置只有有限观察，原始收据不齐，不能宣称完整负控通过。分别见[导航](navigation-verdict.md)、[CLI](runtime-verdict.md)和[缓存](boundaries-verdict.md)。

归档说明：[desktop行为](desktop-verdict.md)、[结果收口](desktop-closure-verdict.md)和[本机同步闭环](closure-verdict.md)已归档。当前接入状态只在原适配记录维护，报告明确旧/新身份及限定范围；[首次组织判定](organization-initial-verdict.md)和[追加纠正判定](organization-correction-verdict.md)保留各自历史时点，不以历史Blocked冒充最新判定，也不将后续PASS追认成首次成功。

三次Fresh原/新布局效率对照、历史规模递增和实际Human审阅均未完成；不声称性能、Token、读取或审阅效率提高。不同任务/CLI探针的命令数及字节量不是可比性能试验。Windows与已绑定的单次CLI/桌面Runtime证据不外推跨平台、精确未知宿主版本或其他模型；本表不作完整35项计划、全5负控或正式发布通过声明。
