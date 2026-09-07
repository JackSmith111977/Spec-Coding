# 目标侧本地适配独立语义回查 R2

结论：**BLOCKED**。原包 P 与本地候选 L 的身份和文件完整性均核验通过；L 删除了原包的实质行为，不能证明完整组合保真。发现 8 项阻塞问题。结论来自直接阅读双方全部资产，不以另一通道是否成功执行业务作为依据。

## 身份、输入与边界

本报告中路径前缀具有以下唯一含义，所有行号均为实际文件的一基行号；例如 `P/rules/global.md:21` 精确指向下述 P 目录中的该文件。删除位置用 L 中相邻现存行或 EOF 定位，不虚构本地存在已删除正文。

| 身份 | 完整目录 | 固定 package_sha256 |
|---|---|---|
| P：未修改原包 | `C:/Users/hp/Documents/ChatGPT/Spec Coding/.harness-staging/s06-b-r2/original-harness/` | `4451d39351a32576e99552aada821f98cc69f0c087e041273d294e6bc332db9b` |
| L：目标侧本地转换候选 | `C:/Users/hp/Documents/ChatGPT/Spec Coding/.harness-staging/s06-b-r2/harness/` | `d320513e8e29116d79903946f6edaba18eeaa25ebbd7ca8b6f04937d0444dad7` |

两侧 manifest 均声明 version=`0.12.0`、source_revision=`2f585f0faa8c0ba831161858a2e1418fd2d527e7`、build_mode=`FULL`。这里以固定 P 的实际完整行为作为本地转换的比较基准；不重新裁定其 Canonical 编译正确性，也不把相同 source_revision 当作本地保真证明。

本轮直接完整读取 P 的 23 个文件和 L 的 23 个文件，包括全部 11 个 Skills、4 个共享规则、接入参考资源、入口/路由/能力要求、README、plugin、脚本和双方完整 manifest。对共同段逐行显示正文并标注双方行号，对变化段逐行显示双方内容；字节相同文件在核对双方原始字节后完整读取。manifest 分段读取至双方第 558 行。不是仅看 diff、搜索命中或文件名。完整读覆盖为 P 1390 行、L 1365 行，详见文末逐文件清单。

未读取 coordinator-input.json、Oracle 内容、Builder 变异/修复摘要、协调者解释、任何行为测试回报或其他 Reviewer 报告作为本轮输入。未读取业务实现、测试实现或运行它们；未跟随项目 OI 中指向行为执行记录的 evidence 链接。本轮仅额外直接读取用户允许的两份项目权威文件以识别任务和 OI 适用范围。只写本报告，不修改 P、L、Canonical 或项目资产，不向另一个盲测通道发送报告。

## 完整性与变化核验

按 `P/README.md:17` 的算法独立计算：包内 POSIX 相对路径排序，每行由原始文件字节 SHA-256、两个空格、相对路径、换行组成，整体再取 SHA-256；包含 manifest。所得 P/L Hash 均与用户固定值精确匹配。

实际执行以下只读包完整性检查，均退出 0、报告 integrity=PASS、files=23，并分别返回上述 P/L Hash：

```text
python -B .harness-staging/s06-b-r2/original-harness/scripts/verify.py .harness-staging/s06-b-r2/original-harness
python -B .harness-staging/s06-b-r2/harness/scripts/verify.py .harness-staging/s06-b-r2/harness
```

另行内存核对双方各 21 项 artifact 的范围哈希，全部匹配；dependencies 的 ID 均存在，Markdown 本地链接目标均存在。双方均无增删文件。13 个文件字节完全相同；9 个行为文件共删除 25 行完整行为正文，无新增行为行；另有 manifest 的对应哈希更新，共 10 个文件改变。剔除 sha256 与 files 哈希映射后，双方 manifest 元数据完全相同。完整性自洽没有检测到下述行为丢失，`scripts/verify.py:48–64` 本来就不执行语义审查。

## 阻塞 Finding

### B01：共享 OI 生命周期及不可裁剪约束被删除，所有流程的共享依赖发生变化

