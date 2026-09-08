const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),zlib=require('node:zlib'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const code=zlib.gunzipSync(Buffer.from([0,1,2].map(i=>fs.readFileSync(path.join(root,`app.bundle.part${i}.b64`),'utf8')).join(''),'base64')).toString();
const source=code.slice(code.indexOf('let cameraGeneration=0;'),code.indexOf('async function persistCapture('));
function fixture(){
 let resolve,stopped=0,gps=0,played=0;
 const stream={getTracks:()=>[{stop:()=>stopped++}]};
 const elements=new Proxy({}, {get:(t,k)=>t[k]||(t[k]={hidden:true,classList:{remove(){}},play:async()=>played++})});
 const c={console,$:id=>elements[id],navigator:{mediaDevices:{getUserMedia:()=>new Promise(r=>resolve=r)}},cameraStream:null,cameraFacing:'environment',cameraLocation:null,cameraLocationPromise:null,getLocationFast:async()=>{gps++;return null}};
 vm.createContext(c);vm.runInContext(source+'\nglobalThis.start=startCamera;globalThis.stop=stopCamera;',c);
 return {c,elements,grant:()=>resolve(stream),stats:()=>({stopped,gps,played})};
}
(async()=>{
 let f=fixture(),pending=f.c.start();assert.equal(f.stats().gps,0,'GPS must wait while camera permission is pending');f.grant();await pending;assert.equal(f.stats().played,1);assert.equal(f.stats().gps,1);assert.equal(f.elements.cameraVideo.hidden,false);
 f=fixture();pending=f.c.start();f.c.stop();f.grant();await pending;assert.equal(f.stats().stopped,1);assert.equal(f.stats().played,0);assert.equal(f.stats().gps,0);assert.equal(f.elements.cameraVideo.hidden,true);
 console.log('PASS: permission ordering, explicit playback, and stale stream cleanup');
})();
