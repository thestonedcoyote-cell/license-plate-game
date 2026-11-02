#!/usr/bin/env python3
"""One-to-one, source-hash pinned official Idaho plate-art integration.

The original agency pages, image registries, and binaries are recovered from a
private archived Actions artifact. Only reproducible display and thumbnail JPEG
derivatives are published. No issue-era or human/rights approval is asserted.
"""
import argparse, hashlib, io, json
from pathlib import Path
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
PREFIX='globalThis.LPG_CATALOG_IMAGES='
OLD='lpg-current-images-20261102-njstandard1'
NEW='lpg-current-images-20261102-idaho3'
RUN=41486647380
AGENCIES={
    'scenic':{
        'folder':'ID/Idaho_DMV_License_Plate_Program_Guide_html',
        'registry_sha':'bd9c680e71456160d781a132f148ec3559672d4122cd09c3cdfc966adf66c2ee',
        'html_sha':'56cd6ab8cbbbc67cce73cda91f1481578981aa9528d5f89e2a9789b0c0e2fcd8'
    },
    'new_2026':{
        'folder':'ID/Idaho_Two_New_Plates_July_2026_html',
        'registry_sha':'891c1154f935d4d02a8e4289a1672682a1bceaddec4dc17f9e33ef08323342d9',
        'html_sha':'7bc4b84e31386d474b8a9a567809d04e94eb8774bd33e87253b25329880fa7a4'
    }
}
ROWS=[
    {'uid':'LPG-US-ID-00001','name':'Scenic Idaho','gallery':'scenic','num':2,'ext':'jpeg',
     'url':'https://itd.idaho.gov/wp-content/uploads/2025/03/Idaho_Sample-High-Res-1024x536.jpeg',
     'page':'https://itd.idaho.gov/dmv/registrations-plates-titles/license-plates/',
     'sha':'d271de9aff6654caf9cff0f2471484ff9195dee3fc1a7d35560140b514da18ec',
     'size':[1024,536],'bytes':148965,
     'alt':'An Idaho license plate that says Idaho on it.',
     'visual':'Red/white/blue Scenic Idaho mountain silhouette, FAMOUS POTATOES and SAMP sample (official standard-plate example).'},
    {'uid':'LPG-US-ID-00003','name':'Agriculture — Harvest the Future','gallery':'new_2026','num':3,'ext':'png',
     'url':'https://itd.idaho.gov/wp-content/uploads/2026/06/image-1-1024x515.png',
     'page':'https://itd.idaho.gov/news/two-new-idaho-license-plates-available-july-1st-2026/',
     'sha':'72b4602e2bf41ac9008ef58f972e4a58738b346382a0ac22a9980b53f348413b',
     'size':[1024,515],'bytes':167781,
     'alt':'Idaho plate with sunrise, mountains, fields, cows, wheat, and potatoes, with “Harvest the Future” on a yellow banner.',
     'visual':'Illustrated fields, cattle, crops, mountains and yellow HARVEST THE FUTURE banner, specifically the 2026 variant.'},
    {'uid':'LPG-US-ID-00033','name':'White & Black Standard','gallery':'new_2026','num':4,'ext':'png',
     'url':'https://itd.idaho.gov/wp-content/uploads/2026/06/WhiteBlack-e1782405776923.png',
     'page':'https://itd.idaho.gov/news/two-new-idaho-license-plates-available-july-1st-2026/',
     'sha':'f677cc9f90a7827e35f327660e3a66624f5908781175f76517420f530fb0220c',
     'size':[501,255],'bytes':25019,
     'alt':'Idaho plate template with “IDAHO” at top and six black zeros centered on a white background.',
     'visual':'Minimal black IDAHO lettering and dark serial zeros on white plate, the 2026 white-and-black option.'},
]

def sha(b):return hashlib.sha256(b).hexdigest()
def once(text,old,new):
    if text.count(old)!=1 or (old!=new and new in text):
        raise ValueError('Missing or ambiguous baseline marker: '+old)
    return text.replace(old,new)
