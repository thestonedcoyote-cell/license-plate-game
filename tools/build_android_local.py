#!/usr/bin/env python3
"""Full native build with official Android tools; useful without a Gradle install.
Requires Java 17 (jdk.compiler), Android 35 android.jar, build-tools, and the private key.
APK_STORE_PASSWORD supplies the keystore password. Outputs must be device-tested.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import argparse,subprocess,tempfile,re,xml.etree.ElementTree as ET
p=argparse.ArgumentParser()
for n in ['sdk-jar','build-tools','keystore','out']:p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--alias',default='lpgdebug');a=p.parse_args();root=Path(__file__).resolve().parents[1]
run=lambda *cmd:subprocess.run([str(x) for x in cmd],check=True)
gradle=(root/'android-app/app/build.gradle').read_text()
version_code=re.search(r'versionCode\s+(\d+)',gradle)[1]
version_name=re.search(r"versionName\s+'([^']+)'",gradle)[1]
run('python3',root/'tools/take_out_trash.py','--strict')
with tempfile.TemporaryDirectory() as d:
 d=Path(d);runtime=d/'www';classes=d/'classes';classes.mkdir();dex=d/'dex';dex.mkdir();gen=d/'gen';gen.mkdir()
 run('python3',root/'tools/build_runtime.py',runtime)
 manifest=ET.parse(root/'android-app/app/src/main/AndroidManifest.xml');manifest.getroot().set('package','com.thelostharbor.licenseplategame');manifest.write(d/'AndroidManifest.xml')
 run(a.build_tools/'aapt2','compile','--dir',root/'android-app/app/src/main/res','-o',d/'resources.zip')
 run(a.build_tools/'aapt2','link','-o',d/'base.apk','-I',a.sdk_jar,'--manifest',d/'AndroidManifest.xml','--min-sdk-version','26','--target-sdk-version','35','--version-code',version_code,'--version-name',version_name,'--java',gen,d/'resources.zip')
 sources=list((root/'android-app/app/src/main/java').rglob('*.java'))+list(gen.rglob('*.java'))
 run('java','com.sun.tools.javac.Main','-source','17','-target','17','-cp',a.sdk_jar,'-d',classes,*sources)
 with ZipFile(d/'classes.jar','w') as z:
  for f in classes.rglob('*.class'):z.write(f,f.relative_to(classes).as_posix())
 run(a.build_tools/'d8','--release','--min-api','26','--lib',a.sdk_jar,'--output',dex,d/'classes.jar')
 with ZipFile(d/'base.apk','a') as z:
  for f in dex.glob('*.dex'):z.write(f,f.name,compress_type=ZIP_DEFLATED)
  for f in runtime.rglob('*'):
   if f.is_file():z.write(f,'assets/www/'+f.relative_to(runtime).as_posix(),compress_type=ZIP_DEFLATED)
 run(a.build_tools/'zipalign','-f','-p','4',d/'base.apk',d/'aligned.apk');a.out.parent.mkdir(parents=True,exist_ok=True)
 run(a.build_tools/'apksigner','sign','--ks',a.keystore,'--ks-key-alias',a.alias,'--ks-pass','env:APK_STORE_PASSWORD','--key-pass','env:APK_STORE_PASSWORD','--v2-signing-enabled','true','--v3-signing-enabled','true','--out',a.out,d/'aligned.apk')
 run(a.build_tools/'apksigner','verify','--verbose','--print-certs',a.out);run(a.build_tools/'zipalign','-c','4',a.out)
 with ZipFile(a.out) as z:
  assert z.testzip() is None
  for f in runtime.rglob('*'):
   if f.is_file():assert z.read('assets/www/'+f.relative_to(runtime).as_posix())==f.read_bytes()
print('Full native APK built and verified:',a.out)
