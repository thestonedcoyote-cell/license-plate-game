# Process Notes & Completion Standard

This project assumes future humans and future AI sessions will need to understand why work was done, what actually happened, and what remains unresolved. Therefore **notes are a required output of the process, not optional commentary**.

## Required for every repeatable process

Every automated or manual process must produce notes containing:

1. **Purpose** — what the process was trying to accomplish.
2. **Inputs** — files, URLs, records, versions, parameters, and relevant assumptions.
3. **Step notes** — for every substantive step: what was done, why, and the result.
4. **Exceptions / failures** — anything skipped, blocked, ambiguous, suspicious, or incomplete. Never silently omit failures.
5. **Outputs** — created/changed artifacts, counts, hashes or identifiers when useful, and provenance.
6. **Rights / privacy notes** when images, user data, locations, trademarks, or third-party material are involved.
7. **Final recheck** — an explicit verification that each intended step ran, required outputs exist, exceptions are recorded, and no unfinished step is being presented as complete.
8. **Completion status** — `COMPLETE`, `COMPLETE_WITH_EXCEPTIONS`, or `INCOMPLETE`.

## Notes format

Automated processes should emit `PROCESS_NOTES.md` into their output package. Human review batches should export reviewer notes with each decision.

Minimum Markdown sections:

- `# Process Notes`
- `## Purpose`
- `## Inputs`
- `## Step notes`
- `## Exceptions / failures`
- `## Outputs`
- `## Final recheck`
- `## Completion status`

Step notes should use entries beginning with `- Step` so the checker can verify that at least one substantive note exists.

## Final recheck rule

The final substantive step of every process must be a recheck, performed **after work is complete and before the result is treated as publishable/accepted**. Packaging or artifact upload may occur afterward, but must package the already-checked output unchanged.

The recheck asks:

- Did every required process step run?
- Do the expected files/records exist?
- Do counts and identifiers reconcile?
- Were ambiguous or failed items captured in notes/exception queues?
- Were user-facing claims checked against the actual output?
- Are provenance/rights/privacy notes present where required?
- Is the completion status honest?

## Enforcement

`tools/check_process_notes.py` fails automated jobs when required note sections, step notes, final recheck, or completion status are absent. Workflows should run it immediately before publishing or uploading their output.

A process that failed can still produce valid notes. The notes should say `INCOMPLETE` or `COMPLETE_WITH_EXCEPTIONS`; the documentation checker is intended to prevent undocumented failure, not force a dishonest green status.
