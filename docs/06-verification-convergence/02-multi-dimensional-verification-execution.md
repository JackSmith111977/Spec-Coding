# 2. Multi-dimensional Verification Execution｜多维验证执行

## 2.1 目标

基于 Verification Baseline，对完整 Requirement / Change 执行多维验证，形成可复核 Verification Results、Evidence 与 Findings。

本步骤负责**只读验证实际实现**，不在验证过程中通过修改业务实现来“让结果通过”。

---

## 2.2 Read-only Verification

验证期间默认不得修改业务代码、业务配置、业务数据模型等被验证对象。

可以修正测试、Fixture、Mock、验证数据或 Harness 本身，但必须满足：

- 修正的是 Verification Asset / Environment，而非被测业务实现。
- 不降低原有 Pass Condition。
- 不通过改变验证标准掩盖真实失败。

发现业务实现问题时形成 Finding，交由下一阶段判定和路由。

---

## 2.3 验证准备

对每个 Verification Item 明确：验证什么、采用什么方法、在哪里执行、通过条件是什么、需要保存什么 Evidence。

已有 Evidence 仍然有效时优先复用；Cross-Task、关键 Gate、已失效 Evidence 或仍有缺口的部分重新执行。

---

## 2.4 Deterministic Verification

优先执行 Build / Static、Unit / Integration / Regression、Contract / Permission / Data、Security、Runtime Check 等可以客观判定的检查。

每个结果都需要明确 Pass / Fail / Unverified，并保留可复现证据。

> **Deterministic First｜确定性工具优先。**

---

## 2.5 Independent Review 与 Human Acceptance

对于需要跨链路推理、correctness / regression / security / boundary 等高风险内容，可使用 Fresh Verifier 独立审查；规模和风险较大时可并行多个 Verifier，再汇总结论。

Writer / Verifier 尽量分离，审查主动寻找反例，以 Evidence 而非 Agent 声明作为通过依据。

对真实用户端到端、UI / UX、视觉体验或业务最终确认场景，执行必要 Human Acceptance。

---

## 2.6 汇总结果与 Finding Handoff

建立：

```text
Verification Item
      ↓
Result
      ↓
Evidence
      ↓
Finding
```

Verifier 对失败或争议项记录现象、复现方式、Evidence、影响 / 严重性和 `Suspected Origin`，但不直接修改业务实现或替 Human 做最终归因。

后续由 Human Triage 判定为 Verification Issue、Implementation Defect、Upstream Deviation、Accepted Deviation 等。

### 产物

- `Verification Results`
- `Evidence`
- `Findings`
- `Suspected Origin`
- `Unverified Items`

---

## 2.7 完成标准

- Baseline 要求的验证项已完成或明确无法执行。
- Deterministic Verification 已优先执行并形成证据。
- 必要 Independent Review 和 Human Acceptance 已完成。
- 所有失败项有可复现 Evidence 与清晰 Finding。
- 验证过程中未修改业务实现。
- 未通过 / 未验证 / 有争议结果均已准备移交下一阶段。

最终结果：**Verification Results Ready**。

```text
Verification Baseline
        ↓
1. Verification Preparation
        ↓
2. Deterministic Verification
        ↓
3. Independent Review
   + Human Acceptance
        ↓
4. Result Consolidation
   + Finding Handoff
        ↓
Verification Results Ready
```

> **通过确定性工具、独立 Agent 与必要的人工验收，对完整变更进行只读验证，并将所有结果沉淀为可复核 Evidence 与 Findings，为后续偏差判定与收敛提供事实依据。**