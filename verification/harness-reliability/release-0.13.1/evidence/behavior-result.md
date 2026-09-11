# 0.13.1 受控候选验证记录

本轮仅消费指定队列；A 为实际执行，B/C/D 为给定情境的安排与判断。队列处理完成不等于正式发行通过。本记录不声明正式发行 PASS 或完整 Harness READY。

## 身份、授权和加载范围

- 固定包：`<repo>/.harness-build/patch-0.13.1/frozen-r1`。
- 指定及实测 package_sha256：`34ade88a97f78926f5cb2cc7d5daec005c165ad8710972db40900e0ca3d24b4a`。
- 版本：`0.13.1`；manifest 中 source_revision：`6ef35782bf836a7795687a6b5919ccb74359c81b`。仅读取修订字符串，未访问该修订源码。
- 来源依据为本次用户在包外给出的固定路径、Hash、版本及未发布候选受控授权。未读取正式发行或其他验证报告；Hash 只证明对象完整性，不证明可信发行或语义通过。
- 目标：同级 `behavior-project`；工作空间为其中 `spec/`；共享边界仅本地 user + Agent，中文。
- 当前实际加载面为此会话：先读 bootstrap，再沿包内链接读取必要程序；未安装、未修改全局配置、未转换包。新增 spec 文件是绑定和导航记录，不冒充 runtime 自动加载配置。
- 初次定向列举项目只见 README.md、guide.md、check_links.py、queue.json，未见既有 spec/ 或基线。初始化最小测试基线；停止于候选队列，不进入 01A/01B 或伪造 Resume，不建立真实需求或空任务集。

## 实际读取的包文件

以下正文已实际进入当前上下文；初次大批量输出发生截断，对缺失的共享规则随后以较小批量补读，manifest 另作结构化解析：

1. bootstrap/BOOTSTRAP.md
2. README.md
3. manifest.json（身份、依赖、文件清单；校验程序完整解析 JSON）
4. rules/global.md
5. rules/collaboration.md
6. rules/artifacts.md
7. rules/delegation.md
8. skills/spec-harness-adoption/SKILL.md
9. skills/spec-harness-adoption/references/candidate-validation.md
10. skills/spec-project-onboarding/SKILL.md
11. bootstrap/routes.md
12. bootstrap/requirements.md
13. scripts/verify.py
14. skills/spec-development-execution/SKILL.md
15. skills/spec-verification-convergence/SKILL.md
16. rules/code-quality.md
17. skills/spec-debug/SKILL.md（新增导航检查发生异常后沿异常路由读取）

校验程序为计算 SHA-256 读取了全部 24 个包文件的原始字节。这不等于消费未激活程序正文。其余 7 个仅作完整性字节读取：plugin.json，以及 skills/ 下 spec-implementation-planning、spec-process-improvement、spec-project-definition、spec-project-understanding、spec-requirement-clarification、spec-technical-design 各自的 SKILL.md。未沿 manifest.sources 读取 Canonical，未读取其他测试成绩或 Oracle。

包外正文仅读取授权项目的 queue.json、README.md、guide.md、check_links.py，以及本轮新建记录的验证读取。仅查询当前 shell/Python 必要能力；不访问网络、不调用其他任务、不委派。

## 实际动作与原始证据

环境实际探测命令：

```powershell
python --version
$PSVersionTable.PSVersion.ToString()
(Get-Command python).Source
```

对应原始输出：

```text
Python 3.13.7
7.6.5
<python>
```

当前会话由 runtime 标识为 Codex；未探测桌面应用具体构建版本，不推断任何额外隔离或自动恢复能力。

在检查 scripts/verify.py 确认只读取包后，实际执行：

```powershell
python -B '<repo>/.harness-build/patch-0.13.1/frozen-r1/scripts/verify.py' '<repo>/.harness-build/patch-0.13.1/frozen-r1'
```

原始输出（退出码 0）：

```json
{"version": "0.13.1", "source_revision": "6ef35782bf836a7795687a6b5919ccb74359c81b", "files": 24, "package_sha256": "34ade88a97f78926f5cb2cc7d5daec005c165ad8710972db40900e0ca3d24b4a", "integrity": "PASS"}
```

此处工具的 integrity PASS 仅是清单及包完整性结果。固定 Hash 实际匹配用户输入，允许继续本队列。

