# Feature Specification: Configure HiDPI Relayout Completion

**Feature Branch**: `001-configure-hidpi-relayout` (on `hidpi-configure-form`)

**Created**: 2026-09-01

**Status**: Draft

**Input**: Operator validation @ 150% — Options PASS; all other Configure sections overlap/clip. RCA in [research.md](./research.md).

**Depends on**: ComicRack CE PerMonitorV2 host (`005-hidpi-foundation`); plugin `lodpi.py` foundation from 2.1.15–2.1.18.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Overview readable at 150% (Priority: P1)

A user opens **Library Organizer → Configure → Overview** at 150% display scale. Mode radios, organization checkboxes, base-folder row, and fileless-thumbnail options are legible without overlapping controls.

**Independent Test**: Overview only @ 150%; no clipped text fields or stacked buttons.

**Acceptance Scenarios**:

1. **Given** Windows 150% and CE PerMonitorV2, **When** Configure opens on Overview, **Then** base-folder textbox and Browse button fit on one row without overlap.
2. **Given** Overview @ 150%, **When** user toggles Copy mode, **Then** copy-option checkbox remains visible and not clipped.

---

### User Story 2 — Files/Folders chrome + insert tabs at 150% (Priority: P1)

A user opens **Files** or **Folders** and navigates all insert sub-tabs (Text, Number, Yes/No, Multiple Value, Calculated, Search). Structure/preview rows and insert field grids are legible.

**Independent Test**: Each insert sub-tab @ 150%; two-column fields do not overlap; Search round-trip restores layout.

**Acceptance Scenarios**:

1. **Given** Files @ 150%, **When** user views Text Fields tab, **Then** two-column insert rows have no horizontal overlap.
2. **Given** Files @ 150%, **When** user opens Search then returns to Text Fields, **Then** layout matches pre-Search state.
3. **Given** Folders @ 150%, **When** user views structure + preview + insert tabs, **Then** header rows and insert grids are legible.

---

### User Story 3 — Rules at 150% (Priority: P1)

A user opens **Rules → Folder Rules** and **Metadata Rules**. Lists, header combos, Add buttons, and rule rows fit without overlap.

**Independent Test**: Metadata Rules with at least one existing rule row @ 150%.

**Acceptance Scenarios**:

1. **Given** Folder Rules @ 150%, **When** list and Add/Remove are shown, **Then** buttons align beside list without clipping.
2. **Given** Metadata Rules @ 150%, **When** header row and rule rows render, **Then** field/operator/value/remove controls do not overlap.

---

### User Story 4 — Regression at 100% (Priority: P2)

A user at 100% display scale sees Configure layout unchanged from pre-fix baseline (no new gaps or overflow).

**Independent Test**: Spot-check Overview, Files Text tab, Rules @ 100%.

---

### User Story 5 — Operator sign-off matrix (Priority: P1)

Operator completes `docs/validation-results.md` for 2.1.19 @ 100% and 150%.

## Requirements

### Functional

- **FR-001**: `relayout_all_hidpi()` MUST call relayout for Overview and Files/Folders chrome, not only Options/Rules/insert grids.
- **FR-002**: Insert grid relayout MUST apply `apply_hidpi_metrics` before measuring column widths.
- **FR-003**: Two-column insert layout MUST use row heights derived from control bounds after metrics, not fixed 45px design step only.
- **FR-004**: Metadata rule/group controls MUST reflow child controls horizontally after HiDPI metrics (via `layout_row` or equivalent).
- **FR-005**: Rules metadata header MUST place Add Rule/Add Group without overlapping mode/operator combos @ 150%.
- **FR-006**: `change_page` MUST trigger page-specific relayout for Overview, Files, Folders, Rules (same as Options).

### Non-functional

- **NFR-001**: Reuse `lodpi.layout_row`; no new DPI helper module.
- **NFR-002**: Bump `Package.ini` / dialog title version to **2.1.19** with changelog entry.
- **NFR-003**: Known limitation unchanged: reopen Configure after display-scale change.

## Success Criteria

| ID | Criterion |
|----|-----------|
| SC-001 | Operator PASS all Configure layout rows in `validation-results.md` @ 150% |
| SC-002 | Operator PASS regression spot-check @ 100% |
| SC-003 | Options tab still PASS @ 150% (no regression) |

## Constitution Check

| Principle | Status |
|-----------|--------|
| I. Fork-first | ✅ Fork branch only |
| II. IronPython WinForms | ✅ In-place relayout |
| III. Real HiDPI validation | ✅ SC-001/002 operator |
| IV. Spec before implement | ✅ This artifact set |
| V. Surgical diffs | ✅ Extend `lodpi` / `relayout_*` |
