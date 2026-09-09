(async()=>{
  const VERSION='11.1-alpha';
  const SUPABASE_URL='https://ffhsqvhorsyonavahlul.supabase.co';
  const SUPABASE_KEY='sb_publishable_D3QTDq1I5LOJ6Nk50D4Hew_KKo5VkCk';
  const PROFILE_KEY='lpg.profile.v1', CLOUD_KEY='lpg.cloud.v1';
  const $=id=>document.getElementById(id);
  const mod=await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.115.0/+esm');
  const sb=mod.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
  window.LPG_SUPABASE=sb;
  let user=null, lastUploadedSrc='';
  let cloud={photo_sync:false}; try{cloud={...cloud,...JSON.parse(localStorage.getItem(CLOUD_KEY)||'{}')}}catch(e){}
  const saveCloud=()=>localStorage.setItem(CLOUD_KEY,JSON.stringify(cloud));
  const localProfile=()=>{try{return JSON.parse(localStorage.getItem(PROFILE_KEY)||'{}')}catch(e){return {}}};
  const toast=(msg,bad=false)=>{const t=$('toast');if(t){t.textContent=msg;t.className='toast show'+(bad?' bad':'');setTimeout(()=>t.classList.remove('show'),2800)}};
  const setStatus=(msg,kind='')=>{const e=$('cloudStatus');if(e){e.textContent=msg;e.className='cloud-status '+kind}};

  function mount(){
    const grid=document.querySelector('.settings-grid'); if(!grid||$('cloudAccountCard'))return false;
    const card=document.createElement('div');card.id='cloudAccountCard';card.className='setting cloud-card';
    card.innerHTML=`<h3>Account & cloud <span class="beta">v11.1</span></h3>
      <p>Optional account for backup, desktop photo review, and future friends/scoreboards. Local play still works without signing in.</p>
      <div id="cloudSignedOut"><input id="cloudEmail" type="email" autocomplete="email" placeholder="Email"><input id="cloudPassword" type="password" autocomplete="current-password" placeholder="Password"><div class="cloud-actions"><button id="cloudSignIn" class="action primary">Sign in</button><button id="cloudSignUp" class="action">Create account</button></div></div>
      <div id="cloudSignedIn" hidden><strong id="cloudWho"></strong><div class="cloud-actions"><button id="cloudPhotos" class="action primary">Review cloud photos</button><button id="cloudSignOut" class="action">Sign out</button></div><label class="cloud-toggle"><input id="cloudPhotoSync" type="checkbox"><span><strong>Private photo backup</strong><br>Upload new camera captures to your private account storage. Off by default.</span></label></div>
      <div id="cloudStatus" class="cloud-status">Not signed in.</div>`;
    grid.prepend(card);
    const review=document.createElement('div');review.id='cloudReview';review.className='cloud-review';review.innerHTML=`<div class="cloud-review-head"><h1>Cloud photo desk</h1><button id="closeCloudReview" class="action">Close</button></div><div class="craft-panel">Private photos synced to this account. Use this larger view to inspect what needs identifying.</div><div id="cloudPhotoGrid" class="cloud-photo-grid"></div>`;document.querySelector('.app')?.appendChild(review);
    $('cloudSignIn').onclick=()=>auth('in'); $('cloudSignUp').onclick=()=>auth('up'); $('cloudSignOut').onclick=()=>sb.auth.signOut();
    $('cloudPhotoSync').checked=!!cloud.photo_sync;$('cloudPhotoSync').onchange=e=>{cloud.photo_sync=e.target.checked;saveCloud();setStatus(cloud.photo_sync?'Private photo backup enabled.':'Private photo backup off.',cloud.photo_sync?'good':'')};
    $('cloudPhotos').onclick=()=>{review.classList.add('active');loadCloudPhotos()};$('closeCloudReview').onclick=()=>review.classList.remove('active');
    renderAuth(); return true;
  }
  async function auth(mode){
    try{
    const email=$('cloudEmail')?.value.trim(),password=$('cloudPassword')?.value||''; if(!email||password.length<6){setStatus('Enter an email and a password of at least 6 characters.','bad');return}
    setStatus(mode==='up'?'Creating account…':'Signing in…');
    const res=mode==='up'?await sb.auth.signUp({email,password}):await sb.auth.signInWithPassword({email,password});
    if(res.error){setStatus(res.error.message,'bad');return} setStatus(mode==='up'?'Account created. Check email if confirmation is required.':'Signed in.','good');
    }catch{setStatus('Account service unavailable. Your local game is still available.','bad')}
  }
  async function migrateProfile(){
    if(!user)return;const lp=localProfile();
    const {data}=await sb.from('profiles').select('username,local_player_id').eq('user_id',user.id).maybeSingle();
    const patch={local_player_id:lp.player_id||null};if(lp.username&&!data?.username)patch.username=lp.username;
    const {error}=await sb.from('profiles').upsert({user_id:user.id,...patch},{onConflict:'user_id'});if(error)setStatus('Signed in, but profile sync needs attention: '+error.message,'bad');
    else setStatus('Account connected. Local player identity linked.','good');
  }
  async function renderAuth(){
    if(!$('cloudAccountCard'))return;const {data:{user:u}}=await sb.auth.getUser();user=u||null;$('cloudSignedOut').hidden=!!user;$('cloudSignedIn').hidden=!user;
    if(user){$('cloudWho').textContent=user.email||'Signed-in player';$('cloudPhotoSync').checked=!!cloud.photo_sync;await migrateProfile()}else setStatus('Not signed in.');
  }
  sb.auth.onAuthStateChange(()=>setTimeout(renderAuth,0));

  async function syncCapture(src){
    if(!user||!cloud.photo_sync||!src||src===lastUploadedSrc)return;lastUploadedSrc=src;
    try{
      const blob=await fetch(src).then(r=>r.blob());if(!blob.type.startsWith('image/'))return;
      const clientId=crypto.randomUUID();const now=new Date().toISOString();
      const {data:s,error:se}=await sb.from('sightings').insert({user_id:user.id,client_sighting_id:clientId,identification_status:'unidentified',observed_at:now,captured_at:now,source:'camera'}).select('id').single();if(se)throw se;
      const ext=(blob.type.split('/')[1]||'jpg').replace('jpeg','jpg');const path=`${user.id}/${s.id}/original.${ext}`;
      const {error:ue}=await sb.storage.from('sighting-photos').upload(path,blob,{contentType:blob.type,upsert:false});if(ue)throw ue;
      const {error:pe}=await sb.from('sighting_photos').insert({user_id:user.id,sighting_id:s.id,storage_path:path,mime_type:blob.type});if(pe)throw pe;
      toast('Private photo backup complete.');
    }catch(e){console.error(e);toast('Cloud photo backup failed; local copy is still safe.',true);lastUploadedSrc=''}
  }
  function watchCamera(){const p=$('cameraPreview');if(!p)return setTimeout(watchCamera,250);const check=()=>{if(!p.hidden&&p.src)syncCapture(p.src)};new MutationObserver(check).observe(p,{attributes:true,attributeFilter:['src','hidden']});check()}
  async function loadCloudPhotos(){const box=$('cloudPhotoGrid');if(!box)return;box.innerHTML='<p>Loading…</p>';if(!user){box.innerHTML='<p>Sign in first.</p>';return}
    const {data,error}=await sb.from('sighting_photos').select('id,storage_path,created_at,sighting_id').order('created_at',{ascending:false}).limit(150);if(error){box.textContent=error.message;return}
    if(!data?.length){box.innerHTML='<p>No cloud photos yet. Turn on Private photo backup, then take a picture.</p>';return}
    const cards=[];for(const row of data){const {data:signed}=await sb.storage.from('sighting-photos').createSignedUrl(row.storage_path,900);if(!signed?.signedUrl)continue;cards.push(`<article class="cloud-photo"><img src="${signed.signedUrl}" alt="Private plate capture"><small>${new Date(row.created_at).toLocaleString()}</small></article>`)}box.innerHTML=cards.join('')||'<p>No readable photos.</p>';
  }
  const boot=()=>{if(!mount())return setTimeout(boot,120);watchCamera();document.documentElement.dataset.lpgCloudVersion=VERSION};boot();
})().catch(e=>console.warn('Optional cloud service unavailable; local play remains available.',e));
