(()=>{
  const VERSION='10.0-alpha';
  const $=id=>document.getElementById(id);
  const R=window.LPG_R||{};
  let lastPhotoSrc='';
  const COLOR={white:'#f8f7f1',black:'#151515',blue:'#5f89aa',dark_blue:'#183f68',navy:'#18334f',red:'#b04a42',dark_red:'#783b3b',green:'#4f7958',dark_green:'#34513e',yellow:'#e3bd48',light_yellow:'#f2df88',gold:'#d9ad38',orange:'#d98243',pink:'#e5a6bd',turquoise:'#62b7b6',gray:'#979b98',dark_gray:'#484d4e',grey:'#979b98',brown:'#80644c',purple:'#735e86',crimson:'#8b2635',dark:'#242829',unknown:'#2d3437',light_blue:'#b8d8e7'};
  const col=(v,fallback)=>COLOR[String(v||'').toLowerCase()]||fallback;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const motif=(fam,ink)=>{
    switch(fam){
      case 'm':return `<path d="M8 49 L34 19 L51 39 L68 25 L92 49 Z" fill="none" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/><path d="M32 22 L38 30 L31 29" fill="none" stroke="${ink}" stroke-width="2"/>`;
      case 'w':return `<path d="M4 38 Q18 29 32 38 T60 38 T88 38" fill="none" stroke="${ink}" stroke-width="3"/><path d="M12 47 Q25 40 38 47 T64 47 T90 47" fill="none" stroke="${ink}" stroke-width="2"/>`;
      case 'a':return `<circle cx="47" cy="34" r="8" fill="${ink}" opacity=".78"/><circle cx="35" cy="24" r="5" fill="${ink}" opacity=".78"/><circle cx="47" cy="20" r="5" fill="${ink}" opacity=".78"/><circle cx="59" cy="24" r="5" fill="${ink}" opacity=".78"/><path d="M35 44 Q47 52 59 44" fill="${ink}" opacity=".78"/>`;
      case 'f':return `<path d="M15 16 V51" stroke="${ink}" stroke-width="3"/><path d="M18 18 H75 L67 28 L75 38 H18 Z" fill="none" stroke="${ink}" stroke-width="3"/><path d="M27 22 L31 30 L22 25 H32 L23 30 Z" fill="${ink}"/>`;
      case 'g':return `<circle cx="72" cy="22" r="8" fill="none" stroke="${ink}" stroke-width="2"/><path d="M8 47 Q30 31 50 47 Q70 32 94 47" fill="none" stroke="${ink}" stroke-width="3"/><path d="M25 49 V30 M22 35 L25 39 L29 34 M22 42 L25 45 L29 40" stroke="${ink}" stroke-width="2" fill="none"/>`;
      case 'v':return `<path d="M18 41 L26 29 H67 L78 41 V48 H18 Z" fill="none" stroke="${ink}" stroke-width="3"/><circle cx="31" cy="49" r="5" fill="${ink}"/><circle cx="66" cy="49" r="5" fill="${ink}"/>`;
      case 's':return `<path d="M50 15 L57 32 L76 33 L61 44 L66 62 L50 52 L34 62 L39 44 L24 33 L43 32 Z" fill="none" stroke="${ink}" stroke-width="3"/>`;
      case 'e':return `<path d="M15 28 L50 14 L85 28 L50 42 Z" fill="none" stroke="${ink}" stroke-width="3"/><path d="M28 35 V49 Q50 58 72 49 V35" fill="none" stroke="${ink}" stroke-width="3"/>`;
      case 't':return `<path d="M25 18 H73 L80 31 L72 55 H30 L20 39 Z" fill="none" stroke="${ink}" stroke-width="3" stroke-linejoin="round"/>`;
      case 'h':return `<circle cx="30" cy="48" r="8" fill="none" stroke="${ink}" stroke-width="3"/><circle cx="68" cy="48" r="8" fill="none" stroke="${ink}" stroke-width="3"/><path d="M22 43 H75 L67 24 H33 L22 43 Z M38 24 V15 H63 V24" fill="none" stroke="${ink}" stroke-width="3"/>`;
      case 'x':return `<rect x="27" y="18" width="46" height="36" rx="8" fill="none" stroke="${ink}" stroke-width="3"/><path d="M36 45 L64 27 M36 27 L64 45" stroke="${ink}" stroke-width="2" opacity=".65"/>`;
      default:return `<path d="M29 35 H71" stroke="${ink}" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="35" r="11" fill="none" stroke="${ink}" stroke-width="2" opacity=".65"/>`;
    }
  };
  const plateSvg=a=>{
    const [bgName,textName,slogan,fam,code]=a;
    const ink=col(textName,'#1f2e38');
    const multi=/multi|illustrated/.test(String(bgName));
    const bg=multi?'url(#g)':col(bgName,'#e7e4dc');
    const sl=esc(String(slogan||'').slice(0,27));
    return `<svg class="lpg-ref-svg" viewBox="0 0 200 100" role="img" aria-label="License Plate Game reference rendering"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#d8c986"/><stop offset=".48" stop-color="#d9e5df"/><stop offset="1" stop-color="#70a3b8"/></linearGradient></defs><rect x="3" y="3" width="194" height="94" rx="9" fill="${bg}" stroke="${ink}" stroke-width="3"/><circle cx="16" cy="14" r="3" fill="none" stroke="${ink}" opacity=".42"/><circle cx="184" cy="14" r="3" fill="none" stroke="${ink}" opacity=".42"/><g transform="translate(101 3) scale(.42)" opacity=".26">${motif(fam,ink)}</g><text x="100" y="20" text-anchor="middle" fill="${ink}" font-family="Arial,sans-serif" font-size="10" font-weight="700" letter-spacing="1.1">${esc(code)}</text><text x="100" y="62" text-anchor="middle" fill="${ink}" font-family="Arial,sans-serif" font-size="25" font-weight="800" letter-spacing="3">LPG 000</text>${sl?`<text x="100" y="84" text-anchor="middle" fill="${ink}" font-family="Arial,sans-serif" font-size="8" font-weight="700">${sl}</text>`:''}<text x="187" y="92" text-anchor="end" fill="${ink}" font-family="Arial,sans-serif" font-size="5" opacity=".55">REF</text></svg>`;
  };
  const uidForCard=card=>{const el=card.querySelector('[data-add],[data-detail],[data-plate-uid],[data-uid]');return el?.dataset.add||el?.dataset.detail||el?.dataset.plateUid||el?.dataset.uid||''};
  const decorateCard=card=>{if(card.dataset.refDecorated==='1')return;const uid=uidForCard(card),spec=R[uid];if(!spec)return;const old=card.querySelector('.plate-fallback');const box=document.createElement('div');box.className='reference-plate';box.dataset.publicReference='1';box.innerHTML=plateSvg(spec);if(old)old.replaceWith(box);else card.prepend(box);card.dataset.refDecorated='1'};
  const decorateAll=()=>document.querySelectorAll('.result').forEach(decorateCard);
  decorateAll();new MutationObserver(decorateAll).observe(document.body,{subtree:true,childList:true});

  const syncCameraMode=()=>document.body.classList.toggle('lpg-camera-mode',!!$('camera')?.classList.contains('active'));
  syncCameraMode();new MutationObserver(syncCameraMode).observe(document.querySelector('main')||document.body,{subtree:true,attributes:true,attributeFilter:['class']});

  const captureCard=$('captureCard');
  if(captureCard&&!$('cameraSavedPhotos')){const note=document.createElement('div');note.className='capture-destination';note.innerHTML='<span>Photo saved in <b>Collection → Unidentified</b>.</span><button id="cameraSavedPhotos" class="action soft" type="button">Saved photos</button>';captureCard.appendChild(note);$('cameraSavedPhotos').onclick=()=>{document.querySelector('[data-screen="collection"]')?.click();setTimeout(()=>document.querySelector('[data-collection-mode="unknown"]')?.click(),30)}}
  if($('captureIdentify'))$('captureIdentify').textContent='Identify this photo →';
  const preview=$('cameraPreview');
  const captureState=()=>{const has=!!(preview&&!preview.hidden&&preview.src);document.body.classList.toggle('lpg-has-capture',has);if(has)lastPhotoSrc=preview.src};
  if(preview)new MutationObserver(captureState).observe(preview,{attributes:true,attributeFilter:['src','hidden']});captureState();

  const attachPhotoToIdentify=()=>{const banner=$('pendingPhotoBanner');if(!banner||!lastPhotoSrc)return;let wrap=banner.querySelector('.attached-photo');if(!wrap){wrap=document.createElement('div');wrap.className='attached-photo';banner.prepend(wrap)}wrap.innerHTML=`<img src="${lastPhotoSrc}" alt="Photo being identified"><div><strong>Working from this photo</strong><span>Use the clues below to connect it to a plate.</span></div>`;banner.classList.add('has-photo')};
  $('captureIdentify')?.addEventListener('click',()=>{if(preview?.src)lastPhotoSrc=preview.src;setTimeout(attachPhotoToIdentify,40)},true);
  document.body.addEventListener('click',e=>{const b=e.target.closest('#collectionUnknown button');if(!b||!/identify/i.test(b.textContent||''))return;const card=b.closest('.unknown-card,[data-sighting-id],article,div');const img=card?.querySelector('img');if(img?.src)lastPhotoSrc=img.src;setTimeout(attachPhotoToIdentify,60)},true);
  $('captureAgain')?.addEventListener('click',()=>document.body.classList.remove('lpg-has-capture'));

  document.documentElement.dataset.lpgVersion=VERSION;
  const home=$('home');if(home&&!home.querySelector('.notebook-kicker')){const k=document.createElement('div');k.className='notebook-kicker';k.innerHTML='<span>road notebook</span><i></i><span>spot • snap • collect</span>';home.prepend(k)}
})();
