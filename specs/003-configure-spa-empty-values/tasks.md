# Tasks: Configure SPA Empty Values (Phase D)

**Input**: `specs/003-configure-spa-empty-values/`  
**Branch**: `configure-spa-phase-d`  
**Package**: 2.2.4

## Phase 1: Setup

- [x] T001 Confirm active feature `.specify/feature.json` → `specs/003-configure-spa-empty-values`
- [x] T002 Review [contracts/bridge-empty-values.md](./contracts/bridge-empty-values.md) and classic `EmptyData` / `FailedFields` / `ExcludedEmptyFolder` load/save in `configureform.py`

## Phase 2: Foundational — Python bridge

- [x] T003 [P] Add `_json_string_list` and `_json_empty_data` helpers in `libraryorganizer.py`
- [x] T004 [P] Extend `_profile_overview_item` to emit `emptyData`, `failedFields`, `excludedEmptyFolder`
- [x] T005 [P] Add `_bridge_extract_string_list` and `_bridge_extract_empty_data` parsers
- [x] T006 [P] Extend `_apply_overview_from_bridge` to apply Empty values properties (FR-002–FR-005)
- [x] T007 Bump bridge `version` string to `2.2.4`

## Phase 3: US1 — Empty substitutions (P1)

- [x] T010 [US1] Add Empty values tab + field select + value input in `ui/src/index.html`
- [x] T011 [US1] Wire fill/read for `emptyData` in `ui/src/app.js` with LABEL_TO_FIELD catalog (FR-006)
- [x] T012 [US1] Sync `ui/dist/*` from `ui/src`

## Phase 4: US2 — Failed fields (P1)

- [x] T020 [US2] Add failed-fields checklist UI in Empty values panel
- [x] T021 [US2] Persist `failedFields` array in SPA state on Save

## Phase 5: US3 — Empty-folder exceptions (P2)

- [x] T030 [US3] Add excluded-empty-folder list + add/remove controls
- [x] T031 [US3] Persist `excludedEmptyFolder` on Save

## Phase 6: Polish & ship

- [x] T040 Bump `Package.ini`, `plugin.json`, `configureform.py` VERSION, `changelog.txt` to 2.2.4 (FR-008)
- [x] T041 Write `docs/validation-spa-phase-d.md` (pending operator)
- [x] T042 Copy package to AppData Scripts for operator smoke
- [x] T043 Push branch; open fork PR to `hidpi-configure-form`
- [ ] T044 Operator SC-D1–D4 per [quickstart.md](./quickstart.md)
- [x] T045 Fix `_bridge_profile_chunk` brace-matching (SC-D1: emptyData truncated at first `]`); bump **2.2.4**; reinstall AppData
- [x] T046 Configure hang: ConfigScript classic fallback passes `[]` (no GetLibraryBooks); `force-classic-configure` sentinel; hotReload false; bump **2.2.5**
- [ ] T047 After CE UserDataFolder fix: delete AppData `force-classic-configure`; retest SPA SC-D1–D4
- [x] T048 Wait dialog on ConfigScript (Opening / Preparing / Building Configure); bump **2.2.6**

## Dependencies

- T003–T007 before T010+
- T010–T012 before T020–T031 (shared tab shell)
- T040 after code complete; T044 after T042

## Parallel opportunities

- T003–T005 can be done together; T010 HTML while T003–T007 in progress once contract fixed
