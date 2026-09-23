# Plan: Configure SPA Phase A

1. Add `plugin.json` + `ui/dist` SPA (host-bridge + overview shell).
2. Bridge: Python writes profile overview JSON to `webview-ui.config` before ShowWebConfigure; reads `openClassic` after close.
3. Wire `ConfigLibraryOrganizer` / `ConfigureLibraryOrganizer` hybrid path.
4. Bump package to **2.2.0**; changelog + validation notes.
5. Push `configure-spa`; fork PR to `hidpi-configure-form` or `master` (not Stonepaw unless asked).
