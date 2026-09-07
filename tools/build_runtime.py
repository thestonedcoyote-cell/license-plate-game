#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil
from runtime_files import RUNTIME_MAP
p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();root=Path(__file__).resolve().parents[1];out=Path(a.output);shutil.rmtree(out,ignore_errors=True);out.mkdir(parents=True)
for src,dest in RUNTIME_MAP:
 s=root/src
 if not s.is_file(): raise SystemExit(f'missing runtime file: {src}')
 d=out/dest;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,d)
print(f'Built runtime with {len(RUNTIME_MAP)} files at {out}')
