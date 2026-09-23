# Feature Specification: Configure SPA Empty Values (Phase D)

**Feature Branch**: `configure-spa-phase-d`  
**Created**: 2026-09-23  
**Status**: Draft  
**Package version**: 2.2.3  
**Depends on**: Configure SPA Phases A–C (2.2.0–2.2.2) on `hidpi-configure-form`  
**Host**: ComicRack CE with WebView2 Host API v1 (`ShowWebConfigure`)

**Input**: Continue Library Organizer Configure SPA after Phase C Options scalars — port Empty values substitution map, failed-fields checklist, and empty-folder exception list into the WebView2 SPA; keep Files/Folders/Rules classic.

## Constitution Check

| Principle | Status |
|-----------|--------|
| I. Fork-first; no Stonepaw PR without operator OK | PASS — fork PR to `hidpi-configure-form` only |
| II. IronPython WinForms in-place (HiDPI) | N/A for SPA slice — classic Configure unchanged |
| III. Operator Windows validation | PASS — `docs/validation-spa-phase-d.md` |
| IV. Spec before implement | PASS — this feature |
| V. Surgical diffs | PASS — extend existing bridge + SPA tabs only |

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Empty field substitutions (Priority: P1)

A user opens Configure on CE, selects a profile, opens the **Empty values** tab, picks a metadata field, enters a substitute string for when that field is empty, saves, and sees the same value in classic Configure Empty values.

**Why this priority**: Core Empty values behavior; without it users must drop to classic for everyday path templates.

**Independent Test**: Set Series substitution to `Unknown` in SPA → Save → reopen classic Empty values → Series shows `Unknown`.

**Acceptance Scenarios**:

1. **Given** SPA Configure with a profile that has empty `EmptyData`, **When** user sets a field substitution and Saves, **Then** `Profile.EmptyData` persists that field→value.
2. **Given** a profile with existing `EmptyData`, **When** SPA opens, **Then** selecting that field shows the stored value.

---

### User Story 2 — Failed-when-empty field checklist (Priority: P1)

A user marks which fields cause a failed move when empty (`FailedFields`), saves, and verifies in classic Empty values checked list.

**Why this priority**: Complements Phase C `failEmptyValues` / `moveFailed` / `failedFolder` scalars already in SPA.

**Independent Test**: Check Series + Number in SPA → Save → classic shows those items checked.

**Acceptance Scenarios**:

1. **Given** SPA Empty values tab, **When** user toggles failed-field checkboxes and Saves, **Then** `Profile.FailedFields` matches selected internal field keys.
2. **Given** existing `FailedFields`, **When** SPA loads, **Then** those checkboxes are checked.

---

### User Story 3 — Empty-folder exception paths (Priority: P2)

A user adds/removes paths that must not be deleted when removing empty folders (`ExcludedEmptyFolder`), saves, and verifies the classic Options empty-folder exceptions list.

**Why this priority**: Complements Phase C `removeEmptyFolder` / `emptyFolder`; exception list was deferred in C.

**Independent Test**: Add a path in SPA → Save → classic Options exceptions list contains it.

**Acceptance Scenarios**:

1. **Given** SPA Empty values (or Options) exceptions UI, **When** user adds a path and Saves, **Then** `Profile.ExcludedEmptyFolder` contains that path.
2. **Given** existing exceptions, **When** user removes one and Saves, **Then** it is absent from the profile list.

---

### User Story 4 — Classic escape hatch unchanged (Priority: P1)

Files/Folders/Rules and any unported Options chrome remain available via **Open classic Configure…**.

**Independent Test**: Classic button still opens WinForms Configure with prior SPA saves visible.

### Edge Cases

- Empty substitution value clears or stores empty string for that field (match classic Leave behavior).
- Unknown field keys in bridge JSON are ignored on apply (do not crash).
- Paths with backslashes / quotes escape correctly in bridge JSON.
- Profile switch mid-edit keeps per-profile empty maps without cross-bleed.
- Host without `ShowWebConfigure` still opens classic only (no regression).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: SPA MUST expose an **Empty values** tab (in addition to Overview + Options).
- **FR-002**: Bridge MUST serialize/deserialize per-profile `EmptyData` as field-key → string (ComicRack field ids, e.g. `ShadowSeries`).
- **FR-003**: Bridge MUST serialize/deserialize per-profile `FailedFields` as an array of field keys.
- **FR-004**: Bridge MUST serialize/deserialize per-profile `ExcludedEmptyFolder` as an array of path strings.
- **FR-005**: On Save (`saveOverview: true`), Python MUST apply Empty values fields together with existing Overview/Options apply path and call `save_profiles`.
- **FR-006**: SPA MUST offer the same substitution field labels as classic `empty_substitution_items` and failed-field labels as classic `failed_items` (mapped via `name_to_field` / `field_to_name`).
- **FR-007**: Files template, Folders template, Rules, IllegalCharacters, Months, and ExcludeFolders (folder-rules exclude list) remain **out of scope** (classic only).
- **FR-008**: Package version MUST bump to **2.2.3**; changelog + validation doc updated.

### Non-Functional

- **NFR-001**: ASCII-only IronPython sources (or coding cookie); no Unicode that breaks import.
- **NFR-002**: No new runtime dependencies; hand-rolled bridge JSON remains compatible with Host API `host.config.*`.
- **NFR-003**: Operator validation only (constitution III); no CI IronPython harness required.

## Success Criteria *(mandatory)*

- **SC-D1**: Set empty substitution in SPA → Save → classic Empty values shows same value for that field.
- **SC-D2**: Toggle failed-fields in SPA → Save → classic checked list matches.
- **SC-D3**: Add/remove empty-folder exception path in SPA → Save → classic Options exceptions list matches.
- **SC-D4**: Open classic from SPA still works; Files/Rules unchanged.

## Out of Scope

- Full Files/Folders/Rules SPA parity
- Illegal character map / month name editors
- Folder exclude rules (`ExcludeFolders` / metadata rules)
- Upstream Stonepaw PR
