# Implementation Plan: Configure HiDPI Relayout Completion

**Branch**: `001-configure-hidpi-relayout` | **Date**: 2026-09-01 | **Spec**: [spec.md](./spec.md)

## Summary

Complete Configure HiDPI relayout by extending the **Options-tab pattern** (`lodpi.layout_row` + vertical flow) to Overview, Files/Folders chrome, insert grids, and Rules. Fix insert-grid **measure-before-scale** ordering and row-height math. Bump plugin to **2.1.19**.

## Technical Context

**Language**: IronPython 2.7 / .NET WinForms  
**Key files**: `configureform.py`, `configformcontrols.py`, `lodpi.py`  
**Testing**: Manual — `docs/validation-results.md` + `quickstart.md`  
**Host**: ComicRack CE PerMonitorV2

## Constitution Check

**Gate**: PASS — proceed after analyze + checklist.

## Phases

### Phase A — `lodpi.py` grid fix

1. Reorder `relayout_insert_control_grids`: metrics → measure → position.
2. Replace fixed row-step Y assignment in `relayout_two_column_grid` with per-row `max(Height)` stacking.

### Phase B — New page relayouts (`configureform.py`)

1. `relayout_overview_page()` — base folder row, mode groupbox size, fileless row.
2. `relayout_files_page_chrome()` / `relayout_folders_page_chrome()` — structure + preview rows.
3. Wire into `relayout_all_hidpi()` and `change_page()`.

### Phase C — Rules + metadata controls

1. `relayout_rules_page()` — flow header including Add buttons; use tab client width.
2. `MetadataExcludeRuleControl.apply_hidpi_metrics` — `layout_row` for field/operator/value/remove.
3. Ensure `load_rules_page_settings` / add rule paths call metrics + parent relayout.

### Phase D — Version + validation

1. Version **2.1.19** in `Package.ini`, `configureform.VERSION`, `changelog.txt`.
2. Reset `docs/validation-results.md` for re-test; operator quickstart.

## Risks

| Risk | Mitigation |
|------|------------|
| Overview mode groupbox internal layout | Scale groupbox size; keep internal radios (AutoSize) |
| Tight 500px panel width @ 200% | Optional 200% operator pass; vertical stack fallback in overview if needed |
| Search tab reparenting | Existing `insert_controls_deselected` + grid relayout unchanged |

## Out of scope

- AutoScaleMode migration for Configure form.
- CI automation for IronPython UI.
