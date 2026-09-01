# Library Organizer (fork) — agent briefings

Upstream: [Stonepaw/comicrack-library-organizer](https://github.com/Stonepaw/comicrack-library-organizer)  
Fork: [ChrisFab16/comicrack-library-organizer](https://github.com/ChrisFab16/comicrack-library-organizer)

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `master` | Sync with `upstream/master` |
| `hidpi-configure-form` | **Fork tracking** — HiDPI Configure remediation + `docs/`, `AGENTS.md` |
| `hidpi-configure-form-upstream` | **Hypothetical upstream PR** — product `.py` + `Package.ini` + `changelog.txt` only |

**Do not open upstream PRs without operator confirmation** (Codesync `AGENTS.md` §1).

## Upstream PR hygiene (if ever reopened)

1. **Diff audit** — no `docs/HiDPI-remediation.md`, `AGENTS.md`, or internal review notes in the diff.
2. **Plain English** — PR body and changelog; no internal review IDs in user-facing text.
3. **Single squashed commit** on `-upstream` branch before `gh pr create`.
4. **Link fork docs** in PR description; do not rely on **Files changed** for design context.
5. **Version** — bump `Package.ini` once; `changelog.txt` one consolidated entry per release.

## Operator install (fork)

Copy **one** folder to ComicRack `Scripts/` (e.g. `Library Organizer`). Verify `Package.ini` `Version=` matches the fork tag. Remove stale duplicate plugin folders before copy.

## Spec Kit (enabled on `hidpi-configure-form`)

Active feature: `specs/001-configure-hidpi-relayout/` (`.specify/feature.json`).

Workflow: constitution → spec → plan → tasks → analyze → checklist → implement → operator validation.

## References

- Manual validation matrix: [docs/validation-results.md](docs/validation-results.md)
- Design / review notes: [docs/HiDPI-remediation.md](docs/HiDPI-remediation.md)

## Lessons (2026-09-01)

- Audit **every** Configure tab (Files, Folders, Options, Rules, Empty values, Yes/No, Calculated) — not only the first screenshot.
- IronPython: use `owner.CreateGraphics()` or `Graphics.FromHwnd`; not static `Control.CreateGraphics()`.
- **IronPython 2.7 source must be ASCII-only** (or declare `# -*- coding: utf-8 -*-`); em dashes / Unicode in docstrings break `import lodpi` silently from Configure.
- Relayout on load only; reopen Configure after display-scale or cross-monitor change.
- ComicRack CE HiDPI foundation is separate (`ComicRackCE` `005-hidpi-foundation`); plugin layout stays in this repo.
