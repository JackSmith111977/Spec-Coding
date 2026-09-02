# Harness Compiler V2 Tools

这组工具为 [`Harness Compilation Protocol`](../../docs/meta-protocols/harness-compilation.md) 提供可重复执行的证据与门禁。它们不替代 Agent 的 Read / Derive 判断，不调用模型 API，也不把 Workflow、Rules、Adoption Baseline 或 Runtime Evidence 变成新的事实源。

## 边界与前置条件

工具只接受两个明确根目录：

- `--spec-root`：包含 `VERSION` 与 `docs/manifest.yaml` 的 Spec Coding 工作区；
- `--target-root`：将接收 Harness 输出的目标工作区。

在 `spec-root` 中必须有一个通过 Project Onboarding 形成的 Adoption Baseline（接入基线）和其 `workflow_route`。缺失、无效或与当前 Target 不匹配时，`resolve` 会失败；应返回 Project Onboarding，而不是猜测边界。

```json
{
  "adoption_version": 1,
  "target": {"id": "target-id"},
  "spec_workspace": {"id": "stable-spec-workspace-id"},
  "publication": {"boundary": "repository-native", "component_root": "."},
  "integration": {"scope": "project"},
  "runtime": {
    "id": "pi",
    "version": "optional-current-version",
    "evidence": ["local://pi-context-file-discovery"],
    "loader_rules": {
      "context_files": ["AGENTS.md"],
      "skill_dirs": [],
      "extension_dirs": []
    }
  },
  "workflow_route": "adoption/final-route.json",
  "constraints": [
    {"id": "merge-policy", "value": "verified-only"}
  ]
}
```

`boundary` 只能是 `local`、`shared` 或 `repository-native`；`component_root` 必须是 `target-root` 内的相对路径。`runtime.loader_rules` 是经过当前 Runtime Discovery 复核的**输出发现契约**：`context_files` 为精确加载的上下文文件，`skill_dirs` 与 `extension_dirs` 为递归可发现目录。这里刻意使用精确的 `context_files`，而非过宽的 `context_dirs`：若只声明项目根目录，任意根目录文件都会被误判为可加载。

每一个 COMPILE 输出都必须落在至少一个已声明的加载表面；例如 Pi 的项目指令应生成到可发现的 `AGENTS.md`，不能只放在任意的 `harness/AGENTS.md` 子目录。`runtime.evidence` 必须指出实际探测或对应版本资料；它不是模型能力清单。

最终 Route（路由）至少选择一个 Main Workflow Stage：

```json
{
  "stages": ["01b", "02"],
  "rule_ids": [],
  "exception_ids": []
}
```

空 `rule_ids` 会按 `manifest.yaml` 的 `applies_to` 自动解析适用规则；Exception Workflow 只有在 Trigger 已成立时才填入。

## 安装与命令链

```bash
python -m pip install -r requirements.txt

python -m tools.harness_compiler resolve \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --output "$TARGET_ROOT/.harness-state/candidates.json"

python -m tools.harness_compiler scan \
  --spec-root "$SPEC_ROOT" \
  --candidates "$TARGET_ROOT/.harness-state/candidates.json" \
  --output "$TARGET_ROOT/.harness-state/source-inventory.json"

python -m tools.harness_compiler seed \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --source-inventory "$TARGET_ROOT/.harness-state/source-inventory.json" \
  --output "$TARGET_ROOT/.harness-state/compilation-state.json"
```

`seed` 只生成完整来源账本和非 Ready 初始状态，绝不自动生成语义。此后 Agent 根据 Source Inventory（来源清单）、当前 Target、Existing Harness 与 Current Runtime Evidence 推导 `Compilation State`（编译状态）。状态是短生命周期 JSON；其结构由 [`schema/compilation-state.schema.json`](schema/compilation-state.schema.json) 约束，额外语义检查由 `validate` 执行。它必须逐项记录：

- 每个 Canonical / Adoption 来源的引用、摘要、状态以及 Contract（契约）链接；
- Contract → Existing / Compile / Blocked 决策和 Runtime Evidence；
- 仅针对 `COMPILE` Contract 的组件、暂存内容摘要和发布目标；
- 十一个验证维度的证据，以及独立 Reviewer 的语义忠实 Verdict。

