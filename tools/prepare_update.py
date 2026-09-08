#!/usr/bin/env python3
"""Produce release metadata only for a verified APK signed by the distribution key."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
PREFIX='https://github.com/thestonedcoyote-cell/license-plate-game/releases/download/'
CERT='6c858b7a667848c1243985743dbc0c315f47636507aec241b042af284b5bcc4b'
def main():
 p=argparse.ArgumentParser();p.add_argument('apk',type=Path);p.add_argument('--build-tools',type=Path,required=True);p.add_argument('--url',required=True);p.add_argument('--notes',required=True);p.add_argument('--output',type=Path,default=Path('update.json'));a=p.parse_args()
 if not a.url.startswith(PREFIX) or not a.url.endswith('.apk') or any(x in a.url for x in ['?','#','..']):p.error('Use the stable GitHub release asset URL')
 signed=subprocess.check_output([str(a.build_tools/'apksigner'),'verify','--print-certs',str(a.apk)],text=True)
 if f'Signer #1 certificate SHA-256 digest: {CERT}' not in signed:raise SystemExit('Signing key is not the preserved distribution key; refusing update metadata')
 subprocess.run([str(a.build_tools/'zipalign'),'-c','4',str(a.apk)],check=True)
 badging=subprocess.check_output([str(a.build_tools/'aapt2'),'dump','badging',str(a.apk)],text=True)
 package=re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'",badging)
 sdk=re.search(r"sdkVersion:'(\d+)'",badging,re.I)
 if not package or not sdk or package[1]!='com.thelostharbor.licenseplategame':raise SystemExit('Unexpected APK manifest')
 m=dict(applicationId=package[1],versionCode=int(package[2]),versionName=package[3],minSdk=int(sdk[1]),url=a.url,sha256=hashlib.sha256(a.apk.read_bytes()).hexdigest(),notes=a.notes)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(m,indent=2)+'\n');print('Verified release metadata:',a.output)
if __name__=='__main__':main()
