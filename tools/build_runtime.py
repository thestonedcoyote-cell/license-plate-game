#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil
from runtime_files import RUNTIME_FILES
p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.output);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
for rel in RUNTIME_FILES:
 s=root/rel
 if not s.is_file(): raise SystemExit(f'missing runtime file: {rel}')
 d=out/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,d)
print(f'Built runtime with {len(RUNTIME_FILES)} files at {out}')
