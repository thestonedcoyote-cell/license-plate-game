(()=>{
  const INTRO_KEY='lpg.v8.onboarded';
  const PROFILE_KEY='lpg.profile.v1';
  const VERSION='9.0-alpha';
  const $=id=>document.getElementById(id);

  // Layer the newer visual skin over the stable core. Keeping this as a patch lets us
  // iterate on the phone UI without destabilizing catalog/camera/sighting logic.
  const ensureCss=(href,key)=>{
    if(document.querySelector(`link[data-${key}]`))return;
    const link=document.createElement('link'); link.rel='stylesheet'; link.href=href; link.dataset[key]='1'; document.head.appendChild(link);
  };
  ensureCss('./v8.css','lpgV8');
  ensureCss('./v9.css','lpgV9');

  const makePlayerId=()=>crypto.randomUUID?.()||`local-${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
  const loadProfile=()=>{
    let p={}; try{p=JSON.parse(localStorage.getItem(PROFILE_KEY))||{}}catch(e){}
    if(!p.player_id)p.player_id=makePlayerId();
    if(!p.created_at)p.created_at=new Date().toISOString();
    p.username=p.username||'';
    p.schema_version=1;
    p.score_version=p.score_version||'alpha-1';
    p.social_sync='local_only';
    localStorage.setItem(PROFILE_KEY,JSON.stringify(p));
    return p;
  };
  let profile=loadProfile();

  const wait=()=>{
    if(!$('launchIdentify')?.onclick || !$('useGps')?.onclick){setTimeout(wait,80);return}

    // Camera must always have an obvious escape hatch.
    $('cameraToIdentify')?.addEventListener('click',()=>$('launchIdentify').click());
    $('cameraToHome')?.addEventListener('click',()=>document.querySelector('[data-screen="home"]')?.click());

    // First-run introduction is intentionally short and can be reopened from More.
    const intro=$('introModal');
    const openIntro=()=>intro?.classList.add('open');
    const closeIntro=()=>{localStorage.setItem(INTRO_KEY,'1');intro?.classList.remove('open')};
    $('introStart')?.addEventListener('click',closeIntro);
    $('howToPlay')?.addEventListener('click',openIntro);
    if(!localStorage.getItem(INTRO_KEY))openIntro();

    // Preserve core location logic, but keep the sheet visible long enough to confirm the result.
    const gps=$('useGps'), manual=$('useManual'), modal=$('locationModal'), status=$('gpsStatus'), sel=$('manualLocation');
    const originalGps=gps?.onclick, originalManual=manual?.onclick;
    const setStatus=(ok,title,detail)=>{
      if(!status)return;
      status.className='location-status'+(ok?' ready':'');
      status.innerHTML=`<strong>${ok?'✓ ':''}${title}</strong><span>${detail}</span>`;
    };
    if(gps&&originalGps){
      gps.onclick=async()=>{
        gps.disabled=true; const old=gps.textContent; gps.textContent='Checking GPS…';
        try{
          await originalGps(); modal?.classList.add('open');
          if(!navigator.geolocation){setStatus(false,'GPS unavailable','Choose a state or province manually instead.');return}
          navigator.geolocation.getCurrentPosition(
            p=>setStatus(true,'Phone location confirmed',`Accuracy about ${Math.round(p.coords.accuracy)} m. New sightings will use your current location.`),
            ()=>setStatus(false,'Could not confirm GPS','Your browser did not return a location. Try again or choose an area manually.'),
            {enableHighAccuracy:false,timeout:3500,maximumAge:300000}
          );
        } finally {gps.disabled=false; gps.textContent=old}
      };
    }
    if(manual&&originalManual){
      manual.onclick=()=>{
        if(!sel?.value){setStatus(false,'Choose an area first','Pick a state or province from the list below.');return}
        originalManual(); modal?.classList.add('open');
        setStatus(true,`Using ${sel.options[sel.selectedIndex]?.textContent?.split(' · ')[0]||'selected area'}`,'New sightings will use this as the playing area.');
      };
    }

    // Social foundation. Nothing is sent anywhere yet. The stable player ID is intentionally
    // created now so later account/sync work can migrate rather than reinvent local identity.
    const settingsGrid=document.querySelector('.settings-grid');
    if(settingsGrid&&!document.querySelector('.player-card')){
      const card=document.createElement('div'); card.className='setting player-card';
      card.innerHTML=`<h3>Player profile <span class="beta">FOUNDATION</span></h3>
        <p>Pick a username for scoreboards and friends later. For now it stays only on this device; online uniqueness is not claimed yet.</p>
        <div class="username-row"><input id="playerUsername" maxlength="24" autocomplete="off" placeholder="Username" aria-label="Player username"><button id="saveUsername" class="action">Save</button></div>
        <div id="usernameStatus" class="player-id"></div>
        <div class="social-preview"><div><strong id="profileUnique">0</strong><span>plates</span></div><div><strong id="profileOrigins">0</strong><span>origins</span></div><div><strong id="profileWins">0</strong><span>wins</span></div></div>`;
      settingsGrid.prepend(card);
      const input=$('playerUsername'), info=$('usernameStatus'); input.value=profile.username||'';
      const showProfileStatus=(msg)=>info.textContent=`${msg} · Player ID ${profile.player_id.slice(0,8)}… · local only`;
      showProfileStatus(profile.username?`@${profile.username}`:'No username yet');
      $('saveUsername').onclick=()=>{
        const v=input.value.trim();
        if(v && !/^[A-Za-z0-9._-]{3,24}$/.test(v)){showProfileStatus('Use 3–24 letters, numbers, dot, dash, or underscore');return}
        profile.username=v; profile.updated_at=new Date().toISOString(); localStorage.setItem(PROFILE_KEY,JSON.stringify(profile));
        showProfileStatus(v?`@${v}`:'Username cleared'); renderProfileSlip();
      };
    }

    const home=document.getElementById('home');
    const renderProfileSlip=()=>{
      let slip=document.querySelector('.profile-slip');
      if(!slip&&home){slip=document.createElement('div');slip.className='profile-slip';const actions=home.querySelector('.home-actions');home.insertBefore(slip,actions)}
      if(!slip)return;
      slip.innerHTML=`<div><strong>${profile.username?'@'+profile.username:'Your road notebook'}</strong><br><span>${profile.username?'local profile ready for future social sync':'Add a username in More when you feel like it'}</span></div><span>v${VERSION}</span>`;
    };
    renderProfileSlip();

    const syncProfileCounts=()=>{
      const txt=id=>parseInt($(id)?.textContent||'0',10)||0;
      $('profileUnique')&&($('profileUnique').textContent=txt('homeUnique'));
      $('profileOrigins')&&($('profileOrigins').textContent=txt('homeOrigins'));
      $('profileWins')&&($('profileWins').textContent=txt('earnedCount'));
    };
    syncProfileCounts();
    new MutationObserver(syncProfileCounts).observe(document.body,{subtree:true,childList:true,characterData:true});

    // Installed PWA update behavior: same icon/link forever. Check on every launch and expose a
    // manual button. We avoid surprise mid-camera reloads; when a new worker takes over, offer refresh.
    const updateBox=document.createElement('div'); updateBox.className='update-note'; updateBox.innerHTML='<strong>Plate Game update ready.</strong><button type="button">Refresh</button>'; document.body.appendChild(updateBox);
    updateBox.querySelector('button').onclick=()=>location.reload();
    let changing=false;
    const showUpdate=()=>updateBox.classList.add('show');
    if('serviceWorker' in navigator){
      navigator.serviceWorker.ready.then(reg=>{
        reg.update().catch(()=>{});
        reg.addEventListener('updatefound',()=>{
          const w=reg.installing; if(!w)return;
          w.addEventListener('statechange',()=>{if(w.state==='installed'&&navigator.serviceWorker.controller)showUpdate()});
        });
      });
      navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!changing){changing=true;showUpdate()}});
    }
    if(settingsGrid&&!$('checkUpdates')){
      const updateCard=document.createElement('div'); updateCard.className='setting';
      updateCard.innerHTML=`<h3>App updates</h3><p>Your installed app uses this same web address and checks for a newer build when it opens. You should not need to reinstall or hunt down a new link.</p><button id="checkUpdates" class="action">Check now</button> <span class="player-id">v${VERSION}</span>`;
      settingsGrid.appendChild(updateCard);
      $('checkUpdates').onclick=async()=>{const reg=await navigator.serviceWorker?.getRegistration(); if(!reg){alert('No service worker is active.');return} await reg.update(); alert('Update check complete. If a newer build is ready, a refresh notice will appear.')};
    }

    // Remove database-flavored wording from user-facing copy as it appears.
    const softenWords=()=>{
      document.querySelectorAll('.badge-desc,.setting p,.uncertain,.drawer').forEach(el=>{
        el.childNodes.forEach(n=>{if(n.nodeType===Node.TEXT_NODE)n.textContent=n.textContent.replace(/jurisdictions/gi,'places').replace(/jurisdiction/gi,'place')})
      });
    };
    softenWords(); new MutationObserver(softenWords).observe(document.body,{subtree:true,childList:true});
  };
  wait();
})();
