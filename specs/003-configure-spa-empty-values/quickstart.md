# Quickstart: Configure SPA Phase D

**Package**: 2.2.3  
**Host**: ComicRack CE Debug with WebView2

## Install

1. Copy plugin folder to `%AppData%\cYo\ComicRack Community Edition\Scripts\Library Organizer\` (or Packages path used by operator).
2. Confirm `Package.ini` / `plugin.json` Version **2.2.3**.
3. Restart ComicRack CE if script already loaded.

## SC-D1 — Empty substitution

1. Configure → SPA → Empty values.
2. Select field **Series**, set value `Unknown`, **Save**.
3. Open classic Configure → Empty values → Series shows `Unknown`.

## SC-D2 — Failed fields

1. SPA Empty values → check **Series** and **Number** under failed-when-empty list → Save.
2. Classic Empty values → those items checked.

## SC-D3 — Empty-folder exceptions

1. SPA → add path (e.g. `C:\Comics\_keep`) to exceptions → Save.
2. Classic Options → empty-folder exceptions list contains path.
3. Remove path in SPA → Save → classic list updated.

## SC-D4 — Classic escape

1. SPA → Open classic Configure… → WinForms opens; Files/Rules still work.
