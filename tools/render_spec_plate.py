#!/usr/bin/env python3
"""Render a deliberately simple license-plate reference from factual/spec inputs.

This tool does not trace or ingest copyrighted artwork. It renders only elements
explicitly supplied in a JSON spec. Protected/uncleared marks are represented by
labeled placeholders until separately cleared.
"""
import argparse, json, html
from pathlib import Path

def esc(x): return html.escape(str(x))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('--out')
    a=ap.parse_args()
    s=json.loads(Path(a.spec).read_text(encoding='utf-8'))
    w=int(s.get('width',1200)); h=int(s.get('height',600))
    bg=s.get('background','#f5f5f2'); fg=s.get('text_color','#17254a')
    state=s.get('state_name',''); top=s.get('top_text',''); bottom=s.get('bottom_text','')
    serial=s.get('serial_example','ABC 123'); border=s.get('border_color',fg)
    layers=[]
    for band in s.get('bands',[]):
        y=float(band.get('y',0))*h; bh=float(band.get('height',0))*h
        layers.append(f'<rect x="0" y="{y:.1f}" width="{w}" height="{bh:.1f}" fill="{esc(band.get("color",bg))}"/>')
    for mark in s.get('uncleared_marks',[]):
        x=float(mark.get('x',.08))*w; y=float(mark.get('y',.5))*h; mw=float(mark.get('width',.18))*w; mh=float(mark.get('height',.28))*h
        label=esc(mark.get('label','mark'))
        layers.append(f'<rect x="{x:.1f}" y="{y-mh/2:.1f}" width="{mw:.1f}" height="{mh:.1f}" rx="16" fill="none" stroke="{fg}" stroke-dasharray="12 10" opacity=".42"/>')
        layers.append(f'<text x="{x+mw/2:.1f}" y="{y+8:.1f}" text-anchor="middle" font-size="28" fill="{fg}" opacity=".58">{label}</text>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="100%" height="100%" rx="34" fill="{bg}"/>
{''.join(layers)}
<rect x="18" y="18" width="{w-36}" height="{h-36}" rx="28" fill="none" stroke="{border}" stroke-width="10"/>
<text x="{w/2}" y="{h*.15}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{h*.10:.0f}" font-weight="700" fill="{fg}">{esc(state or top)}</text>
<text x="{w/2}" y="{h*.57}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{h*.28:.0f}" font-weight="700" letter-spacing="12" fill="{fg}">{esc(serial)}</text>
<text x="{w/2}" y="{h*.88}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{h*.075:.0f}" font-weight="600" fill="{fg}">{esc(bottom)}</text>
</svg>'''
    out=Path(a.out or Path(a.spec).with_suffix('.svg')); out.write_text(svg,encoding='utf-8')
    out.with_suffix('.provenance.json').write_text(json.dumps({'renderer':'render_spec_plate.py v1','spec_file':str(Path(a.spec).name),'legal_sources':s.get('legal_sources',[]),'verification_references':s.get('verification_references',[]),'human_verification_status':s.get('human_verification_status','pending'),'public_use_class':s.get('public_use_class','unassessed'),'note':'Independent rendering from supplied specifications; no source image pixels were copied.'},indent=2),encoding='utf-8')
    print(out)
if __name__=='__main__': main()
