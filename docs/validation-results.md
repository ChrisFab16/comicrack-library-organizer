# Validation Results: Library Organizer HiDPI (Configure)

**Fork**: [ChrisFab16/comicrack-library-organizer](https://github.com/ChrisFab16/comicrack-library-organizer)  
**Branch**: `hidpi-configure-form` / feature `001-configure-hidpi-relayout`  
**Package version**: `2.1.21` (`Package.ini`)  
**Host**: ComicRack CE debug build (PerMonitorV2 foundation)

## Automated

| Gate | Result | Date | Notes |
|------|--------|------|-------|
| IronPython import smoke | **PASS** | 2026-09-01 | `lodpi` + `configureform` via ComicRack IronPython host |
| Unit / CI tests | **N/A** | — | IronPython + WinForms; manual only |

## Operator — install gate

| Check | Result | Notes |
|-------|--------|-------|
| Single `Scripts/` folder; stale copies removed | **PASS** | |
| `Package.ini` `Version=2.1.21` | **PASS** | |
| Plugin loads without script error | **PASS** | 2.1.20 import bug fixed in 2.1.21 |
| Dialog title `Library Organizer 2.1.21` | **PASS** | |

## Operator — Configure layout

| Tab / area | 100% | 150% | 200% | Notes |
|------------|------|------|------|-------|
| **Overview** | **PASS** | **PASS** | — | Mode groupbox, base folder, fileless options |
| Files — chrome (structure/preview) | **PASS** | **PASS** | — | |
| Files — insert tabs (Text, Number, Multiple Value) | **PASS** | **PASS** | — | No column overlap |
| Files — Search tab round-trip | **PASS** | **PASS** | — | Layout restores after Search |
| Folders — chrome + insert tabs | **PASS** | **PASS** | — | Tab spacing acceptable |
| Yes/No Fields | **PASS** | **PASS** | — | |
| Calculated | **PASS** | **PASS** | — | |
| Rules — Folder Rules | **PASS** | **PASS** | — | Add/Remove readable |
| Rules — Metadata Rules | **PASS** | **PASS** | — | |
| **Options** | **PASS** | **PASS** | — | Regression guard |
| Empty values | **PASS** | **PASS** | — | |
| Dialog shell | **PASS** | **PASS** | — | OK/Cancel readable |
| ToolStrip — Profile Action | **PASS** | **PASS** | — | |

## Operator — functional smoke

| Check | Result | Notes |
|-------|--------|-------|
| Edit template field; OK saves | **PASS** | |
| Preview / path tokens sane (if used) | **PASS** | |

## Known limitation (not a fail)

- Relayout runs on **Configure open** and **page switch**. After changing Windows display scale, **close and reopen** Configure.

## Sign-off

- [x] Install gate pass
- [x] Configure layout @ 100% (regression) — SC-002
- [x] Configure layout @ 150% (required) — SC-001
- [ ] Configure layout @ 200% (optional) — not tested
- [x] Functional smoke pass
- [x] Fork install ready for daily use

**Tester**: operator  
**Date**: 2026-09-01  
**Display scale(s) tested**: 100%, 150%

## References

- Spec: [specs/001-configure-hidpi-relayout/spec.md](../specs/001-configure-hidpi-relayout/spec.md)
- Quickstart: [specs/001-configure-hidpi-relayout/quickstart.md](../specs/001-configure-hidpi-relayout/quickstart.md)
- Manual checklist detail: [HiDPI-remediation.md](HiDPI-remediation.md)