- 原包：`P/rules/global.md:7,21`；本地：`L/rules/global.md:5–8,18–23`。L 保留深度选择以及“开放项传递”标题，但后者正文为空。原第 7 行位于 L 第 6/7 行之间的删除点，原第 21 行位于 L 第 19/20 行之间的删除点。
- 丢失行为：任意执行深度都不能裁掉 Blocking OI、必要 Gate、风险相称证据、授权、决策就绪与纠偏链；OI 首次建立条件、稳定 ID、必需事实字段、open/resolved/deferred、resolved 的结论依据、deferred 的理由和承接位置、同 ID 单一事实源、blocking 不越对应 Gate。部分跨流程重复保障也在 B03–B07 中同时消失。
- 消费者影响：`L/rules/global.md:3` 仍要求所有正式主流程/异常流程加载共享规则；各 Skill 的全局引用仍指向该削弱文件。01A、01B、05、07 即使自身字节没改，组合依赖也已变化。新 OI、跨阶段承接和延期情形缺少完整共同执行契约；不能凭这些消费者自己的文件哈希复用旧组合通过证据。
- 保留边界：L 全局第 12–16 行的三类权限与授权复用仍在；05 第 12 行仍要求无有效 Blocker，04 第 28 行仍禁止 Task 完成自动关闭 OI，06 第 18、38 行仍区分/引用 OI。这些局部保障不能补回完整的全局 OI 生命周期及所有深度的不可裁剪约束。本 Finding 不声称 L 已取消全部权限或所有门禁。
- 严重性：阻塞；它改变原包执行含义，不是字段排版偏好。

### B02：15 个消费者仍声明必需的权限／状态能力已无定义和可观察验收

- 原包：`P/bootstrap/requirements.md:9` 的 `authority-and-state` 整行；本地：`L/bootstrap/requirements.md:8–9` 从 identity-and-scope 直接跳到 trace-and-evidence，全文无该 ID。
- 两侧 `manifest.json:23,41,60,81,104,127,150,173,196,220,246,271,294,313,334` 仍引用该要求。消费者是四个规则及全部 11 个 Skills。`manifest.json:342` 等要求定位仍指向本地 requirements 文件。
- 丢失行为：授权复用与 Human 边界、单一事实源/稳定 ID、blocking OI/必要 Gate、Meta 不继承 Workflow Task Gate 的要求→实现→可观察验收→失败回流契约。尤其“已授权局部动作继续、未授权 AC/风险接受停止、blocking 不过 Gate”的验收目标不再由此能力项承载。
- 消费者影响：接入的逐项能力发现和验收没有可解析的对应定义；manifest 仍声称同样的需要和来源，却不承载原有验收内容。普通 dependencies ID 检查全通过，不能弥补 requires 指向不存在的能力定义。
- 保留边界：`L/bootstrap/requirements.md:16,18` 和本地接入第 34、36 行仍要求 Authority/Gate 检查及原包预期不变；正因这些规则仍在，删除该定义不能被解释为合法调整验收方法。应恢复等价行为与可检验映射，单补一个 ID 名称不足。
- 严重性：阻塞。

### B03：有效协作反馈更新权威源及跨阶段承接程序消失

- 原包：`P/rules/collaboration.md:10`；本地：`L/rules/collaboration.md:9–10`，原编号 6 的程序被删除，第 10 行直接进入原编号 7 的共享模型修复。
- 丢失行为：有效反馈改变依赖事实时，应找到最早权威来源；稳定意图/绑定更新 Adoption Baseline，Workflow 语义更新对应产物；下游引用新来源，仅刷新受影响 Trace；无法决断且需下游承接时复用 OI，且同步完成不表示阻塞解除。
- 消费者影响：双方全局第 3 行及 Skills 均要求使用协作程序，元协议也明确复用适用协作规则。因此这影响业务流程以及保持原字节的两个 Meta Skills。一般的“引用/更新已有产物”和旧模型修复仍在，但不能等价替代这套正向反馈落位及阻塞承接程序。
- 严重性：阻塞；不是仅因编号跳号。

### B04：需求澄清丢失 OI 承接、范围规则固化及向 AC/Design 移交条件

