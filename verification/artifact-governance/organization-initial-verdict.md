# R2 产物组织场景独立行为判定

2026-09-09。**整体 BLOCKED：F02 限定范围 PASS；F05 BLOCKED；F07 BLOCKED。**

本次只审查已经停止的三组行为。读取了相关完整 Canonical、固定包程序、REQUEST、真实正文/快照、保存脚本、coordinator-tools.jsonl、初始哈希清单和 r2-selected-fixture-oracle.md；未以执行者声明或自写断言替代独立语义判断。未运行行为检查、执行者脚本或 Builder；只写本报告，R1/R2历史报告保留。

下文 Fxx 路径相对 `.harness-staging/v013-r2-organization/`，docs 路径相对工作区；JSONL行号指整个调用/返回事件。

## 固定身份与证据可信边界

- source_revision：`8a41958f3feaf08f02dabc5fd67c9b70c7f87604`。
- 包 SHA256：`3a32530d2d28dd43b8c0afed75faa13c130a04d39b78cfce6afa7ed81906540c`。独立按相对路径排序、原始文件字节哈希重算，三组各24文件均匹配。
- 直接读取 docs/manifest.yaml；复用此前完整相关原文读取，本轮完整重读06四篇、Debug四篇、05第4篇及项目接入协议。manifest、五规则、两Meta及05/06/Debug共20个文件与固定commit比较，除CRLF/LF外无差异；未扩展全Corpus。
- 初始清单逐项比较：F02共43个非Git文件，改变10个迁移相关文件；F05共38个，改变7个spec文档；F07共36个，改变app.py及4个spec文档。三组均无初始文件丢失。三组修改前快照分别11/7/6份，全部匹配维护者初始清单。
- F02两仓、F05仓的全部初始Git文件未变。F07新增修复提交，5个初始Git文件改变（提交消息、index、HEAD/分支reflog、分支ref），其余初始Git文件未变。
- 工具轨迹导出分别26/32/28行；重算SHA256分别为 `919bf77d477ca7555d4ff554b410cbebbb3035e3474258a6d6b21fb6bfbfb96f`、`2d50482a0d953f3df0e9c4260aa65312a794400a1bc0c933faf9974002814198`、`1af021353a7cd0be060b75d50f38c32413fbc436e67a722410b7102d333bd2f6`，均与导出identity一致。未另行审计原始会话文件；identity只用于绑定导出，不证明行为PASS。

## F02：限定范围 PASS

**结论：** REQUEST要求的甲空间资料迁移、引用、身份及用户资料保护成立；不扩张为正式Task关闭或完整Runtime验收。

**具体证据：**

- `records/coordinator-tools.jsonl:13–22` 先读旧绑定、旧任务/正文、迁移记录及新副本；`:23–24` 实际保存11份快照并迁移，返回0；`:25–26` 执行核对，返回0。独立比对实际文件，不以脚本“33项通过”作为结论。
- `新 空间/requirements/REQ-01.md:1–8` 与初始旧正文相比仅替换展示标题，完整保留用户补充、甲空间::REQ-01、AC及req-01锚点。复制时正文与用户补充后正文均有匹配初始哈希的快照。`迁移记录.md:2–4,8–10` 保留先复制、后补充、再切绑定的依据，没有按修改时间盲选。
- 新adoption第2–7行仍绑定repo-a；当前入口第2行改向新空间，第3行乙入口未改。旧README/adoption/tasks/REQ均明确是兼容导航；新正文是唯一可修改权威。当前正文及非历史记录34个Markdown链接/适用锚点独立核对可达。
- repo-a、repo-b当前HEAD分别仍为 `6ff6f8fec903b7463cb5cc074684cd0522be9d3f`、`fbff448438b55c90c07a2d6a7aab8a3720f1936a`；两仓identity、乙空间全部原文件及两仓初始Git文件字节未变。甲Task没有串用乙仓引用。执行者未宣称核验既有commit，本审查的Git对象确认不倒填为当时行为。
- 新tasks第3行保持Ready，第11行明确交原Owner正式收敛；没有因迁移自动写Done/Verified。符合项目接入协议第157–160行及产物规则身份、引用、保护要求。

