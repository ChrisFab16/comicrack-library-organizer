# Tasks: Configure SPA (Phases A–C)

**Feature**: `002-configure-spa`  
**Status**: Implemented (A–C) — retrospective task list for Spec Kit tracking  
**Versions**: 2.2.0 (A) → 2.2.1 (B) → 2.2.2 (C)

## Phase A — Shell (2.2.0)

- [x] T001 Add `plugin.json` (`kind: python`, `apiVersion: 1`, `ui.configure`)
- [x] T002 Scaffold Vite SPA under `ui/` with Host API bridge
- [x] T003 Wire ConfigScript / Configure to prefer `ShowWebConfigure`
- [x] T004 Classic fallback + in-SPA “Open classic Configure…”
- [x] T005 Bump `Package.ini` 2.2.0; changelog; `docs/validation-spa-phase-a.md`
- [x] T006 Operator SC-001–SC-003 sign-off

## Phase B — Overview (2.2.1)

- [x] T010 SPA Overview: BaseFolder / mode / fileless flags
- [x] T011 Python bridge apply-on-close for overview fields
- [x] T012 Bump 2.2.1; validation-spa-phase-b; operator SC-B* sign-off

## Phase C — Options (2.2.2)

- [x] T020 SPA Options scalars (see `phase-c.md`)
- [x] T021 Python bridge apply/save for Options fields
- [x] T022 Bump 2.2.2; validation-spa-phase-c; operator SC-C1–C3 sign-off

## Out of scope (next Spec Kit feature)

- Empty-value substitution map, exception lists, Files/Folders/Rules full SPA parity
- Automated CI for IronPython bridge (constitution: operator gates OK)

## Spec Kit process (from 2026-09-23)

Any **new** product scope MUST run: specify → plan → tasks → analyze → checklist-pre-implement → implement. Do not extend this feature with silent hotfixes.
