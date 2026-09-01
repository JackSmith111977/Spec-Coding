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
  "publication": {"boundary": "repository-native", "component_root": "harness"},
  "integration": {"scope": "project"},
  "workflow_route": "adoption/final-route.json",
  "constraints": [
    {"id": "merge-policy", "value": "verified-only"}
  ]
}
```

`boundary` 只能是 `local`、`shared` 或 `repository-native`；`component_root` 必须是 `target-root` 内的相对路径。最终 Route（路由）至少选择一个 Main Workflow Stage：

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
- `compose` 先对同一份 State 和 Source Inventory 完整校验，再预检全部暂存产物；任一项失败时不写入任何 Harness 文件。
- 组件只能写入 Adoption Baseline 指定的 `component_root`，且 `create` / `modify`、目标路径和 SHA-256 必须匹配 State。
- `verify` 检查目标摘要、加载命令、成功命令和确定性组件的失败命令；命令以无 Shell 的参数数组执行。
- `unknown` 或 `unavailable` 的关键运行时能力、`UNRESOLVED` 来源、`BLOCKED` 映射、缺少独立语义审查，都会阻止 Harness Ready。

## 开发验证

```bash
python -m unittest discover -v
```

测试覆盖 Adoption 缺失、真实 Canonical 语料解析与扫描、重复标题、前言扫描、来源遗漏、状态 Schema、未知运行时、Blocked / Orphan / Missing Mapping、暂存漂移、无部分写入、通用 Probe（探针）执行器及受控目标级 E2E。