**未测限制：** 覆盖A06、A19复制后切绑定前的静态恢复点、A31中文空格路径/稳定锚点。未测真正中断后第二Fresh恢复、切绑定后清理中断、Monorepo/传递依赖/并发ID、junction逃逸、POSIX与大小写敏感文件系统，以及正式Task验收。以上不升级为新Gate。

## F05：BLOCKED

**Finding ORG-R2-F05-01：未完成必要上游同步却写两需求Verified。**

- 位置：`spec/tasks.md:15` 自行写“Push不适用且未执行”；`spec/closures/REQ-01.md:2`、`REQ-02.md:2` 均写Verified，第5行以无代码集成变化、无远程Push说明门禁。实际写入见 `records/coordinator-tools.jsonl:29–30`。共享verification第28行也确认未Push。
- 原Gate：`docs/workflows/main/05-development-execution/04-state-commit-and-continuous-progression.md:97–102,139–141` 要求Integration/AC Gate/Push完成后进入06；`docs/workflows/main/06-verification-convergence/01-verification-baseline-establishment.md:20–24` 要求已确认Requirement Sync。06第4篇第66–74行要求必要Gate通过，否则Blocked。包05 Skill第59–63行保留该条件。
- 无业务代码变化、同一共享检查允许复用局部证据，不需要虚构额外集成测试；但没有证据证明必要Push完成。用户决定只接受装饰偏差，REQUEST禁止网络外发也没有将未执行Gate变成已满足。因此两份现有Verified不能成立。
- **最早回流：05第4步Requirement Sync Owner**，记录未完成Push、对象引用、缺少的远程/权限条件及恢复位置；再由06基线/关闭Owner纠正为Blocked。不得擅自外发。保留有效Task、AC和Accepted事实，不把同步缺口写成代码失败。

**已成立的局部证据：**

- 轨迹21–24行实际执行原check.py/app.py；首次乱码保留，UTF-8重跑输出“你好，小明”。27–28行再次执行原check.py并返回0；保存记录03/04与工具输出对应。
- 真实HEAD为 `f02c8c5d853f5fe9a5d7e2085d52c7353357608f`；app.py/check.py初始哈希、Git blob及当前字节一致，没有实施未来目标或降低检查标准。
- `用户决定.md:2–5` 与 `spec/shared/verification.md:17–25` 对应：原装饰偏差仍在，Decision=Accepted Deviation、Status=Accepted、Authority=Human Decision，限定两REQ装饰范围，不豁免中文检查，保留视觉风险和后续承接。**Accepted本身成立；它既不自动产生Verified，也不必然阻止Verified。**
- 两需求分别保留AC主归属，引用唯一共享design/verification；project第2–6行与design第7行正确区分当前中文与尚未实施的未来大写目标。当前65个Markdown链接/适用锚点可达。
- 自写 `records/复核.py:17–18` 仅检查关键词，不能证明Authority/Gate完整；第27–29行才实际运行原检查。本审查直接读决定与正文后认可有限Accepted语义，未采纳脚本未验证的关闭结论。Task局部完成事实不因需求同步缺口自动回退。

**未测限制：** 覆盖共享正文、已有用户决定分支、当前/未来区分及真实中文检查；未测未决Human分支、人工体验/时间指标、Greenfield反向场景、共享设计实际变更回归、大型集成、完整交付或Runtime。缺少Fresh Reviewer没有被追加成Gate。

## F07：BLOCKED，真实修复及局部Owner回接成立

**Finding ORG-R2-F07-01：精确提交Gate通过后仍豁免Push写Verified。**

