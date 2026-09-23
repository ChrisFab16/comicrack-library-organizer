# Pre-Implement Checklist: Configure SPA (Phases A–C) — retrospective

**Feature**: `002-configure-spa`  
**Date**: 2026-09-23  
**Note**: Completed after implement for A–C. **New scope must complete this checklist before code.**

## 1. Failure modes

| ID | Failure mode | Detection | Done |
|----|--------------|-----------|------|
| FM-1 | Host lacks ShowWebConfigure | Classic Configure path | [x] |
| FM-2 | Bridge JSON missing/corrupt | Fallback + openClassic | [x] |
| FM-3 | SPA save does not persist | Operator SC-B* / SC-C* vs classic tabs | [x] |
| FM-4 | Nested ui/dist not packed | Package.ini + AppData install smoke | [x] |
| FM-5 | Duplicate Scripts folders | Operator install checklist | [x] |

## 2. Call-site audit

| Entry | Bypass risk | Mitigation | Done |
|-------|-------------|------------|------|
| ConfigLibraryOrganizer / Configure | Direct classic only | Prefer ShowWebConfigure when present | [x] |
| webview-ui.config write/read | Stale file | Write before open; read on close | [x] |
| Classic tabs not in SPA | User needs Files/Rules | “Open classic” + SC-C3 | [x] |

## 3. Tests / validation

| Contract | Gate | Artifact |
|----------|------|----------|
| SPA opens + profiles | Operator | validation-spa-phase-a.md |
| Overview persist | Operator | validation-spa-phase-b.md |
| Options persist | Operator | validation-spa-phase-c.md (**PASS** 2026-09-23) |

## Gate

| Gate | Status |
|------|--------|
| Analyze PASS | ✅ retrospective |
| Checklist complete | ✅ retrospective |
| Phase C operator sign-off | ✅ |
| Proceed to **new** implement | ❌ — start new Spec Kit feature first |