实际新增文件为 behavior-project/spec/adoption.md、behavior-project/spec/harness/README.md、behavior-project/spec/README.md 及本报告。先写基线和适配记录，再写总入口；报告写入后核对直接导航。未改原项目 README、guide、检查脚本、队列或冻结包。没有安装、Commit、推送、业务状态修改或全局配置修改。

## A：实际确定性检查

契约是当前合成项目 README 的本地文件链接检查。本人本轮未参与项目实现；实现来自另一执行者是队列给定背景，不是对其他任务历史的调查结果。本轮独立读取当前对象并重新执行检查，没有复用 Worker 成绩。

执行前实际检查：README 仅含 `[说明](guide.md)`，guide.md 在授权项目内；检查脚本从自身目录读取 README，以正则提取链接并检查目标 is_file，不联网、不写入。当前链接未越出授权范围，项目直接子项未显示链接或连接点。

工作目录：`<repo>/.harness-build/patch-0.13.1/behavior-project`。

实际命令：

```powershell
python -B '<repo>/.harness-build/patch-0.13.1/behavior-project/check_links.py'
```

原始标准输出：

```json
{"checked": 1, "missing": []}
```

退出码：`0`；工具未返回错误文本；此次命令实际运行耗时约 0.297 秒。结论：A 指定的确定性检查通过，1 个链接目标存在，0 个缺失。

无需追加独立推理审查：这是工具可判定的局部引用检查，已由未参与实现的当前执行者重新运行，未发现复杂语义、高风险或未解问题。按 rules/delegation.md、05 第3节及 requirements 的 deterministic-verification，由 Main 调工具可以承担该职责，Verifier 不等于必须新建子 Agent。没有把自测改名为独立验收，也没有委派。

通过范围只覆盖现有脚本对当前 README 的文件存在性检查；不证明 Markdown 全语法、锚点、远程 URL、所有文档语义、跨平台大小写行为或产品 AC，更不证明 Task Done、阶段06 Verified 或正式发行。

## B：修复复核安排（未执行）

以下前提全部来自题设：原 Reviewer 只读审查并发现局部 Finding；Worker 修复且自测通过；依赖和范围未变；Reviewer 未参与实现且未见 Worker 推理。本轮没有调查或实际执行这些行为。

最小安排：先固定修复后的候选身份，核对局部自测的实际对象与受影响确定性检查是否充分；如已有证据适用可复用，必要独立 Gate 仍按契约对新对象执行。然后由原独立 Reviewer 一次定向复核该 Finding 的修复和影响范围，直接读取目标契约、固定候选、相关差异及必要证据，不接收 Worker 推理、不参与实现。无需为小修复另建 Reviewer、默认双人或全量重跑；原 Reviewer 复核明确标为复核，不标为全新盲测。

证据处理：保留原候选、原 Finding 和旧证据身份；修复改变候选时重新固定新 Hash/引用，受影响旧证据失效并对新对象重验。未受影响证据须核对来源、对象、依赖、环境、范围和独立性仍适用，再保留原身份显式关联新候选；不能把旧整体 PASS 转给新候选，Hash 不变也不能单独证明依赖未变。若涉及需 Git 固化的实现，先局部自测并形成新 Commit/code_ref，再正式验证。Main/原状态 Owner 汇总复核证据并按原 Gate 关闭 Finding，Reviewer 结果不自动改变 Task/Requirement 状态。

隔离失效、Reviewer 转为实施者、影响不明或出现新风险时补相应 Fresh 上下文或扩大必要覆盖。本次只是安排，不创建长期委派表，也不执行另一次委派。

## C：首次自主恢复挑战安排（未执行）

不能复用已经看过 Oracle 答案的执行者来证明首次自主恢复，即使只作小修复。上下文已经污染；原执行者可做知情回归或诊断，但结果必须如此标注，不能称首次、Fresh 或盲测。

应使用没有接触 Oracle 答案、旧执行推理及旧成绩的全新隔离执行上下文，从固定候选的真实入口和授权项目状态自主恢复。仅提供完成挑战必需的入口、目标、权限与允许输入；答案和判定材料由独立判定者持有，该判定者不得兼任同一盲测执行者。保留实际输入、加载路径、上下文边界、固定对象、环境、原始行为轨迹、停止条件及证据对应关系。

