# Pre-Implement Checklist: Configure HiDPI Relayout

**Feature**: `001-configure-hidpi-relayout`  
**Branch**: `hidpi-configure-form`  
**Date**: 2026-09-01

## 1. Failure modes

| ID | Failure mode | Automated | Operator | Task | Done |
|----|--------------|-----------|----------|------|------|
| FM-1 | Insert col2 overlap (measure before scale) | — | Text tab @ 150% | T005 | [x] |
| FM-2 | Row vertical overlap (fixed 45px step) | — | Tall Calculated rows | T006 | [x] |
| FM-3 | Overview fixed coords | — | Overview @ 150% | T007 | [x] |
| FM-4 | Metadata rule intra-row overlap | — | Metadata Rules | T010 | [x] |
| FM-5 | Options regression | — | Options @ 150% | T014 | [ ] |

## 2. Call-site audit

| Subsystem | Entry point | Bypass risk | Done |
|-----------|-------------|-------------|------|
| All pages | `relayout_all_hidpi()` | `change_page` skips page | [x] T009 |
| Lazy insert create | `create_insert_controls` end | early measure | [x] T005 |
| Add metadata rule | `add_metadata_rule` | metrics only, no reflow | [x] T010 |

## 3. Lifecycle

| Question | Answer | Done |
|----------|--------|------|
| When is relayout first run? | `configure_form_load` + `change_page` + lazy create | [x] |
| DPI while dialog open? | Reopen Configure (documented) | [x] |

## 4. Tests

| Contract | CI | Operator | Task |
|----------|-----|----------|------|
| Page relayout | N/A | validation-results.md | T014 |

## Gate

| Gate | Status |
|------|--------|
| Analyze PASS | ✅ |
| Checklist complete | ✅ |
| Proceed to implement | ✅ |