- 原包：`P/skills/spec-requirement-clarification/SKILL.md:24,30,32`；本地：同相对路径 L 第 `23–25,28–31` 行的空白删除点。
- 丢失行为：跨阶段 OI 的必要信息、已解决/延期处理和同 ID 承接；固化歧义解释、范围取舍、核心规则与非阻塞 OI；不通过默认假设关闭未知；Scope & Rule Definition 所承载的 In/Out Scope、边界、规则和决策；关键未知回歧义步骤，必要 Human 决策完成且不阻塞 AC/Design 才移交。
- 消费者影响：03/04 接管的范围、固定规则和 OI 缺少完整上游形成程序，后续不能仅根据笼统“必要决策已完成”恢复被删的关键未知回流与稳定结果。L 第 8、35、39 行及全局 Human Decision 仍保留相关授权边界，本 Finding 不把它们误报为整体消失。
- 严重性：阻塞；问题在决策/未知的处理和交接语义，不要求照搬普通章节格式。

### B05：技术设计丢失基线推进、假设验证、阻塞回流与 Ready 判定

- 原包：`P/skills/spec-technical-design/SKILL.md:16,36,42,44,46`；本地：同相对路径 L 第 `15–17,34–36,39–41` 行及第 41 行 EOF。
- 丢失行为：Impact Baseline 的可解释/可追溯且无重大未知才继续；需求歧义回02、技术缺证继续取证；详细设计形成与最早上游回流，以及不下沉具体文件/函数/实现步骤的层级边界；关键假设用实际证据判断 Validated/Open/Invalid；阻塞 OI 不进实施，按需求/影响/核心决策/细节分流并沿同 OI 更新 resolution、重验受影响 Trace；Design Acceptance Result 的 Ready/Not Ready 条件及只有 Ready 可移交04。
- 消费者影响：`L/bootstrap/routes.md:15` 仍以设计 Ready 路由04，但 L 设计正文的就绪结果契约已丢失；B06 又删除接收侧的完整准入，形成跨阶段组合缺口。L 第 38 行的覆盖/一致性检查不能补齐假设证据状态、阻塞处理及稳定交接判定。
- 严重性：阻塞。

### B06：实施规划丢失接管契约、风险/OI 承接和 Executability 实际检查

- 原包：`P/skills/spec-implementation-planning/SKILL.md:12,14,18,28,57`；本地：同相对路径 L 第 `11–14,15–17,24–26,52–53` 行的删除点。
- 丢失行为：仅接管最新已收敛且 Ready、无阻塞规划实施 OI 的设计，Not Ready 回 Owner；最终确认事实优先、上游引用及原 OI 状态/Owner 承接；Implementation Baseline 的实际内容与无过时/冲突/不可追溯/阻塞才继续；风险绑定 Coverage/后续验证、可独立验证 OI 任务的 Trace、阻塞回流和 Candidate Task Set 阶段边界；Executability 的无循环依赖、真实阻塞依赖、上下文可得、无未定义中间契约/基础能力及遗漏 blocking OI 的检查。
- 消费者影响：05 第 12、14 行需要 Ready 任务及有效约束，06 第 12 行接收 Implementation Baseline，但相应生产/接管程序已削弱。L 第 51–53 行只剩三个验收维度，第 57 行却仍要求“四维通过”并记录 Executability: Pass，存在检查内容缺失与结果声明的组合不一致。
- 保留边界：L 第 3 行仍描述接管 Ready 设计；第 28、33、39、57 行保留 Draft→Ready、无未处理阻塞、Ready 非 Runnable 等要求。故缺陷不是“完全取消规划 Gate”，而是原本足以执行该 Gate 的输入/检查/交接内容丢失。
- 严重性：阻塞。

### B07：正式验证丢失纠偏重验闭环、Finding 状态所有权和最终关闭条件

