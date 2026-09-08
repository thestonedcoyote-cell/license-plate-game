#!/usr/bin/env python3
"""Stage audited web assets into the recovered native shell and sign with Android tools.
For native Java/resource changes use the Gradle build instead.
Password is read by apksigner from APK_STORE_PASSWORD; never stored in the repo.
"""
import argparse, struct, subprocess, tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED

def bump_manifest(data, version):
    data=bytearray(data); strings=[]; offset=8; updated=False
    while offset < len(data):
        kind, header, size=struct.unpack_from('<HHI',data,offset)
        if not size: raise ValueError('Invalid binary XML')
        if kind==1:
            count,_,flags,start=struct.unpack_from('<IIII',data,offset+8)
            utf8=bool(flags&0x100)
            def length(pos):
                if utf8:
                    n=data[pos];pos+=1
                    if n&128:n=((n&127)<<8)|data[pos];pos+=1
                else:
                    n=struct.unpack_from('<H',data,pos)[0];pos+=2
                    if n&32768:n=((n&32767)<<16)|struct.unpack_from('<H',data,pos)[0];pos+=2
                return n,pos
            for i in range(count):
                p=offset+start+struct.unpack_from('<I',data,offset+header+4*i)[0]
                n,p=length(p)
                if utf8:n,p=length(p)
                strings.append(bytes(data[p:p+n*(1 if utf8 else 2)]).decode('utf-8' if utf8 else 'utf-16le'))
        if kind==0x102:
            attrstart,attrsize,count=struct.unpack_from('<HHH',data,offset+24)
            for i in range(count):
                p=offset+16+attrstart+i*attrsize
                name=struct.unpack_from('<I',data,p+4)[0]
                if strings[name]=='versionCode':
                    old=struct.unpack_from('<I',data,p+16)[0]
                    if version<=old: raise ValueError('Version must increase')
                    struct.pack_into('<I',data,p+16,version);updated=True
        offset+=size
    if not updated: raise ValueError('versionCode missing')
    for enc in ('utf-8','utf-16le'):
        data=data.replace('0.1.0-alpha'.encode(enc),'0.2.0-alpha'.encode(enc))
    return bytes(data)

def main():
    p=argparse.ArgumentParser()
    for n in ['base','runtime','build-tools','keystore','out']:p.add_argument('--'+n,required=True,type=Path)
    p.add_argument('--alias',required=True);p.add_argument('--version-code',type=int,default=2);a=p.parse_args()
    run=lambda *cmd:subprocess.run([str(x) for x in cmd],check=True)
    run(a.build_tools/'apksigner','verify',a.base)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        unsigned=Path(td)/'unsigned.apk';aligned=Path(td)/'aligned.apk'
        with ZipFile(a.base) as base,ZipFile(unsigned,'w') as dest:
            for i in base.infolist():
                if i.is_dir() or i.filename.startswith(('META-INF/','assets/www/')):continue
                payload=base.read(i.filename)
                if i.filename=='AndroidManifest.xml':payload=bump_manifest(payload,a.version_code)
                dest.writestr(i.filename,payload,compress_type=ZIP_STORED if i.filename=='resources.arsc' else i.compress_type)
            for f in sorted(a.runtime.rglob('*')):
                if f.is_file():dest.write(f,'assets/www/'+f.relative_to(a.runtime).as_posix(),compress_type=ZIP_DEFLATED)
        run(a.build_tools/'zipalign','-f','-p','4',unsigned,aligned)
        run(a.build_tools/'apksigner','sign','--ks',a.keystore,'--ks-key-alias',a.alias,'--ks-pass','env:APK_STORE_PASSWORD','--key-pass','env:APK_STORE_PASSWORD','--v2-signing-enabled','true','--v3-signing-enabled','true','--out',a.out,aligned)
    run(a.build_tools/'apksigner','verify','--verbose','--print-certs',a.out)
    run(a.build_tools/'zipalign','-c','4',a.out)
    with ZipFile(a.out) as z:
        assert z.testzip() is None
        for f in a.runtime.rglob('*'):
            if f.is_file():assert z.read('assets/www/'+f.relative_to(a.runtime).as_posix())==f.read_bytes()
    print('Signed APK and staged runtime verified:',a.out)
if __name__=='__main__':main()
