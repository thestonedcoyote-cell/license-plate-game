(()=>{
  const KEY='lpg.v8.onboarded';
  const $=id=>document.getElementById(id);
  const wait=()=>{
    if(!$('launchIdentify')?.onclick || !$('useGps')?.onclick){setTimeout(wait,80);return}

    // Camera must always have an obvious escape hatch.
    $('cameraToIdentify')?.addEventListener('click',()=>$('launchIdentify').click());
    $('cameraToHome')?.addEventListener('click',()=>document.querySelector('[data-screen="home"]')?.click());

    // First-run introduction is intentionally tiny and can be reopened from More.
    const intro=$('introModal');
    const openIntro=()=>intro?.classList.add('open');
    const closeIntro=()=>{localStorage.setItem(KEY,'1');intro?.classList.remove('open')};
    $('introStart')?.addEventListener('click',closeIntro);
    $('howToPlay')?.addEventListener('click',openIntro);
    if(!localStorage.getItem(KEY))openIntro();

    // Preserve the app's location logic, but keep the sheet visible long enough
    // to explicitly confirm what happened. Existing internal location state remains authoritative.
    const gps=$('useGps'), manual=$('useManual'), modal=$('locationModal'), status=$('gpsStatus'), sel=$('manualLocation');
    const originalGps=gps?.onclick;
    const originalManual=manual?.onclick;
    const setStatus=(ok,title,detail)=>{
      if(!status)return;
      status.className='location-status'+(ok?' ready':'');
      status.innerHTML=`<strong>${ok?'✓ ':''}${title}</strong><span>${detail}</span>`;
    };
    if(gps&&originalGps){
      gps.onclick=async()=>{
        gps.disabled=true; const old=gps.textContent; gps.textContent='Checking GPS…';
        try{
          await originalGps();
          modal?.classList.add('open');
          if(!navigator.geolocation){setStatus(false,'GPS unavailable','Choose a state or province manually instead.');return}
          navigator.geolocation.getCurrentPosition(
            p=>setStatus(true,'Phone location confirmed',`Accuracy about ${Math.round(p.coords.accuracy)} m. New sightings will use your current location.`),
            ()=>setStatus(false,'Could not confirm GPS','Your browser did not return a location. You can try again or choose an area manually.'),
            {enableHighAccuracy:false,timeout:3000,maximumAge:300000}
          );
        } finally {gps.disabled=false; gps.textContent=old}
      };
    }
    if(manual&&originalManual){
      manual.onclick=()=>{
        if(!sel?.value){setStatus(false,'Choose an area first','Pick a state or province from the list below.');return}
        originalManual();
        modal?.classList.add('open');
        setStatus(true,`Using ${sel.options[sel.selectedIndex]?.textContent?.split(' · ')[0]||'selected area'}`,'New sightings will use this as the playing area.');
      };
    }

    // Remove the database-flavored word from user-facing copy as it appears.
    const softenWords=()=>{
      document.querySelectorAll('.badge-desc,.setting p,.uncertain,.drawer').forEach(el=>{
        el.childNodes.forEach(n=>{if(n.nodeType===Node.TEXT_NODE)n.textContent=n.textContent.replace(/jurisdictions/gi,'places').replace(/jurisdiction/gi,'place')})
      });
    };
    softenWords();
    new MutationObserver(softenWords).observe(document.body,{subtree:true,childList:true});
  };
  wait();
})();