- 原包：`P/skills/spec-verification-convergence/SKILL.md:42,44,52,54`；本地：同相对路径 L 第 `41–44,49–50` 行空白及第 50 行 EOF。
- 丢失行为：纠正源→受影响 Trace→刷新基线→重验/必要回归的闭环；OI 只有实际解决且有结论才 resolved；Debug Closure 只是证据，Finding 生命周期由06判定；Finding Resolution 的 Decision、实际 Authority、Status、回流和重验范围；Verification Converged/Blocked 判定；Required Verification、必要 Gate、关键 Finding、无阻塞 OI 和追溯完整共同成立才 Verified，否则 Blocked；Closure 中 Decision 与 Status 分开、Gates 与阻塞原因显式记录。
- 消费者影响：05 第 59 行仍移交06；L 06 第 46 行要求汇总 Finding Resolution/重验，第 48 行仍检查 Trace，但其生产与最终状态判定程序已不完整。Debug 回传也失去本阶段明确的状态接管边界，07失去明确的最终关闭记录承接。
- 保留边界：L 第 8 行仍禁止把 Task Done/Push 当 Verified，第 36 行仍规定 Accepted Deviation 属 Human Decision、不能跳 Gate/标 Pass，第 38、40 行仍有 OI 区分与最早源路由。因此不能把缺陷描述成 Accepted 已被直接改为 Pass；缺陷在明确生命周期和必要关闭条件被删，剩余原则不足以保真。
- 严重性：阻塞。

### B08：Debug 丢失阶段推进/阻塞条件及 Failure Closure 契约

- 原包：`P/skills/spec-debug/SKILL.md:20,30,50`；本地：同相对路径 L 第 `19–21,28–30,47–49` 行的删除点。
- 丢失行为：Failure Baseline 的故障引用/现象/预期实际/影响/现场/复现/证据，以及可靠复现或观察成立才定位、否则记录缺口阻塞；从系统到 Fault Boundary 的逐步缩小及按需 Good/Bad/Bisect 指导；Fault Localization Result 的证据、假设状态、定位范围和不能继续时的缺证阻塞；原故障消失且必要受影响验证通过才 Failure Closure.Status=Resolved，否则 Blocked；Residual Risk/OI、Correction 来源、适用 code_ref、Recheck/Reverification/Trace Status 的关闭承接。
- 消费者影响：`L/skills/spec-development-execution/SKILL.md:46` 仍要求 Debug 的 Root Cause、Correction、Closure，`L/skills/spec-verification-convergence/SKILL.md:38` 仍可触发 Debug；L Debug 第 49 行仍回 Owner，但回传结果的关闭判定与必要证据已不完整。
- 保留边界：复现、定位证据、假设/根因状态、实际重验、复用验证程序和 Owner 状态边界的其他正文仍存在。本 Finding 不声称整个 Debug 程序不可达或已允许无验证关闭，而是其明确阶段产物、可推进标准、阻塞结果与最终 Closure 契约失真。
- 严重性：阻塞；不仅是产物命名或排版差异。

## 非阻塞差异、保真部分及组合判断

`P/bootstrap/routes.md:26` 被删除，对应 `L/bootstrap/routes.md:25` EOF。该行包含执行中环境变化前复核、不能复用旧 READY、稳定绑定变化才回项目接入及不可裁权限/OI/Gate。其运行中变化部分仍由双方未改的 `bootstrap/BOOTSTRAP.md:12`、`skills/spec-harness-adoption/SKILL.md:52`、`rules/delegation.md:45` 承载，不另报“整个运行中恢复机制丢失”的阻塞；OI/Gate 的共享削弱计入 B01/B02。编号、空白、章节排列不作为阻塞依据。

13 个未改文件全部重新直接完整读取，并非沿用 R1/R2 报告。保真的内容包括：安装前 Bootstrap 可读及渐进路由；plugin 的 Skill 发现；11 条 Skill 入口仍可达；01A/01B 的建模职责；05 的 Runnable 前置、Task Commit/code_ref、正式验证与 Task 状态、依赖任务不机械级联 Blocked、同 REQ 集成与 AC Gate/授权 Push 的区别；委派 Main/单写 Owner/权限/候选结果及隔离要求；代码质量；07的证据与改进权限；两个 Meta Skills 的稳定意图/绑定与运行事实分离、受控候选例外及适配失败路由。这些均未因文本删减而完全消失。

