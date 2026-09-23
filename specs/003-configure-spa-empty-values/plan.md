# Implementation Plan: Configure SPA Empty Values (Phase D)

**Branch**: `configure-spa-phase-d` | **Date**: 2026-09-23 | **Spec**: [spec.md](./spec.md)

## Summary

Extend the existing Configure SPA (Phases A–C) with an **Empty values** tab and bridge fields for `EmptyData`, `FailedFields`, and `ExcludedEmptyFolder`. Reuse `_write_spa_bridge` / `_apply_overview_from_bridge` / Host API `host.config.set` close path. Bump package to **2.2.4**.

## Technical Context

| Item | Choice |
|------|--------|
| Language | IronPython 2.7 (plugin) + vanilla JS SPA (`ui/src`) |
| Host | ComicRack CE `ShowWebConfigure` + JSON-RPC Host API v1 |
| Persistence | `losettingsx.dat` via existing `save_profiles` |
| JSON | Hand-rolled string builders/parsers in `libraryorganizer.py` (no new deps) |

## Constitution Check

All gates PASS (see spec Constitution Check). Principle II (WinForms-only HiDPI) does not block SPA Configure continuation already on this fork.

## Design Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | Store bridge keys as **internal field ids** (`ShadowSeries`, …) | Matches `Profile.EmptyData` / `FailedFields` storage; SPA maps labels via static catalog |
| D2 | Encode maps/lists as JSON arrays of objects / strings inside each profile object | Fits existing per-profile chunk apply without a full JSON parser |
| D3 | Add SPA tab `empty` rather than stuffing into Options | Matches classic Empty values tab separation; Options already dense |
| D4 | Empty-folder exceptions live on Empty tab in SPA (classic keeps them on Options) | UX clarity; same profile property |
| D5 | Extend `_bridge_extract_*` with array helpers; keep ASCII | Consistent with Phase B/C bridge |

## Project Structure (touched)

```text
libraryorganizer.py          # bridge write/apply for EmptyData, FailedFields, ExcludedEmptyFolder
ui/src/index.html            # Empty values tab + controls
ui/src/app.js                # fill/read/persist empty fields
ui/src/styles.css            # list/checklist layout tweaks
ui/dist/*                    # copy/build from src
Package.ini / plugin.json / changelog.txt / configureform.py VERSION
specs/003-configure-spa-empty-values/
docs/validation-spa-phase-d.md
```

## Contracts

See [contracts/bridge-empty-values.md](./contracts/bridge-empty-values.md).

## Implementation Phases

1. Artifacts (this plan, tasks, analyze, checklist)
2. Python bridge serialize + apply + array parsers
3. SPA Empty values UI
4. Version bump, dist sync, AppData install notes
5. Operator SC-D1–D4

## Risks

| Risk | Mitigation |
|------|------------|
| Hand-rolled JSON breaks on `\` in paths | Reuse `_json_esc`; add quickstart path with backslash |
| Field label drift vs classic | Copy catalogs from `configureform.py` lists into SPA constants |
| Large EmptyData blobs | Only non-empty entries need write; apply replaces map keys present in bridge |
| Profile chunk truncated at first `]` (SC-D1) | `_bridge_profile_chunk` brace-matches full object (2.2.4) |

## Test Strategy

Operator manual gates in `docs/validation-spa-phase-d.md` (SC-D1–D4). No automated CI.
