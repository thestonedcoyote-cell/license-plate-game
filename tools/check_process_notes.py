#!/usr/bin/env python3
"""Fail if a process notes file is missing required documentation/recheck sections."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

REQUIRED = [
    "Purpose",
    "Inputs",
    "Step notes",
    "Exceptions / failures",
    "Outputs",
    "Final recheck",
    "Completion status",
]
VALID_STATUS = {"COMPLETE", "COMPLETE_WITH_EXCEPTIONS", "INCOMPLETE"}


def section(text: str, heading: str) -> str:
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = pat.search(text)
    if not m:
        return ""
    nxt = re.search(r"^##\s+", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text[m.end():]))
    return text[m.end():end].strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("notes", type=Path)
    args = ap.parse_args()
    if not args.notes.exists():
        print(f"ERROR: process notes missing: {args.notes}")
        return 2
    text = args.notes.read_text(encoding="utf-8")
    errors = []
    if "# Process Notes" not in text:
        errors.append("missing '# Process Notes' title")
    for h in REQUIRED:
        body = section(text, h)
        if not body:
            errors.append(f"missing or empty section: {h}")
    steps = section(text, "Step notes")
    if steps and not re.search(r"^-\s*Step\b", steps, re.M | re.I):
        errors.append("Step notes must contain at least one '- Step ...' entry")
    final = section(text, "Final recheck")
    # Accept natural forms such as recheck, rechecked, checking, verified, verification.
    if final and not re.search(r"\b(?:recheck(?:ed|ing)?|check(?:ed|ing)?|verif(?:y|ied|ication))\b", final, re.I):
        errors.append("Final recheck does not state a verification/recheck")
    status_body = section(text, "Completion status")
    status = next((s for s in VALID_STATUS if re.search(rf"\b{re.escape(s)}\b", status_body)), None)
    if status_body and not status:
        errors.append("Completion status must contain COMPLETE, COMPLETE_WITH_EXCEPTIONS, or INCOMPLETE")
    if re.search(r"\b(TODO|TBD|FIXME)\b", final, re.I):
        errors.append("Final recheck contains unfinished placeholder")
    if errors:
        print("PROCESS NOTES CHECK: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"PROCESS NOTES CHECK: PASS ({status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