但是，`L/bootstrap/BOOTSTRAP.md:8` 和本地接入第 16、28、34 行仍将共享规则、当前 Skill 及依赖作为实际组合的一部分。未改消费者仍读变化后的 global/collaboration/requirements；“自身原样”不等于“依赖与作用域不变”。本轮没有用同文件 Hash 代替完整组合判断，也没有用原包在 Reviewer 上下文中的内容替 L 补充运行知识。

没有发现新增行为正文或新增强制义务。manifest 的 sources/dependencies/requires 保留了 P 的声明，路径也仍可达；对发生语义删减的资产而言，这些声明及重算哈希不能证明原行为仍被完整承载。B02 还存在实际能力定义缺失。本报告不把未改的 P 来源映射重新宣布为 Canonical 审查通过。

## 项目适用范围与并发变化边界

仅额外读取以下两份允许的权威文件：

- `C:/Users/hp/Documents/ChatGPT/Spec Coding/.harness-staging/s06-b-r2/project/spec/tasks.md`，全文 1–23 行。
- `C:/Users/hp/Documents/ChatGPT/Spec Coding/.harness-staging/s06-b-r2/project/spec/open-items.md`，首次全文 1–8 行；后续变化后全文 1–11 行。

首次读取时，T01/T02 均为 Ready，T01 引用 OI-021；OI-021 为 open、blocking=true、Owner=development-execution，内容为等待测试管理员确认当前目标目录可写。由此可确定 OI/权限/调度语义在当前任务中实际相关，而不是无消费者的闲置文字。

在本轮继续只读核验期间，这两份权威文件出现并发修改。于 `2026-09-07T05:58:07.749785+00:00` 再次直接取同一读取内容计算 Hash 并显示全文时：tasks.md 第 4 行为 In Progress，第 16 行 T02 仍 Ready，第 20 行仍依赖 T01；open-items.md 第 5–6 行改为 resolved/false，第 9–11 行新增 resolution/evidence/resolved_by。该时点身份为：

| 权威文件 | SHA-256 |
|---|---|
| `project/spec/tasks.md` | `1ffea41e87b297cb193baf6858fa5fd6ad04b2742b6ed1933f85d96d709469dd` |
| `project/spec/open-items.md` | `ff0321ad34d91be9ba16bed7ab07e6b31278e540352b91c5ed72962322b051bd` |

这里仅记录允许读取的权威文件在不同读取时点所声明的状态，**不验证该 resolution 的真实性、充分性或执行者权限**，不打开其第 10 行引用的行为记录，不把它作为 P/L 保真依据。没有把首次 open 状态误写成审查结束时仍 open，也不根据本次语义删减推断某次业务动作必然越权。L 的05仍保留“Ready、依赖满足、无有效 Blocker、环境可用”的调度条件，不能忽略这项反证。对 OI-021 应否以具体环境探测解除，本通道没有读取相关授权和执行证据，不作行为判决。

上述并发修改不影响绑定固定 P/L Hash 的 B01–B08：OI 建立、跨阶段承接及关闭要求在转换中确实丢失，即使某个现存 OI 已有完整字段，数据自身也不能代替供后续消费者执行的通用程序。未激活的设计、规划、验证和 Debug 仍包含在完整 L 候选中，不能因当前任务从05开始而将这些入口的语义损失判为保真；激活范围内至少共享依赖与能力定义已经受影响。

## 最早回流点与复核要求

最早失真源为 **P→L 的目标侧本地转换/提取/装配**。回到双方均未修改的 `skills/spec-harness-adoption/SKILL.md:24–30` 第3节“选择、装配与固定本地候选”，对应第 45 行“实现映射/组合/本地配置错误→适配装配”。这是本次适配保真失败，不要求修改 Canonical，也不把 B04–B08 误路由为真实项目需求、设计或业务代码的修复任务。

修复应恢复上述实际行为及其共享消费者承接，或提供逐项等价且进入实际加载面的实现；不能只补空标题、要求名称、哈希或通过声明。按接入第 34、48 行，受影响证据失效，修复后固定新 L 身份，重新检查共享依赖和全部受影响阶段/异常组合，并在独立行为通道按原包固定预期验收。本报告不替代真实加载/行为验证、不宣称候选 READY；也不以改变验证预期来消除语义缺失。

