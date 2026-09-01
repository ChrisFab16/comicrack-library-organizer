# Library Organizer (fork) Constitution

## Core Principles

### I. Fork-First, Operator-Confirmed Upstream

HiDPI and layout work ships on **`hidpi-configure-form`** for local install. Do **not** open upstream PRs to Stonepaw without explicit operator confirmation.

### II. IronPython WinForms In-Place

Remediate layout within existing **`configureform.py`** / **`configformcontrols.py`** / **`lodpi.py`**. No framework migration.

### III. Real Windows HiDPI Validation

Configure dialog MUST be operator-validated at **100%** (regression) and **150%** (required) on Windows with ComicRack CE PerMonitorV2 host. Record results in `docs/validation-results.md`.

### IV. Spec Before Implement

Non-trivial layout fixes follow Spec Kit: **specify → plan → tasks → analyze → checklist → implement**. No silent hotfixes on `master`.

### V. Surgical Diffs

Reuse **`lodpi.layout_row`** and existing `relayout_*` entry points. Extend coverage; do not duplicate parallel scaling systems.

## Project Constraints

- **Host**: ComicRack CE with embedded PerMonitorV2 manifest.
- **DPI at runtime**: `owner.CreateGraphics()` on Configure form handle; reopen dialog after display-scale change.
- **Testing**: Manual Configure checklist only (no headless IronPython harness in CI).

## Governance

Specs live under `specs/` on `hidpi-configure-form`. Upstream `-upstream` branch excludes `specs/`, `AGENTS.md`, and agent docs.

**Version**: 1.0.0 | **Ratified**: 2026-09-01 | **Last Amended**: 2026-09-01
