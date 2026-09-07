#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys
from runtime_files import RUNTIME_FILES
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--report');p.add_argument('--strict',action='store_true');a=p.parse_args()
legacy=[]
for pat in ('v[0-9]*.css','v[0-9]*.js'):
 legacy += [x.relative_to(root).as_posix() for x in root.glob(pat)]
legacy += [x.relative_to(root).as_posix() for x in (root/'.github/workflows').glob('validate-v*.yml')]
obsolete_assets=[x for x in ('assets/roadmap-v12.svg','assets/roadmap-crumpled-v12.1.webp') if (root/x).exists()]
missing=[x for x in RUNTIME_FILES if not (root/x).is_file()]
runtime_text='\n'.join((root/x).read_text(errors='ignore') for x in RUNTIME_FILES if (root/x).is_file() and (root/x).suffix in {'.js','.css','.html','.webmanifest'})
stale_refs=sorted(set(re.findall(r'v(?:8|9|10|11|12|13(?:\.0\.[123])?)[^\s\"\']*\.(?:css|js)',runtime_text)))
assets=[x for x in (root/'assets').glob('*') if x.is_file()]
active_refs='\n'.join((root/x).read_text(errors='ignore') for x in RUNTIME_FILES if (root/x).is_file() and (root/x).suffix in {'.js','.css','.html','.webmanifest'})
unreferenced_assets=[x.relative_to(root).as_posix() for x in assets if x.name not in active_refs and x.relative_to(root).as_posix() not in RUNTIME_FILES]
status='COMPLETE' if not (legacy or obsolete_assets or missing or stale_refs or unreferenced_assets) else 'INCOMPLETE'
lines=['# Take Out the Trash Audit','', '## Purpose','Scan the working tree for obsolete release layers, stale references, missing runtime files and unreferenced assets before release.','', '## Findings',f'- Legacy versioned runtime/validator files: {len(legacy)}',*[f'  - {x}' for x in legacy],f'- Obsolete map assets: {len(obsolete_assets)}',*[f'  - {x}' for x in obsolete_assets],f'- Missing active runtime files: {len(missing)}',*[f'  - {x}' for x in missing],f'- Stale version references in active runtime: {len(stale_refs)}',*[f'  - {x}' for x in stale_refs],f'- Unreferenced assets: {len(unreferenced_assets)}',*[f'  - {x}' for x in unreferenced_assets],'','## Final recheck',f'Runtime manifest contains {len(RUNTIME_FILES)} files. Audit status: {status}.','','## Completion status',status]
text='\n'.join(lines)+'\n';print(text)
if a.report: Path(a.report).write_text(text)
if a.strict and status!='COMPLETE': sys.exit(1)