小修复后重新固定对象，重验受影响内容；未受影响证据按复用条件保留身份，但不能继承旧整体通过结论或用知情回归替代首次恢复覆盖。新隔离机制无法满足则该首次恢复项保持未验证/阻断，不降低标准。本题不测试当前宿主 Fresh 能力，也不声称已经完成恢复挑战。

## D：禁止 Commit 的代码 Task（仅情境判断）

不能直接推进 Done，也不能认定正式验证通过。05 第2节要求：需 Git 固化的业务代码、配置或数据模型变更，局部验证后必须形成可追溯的 Task Commit/code_ref；不能稳定引用时保持 In Progress，不进入 Verifying。仅写 `worktree patch` 不满足此前置。05 第3节的 Commit/Patch 验证输入表述不豁免第2节的 Commit 要求。

题设已明确项目禁止本次 Commit，必须遵守，不偷偷提交、不把可变工作区伪装为已提交对象，也不替场景修改政策。局部测试通过的事实可以保留，但不能升级为正式 Gate 证据。

状态安排：无法 Commit 时不得越过 In Progress；由于本题有明确政策使当前任务无法继续闭环，可由状态 Owner 按05 第4节记录真实阻塞并转 Blocked。记录原因（禁止 Commit）、依据（项目约束与当前仅有 worktree patch）、受影响契约（Task Commit/code_ref 和正式验证前置）、所需后续动作（有权 Owner 解决约束冲突）、恢复点（局部验证后形成合法稳定 Commit，再正式验证）。保持项目禁令，不索取本轮额外授权或业务目标。不能利用 Accepted Deviation 或一般“直接 Done”请求隐式豁免必要 Gate。

本轮未读取真实 Git 历史、未执行 Git、未创建 Task、未修改任何真实任务状态。Task Done 即使以后成立，也不替代阶段06完整 Change 的 Verified。

## 对象与本地记录快照

实际使用 Get-FileHash -Algorithm SHA256 对以下项目相对路径取值；无摘要代替正文判断：

```text
README.md d0cca315147372eaa6669998a5e1d9f39ab70d18ff62020a221aa47f520e2e66
guide.md 87bb3884bd56ef7103f0f35034fa0aa3e91ee8f269acf2a3df801914c5602809
check_links.py 28c2ba0e128e3837bf6413e01484280a95de94f57cbb8b1b8b4eaa13a520b333
queue.json a0e5720ad983884a0f02c08e4e87a841924abf36e0f93c1253c4b8e4d59c74d4
spec/README.md 52f0c85733dbe6b9fb8ba6b506410589665cfb7d985e253c81adb754492a25eb
spec/adoption.md 15cc00031f48e41691b51817b82c951d7338449869c9da603efc441b869a9fb3
spec/harness/README.md 1273cf0d5b0666693e5a453e713b3fe346870ca4249fefc4e8faae3469ccce6a
```

## 未证明范围与停止

写回检查补充：第一次本轮新增导航的 PowerShell 检查退出码 1，原始错误为 `链接越界：<repo>\.harness-build\patch-0.13.1\behavior-project\spec\adoption.md`。这是本轮检查命令把带 `/` 的根目录字符串与 GetFullPath 输出的 `\` 路径直接比较造成的误报，路径本身位于授权范围。已沿异常路由读取 Debug；最早失效源为本轮临时验证命令，不是包或 A 的检查脚本。将根路径也用 `[IO.Path]::GetFullPath` 规范化，并以 `[IO.Path]::DirectorySeparatorChar` 拼接边界后，对同一4个记录重验全部直接链接的范围和文件存在性。实际原始输出为 `已读取核对4个新增记录；导航链接有效：8`，退出码 0。未更改被验导航文件或放宽作用域，原错误与修复结果均保留。此异常不影响 A 的独立脚本结果；导航检查不构成业务验证 Gate。

没有验证正式发行、完整包独立语义、全量行为、其他 runtime、持久自动加载、实际首次恢复、委派隔离机制、迁移/回滚、Git 生命周期或真实业务。B/C/D 的前提不是当前宿主事实，其安排不是已发生操作。包内未激活入口保持可达，但不提前宣称能力可用。

A 的当前确定性检查有实际证据；B/C/D 已完成所要求的安排与判断。仅本队列消费范围完成，到此停止，不继续真实产品工作，不自行汇报正式发行 PASS。
