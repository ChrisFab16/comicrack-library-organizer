# Validation: Configure hang (2026-09-25)

## Symptoms

Clicking Library Organizer **Configure** appeared to do nothing or hang until the app was closed.

## Causes

1. **ConfigScript classic fallback** called `GetLibraryBooks()` for the whole library before opening WinForms Configure — can take a very long time on large libraries.
2. **WebView2 user-data contention** (CE): plugin Configure and HTML Info panels shared the process-default WebView2 profile, which can hang `EnsureCoreWebView2Async`.

## Fixes

| Layer | Change |
|-------|--------|
| LO **2.2.5** | Classic fallback passes `[]` (no library load); `force-classic-configure` sentinel; `hotReload: false` |
| CE Debug | Dedicated LocalAppData folders: `WebView2/PluginConfigure` and `WebView2/HtmlPanels` |

## Operator now

1. **Restart ComicRack CE** (new Plugins DLL already built into Debug).
2. Configure should open **classic WinForms** immediately (`force-classic-configure` is present in AppData Scripts).
3. After confirming classic works: delete `%AppData%\cYo\ComicRack Community Edition\Scripts\Library Organizer\force-classic-configure` to resume SPA testing (SC-D*).
