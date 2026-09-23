# Validation: Configure SPA Phase D (2.2.4)

| Gate | Result | Notes |
|------|--------|-------|
| SC-D1 Empty substitution persists | **PENDING** | Retest after T045 chunk-slice fix (2.2.4) |
| SC-D2 Failed fields persist | **PENDING** | Operator |
| SC-D3 Empty-folder exceptions persist | **PENDING** | Operator (include path with `\`) |
| SC-D4 Classic escape hatch | **PENDING** | Operator |

**Tester**: —  
**Host**: ComicRack CE Debug (ShowWebConfigure / Host API v1)  
**Quickstart**: `specs/003-configure-spa-empty-values/quickstart.md`

## SC-D1 failure (2026-09-23)

Bridge apply sliced the profile at the first `]`, which ends `emptyData` arrays early so `_bridge_extract_empty_data` returned `None` and substitutions never saved. Fixed in 2.2.4 via brace-matched `_bridge_profile_chunk`.
