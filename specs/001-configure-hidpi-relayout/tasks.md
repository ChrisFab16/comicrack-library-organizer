# Tasks: Configure HiDPI Relayout Completion

**Branch**: `001-configure-hidpi-relayout`  
**Prerequisites**: spec.md, plan.md, research.md

## Phase 1 — Spec Kit gates

- [x] T001 Constitution + spec + plan + research
- [x] T002 tasks.md (this file)
- [x] T003 analyze-report.md — PASS
- [x] T004 checklist-pre-implement.md — PASS

## Phase 2 — lodpi / insert grids (FR-002, FR-003)

- [x] T005 Reorder `relayout_insert_control_grids`: `apply_hidpi_metrics` before `measure_column_widths`
- [x] T006 Update `relayout_two_column_grid` to stack rows by measured control height + gap

## Phase 3 — Page relayouts (FR-001, FR-006)

- [x] T007 Add `relayout_overview_page()` with `layout_row` / vertical flow
- [x] T008 Add `relayout_files_page_chrome()` and `relayout_folders_page_chrome()`
- [x] T009 Wire `relayout_all_hidpi()` + `change_page()` for Overview/Files/Folders

## Phase 4 — Rules (FR-004, FR-005)

- [x] T010 Reflow `MetadataExcludeRuleControl.apply_hidpi_metrics` with proportional widths + PerformLayout
- [x] T011 Fix `relayout_rules_page` header row (flow Add buttons; use client width)

## Phase 5 — Release + validation (NFR-002, SC-001–003)

- [x] T012 Bump version to 2.1.19 (`Package.ini`, `configureform.VERSION`, `changelog.txt`)
- [x] T013 Update `docs/validation-results.md` + `quickstart.md` for operator re-test
- [x] T014 Operator sign-off @ 150% (SC-001) — **PASS @ 2.1.21**
- [x] T015 Operator regression @ 100% (SC-002) — **PASS @ 2.1.21**

## Phase 6 — Converge 2.1.20 (FR-007–FR-011)

- [x] T016 `relayout_mode_groupbox()` — interior flow + dynamic height
- [x] T017 Base-folder row: precompute width/height before `layout_row`
- [x] T018 `apply_hidpi_shell_metrics()` — OK/Cancel + ToolStrip profile
- [x] T019 Folder Rules Add/Remove `apply_button_metrics`
- [x] T020 `relayout_insert_tab_metrics()` — tab padding + ItemSize
- [x] T021 Bump version to 2.1.20

## Phase 7 — Hotfix 2.1.21 (import gate)

- [x] T022 Remove non-ASCII docstrings (IronPython 2.7 `lodpi` import)
- [x] T023 `configure_form_load` error dialog on HiDPI layout failure
- [x] T024 Bump version to 2.1.21; operator re-validation PASS