全部分配的本地资产及其原包对应资源已完整读完，BLOCKED 原因是已确认语义损失，而不是读覆盖不足。以下清单记录本次直接读取的完整范围及文件字节身份。

## 逐文件完整读覆盖与固定字节证据

下表相对路径分别与前述 P、L 完整目录拼接，构成双方具体路径。完整范围包括空行；“相同”仅表示文件字节相同，不表示变化后的依赖组合已通过。

| 相对路径（P 与 L 各一份） | P 完整读取行 | L 完整读取行 | 变化 | P 文件 SHA-256 | L 文件 SHA-256 |
|---|---|---|---|---|---|
| `README.md` | 1–27 | 1–27 | 相同 | `66e31f7e58e74b01c731e40f1f5830d06f25980b5654eb3108099a9c7e7c21f9` | `66e31f7e58e74b01c731e40f1f5830d06f25980b5654eb3108099a9c7e7c21f9` |
| `bootstrap/BOOTSTRAP.md` | 1–12 | 1–12 | 相同 | `40784682fa52df74b9006d3f7b11f410fad2a385028c51c86a40bf2969f550e2` | `40784682fa52df74b9006d3f7b11f410fad2a385028c51c86a40bf2969f550e2` |
| `bootstrap/requirements.md` | 1–19 | 1–18 | 正文删除 | `ab68478fe5e106bfbc1a5d8fb1a701d8d9f1856e8fb7022d85704bf0da638c66` | `06b88f40cc9fcf42204a88979fe3ca9d169409a8f320a83478cd8fc1e9b56299` |
| `bootstrap/routes.md` | 1–26 | 1–25 | 正文删除 | `704704864ffd62ab555df40b0ce718a205bfe34b8db0581d0192fa58dc5778d8` | `53a0af43975736c64561de0659c822043e1f88d07e3f89fb2c8b9886f7b264cf` |
| `manifest.json` | 1–558 | 1–558 | 哈希更新 | `eed8d83f7d3db9b454d6e264aafbb6517dd65fc4b34a28ee2304527ba5e6ad79` | `f38a5a17bc9362c03a02b7e190c2c4d7a319de0ebd04db9929b5c9f4bf837f38` |
| `plugin.json` | 1–7 | 1–7 | 相同 | `5ce1881e1359dfb7657c041c8cdb9826db14335cfc8f01eb95450bae4a2c6c80` | `5ce1881e1359dfb7657c041c8cdb9826db14335cfc8f01eb95450bae4a2c6c80` |
| `rules/code-quality.md` | 1–8 | 1–8 | 相同 | `7f6b0e5d05f8a79778dda950844ce3f0bf0aeccd3d9c0666eb307f1c9b3cae89` | `7f6b0e5d05f8a79778dda950844ce3f0bf0aeccd3d9c0666eb307f1c9b3cae89` |
| `rules/collaboration.md` | 1–13 | 1–12 | 正文删除 | `7ee8da4fbf8fea89fac19f864700d3772f3f489a53a17cc1057e49168768b413` | `3e32fe2418f9c84ba5d9337c1fd9c094c392833bfa64de124088f0c1267abea5` |
| `rules/delegation.md` | 1–45 | 1–45 | 相同 | `8a70b666b2fbcb4cfdbe042f5fd52cb7334ace01cae165878f26ea7057baf20e` | `8a70b666b2fbcb4cfdbe042f5fd52cb7334ace01cae165878f26ea7057baf20e` |
| `rules/global.md` | 1–25 | 1–23 | 正文删除 | `9871584999e6d58f9e7cc67bcc712f91bf2c06a4896dd5d585e1b18eca5d015a` | `3089f1b4ab47830af38c9a147f62e422b08b26f97fb85c81e2d2e725bd37a9f1` |
| `scripts/verify.py` | 1–72 | 1–72 | 相同 | `62812b7c380421b2dbfb62aa84a72b1543b0efc50c5bf7ca3b7066bbd0b1c6bc` | `62812b7c380421b2dbfb62aa84a72b1543b0efc50c5bf7ca3b7066bbd0b1c6bc` |
| `skills/spec-debug/SKILL.md` | 1–52 | 1–49 | 正文删除 | `a4b2f6d51b338b76e91d42821a1e6cd44285a69e91c21ee867ff3c351597a26c` | `9c34c6767ccd7cef3ec0b1c26d331b8fcd354b4349787e884a19a44b6de7afd2` |
| `skills/spec-development-execution/SKILL.md` | 1–61 | 1–61 | 相同 | `91c74ffb3c020db1468d2abe19eaa281a8278b3deef72577433099293e821147` | `91c74ffb3c020db1468d2abe19eaa281a8278b3deef72577433099293e821147` |
| `skills/spec-harness-adoption/SKILL.md` | 1–54 | 1–54 | 相同 | `5db3edf416e284ac1b2f62248a61ec327091d3478ed7b4e6c99883543767c664` | `5db3edf416e284ac1b2f62248a61ec327091d3478ed7b4e6c99883543767c664` |
| `skills/spec-harness-adoption/references/candidate-validation.md` | 1–9 | 1–9 | 相同 | `8d0bf9d5e4a2ecb24345c8f51be57d9fbcd22e52fec19b6df78007039cacafd4` | `8d0bf9d5e4a2ecb24345c8f51be57d9fbcd22e52fec19b6df78007039cacafd4` |
| `skills/spec-implementation-planning/SKILL.md` | 1–62 | 1–57 | 正文删除 | `394be7b2f687afd9cdf0df60e6f5dfc91cbd8ccc1291598d2f44b35fed2a6b9f` | `eec54c9eeaf26ca0defb87b1541f1386215d12ca9f140ee90e314779c83aff6d` |
| `skills/spec-process-improvement/SKILL.md` | 1–48 | 1–48 | 相同 | `b9d3fc13208c4090a1cc3d436ae9bfd9710374d9f37f62e157939f433e8db123` | `b9d3fc13208c4090a1cc3d436ae9bfd9710374d9f37f62e157939f433e8db123` |
| `skills/spec-project-definition/SKILL.md` | 1–54 | 1–54 | 相同 | `0591557d42d56da275d0007fa61e3aa042af38a518d09e873666d9a1ac83e463` | `0591557d42d56da275d0007fa61e3aa042af38a518d09e873666d9a1ac83e463` |
| `skills/spec-project-onboarding/SKILL.md` | 1–44 | 1–44 | 相同 | `3abbd8c7b6dc765111a9d9c58b055db6d5b131d86a5ac1696ff77267dc4713ab` | `3abbd8c7b6dc765111a9d9c58b055db6d5b131d86a5ac1696ff77267dc4713ab` |
| `skills/spec-project-understanding/SKILL.md` | 1–52 | 1–52 | 相同 | `b750a21f1992a4f977200bac7afb97dc022067b76c512c8eb75d15f9e2f63878` | `b750a21f1992a4f977200bac7afb97dc022067b76c512c8eb75d15f9e2f63878` |
| `skills/spec-requirement-clarification/SKILL.md` | 1–42 | 1–39 | 正文删除 | `3bed21544cc133281660e51d483b6d9406b6d233484169d6cdb85c71f71c09c8` | `f14846ddb1ad29332124c23568badf62874dce293f8c9e03b817a4122840cfd0` |
| `skills/spec-technical-design/SKILL.md` | 1–46 | 1–41 | 正文删除 | `8d61c6eb2d5a4b61ee789cb67145fe2c67023d3b78b8af334147adbe647dbec7` | `425b38447b63c93d2f1dbcc86c5697825d0dcf23ca417110b3a6eaf4829d83b3` |
| `skills/spec-verification-convergence/SKILL.md` | 1–54 | 1–50 | 正文删除 | `b6458519f2f62d44499644186b9ba5366042e9008ef641aae6535f23a1f2fad9` | `241c82e53f6313bdc2b305298a32b231c92a495d6761e3298f5575de8dd5abb8` |

写入清单前再次以全部实际文件重算 P/L 树身份，仍与本报告固定 Hash 精确一致。审查过程没有写入上述两棵候选树或项目资产。
