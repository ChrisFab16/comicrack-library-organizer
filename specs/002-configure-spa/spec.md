# Feature Specification: Configure SPA (Phase A)

**Branch**: `configure-spa`  
**Created**: 2026-09-23  
**Host**: ComicRack CE with WebView2 Host API v1 (`ShowWebConfigure`)  
**Status**: Draft

## Goal

Open Library Organizer **Configure** as a WebView2 SPA on CE when available, without rewriting every WinForms tab yet. Keep classic Configure as fallback and as an in-SPA escape hatch.

## User Stories

### US1 — SPA Configure on CE (P1)

**Given** CE with `ComicRack.ShowWebConfigure`, **When** user runs Configure, **Then** SPA shell opens showing host version and profile list.

### US2 — Classic fallback (P1)

**Given** host without ShowWebConfigure (or SPA bridge failure), **When** Configure runs, **Then** existing WinForms Configure opens.

### US3 — Open classic from SPA (P2)

**Given** SPA is open, **When** user clicks “Open classic Configure…”, **Then** SPA closes and WinForms Configure opens.

## Requirements

- **FR-001**: `plugin.json` with `kind: python`, `apiVersion: 1`, `ui.configure`.
- **FR-002**: ConfigScript MUST prefer ShowWebConfigure when present.
- **FR-003**: SPA MUST use Host API `host.config.*` bridge JSON for profile overview + `openClassic` flag.
- **FR-004**: Full Files/Folders/Rules/Options SPA parity is **out of scope** for Phase A (follow-up).

## Success

- SC-001: CE Debug — Configure opens SPA with profiles listed.
- SC-002: Classic fallback still works (or open-classic path).
- SC-003: Package version bumped; docs in `specs/002-configure-spa/`.