为使这一 Agent 判断可复现，可将派生说明保存为 JSON 并运行 `derive`：它展开来源 ID 范围、要求每个语义来源恰好归入一个 Contract，并按暂存文件重新计算 SHA-256；它不会自动编造自然语言保证或独立审查结论。

```bash
python -m tools.harness_compiler derive \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --seed-state "$TARGET_ROOT/.harness-state/compilation-state.json" \
  --derivation "$TARGET_ROOT/.harness-staging/semantic-derivation.json" \
  --output "$TARGET_ROOT/.harness-state/derived-compilation-state.json"
```

Agent 将语义推导和暂存产物准备完成后，`derive` 输出的 `derived-compilation-state.json` 才是后续命令唯一允许使用的 State；不得把非 Ready 的 seed 输出传给 `validate`、`compose` 或 `verify`。然后运行：

最小 `semantic-derivation.json` 需要显式写出输入格式；`derive` 不会猜测这些语义。以下片段展示 COMPILE Contract 的必填回读、组件验证范围与加载可见性 Probe：

```json
{
  "contracts": [{
    "id": "CT-001",
    "source_selectors": ["SRC-001..SRC-010"],
    "guarantee": "Preserve the selected mandatory workflow behavior.",
    "strength": "must",
    "obligation_type": "workflow-gate",
    "failure_mode": "A skipped gate must block progress.",
    "readback_contract": {
      "when": "before source-derived work",
      "canonical_doc": "docs/workflows/main/05-development-execution/02-autonomous-implementation-and-closure.md",
      "mandatory": true
    }
  }],
  "mappings": [{
    "contract": "CT-001",
    "decision": "COMPILE",
    "primitives": ["instruction"],
    "runtime": {"support": "native", "surfaces": ["AGENTS.md"], "evidence": ["local://runtime-probe"]}
  }],
  "components": [{
    "id": "CMP-001",
    "type": "instruction",
    "covers": ["CT-001"],
    "reason": "runtime-visible instruction is needed",
    "outputs": [{"target": "AGENTS.md", "action": "create", "staged": ".harness-staging/AGENTS.md"}],
    "verification": {
      "covers": ["CT-001"],
      "cannot_cover": ["Fresh-agent behavior requires the protocol acceptance run."],
      "probes": [{"id": "runtime-visible", "type": "runtime-visibility", "covers": ["CT-001"]}]
    }
  }],
  "validation": {
    "source_coverage": {"status": "pass", "evidence": ["review://source-coverage"]},
    "contract_coverage": {"status": "pass", "evidence": ["review://contract-coverage"]},
    "semantic_fidelity": {
      "status": "pass",
      "evidence": ["review://independent-semantic-review"],
      "reviewer": {"independent": true, "verdict": "pass", "findings": []}
    },
    "runtime_mapping": {"status": "pass", "evidence": ["review://runtime-mapping"]},
    "capability_routing": {"status": "pass", "evidence": ["review://capability-routing"]},
    "component_integrity": {"status": "pass", "evidence": ["review://component-integrity"]},
    "minimality": {"status": "pass", "evidence": ["review://minimality"]},
    "runtime_loading": {"status": "pass", "evidence": ["review://runtime-loading"]},
    "executability": {"status": "pass", "evidence": ["review://executability"]},
    "failure_path": {"status": "pass", "evidence": ["review://failure-path"]},
    "reference_drift": {"status": "pass", "evidence": ["review://reference-drift"]},
    "unresolved": 0,
    "blocked": 0
  }
}
```

`source_selectors` 接受单个 `SRC-001` 或包含端点的范围 `SRC-001..SRC-010`。每个语义来源只能归入一个 Contract；每个 `COMPILE` Contract 都必须有 `readback_contract`，其 `canonical_doc` 必须是本次 Resolve / Scan 实际选出的 Canonical 文档。`derive` 封存暂存文件的 SHA-256，随后不得改写。