def jpg(raw,limit):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        image=ImageOps.exif_transpose(im).convert('RGBA')
        if image.width<150 or image.height<70 or not 1.35<=image.width/image.height<=3.8:
            raise ValueError('Implausible source plate dimensions: '+str(image.size))
        white=Image.new('RGBA',image.size,'white');white.alpha_composite(image)
        rgb=white.convert('RGB');rgb.thumbnail((limit,limit),Image.Resampling.LANCZOS)
        dst=io.BytesIO();rgb.save(dst,'JPEG',quality=90,optimize=True,subsampling=0)
        return dst.getvalue(),list(rgb.size)
def integrate(root,evidence):
    if len(ROWS)!=3 or len({r['uid'] for r in ROWS})!=3:raise ValueError('Duplicate batch UID')
    galleries={}
    for k,x in AGENCIES.items():
        folder=evidence/x['folder']
        registry=(folder/'assets.json').read_bytes()
        html=(folder/'source.html').read_bytes()
        if sha(registry)!=x['registry_sha'] or sha(html)!=x['html_sha']:
            raise ValueError('Source page or agency asset registry changed: '+k)
        items=json.loads(registry)
        galleries[k]={Path(a.get('file','')).name:a for a in items if a.get('status')=='downloaded'}
    canonical=json.loads((root/'data/image-campaign/manifest.json').read_text())
    if len(canonical)!=1138 or len({x['uid'] for x in canonical})!=1138:
        raise ValueError('Immutable canonical catalog changed')
    c={x['uid']:x for x in canonical}
    mf=root/'data/catalog-images.js';code=mf.read_text()
    if not code.startswith(PREFIX):raise ValueError('Bad current manifest format')
    current=json.loads(code[len(PREFIX):].strip().removesuffix(';'))
    if len(current)!=698 or any(r['uid'] in current for r in ROWS):
        raise ValueError('Baseline 698 or UID exclusions changed')
    rendered={}; selected={}; records=[]
    for row in ROWS:
        uid=row['uid'];g=row['gallery']
        p=c.get(uid)
        if not p or p['name']!=row['name'] or p['jurisdiction_id']!='US-ID':
            raise ValueError('Exact source-to-canonical UID name mismatch '+uid)
        asset=f"asset_{row['num']:04d}.{row['ext']}"
        rec=galleries[g].get(asset)
        if not rec or (rec.get('source_page_url'),rec.get('direct_image_url'),
                       rec.get('sha256'),rec.get('alt_text'),
                       rec.get('bytes'),rec.get('width_px'),rec.get('height_px'))!=(
                           row['page'],row['url'],row['sha'],row['alt'],
                           row['bytes'],row['size'][0],row['size'][1]):
            raise ValueError('Official archived asset metadata drift '+uid)
        file=(evidence/AGENCIES[g]['folder']/asset).resolve()
        if not file.is_relative_to(evidence.resolve()):raise ValueError('Unsafe original file path')
        raw=file.read_bytes()
        if sha(raw)!=row['sha'] or len(raw)!=row['bytes']:raise ValueError('Original SHA-256 mismatch '+uid)
        with Image.open(io.BytesIO(raw)) as src:
            src.verify()
        with Image.open(io.BytesIO(raw)) as src:
            if list(src.size)!=row['size']:raise ValueError('Original size mismatch '+uid)
        variants={}
        for kind,limit in [('display',800),('thumbnail',300)]:
            path=f'assets/plates/{uid}-{kind}.jpg'
            if (root/path).exists() or path in rendered:raise ValueError('Would overwrite image '+path)
            data,shape=jpg(raw,limit);rendered[path]=data;variants[kind]={'sha256':sha(data),'size':shape}
        selected[uid]={
            'name':row['name'],'image':f'./assets/plates/{uid}-display.jpg',
            'thumbnail':f'./assets/plates/{uid}-thumbnail.jpg',
            'source_sha256':row['sha'],'source_url':row['page'],'source_asset_url':row['url'],
            'source_date':'2026-11-02','source_label':row['alt'],
            'match_status':'source_matched','era_status':'unverified',
            'human_approval':False,'project_use_basis':'owner_directed_fair_use_reference'}
        records.append({
            'uid':uid,'name':row['name'],'jurisdiction_id':'US-ID',
            'government_page_url':row['page'],'government_image_url':row['url'],
            'source_alt_text':row['alt'],'source_visual_identity_basis':row['visual'],
            'original_archive_run':RUN,'original_archive_artifact':f'official-plate-harvest-{RUN}',
            'original_archive_member':AGENCIES[g]['folder']+'/'+asset,
            'source_html_sha256':AGENCIES[g]['html_sha'],
            'source_asset_registry_sha256':AGENCIES[g]['registry_sha'],
            'source_original_sha256':row['sha'],'source_bytes':row['bytes'],
            'display_sha256':variants['display']['sha256'],'thumbnail_sha256':variants['thumbnail']['sha256'],
            'display_size':variants['display']['size'],'thumbnail_size':variants['thumbnail']['size'],
            'match_status':'source_matched','era_status':'unverified','human_approval':False,
            'commercial_rights_approval':False})
    if len(rendered)!=6 or len(current)+len(selected)!=701:raise ValueError('Image selection count mismatch')
    swpath=root/'sw.js'
    new_sw=once(swpath.read_text(),OLD,NEW)
    testpath=root/'tests/catalog-images.cjs'
    tests=once(testpath.read_text(),OLD,NEW)
    tests=once(tests,'assert.equal(cacheCount,1396)','assert.equal(cacheCount,1402)')
    marker="await page.locator('#researchState').selectOption('US-NJ');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),1);"
    tests=once(tests,marker,marker+"await page.locator('#researchState').selectOption('US-ID');assert.equal(await page.locator('#researchResults .catalog-thumb').count(),3);")
    queuepath=root/'docs/CURRENT_IMAGE_CAMPAIGN_QUEUE.md';q=queuepath.read_text()
    q=once(q,'**698 / 1,138 source-matched','**701 / 1,138 source-matched')
    q=once(q,'(61.25%)','(61.60%)')
    q=once(q,'**440 UIDs remain unresolved**','**437 UIDs remain unresolved**')
    q=once(q,'**1,396** public display/thumbnail','**1,402** public display/thumbnail')
    q=once(q,'CA-ON 39, NJ 1.','CA-ON 39, NJ 1, ID 3.')
    q=once(q,'| Idaho | 68 |','| Idaho | 65 |')
    q=once(q,'Remaining **440** distributed','Remaining **437** distributed')
    q=once(q,'All 697 image entries remain','All 701 current image entries remain')
    q=once(q,'## Current truth\n','## Current truth\n- **2026-11-02 Idaho +3:** archived ITD original source files from Actions run 41486647380, independently matched and SHA-pinned for Scenic Idaho, 2026 Harvest the Future Agriculture, and 2026 White & Black standard; original page/registry SHA-pinned. Legacy plate poster source still 404, interactive guide static page contains no downloaded imagery. Idaho remaining 65. Era/human and commercial rights remain unverified; originals retained privately (Library source archive libfile_812c83d5016c8191961afd6e0845b08b).\n')
    recordpath=root/'database/image-reconciliation-idaho-three-20261102.json'
    if recordpath.exists():raise ValueError('Would overwrite reconciliation record')
    for path,binary in rendered.items():
        dst=root/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(binary)
    mf.write_text(PREFIX+json.dumps(dict(sorted({**current,**selected}.items())),separators=(',',':'),ensure_ascii=False)+';\n')
    swpath.write_text(new_sw);testpath.write_text(tests);queuepath.write_text(q)
    recordpath.write_text(json.dumps({'selected_count':3,'baseline_source_matched':698,'total_source_matched':701,
          'remaining':437,'private_archive_library_file_id':'libfile_812c83d5016c8191961afd6e0845b08b',
          'era_status':'unverified','human_approval':False,'rows':records},indent=2,ensure_ascii=False)+'\n')
    return {'added':3,'total':701,'remaining':437,'uids':list(selected)}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--evidence-dir',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(integrate(a.root,a.evidence_dir.resolve()),indent=2))
