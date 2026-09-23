# Research: Configure SPA Empty Values

**Date**: 2026-09-23

## Profile properties (authority)

| UI (classic) | Property | Type |
|--------------|----------|------|
| Empty substitution field+value | `EmptyData` | `dict` fieldId → string |
| Failed-when-empty checklist | `FailedFields` | `list` of fieldIds |
| Empty folder exceptions (Options tab) | `ExcludedEmptyFolder` | `list` of path strings |

Already in SPA (Phase C): `FailEmptyValues`, `MoveFailed`, `FailedFolder`, `RemoveEmptyFolder`, `EmptyFolder`.

## Mapping

`locommon.name_to_field` / `field_to_name` — SPA must not invent alternate ids.

## Bridge parsing

Phase B/C use marker scans. Phase D adds:

- `_json_string_list(seq)` → `["a","b"]`
- `_json_empty_data(dict)` → `[{"field":"…","value":"…"},…]`
- `_bridge_extract_string_list(chunk, key)`
- `_bridge_extract_empty_data(chunk)` → dict

## Out of scope confirmation

`ExcludeFolders` (folder tree excludes), Rules, Files/Folders templates, IllegalCharacters, Months — classic only.
