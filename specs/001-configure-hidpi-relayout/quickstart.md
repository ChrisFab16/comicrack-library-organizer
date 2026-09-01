# Quickstart: Configure HiDPI Relayout (2.1.20)

## Prerequisites

1. ComicRack CE **debug** build with PerMonitorV2 (`ComicRack\bin\Debug\net48\ComicRack.exe`).
2. Plugin **2.1.20** in `%AppData%\cYo\ComicRack Community Edition\Scripts\Library Organizer\` (single folder).
3. Windows display **150%** for primary pass.

## Install

```powershell
Copy-Item -Recurse -Force "H:\Syncthing\Codesync\ComicRackCE\external\comicrack-library-organizer\*" "$env:APPDATA\cYo\ComicRack Community Edition\Scripts\Library Organizer\"
```

Verify `Package.ini` shows `Version=2.1.20`.

## Test @ 150%

1. Open ComicRack → **Automation → Library Organizer → Configure**.
2. Confirm title: **Library Organizer 2.1.20**.
3. Walk [validation-results.md](../../docs/validation-results.md) matrix (all tabs).
4. Record PASS/FAIL in that file.

## Regression @ 100%

1. Set display 100%; sign out/in if required.
2. Spot-check Overview, Files (Text tab), Options, Rules.
3. Record in validation-results.md.

## Known limitation

Close and reopen Configure after changing display scale or moving across monitors.
