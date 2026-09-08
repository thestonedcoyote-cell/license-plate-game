/* Non-destructive identification crops. Original photo blobs stay untouched. */
(()=>{
 let displayUrl='',generation=0;
 async function attach(){
  const slot=document.getElementById('currentPhoto');if(!slot)return;
  const ticket=++generation,photo=await window.LPGPhotoEditor?.active();
  if(ticket!==generation)return;if(!photo){slot.classList.remove('has-photo');slot.replaceChildren();return;}
  if(displayUrl)URL.revokeObjectURL(displayUrl);displayUrl=URL.createObjectURL(photo.cropBlob||photo.blob);
  slot.classList.add('has-photo');slot.innerHTML='<button class="reference-expand" aria-label="Expand reference photo"><img alt="Photo being identified"></button><div class="reference-tools"><strong>Your reference photo</strong><button class="action crop-photo">Crop / Zoom</button></div>';
  slot.querySelector('img').src=displayUrl;
  slot.querySelector('.reference-expand').onclick=slot.querySelector('.crop-photo').onclick=()=>open(photo);
 }
 async function open(photo){
  const dialog=document.createElement('dialog');dialog.className='photo-editor';
  dialog.innerHTML='<h2>Focus on the plate</h2><p>Pinch to zoom. Drag to position, or choose Select crop. Your original stays saved.</p><div class="crop-mode"><button class="action mode-pan" aria-pressed="true">Move photo</button><button class="action mode-select" aria-pressed="false">Select crop</button></div><div class="crop-stage"><canvas aria-label="Drag to select a photo crop"></canvas></div><div class="zoom-controls"><button class="action zoom-out" aria-label="Zoom out">−</button><input class="crop-zoom" aria-label="Photo zoom" type="range" min="1" max="6" step=".05" value="1"><output>1.0×</output><button class="action zoom-in" aria-label="Zoom in">+</button></div><details><summary>Adjust crop precisely</summary><div class="crop-values"></div></details><p class="crop-status" role="status"></p><div class="crop-actions"><button class="action crop-reset">Full photo</button><button class="action crop-cancel">Cancel</button><button class="action primary crop-save">Use crop</button></div>';
  const loadingControls=dialog.querySelectorAll("button:not(.crop-cancel),input");loadingControls.forEach(el=>el.disabled=true);
  document.body.append(dialog);dialog.showModal();
  const original=URL.createObjectURL(photo.blob),img=new Image();
  const close=()=>{URL.revokeObjectURL(original);dialog.close();dialog.remove()};
  dialog.querySelector('.crop-cancel').onclick=close;dialog.addEventListener('cancel',e=>{e.preventDefault();close()});
  try{img.src=original;await img.decode();}catch{dialog.querySelector('.crop-status').textContent='Could not load the original photo.';return;}
  if(!dialog.isConnected)return;
  const canvas=dialog.querySelector('canvas'),ctx=canvas.getContext('2d');
  const scale=Math.min((innerWidth-56)/img.naturalWidth,innerHeight*.48/img.naturalHeight,1);
  canvas.width=Math.max(1,Math.round(img.naturalWidth*scale));canvas.height=Math.max(1,Math.round(img.naturalHeight*scale));
  let crop=photo.crop?{...photo.crop}:{x:0,y:0,w:1,h:1},start=null;let zoom=1,ox=0,oy=0,mode="pan",pinch=null;const pointers=new Map();
  const fields=dialog.querySelector('.crop-values');
  for(const [key,label] of [['x','Left'],['y','Top'],['w','Width'],['h','Height']]){
   const l=document.createElement('label');l.textContent=label;const input=document.createElement('input');input.type='number';input.min=key==='w'||key==='h'?1:0;input.max=100;input.step=1;input.dataset.key=key;l.append(input);fields.append(l);
   input.onchange=()=>{crop[key]=Math.max(+input.min,Math.min(100,+input.value||0))/100;crop.x=Math.min(crop.x,.99);crop.y=Math.min(crop.y,.99);crop.w=Math.max(.01,Math.min(crop.w,1-crop.x));crop.h=Math.max(.01,Math.min(crop.h,1-crop.y));draw()};
  }
  function draw(){
   const {width:w,height:h}=canvas;ctx.clearRect(0,0,w,h);ctx.drawImage(img,ox,oy,w*zoom,h*zoom);ctx.fillStyle='#0009';ctx.beginPath();ctx.rect(0,0,w,h);ctx.rect(ox+crop.x*w*zoom,oy+crop.y*h*zoom,crop.w*w*zoom,crop.h*h*zoom);ctx.fill('evenodd');ctx.strokeStyle='#ffdf76';ctx.lineWidth=3;ctx.strokeRect(ox+crop.x*w*zoom,oy+crop.y*h*zoom,crop.w*w*zoom,crop.h*h*zoom);
   fields.querySelectorAll('input').forEach(i=>i.value=Math.round(crop[i.dataset.key]*100));
  }
  const zoomInput=dialog.querySelector('.crop-zoom');
  const clampPan=()=>{ox=Math.max(canvas.width*(1-zoom),Math.min(0,ox));oy=Math.max(canvas.height*(1-zoom),Math.min(0,oy));};
  function setZoom(next,cx=canvas.width/2,cy=canvas.height/2){next=Math.max(1,Math.min(6,next));ox=cx-(cx-ox)*next/zoom;oy=cy-(cy-oy)*next/zoom;zoom=next;clampPan();zoomInput.value=zoom;dialog.querySelector('output').textContent=zoom.toFixed(1)+'×';draw();}
  zoomInput.oninput=()=>setZoom(+zoomInput.value);dialog.querySelector('.zoom-out').onclick=()=>setZoom(zoom-.25);dialog.querySelector('.zoom-in').onclick=()=>setZoom(zoom+.25);
  for(const name of ['pan','select'])dialog.querySelector('.mode-'+name).onclick=()=>{mode=name;start=null;for(const n of ['pan','select'])dialog.querySelector('.mode-'+n).setAttribute('aria-pressed',String(n===mode));};
  const point=e=>{const b=canvas.getBoundingClientRect();return{x:(e.clientX-b.left)*canvas.width/b.width,y:(e.clientY-b.top)*canvas.height/b.height}};
  const imagePoint=p=>({x:Math.max(0,Math.min(1,(p.x-ox)/(canvas.width*zoom))),y:Math.max(0,Math.min(1,(p.y-oy)/(canvas.height*zoom)))});
  const distance=()=>{const [a,b]=[...pointers.values()];return Math.hypot(a.x-b.x,a.y-b.y)};
  canvas.onpointerdown=e=>{const p=point(e);pointers.set(e.pointerId,p);canvas.setPointerCapture(e.pointerId);start={p,image:imagePoint(p),ox,oy};if(pointers.size===2){pinch={distance:distance(),zoom};start=null}};
  canvas.onpointermove=e=>{
   if(!pointers.has(e.pointerId))return;const p=point(e);pointers.set(e.pointerId,p);
   if(pointers.size===2&&pinch){const [a,b]=[...pointers.values()];setZoom(pinch.zoom*distance()/Math.max(1,pinch.distance),(a.x+b.x)/2,(a.y+b.y)/2);return;}
   if(!start)return;
   if(mode==='pan'){ox=start.ox+p.x-start.p.x;oy=start.oy+p.y-start.p.y;clampPan();}
   else{const q=imagePoint(p),a=start.image;crop={x:Math.min(a.x,q.x),y:Math.min(a.y,q.y),w:Math.abs(a.x-q.x),h:Math.abs(a.y-q.y)}}draw();
  };
  canvas.onpointerup=canvas.onpointercancel=e=>{pointers.delete(e.pointerId);start=null;pinch=null;if(crop.w<.01||crop.h<.01)crop={x:0,y:0,w:1,h:1};draw()};
  dialog.querySelector('.crop-reset').onclick=()=>{crop={x:0,y:0,w:1,h:1};zoom=1;ox=oy=0;zoomInput.value=1;dialog.querySelector('output').textContent='1.0×';draw()};
  dialog.querySelector('.crop-save').onclick=async()=>{
   const save=dialog.querySelector('.crop-save');save.disabled=true;
   try{
    if(mode==='pan'&&zoom>1)crop={x:-ox/(canvas.width*zoom),y:-oy/(canvas.height*zoom),w:1/zoom,h:1/zoom};
    const output=document.createElement('canvas');output.width=Math.max(1,Math.round(crop.w*img.naturalWidth));output.height=Math.max(1,Math.round(crop.h*img.naturalHeight));
    output.getContext('2d').drawImage(img,crop.x*img.naturalWidth,crop.y*img.naturalHeight,crop.w*img.naturalWidth,crop.h*img.naturalHeight,0,0,output.width,output.height);
    const blob=await new Promise(resolve=>output.toBlob(resolve,'image/jpeg',.94));if(!blob)throw Error('Crop failed');
    await window.LPGPhotoEditor.save(photo.id,crop,blob);close();await attach();
   }catch{dialog.querySelector('.crop-status').textContent='Could not save the crop. Your original is safe. Please try again.';save.disabled=false;}
  };draw();loadingControls.forEach(el=>el.disabled=false);dialog.dataset.ready="true";
 }
 window.LPGPhotoUI={attach};
})();
