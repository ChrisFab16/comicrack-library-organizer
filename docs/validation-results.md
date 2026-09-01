# Validation Results: Library Organizer HiDPI (Configure)

**Fork**: [ChrisFab16/comicrack-library-organizer](https://github.com/ChrisFab16/comicrack-library-organizer)  
**Branch**: `hidpi-configure-form`  
**Package version**: `2.1.18` (`Package.ini`)  
**Host**: ComicRack Community Edition (PerMonitorV2 foundation)

## Automated

| Gate | Result | Date | Notes |
|------|--------|------|-------|
| Unit / CI tests | **N/A** | — | IronPython + WinForms; no headless harness (see `HiDPI-remediation.md`) |

## Operator — install gate

| Check | Result | Notes |
|-------|--------|-------|
| Single `Scripts/` folder; stale copies removed | | |
| `Package.ini` `Version=2.1.18` | | |
| Plugin loads without script error | | |

## Operator — Configure layout

Run at **100%** (regression) and **150%** (required). Optional **200%**.

| Tab / area | 100% | 150% | 200% | Notes |
|------------|------|------|------|-------|
| Files — insert tabs (Text, Number, Multiple Value) | | | | No column overlap; fields readable |
| Files — Search tab round-trip | | | | Labels/layout restore after leaving Search |
| Folders — insert tabs | | | | Same as Files |
| Yes/No Fields | | | | Stack without overlap; instructions visible |
| Calculated | | | | Tall rows stack; info label placement |
| Rules — Folder Rules | | | | List + Add/Remove aligned |
| Rules — Metadata Rules | | | | Header + rows fit panel width |
| Options | | | | Month names, illegal chars, empty-folder list |
| Empty values | | | | Substitution + failed-empty blocks vertical |
| Dialog shell | | | | Content not overflowing frame |

## Operator — functional smoke

| Check | Result | Notes |
|-------|--------|-------|
| Edit template field; OK saves | | |
| Preview / path tokens sane (if used) | | |
| Optional: dry-run on test library | | |

## Known limitation (not a fail)

- Relayout runs on **Configure open** only. After changing Windows display scale or moving across monitors, **close and reopen** Configure before sign-off.

## Sign-off

- [ ] Install gate pass
- [ ] Configure layout @ 100% (regression)
- [ ] Configure layout @ 150% (required)
- [ ] Configure layout @ 200% (optional)
- [ ] Functional smoke pass
- [ ] Fork install ready for daily use

**Tester**:  
**Date**:  
**Display scale(s) tested**:

## References

- Manual checklist detail: [HiDPI-remediation.md](HiDPI-remediation.md)
- Agent / branch policy: [AGENTS.md](../AGENTS.md)
