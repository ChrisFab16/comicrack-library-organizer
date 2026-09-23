# Configure SPA Phase C — Options fields

**Branch**: `configure-spa-phase-c`  
**Version**: 2.2.2  

## Goal

Edit selected-profile **Options** scalars in the SPA (plus Overview from Phase B). Empty-value substitution map and exception lists stay classic for now.

## Fields

- `dontAskWhenMultiOne`
- `removeEmptyFolder`
- `emptyFolder`
- `filelessFormat`
- `failEmptyValues`
- `moveFailed`
- `failedFolder`

## Success

- SC-C1: Toggle option + Save overview → persists in classic Options tab
- SC-C2: emptyFolder / filelessFormat / failedFolder text persists
- SC-C3: Classic Configure still opens for Files/Rules/Empty substitutions
