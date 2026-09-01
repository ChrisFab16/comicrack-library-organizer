# Research: Configure HiDPI relayout gaps (operator 2026-09-01)

**Feature**: `001-configure-hidpi-relayout`  
**Host**: ComicRack CE `005-hidpi-foundation` debug build @ **150%**  
**Plugin**: `2.1.18` → fix targets `2.1.19`

## Operator finding

| Area | @ 150% | Notes |
|------|--------|-------|
| Options tab | **PASS** | Flowing `layout_row` relayout |
| Overview | **FAIL** | Overlap / clip |
| Files / Folders (chrome + insert tabs) | **FAIL** | Overlap / clip |
| Rules | **FAIL** | Overlap / clip |
| Empty values | Not re-tested separately | Same `relayout_options_page` as Options |

## Root causes (code audit)

| ID | Cause | Affected UI |
|----|--------|-------------|
| RC-1 | **No relayout** — fixed 96-DPI `Location`/`Size` vs scaled fonts | Overview; Files/Folders header (structure, preview, separator) |
| RC-2 | **Options-only pattern** — only `relayout_options_page` uses flowing `layout_row` with `coords_scaled=True` | Why Options passes |
| RC-3 | **Insert grid measures before `apply_hidpi_metrics`** — column-2 X too small | Text/Number/Multiple Value insert tabs |
| RC-4 | **Fixed `BASE_ROW_STEP`** — row Y from design grid ignores taller controls after metrics | Two-column insert grids |
| RC-5 | **Metadata rule rows** — `apply_hidpi_metrics` widens combos but does not reflow `FlowLayoutPanel` children | Rules → Metadata |
| RC-6 | **Rules header** — Add Rule/Group absolutely positioned from right; can collide with combo row | Rules → Metadata header |

## Architecture (target)

```
configure_form_load / change_page
        │
        ▼
  relayout_all_hidpi()
        ├── apply_hidpi_form_metrics()     (shell — existing)
        ├── relayout_overview_page()       (NEW)
        ├── relayout_files_folders_chrome() (NEW — per visible page)
        ├── relayout_insert_control_grids() (FIX measure order + row heights)
        ├── relayout_options_page()        (existing)
        └── relayout_rules_page()          (FIX header + rule row reflow)
```

## Out of scope

- Live relayout on `WM_DPICHANGED` while Configure stays open (document reopen).
- ComicRack CE host changes.
- Stonepaw upstream PR.