- 位置：`spec/verification.md:10` 将无远程判为Push不适用，`:15` 写Verified；实际写入见 `records/coordinator-tools.jsonl:25–26`。规范依据同F05。
- 本组确有Task Commit、精确提交正式Gate、唯一任务Integration及AC组合证据，不能说全部上游门禁都缺失；缺少的是必要Push。禁止外发意味着停在该缺口，不能自行免除原门禁。
- **最早回流：05第4步Requirement Sync → 06基线/关闭Owner。** 纠正需求Verified，保留Task Done、Failure Resolved、Finding Resolved和仍open的OI，不一并回退或关闭。

**修复及正式Gate的交叉核验：**

- 初始code_ref `59eabb470e168f8106f8d2201d8cecf91c057a03` 的strip与requirement第3–5行原样返回契约冲突；原输出及轨迹19–20行均显示普通中文/空串通过、边界空格丢失。原check直接调用preserve并比较精确相等，支持局部Implementation根因，最早业务纠正点为05/T01。
- 轨迹21–22行初次脚本在git diff --check返回2后中止，外层返回1；失败仍保留于执行记录第50–60行。23–24行真实执行恢复脚本，修正换行后重验并提交，返回0。该中间失败已恢复，不另判未修复阻塞。
- 真实Git新增 `dcc1b8183f4f47853487a259ccaaa99e1ce44186`，父提交是初始引用；仅app.py改变，check.py原字节未改，当前工作区清洁。实际字节差异还含换行规范化。
- `records/继续执行.py:30–40` 先提交、置Verifying，再用git show精确导出该ref的app.py/check.py，在副本cwd独立进程执行原check；第42行补充边界检查。轨迹23行确实创建/执行该脚本，24行在失败中断检查之后输出提交号并返回0；`执行记录.json:157–180` 对应副本cwd、输出、退出码0。
- 独立从Git取blob比较，副本和当前工作区均逐字节相同：app SHA256 `0caa676ea4d11e6e8f3eb11e37510d69c247ec498c866b6c664c46e78f6adc06`，check SHA256 `230dbf0e060d3ae048157fd110e207917ae1b6a8ffad1a5eaca05cd0b59a3614`。因此正式Gate实际绑定code_ref，不只是填写元数据或给局部自检改名。外层没有逐项转发所有子进程stdout，细节来自已审阅的实际执行脚本及记录；不宣称独立模型Reviewer。

**对象Owner与资料保护：**

- Task：tasks第3、10–12行Done，有正式Gate和依赖重算；Failure：故障第6–10行Confirmed/Correction/code_ref/重验/Resolved及回接引用；Finding：verification第11–13行在原位置单独写Decision=Implementation Defect、Authority=Autonomous、Status=Resolved。局部证据支持，不能因同一主执行者依次承担角色就要求不同Agent。
- OI-001：requirement第6–9行原字节未变，仍open、非阻断、owner_stage=requirement-clarification；保留期限没有随代码修复自动决定。
- 原始两份scratch证据晋升到records/原始证据，与初始清单完全一致，原件仍在；故障和验证入站已更新，原正文快照另存。当前44个Markdown链接/适用锚点可达，没有删除初始文件。
- LEGACY-01：证据复核/README第2–4行指向的唯一输出确实缺失；复核结果第2–5行正确写不能关闭及恢复条件，没有拿新修复提交或口头“完成”补出历史PASS。

**未测限制：** 覆盖原失败保留、证据晋升、历史缺证阻止关闭、精确提交Gate、各Owner局部回接、已有非阻断OI可见性。未测外部HTTP/Issue/CI身份/写回、完整“先有效关闭再删除唯一证据”负控制、授权删除执行、完成对象退出活跃导航、未知跨层Debug及多Fresh接力。未测项不新增Gate。

两个Finding均是观察到的状态收口偏离；现有证据不直接证明包漏译或Canonical需改。后续修复应形成新记录，保留本轮实际失败和有效局部成果，不倒填本轮通过。R1报告SHA256仍为 `a88251b400c695f33aa349a67aa981913feec219bbb3b63ac38054f2a457c353`。
