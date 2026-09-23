# Contract: Bridge Empty Values (Phase D)

**Feature**: `003-configure-spa-empty-values`  
**File**: `webview-ui.config` (Host API `host.config.get` / `host.config.set`)

## Root object (existing + unchanged keys)

| Key | Type | Notes |
|-----|------|-------|
| `version` | string | `"2.2.4"` |
| `lastUsed` | string | |
| `selectedProfile` | string | |
| `openClassic` | bool | |
| `saveOverview` | bool | Save applies Overview + Options + Empty values |
| `profiles` | array | Per-profile objects |

## Per-profile additions

| Key | Type | Profile property |
|-----|------|------------------|
| `emptyData` | `[{ "field": "<id>", "value": "<str>" }, ...]` | `EmptyData` dict |
| `failedFields` | `["ShadowSeries", ...]` | `FailedFields` list |
| `excludedEmptyFolder` | `["C:\\path", ...]` | `ExcludedEmptyFolder` list |

Field ids MUST be values from `locommon.name_to_field` (not display labels).

## Apply semantics

When `saveOverview` is true:

1. Apply Overview/Options scalars (existing Phase B/C).
2. For each profile chunk: rebuild `EmptyData` from `emptyData` array (keys present replace; Python MAY replace entire dict with parsed entries).
3. Replace `FailedFields` with parsed array (empty array clears).
4. Replace `ExcludedEmptyFolder` with parsed array.
5. `save_profiles` + `save_last_used`.

## SPA catalogs (labels)

SPA embeds display-name lists matching `empty_substitution_items` and `failed_items` in `configureform.py`, mapping to field ids via a static `LABEL_TO_FIELD` object mirrored from `name_to_field` for those labels only.
