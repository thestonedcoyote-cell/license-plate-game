(()=>{
  const VERSION='12.0-alpha';
  const $=id=>document.getElementById(id);
  document.body.classList.add('lpg-v12-roadtrip');

  const showScreen=id=>{
    document.querySelectorAll('main>.screen').forEach(s=>s.classList.toggle('active',s.id===id));
    document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.screen===id));
    document.body.classList.toggle('lpg-camera-mode',id==='camera');
    if(id==='camera') setTimeout(()=>window.scrollTo(0,0),0);
  };

  const home=$('home');
  const homeHero=home?.querySelector('.home-hero,.hero');
  if(homeHero){
    homeHero.classList.add('home-hero');
    homeHero.innerHTML='<div class="eyebrow">Road trip</div><h1>License Plate Game</h1><p>Road trip notebook.</p>';
  }
  const homeActions=home?.querySelector('.home-actions');
  const cameraLaunch=$('launchCamera');
  const identifyLaunch=$('launchIdentify');
  if(cameraLaunch){
    cameraLaunch.classList.add('camera');
    cameraLaunch.innerHTML='<div class="launch-icon" aria-hidden="true">📷</div><div class="launch-title">Take a picture</div><div class="launch-sub">Snap a license plate on the road.</div>';
  }
  if(identifyLaunch){
    identifyLaunch.classList.add('identify');
    identifyLaunch.innerHTML='<div class="launch-icon" aria-hidden="true">▭</div><div class="launch-title">Identify a plate</div><div class="launch-sub">Not sure where it\'s from? We can help.</div>';
  }
  const researchLaunch=$('researchLaunch');
  if(researchLaunch&&homeActions){
    researchLaunch.classList.remove('v11-kraft','v11-pin');
    researchLaunch.classList.add('launch','v12-research-card');
    researchLaunch.innerHTML='<div class="v12-action-icon" aria-hidden="true">🪪</div><span>Browse collection</span><small>See the plates you\'ve found and research the rest.</small>';
    homeActions.appendChild(researchLaunch);
  }
  home?.querySelector('.home-progress')?.setAttribute('aria-hidden','true');
  if(home&&!$('v12HomeIdentify')){
    const preview=document.createElement('div');
    preview.id='v12HomeIdentify';
    preview.className='v12-home-identify';
    preview.innerHTML=`
      <div class="v12-scribble">SAME COLORS?<br>LET'S SEE!</div>
      <h2>IDENTIFY A PLATE</h2>
      <div class="v12-mini-grid">
        <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#285a93"></div><b>Main color</b><span>Blue</span></div>
        <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#f0eee5"></div><b>Accent</b><span>White</span></div>
        <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#20262e"></div><b>Letters</b><span>Black</span></div>
        <div class="v12-example"><div class="v12-example-label">EXAMPLE<br>RESULT</div><div class="v12-example-plate">ABC 123</div><b style="font-size:.75rem">Michigan</b></div>
      </div>
      <button type="button" class="v12-open-identify">Find Matching Plates →</button>`;
    home.appendChild(preview);
    preview.querySelector('.v12-open-identify').addEventListener('click',()=>showScreen('identify'));
  }

  const nav=[...document.querySelectorAll('.nav-btn')];
  const navDefs=[
    ['home','⌂','Home'],['identify','⌕','Identify'],['camera','📷','Camera'],['collection','▤','Collection'],['settings','•••','More']
  ];
  nav.slice(0,5).forEach((b,i)=>{
    const [screen,icon,label]=navDefs[i];
    b.dataset.screen=screen;
    b.innerHTML=`<b>${icon}</b>${label}`;
    b.addEventListener('click',e=>{e.preventDefault();showScreen(screen);});
  });

  const settings=$('settings');
  const settingsGrid=settings?.querySelector('.settings-grid');
  if(settingsGrid&&!$('v12RoadTools')){
    const tools=document.createElement('div');
    tools.id='v12RoadTools';
    tools.className='setting';
    tools.innerHTML='<h3>Road-trip tools</h3><p>Map and achievements still live here. The footer stays focused on the five things you reach for most often.</p><div class="action-row"><button id="v12OpenMap" class="action">Open map</button><button id="v12OpenWins" class="action">Open wins</button></div>';
    settingsGrid.prepend(tools);
    $('v12OpenMap')?.addEventListener('click',()=>showScreen('map'));
    $('v12OpenWins')?.addEventListener('click',()=>showScreen('achievements'));
  }

  const identifyTitle=document.querySelector('#identify .identify-titleline h1');
  if(identifyTitle) identifyTitle.textContent='IDENTIFY A PLATE';
  const identifyNote=document.querySelector('#identify .identify-titleline small');
  if(identifyNote) identifyNote.innerHTML='SAME COLORS?<br>LET\'S SEE!';
  const labels=document.querySelectorAll('#identify .color-dial>label');
  if(labels[0]) labels[0].textContent='Main color';
  if(labels[1]) labels[1].textContent='Accent';
  if(labels[2]) labels[2].textContent='Letters';

  const captureCard=$('captureCard');
  if(captureCard){
    const strong=captureCard.querySelector('strong');
    if(strong) strong.textContent='Photo saved to Unidentified.';
    const identifyBtn=$('captureIdentify'); if(identifyBtn) identifyBtn.textContent='Identify this photo';
  }
  const camera=$('camera');
  if(camera) camera.setAttribute('data-no-page-scroll','true');

  document.querySelectorAll('.sheet-kicker,.eyebrow').forEach(el=>el.classList.add('v12-marker-note'));
  document.documentElement.dataset.lpgVisual='roadtrip-v12';
  window.LPG_VISUAL_VERSION=VERSION;
  console.info(`License Plate Game ${VERSION}: road-trip mockup skin active`);
})();
