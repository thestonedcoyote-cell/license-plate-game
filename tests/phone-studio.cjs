const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),assert=require('assert');
const runtime=process.env.LPG_RUNTIME,out=process.env.LPG_TEST_OUTPUT;
if(!runtime||!out)throw Error('Set LPG_RUNTIME and LPG_TEST_OUTPUT; optionally CHROME_BIN');
fs.mkdirSync(out,{recursive:true});
const sizes=[[320,568],[360,640],[360,740],[412,844],[360,800],[393,851],[375,667],[390,844],[430,932],[344,882],[768,1024],[820,1180],[1440,1000],[844,412]];
(async()=>{
const server=require('http').createServer((req,res)=>{try{const p=path.join(runtime,req.url==='/'?'index.html':req.url.split('?')[0]);res.setHeader('Content-Type',p.endsWith('.js')?'application/javascript':p.endsWith('.css')?'text/css':p.endsWith('.html')?'text/html':p.endsWith('.svg')?'image/svg+xml':'text/plain');res.end(fs.readFileSync(p))}catch{res.statusCode=404;res.end()}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;const results=[];
try{
browser=await chromium.launch({executablePath:process.env.CHROME_BIN,headless:true,args:['--no-sandbox','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream']});
for(const [width,height] of sizes)for(const theme of ['light','dark']){
const ctx=await browser.newContext({viewport:{width,height},hasTouch:true,permissions:['camera'],serviceWorkers:'block'});
await ctx.route(/^https:\/\//,r=>r.abort());await ctx.addInitScript(()=>localStorage.setItem('lpg.welcome.v1','done'));
const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>document.documentElement.dataset.lpgFeatures==='0.4.0');
await page.locator('.nav-btn[data-screen="settings"]').click();await page.locator('#themeSelect').selectOption(theme);await page.locator('.nav-btn[data-screen="home"]').click();await page.waitForTimeout(200);
const home=await page.locator('#home').evaluate(el=>({scroll:el.scrollHeight,height:el.clientHeight,width:document.documentElement.scrollWidth,viewport:innerWidth}));
assert(home.scroll<=home.height+1,JSON.stringify({width,height,theme,home}));assert(home.width<=home.viewport+1);
await page.screenshot({path:path.join(out,`${width}x${height}-${theme}.png`)});
for(const screen of ['identify','collection','settings']){await page.locator(`.nav-btn[data-screen="${screen}"]`).click();assert(await page.locator('#'+screen).evaluate(e=>e.classList.contains('active')));assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
await page.locator('.nav-btn[data-screen="home"]').click();await page.locator('#homeMileMarkers').click();await page.waitForFunction(()=>document.querySelectorAll('#badges .badge').length>0);
if(width===412&&theme==='light'){
await page.locator('.nav-btn[data-screen="home"]').click();await page.locator('#openNotebook').click();await page.locator('#newTrip').click();await page.locator('[name="title"]').fill('Studio adventure');await page.locator('[name="story"]').fill('A saved road trip story.');await page.locator('#tripForm [type="submit"]').click();await page.getByText('Studio adventure',{exact:true}).waitFor();await page.locator('.close-dialog').click();await page.reload();await page.waitForFunction(()=>document.documentElement.dataset.lpgFeatures==='0.4.0');await page.locator('#openNotebook').click();await page.getByText('Studio adventure',{exact:true}).waitFor();await page.locator('.close-dialog').click();
}
assert.deepEqual(errors,[]);results.push({width,height,theme,home,errors,ok:true});console.log('PASS',width,height,theme);await ctx.close();
}
}finally{fs.writeFileSync(path.join(out,'matrix.json'),JSON.stringify(results,null,2));if(browser)await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
