(()=>{
  const VERSION='13.0.3-alpha';
  const $=id=>document.getElementById(id);
  const show=id=>{
    document.querySelectorAll('main>.screen').forEach(s=>s.classList.toggle('active',s.id===id));
    document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.screen===id));
    document.body.classList.toggle('lpg-camera-mode',id==='camera');
  };

  // Rebuild Home from scratch after every older patch has finished. This intentionally
  // discards legacy injected UI so old v9/v10 presentation cannot ghost through.
  const home=$('home');
  if(home){
    home.innerHTML=`
      <div class="home-hero">
        <h1>License Plate Game</h1>
        <p>Road trip notebook.</p>
      </div>
      <div class="home-actions">
        <button id="fixLaunchCamera" class="launch"><div class="launch-icon">📷</div><div class="launch-title">Take a picture</div><div class="launch-sub">Snap a license plate on the road.</div></button>
        <button id="fixLaunchIdentify" class="launch"><div class="launch-icon">▭</div><div class="launch-title">Identify a plate</div><div class="launch-sub">Not sure where it's from? We can help.</div></button>
        <button id="fixLaunchCollection" class="launch"><div class="launch-icon">🪪</div><div class="launch-title">Browse collection</div><div class="launch-sub">See the plates you've found.</div></button>
      </div>
      <div class="v12-home-identify">
        <div class="v12-scribble">SAME COLORS?<br>LET'S SEE!</div>
        <h2>IDENTIFY A PLATE</h2>
        <div class="v12-mini-grid">
          <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#285a93"></div><b>Main color</b><span>Blue</span></div>
          <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#f0eee5"></div><b>Accent</b><span>White</span></div>
          <div class="v12-mini-dial"><div class="v12-mini-dot" style="background:#20262e"></div><b>Letters</b><span>Black</span></div>
          <div class="v12-example"><div class="v12-example-label">EXAMPLE<br>RESULT</div><div class="v12-example-plate">ABC 123</div><b style="font-size:.72rem">Michigan</b></div>
        </div>
        <button id="fixOpenIdentify" class="v12-open-identify">Find Matching Plates →</button>
      </div>`;
    $('fixLaunchCamera')?.addEventListener('click',()=>show('camera'));
    $('fixLaunchIdentify')?.addEventListener('click',()=>show('identify'));
    $('fixLaunchCollection')?.addEventListener('click',()=>show('collection'));
    $('fixOpenIdentify')?.addEventListener('click',()=>show('identify'));
  }

  // Footer is rebuilt into the approved five-item order and gets its own handlers.
  const nav=document.querySelector('.bottom-nav .nav-inner');
  if(nav){
    nav.innerHTML=`
      <button class="nav-btn active" data-screen="home"><b>⌂</b>Home</button>
      <button class="nav-btn" data-screen="identify"><b>⌕</b>Identify</button>
      <button class="nav-btn" data-screen="camera"><b>📷</b>Camera</button>
      <button class="nav-btn" data-screen="collection"><b>▤</b>Collection</button>
      <button class="nav-btn" data-screen="settings"><b>•••</b>More</button>`;
    nav.querySelectorAll('.nav-btn').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();show(b.dataset.screen)}));
  }

  // Preserve Map/Wins after removing them from the footer.
  const settingsGrid=document.querySelector('#settings .settings-grid');
  if(settingsGrid&&!$('fixRoadTools')){
    const card=document.createElement('div');card.id='fixRoadTools';card.className='setting';
    card.innerHTML='<h3>Road-trip tools</h3><p>Map and achievements are still here.</p><div class="action-row"><button id="fixMap" class="action">Open map</button><button id="fixWins" class="action">Open wins</button></div>';
    settingsGrid.prepend(card);$('fixMap')?.addEventListener('click',()=>show('map'));$('fixWins')?.addEventListener('click',()=>show('achievements'));
  }

  document.documentElement.dataset.lpgVisual='screenshot-reset-v13-0-3';
  window.LPG_VISUAL_VERSION=VERSION;
  console.info('License Plate Game 13.0.3: screenshot-driven Home reset active');
})();
