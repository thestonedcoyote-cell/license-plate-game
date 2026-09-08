/* Non-destructive identification crops. Original photo blobs stay untouched. */
(()=>{
 let displayUrl='',generation=0;
 async function attach(){
  const slot=document.getElementById('currentPhoto');if(!slot)return;
  const ticket=++generation,photo=await window.LPGPhotoEditor?.active();
  if(ticket!==generation)return;if(!photo){slot.classList.remove('has-photo');slot.replaceChildren();return;}
  if(displayUrl)URL.revokeObjectURL(displayUrl);displayUrl=URL.createObjectURL(photo.cropBlob||photo.blob);
  slot.classList.add('has-photo');slot.innerHTML='<button class="reference-expand" aria-label="Expand reference photo"><img alt="Photo being identified"></button><div class="reference-tools"><strong>Your reference photo</strong><button class="action crop-photo">Crop / expand</button></div>';
  slot.querySelector('img').src=displayUrl;
  slot.querySelector('.reference-expand').onclick=slot.querySelector('.crop-photo').onclick=()=>open(photo);
 }
 async function open(photo){
  const dialog=document.createElement('dialog');dialog.className='photo-editor';
  dialog.innerHTML='<h2>Focus on the plate</h2><p>Drag a box around the plate. Your original photo stays saved.</p><div class="crop-stage"><canvas aria-label="Drag to select a photo crop"></canvas></div><details><summary>Adjust crop precisely</summary><div class="crop-values"></div></details><p class="crop-status" role="status"></p><div class="crop-actions"><button class="action crop-reset">Full photo</button><button class="action crop-cancel">Cancel</button><button class="action primary crop-save">Use crop</button></div>';
  document.body.append(dialog);dialog.showModal();
  const original=URL.createObjectURL(photo.blob),img=new Image();
  const close=()=>{URL.revokeObjectURL(original);dialog.close();dialog.remove()};
  dialog.querySelector('.crop-cancel').onclick=close;dialog.addEventListener('cancel',e=>{e.preventDefault();close()});
  try{img.src=original;await img.decode();}catch{dialog.querySelector('.crop-status').textContent='Could not load the original photo.';return;}
  if(!dialog.isConnected)return;
  const canvas=dialog.querySelector('canvas'),ctx=canvas.getContext('2d');
  const scale=Math.min((innerWidth-56)/img.naturalWidth,innerHeight*.48/img.naturalHeight,1);
  canvas.width=Math.max(1,Math.round(img.naturalWidth*scale));canvas.height=Math.max(1,Math.round(img.naturalHeight*scale));
  let crop=photo.crop?{...photo.crop}:{x:0,y:0,w:1,h:1},start=null;
  const fields=dialog.querySelector('.crop-values');
  for(const [key,label] of [['x','Left'],['y','Top'],['w','Width'],['h','Height']]){
   const l=document.createElement('label');l.textContent=label;const input=document.createElement('input');input.type='number';input.min=key==='w'||key==='h'?1:0;input.max=100;input.step=1;input.dataset.key=key;l.append(input);fields.append(l);
   input.onchange=()=>{crop[key]=Math.max(+input.min,Math.min(100,+input.value||0))/100;crop.x=Math.min(crop.x,.99);crop.y=Math.min(crop.y,.99);crop.w=Math.max(.01,Math.min(crop.w,1-crop.x));crop.h=Math.max(.01,Math.min(crop.h,1-crop.y));draw()};
  }
  function draw(){
   const {width:w,height:h}=canvas;ctx.drawImage(img,0,0,w,h);ctx.fillStyle='#0009';ctx.beginPath();ctx.rect(0,0,w,h);ctx.rect(crop.x*w,crop.y*h,crop.w*w,crop.h*h);ctx.fill('evenodd');ctx.strokeStyle='#ffdf76';ctx.lineWidth=3;ctx.strokeRect(crop.x*w,crop.y*h,crop.w*w,crop.h*h);
   fields.querySelectorAll('input').forEach(i=>i.value=Math.round(crop[i.dataset.key]*100));
  }
  const point=e=>{const b=canvas.getBoundingClientRect();return{x:Math.max(0,Math.min(1,(e.clientX-b.left)/b.width)),y:Math.max(0,Math.min(1,(e.clientY-b.top)/b.height))}};
  canvas.onpointerdown=e=>{start=point(e);canvas.setPointerCapture(e.pointerId)};
  canvas.onpointermove=e=>{if(!start)return;const p=point(e);crop={x:Math.min(start.x,p.x),y:Math.min(start.y,p.y),w:Math.abs(start.x-p.x),h:Math.abs(start.y-p.y)};draw()};
  canvas.onpointerup=canvas.onpointercancel=()=>{start=null;if(crop.w<.01||crop.h<.01)crop={x:0,y:0,w:1,h:1};draw()};
  dialog.querySelector('.crop-reset').onclick=()=>{crop={x:0,y:0,w:1,h:1};draw()};
  dialog.querySelector('.crop-save').onclick=async()=>{
   const save=dialog.querySelector('.crop-save');save.disabled=true;
   try{
    const output=document.createElement('canvas');output.width=Math.max(1,Math.round(crop.w*img.naturalWidth));output.height=Math.max(1,Math.round(crop.h*img.naturalHeight));
    output.getContext('2d').drawImage(img,crop.x*img.naturalWidth,crop.y*img.naturalHeight,crop.w*img.naturalWidth,crop.h*img.naturalHeight,0,0,output.width,output.height);
    const blob=await new Promise(resolve=>output.toBlob(resolve,'image/jpeg',.94));if(!blob)throw Error('Crop failed');
    await window.LPGPhotoEditor.save(photo.id,crop,blob);close();await attach();
   }catch{dialog.querySelector('.crop-status').textContent='Could not save the crop. Your original is safe. Please try again.';save.disabled=false;}
  };draw();
 }
 window.LPGPhotoUI={attach};
})();
