# Configure SPA Phase B — Overview fields

**Branch**: `configure-spa-phase-b`  
**Version**: 2.2.1  
**Depends on**: Phase A (2.2.0)

## Goal

Edit selected profile **Overview** fields in the SPA and persist via `save_profiles` on close.

## Fields (selected profile)

- `baseFolder` (string)
- `mode` — Move | Copy | Simulate
- `useFolder`, `useFileName`, `copyMode`, `moveFileless` (bool)

## Flow

1. Python writes richer bridge JSON (per-profile overview fields).
2. SPA edits selected profile; **Save overview** sets `saveOverview: true` and closes.
3. Python applies fields to Profile objects and `save_profiles`.
4. Classic Configure remains for Files/Folders/Rules/Options/Empty.

## Success

- SC-B1: Change BaseFolder in SPA → Save → reopen SPA / classic shows new path.
- SC-B2: Mode radio persists.
- SC-B3: Open classic still works.
