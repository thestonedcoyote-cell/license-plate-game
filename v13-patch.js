(()=>{
  const VERSION='13.0-alpha';
  const COLORS=[
    ['Any','#eee5d2'],['White','#f5f1e9'],['Black','#202020'],['Blue','#5b82aa'],['Light blue','#acd3e5'],
    ['Dark blue','#294f78'],['Red','#b65049'],['Green','#557d5c'],['Yellow','#e4c356'],['Orange','#d68a43'],
    ['Pink','#e2a8ba'],['Purple','#7b668f'],['Gray','#969a99'],['Brown','#80634c'],['Multi','#71829b']
  ];
  const $=id=>document.getElementById(id);
  const standalone=window.matchMedia?.('(display-mode: standalone)').matches||window.navigator.standalone===true;
  const desktop=new URLSearchParams(location.search).get('desktop')==='1'||(!standalone&&window.innerWidth>=900);
  document.body.classList.toggle('lpg-standalone',!!standalone);
  document.body.classList.toggle('lpg-desktop',!!desktop);

  const bg=document.createElement('div');bg.id='regionalMapBg';bg.className='regional-map-bg';
  bg.style.background="url('./assets/roadmap-crumpled-v12.1.webp') center/cover";
  const wear=document.createElement('div');wear.id='regionalMapWear';wear.className='regional-map-wear';
  const credit=document.createElement('div');credit.className='map-credit';credit.textContent='© OpenStreetMap contributors';
  document.body.prepend(credit);document.body.prepend(wear);document.body.prepend(bg);
  let map=null,current={lat:43.8,lon:-108.5},wearKey='fallback',wearScore=0;
  const wearStoreKey='lpg.regionWear.v1';
  const readWear=()=>{try{return JSON.parse(localStorage.getItem(wearStoreKey)||'{}')}catch{return {}}};
  const writeWear=o=>localStorage.setItem(wearStoreKey,JSON.stringify(o));
  const keyFor=(lat,lon)=>`${(Math.round(lat*4)/4).toFixed(2)},${(Math.round(lon*4)/4).toFixed(2)}`;
  const applyWear=()=>{
    const store=readWear();wearScore=store[wearKey]||0;
    const p=Math.min(1,wearScore/45);
    document.documentElement.style.setProperty('--v13-wear',String(.12+p*.88));
  };
  const setRegion=(lat,lon,zoom=7)=>{
    current={lat:Math.round(lat*4)/4,lon:Math.round(lon*4)/4};
    wearKey=keyFor(current.lat,current.lon);applyWear();
    map?.setView([current.lat,current.lon],zoom,{animate:true});
  };
  const bumpWear=(amount=1)=>{
    const store=readWear();store[wearKey]=(store[wearKey]||0)+amount;writeWear(store);applyWear();
  };
  const initMap=()=>{
    if(!window.L)return;
    map=L.map(bg,{zoomControl:false,attributionControl:false,dragging:false,scrollWheelZoom:false,doubleClickZoom:false,boxZoom:false,keyboard:false,touchZoom:false,preferCanvas:true}).setView([43.8,-108.5],5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,crossOrigin:true}).addTo(map);
    setTimeout(()=>map.invalidateSize(),150);
  };
  initMap();
  const locate=()=>{
    if(!navigator.geolocation)return;
    navigator.geolocation.getCurrentPosition(
      p=>setRegion(p.coords.latitude,p.coords.longitude,7),
      ()=>{},
      {enableHighAccuracy:false,maximumAge:900000,timeout:7000}
    );
  };
  if(navigator.permissions?.query){
    navigator.permissions.query({name:'geolocation'}).then(r=>{if(r.state==='granted')locate()}).catch(()=>{});
  }
  $('useGps')?.addEventListener('click',()=>setTimeout(locate,250));
  document.addEventListener('click',e=>{
    if(e.target.closest?.('[data-add]'))bumpWear(2);
    if(e.target.closest?.('#cameraShutter'))bumpWear(1);
  },true);

  const norm=s=>String(s||'').trim().toLowerCase();
  const indexFor=card=>{
    const text=card.querySelector('.dial-value')?.textContent||'Any';
    const i=COLORS.findIndex(c=>norm(c[0])===norm(text));return i>=0?i:0;
  };
  const moveUnderlying=(card,target)=>{
    let current=indexFor(card);target=Math.max(0,Math.min(COLORS.length-1,target));
    if(current===target)return;
    const forward=(target-current+COLORS.length)%COLORS.length;
    const backward=(current-target+COLORS.length)%COLORS.length;
    const dir=forward<=backward?'1':'-1';
    const count=Math.min(forward,backward);
    const btn=card.querySelector(`.dial-arrow[data-dir="${dir}"]`);
    for(let i=0;i<count;i++)btn?.click();
  };
  document.querySelectorAll('#identify .color-dial').forEach(card=>{
    if(card.querySelector('.v13-color-slider'))return;
    const value=indexFor(card);
    const swatch=document.createElement('div');swatch.className='v13-slider-swatch';swatch.style.background=COLORS[value][1];
    const input=document.createElement('input');input.type='range';input.min='0';input.max=String(COLORS.length-1);input.step='1';input.value=String(value);input.className='v13-color-slider';
    const label=document.createElement('div');label.className='v13-slider-value';label.textContent=COLORS[value][0];
    const sync=()=>{const i=Number(input.value);swatch.style.background=COLORS[i][1];label.textContent=COLORS[i][0];moveUnderlying(card,i)};
    input.addEventListener('input',sync);input.addEventListener('change',sync);
    card.appendChild(swatch);card.appendChild(input);card.appendChild(label);
  });
  const tool=$('identify')?.querySelector('.identify-toolbox');
  if(tool&&!tool.querySelector('.v13-slider-help')){
    const h=document.createElement('div');h.className='v13-slider-help';h.textContent='Drag the sliders. Changes apply while your finger moves.';tool.querySelector('.color-dials')?.after(h);
  }
  const refreshSliders=()=>document.querySelectorAll('#identify .color-dial').forEach(card=>{
    const i=indexFor(card),input=card.querySelector('.v13-color-slider'),swatch=card.querySelector('.v13-slider-swatch'),label=card.querySelector('.v13-slider-value');
    if(input&&document.activeElement!==input&&input.value!==String(i))input.value=String(i);
    if(swatch&&swatch.style.background!==COLORS[i][1])swatch.style.background=COLORS[i][1];
    if(label&&label.textContent!==COLORS[i][0])label.textContent=COLORS[i][0];
  });
  document.querySelectorAll('#identify .dial-value').forEach(el=>new MutationObserver(refreshSliders).observe(el,{subtree:true,childList:true,characterData:true}));
  $('v11IdentifyReset')?.addEventListener('click',()=>setTimeout(refreshSliders,0));

  const updateMode=()=>{
    const force=new URLSearchParams(location.search).get('desktop')==='1';
    const d=force||(!standalone&&window.innerWidth>=900);
    document.body.classList.toggle('lpg-desktop',d);
    setTimeout(()=>map?.invalidateSize(),60);
  };
  window.addEventListener('resize',updateMode);updateMode();
  const requested=new URLSearchParams(location.search).get('screen');
  if(requested)setTimeout(()=>document.querySelector(`.nav-btn[data-screen="${CSS.escape(requested)}"]`)?.click(),80);
  document.documentElement.dataset.lpgAppMode=standalone?'standalone':(desktop?'desktop-browser':'mobile-browser');
  document.documentElement.dataset.lpgVisual='real-map-paper-v13';
  window.LPG_VISUAL_VERSION=VERSION;
  console.info('License Plate Game 13: regional map + paper images + drag sliders + desktop desk');
})();
