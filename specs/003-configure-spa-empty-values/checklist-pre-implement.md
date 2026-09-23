# Pre-Implement Checklist: Configure SPA Empty Values (Phase D)

**Feature**: `003-configure-spa-empty-values`  
**Branch**: `configure-spa-phase-d`  
**Date**: 2026-09-23

## 1. Failure modes

| ID | Failure mode | Detection | Task | Done |
|----|--------------|-----------|------|------|
| FM-1 | Backslash/quote in path corrupts JSON | SC-D3 path with `\` | T003, T044 | [ ] |
| FM-2 | Wrong field id (label stored as key) | Classic shows blank / wrong | T011, T006 | [ ] |
| FM-3 | emptyData apply merges stale keys | Replace dict from bridge array | T006 | [ ] |
| FM-4 | FailedFields not cleared when all unchecked | Empty array replace | T006, T021 | [ ] |
| FM-5 | Dist out of sync with src | Visual/version string Phase D | T012 | [ ] |
| FM-6 | IronPython Unicode import break | ASCII-only edits | T003–T007 | [ ] |

## 2. Call-site audit

| Entry | Risk | Mitigation | Done |
|-------|------|------------|------|
| `_write_spa_bridge` | Omits new keys | T004 | [ ] |
| `_apply_overview_from_bridge` | Skips empty maps | T006 | [ ] |
| SPA Save button | Does not read empty tab | `readFormIntoState` covers all tabs | [ ] |
| Classic fallback | Unaffected | No change to WinForms load/save | [ ] |

## 3. Lifecycle

| Question | Answer | Done |
|----------|--------|------|
| When written? | Before `ShowWebConfigure` | [x] |
| When applied? | After close if `saveOverview` | [x] |
| Profile switch | readForm before change; per-profile objects | [x] |

## 4. Tests

| Contract | CI | Operator | Task |
|----------|-----|----------|------|
| SC-D1–D4 | N/A | validation-spa-phase-d.md | T044 |

## Gate

| Gate | Status |
|------|--------|
| Analyze PASS | ✅ CRITICAL=0 |
| Checklist complete | ✅ ready to implement |
| Proceed to implement | ✅ |