然后运行：

```bash
python -m tools.harness_compiler validate \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --state "$TARGET_ROOT/.harness-state/derived-compilation-state.json" \
  --source-inventory "$TARGET_ROOT/.harness-state/source-inventory.json" \
  --output "$TARGET_ROOT/.harness-state/validate.json"

python -m tools.harness_compiler compose \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --state "$TARGET_ROOT/.harness-state/derived-compilation-state.json" \
  --source-inventory "$TARGET_ROOT/.harness-state/source-inventory.json" \
  --output "$TARGET_ROOT/.harness-state/compose.json"

python -m tools.harness_compiler verify \
  --spec-root "$SPEC_ROOT" --target-root "$TARGET_ROOT" \
  --adoption-baseline adoption/baseline.json \
  --state "$TARGET_ROOT/.harness-state/derived-compilation-state.json" \
  --source-inventory "$TARGET_ROOT/.harness-state/source-inventory.json" \
  --output "$TARGET_ROOT/.harness-state/verify.json"
```

每条命令都把机器可读报告写到 `--output`，并以退出码 `0` 表示通过。`verify` 不修复输出；失败必须回到最早的来源、接入、推导或组件 Owner。

## 写入与验证门禁

- `validate` 与 `verify` 只读；`compose` 是唯一 Writer。
- `compose` 先对同一份 State 和 Source Inventory 完整校验，再按 Baseline 的 `runtime.loader_rules` 二次预检每个输出是否可被 Runtime 发现；任一项失败时不写入任何 Harness 文件。
- 组件只能写入 Adoption Baseline 指定的 `component_root`，且 `create` / `modify`、目标路径和 SHA-256 必须匹配 State。
- `verify` 检查目标摘要，并按三类 Probe 出具分层回执：`runtime-visibility` 校验全部输出的 Runtime 可见性；`surface` 校验文件、语法或确定性 Gate；`semantic` 只表示已执行的命令式语义检查。后两类命令以无 Shell 的参数数组执行。
- `surface` Probe（例如 `test -f` 或固定 `grep`）只能证明表面事实，不能作为 Contract 语义忠实或 Runtime 冷启动接管的结论。每个组件必须声明它覆盖的 Contract，以及 `cannot_cover` 的盲区。
- `unknown` 或 `unavailable` 的关键运行时能力、`UNRESOLVED` 来源、`BLOCKED` 映射、不可见输出、缺少独立语义审查，都会阻止编译器通过。编译器的通过结果不替代协议规定的 Fresh-agent 行为验收。

### 重编译纪律

`create` 绝不覆盖已有目标，因而 `CREATE_TARGET_EXISTS` 不是可忽略的重跑噪声。重编译前必须先读取既有 Compose Receipt，并选择一种显式路径：

- 对保留的同一文件，以 `action: "modify"` 和新的暂存摘要替换；或
- 在版本控制可恢复的前提下，明确列出并清理旧的编译输出，再以 `create` 重新组合。

不得用宽泛目录删除绕过该门禁；也不要在工具尚未支持 `replace` 动作时把它写进 State。

## 开发验证

```bash
python -m unittest discover -v
```

测试覆盖 Adoption 缺失、Runtime Loader Profile、真实 Canonical 语料解析与扫描、重复标题、前言扫描、来源遗漏、状态 Schema、未知运行时、Blocked / Orphan / Missing Mapping、回读 Contract、不可见输出、暂存漂移、无部分写入、通用 Probe（探针）执行器及受控**编译流水线** E2E。

仓库还保留一份自举编译测试夹具：[`../../tests/harness_compiler/fixtures/spec-coding-harness/`](../../tests/harness_compiler/fixtures/spec-coding-harness/)。它包含针对当前 Canonical Corpus 的已编译示例、来源账本与独立审查回执；测试会重新执行 `resolve → scan` 并比较来源摘要，同时验证其拒绝无效条件。该目录是测试产物，不是仓库根目录的运行时 Harness，也不是新的 Canonical 事实源。它验证的是编译器行为，不能替代某一真实 Coding Agent Runtime 的冷启动验收。
