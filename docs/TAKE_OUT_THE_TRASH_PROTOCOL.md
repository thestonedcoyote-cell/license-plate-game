# Take Out the Trash Protocol

## Trigger
Run before every release and on every pull request/push through GitHub Actions.

## Purpose
Prevent old update layers, dead code, stale assets and obsolete validation rules from accumulating in the executable app.

## Required steps
- Step 1: Inventory the active runtime from `tools/runtime_files.py`.
- Step 2: Scan for versioned presentation files (`v*.css`, `v*.js`) left in the working tree.
- Step 3: Scan for old version-specific validators.
- Step 4: Scan the active runtime for stale references to removed update layers.
- Step 5: Verify every runtime-manifest file exists.
- Step 6: Scan project assets for files no longer referenced by the active runtime.
- Step 7: Remove obsolete files rather than leaving them dormant.
- Step 8: Run syntax/runtime validation and build the deployable runtime from the same manifest used by Android.
- Step 9: Write audit notes.
- Step 10: Re-run the audit after cleanup. A release is blocked unless the final audit is COMPLETE.

## Notes rule
Every Trash run records findings, actions taken, exceptions and a final recheck. Git history preserves removed implementation history; obsolete runtime files do not need to remain executable merely for archaeology.

## Final recheck
A release may proceed only when `python tools/take_out_trash.py --strict` exits successfully and the active runtime build succeeds.

## Completion status
COMPLETE
