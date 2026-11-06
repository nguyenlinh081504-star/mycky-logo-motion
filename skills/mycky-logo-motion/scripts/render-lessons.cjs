/* Reproduce teaching videos with an existing Playwright/Chromium + FFmpeg.
 * No installs. Example:
 * node scripts/render-lessons.cjs --playwright-module <existing module> --ffmpeg <existing executable> --out <folder>
 */
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url'),{spawn}=require('node:child_process');
const args=process.argv.slice(2),get=(key,fallback)=>{const i=args.indexOf(key);return i<0?fallback:args[i+1];};
const configFile=path.resolve(__dirname,'../runtime.local.json');const cfg=fs.existsSync(configFile)?JSON.parse(fs.readFileSync(configFile,'utf8')):{};
const modulePath=get('--playwright-module',process.env.MYCKY_PLAYWRIGHT_MODULE||cfg.playwright_module||'playwright');
const ffmpeg=get('--ffmpeg',process.env.MYCKY_FFMPEG||cfg.ffmpeg||'ffmpeg');
const out=path.resolve(get('--out',path.join(__dirname,'../assets/lessons')));fs.mkdirSync(out,{recursive:true});
const lessons=get('--lessons','counter,interweave,clone,draw,radial,retract,placement,hbridge,sassembly').split(',');
const fps=+get('--fps','30'),duration=6;
if(fps!==30&&fps!==60)throw Error('Use 30 or 60 FPS.');
const {chromium}=require(modulePath);
async function write(stream,bytes){if(!stream.write(bytes))await new Promise((resolve,reject)=>{
 const done=()=>{stream.off('error',failed);resolve();},failed=e=>{stream.off('drain',done);reject(e);};
 stream.once('drain',done);stream.once('error',failed);
});}
(async()=>{
 const browserPath=get('--browser-executable',process.env.MYCKY_CHROMIUM||cfg.chromium);
 const browser=await chromium.launch({headless:true,...(browserPath?{executablePath:browserPath}:{channel:'chrome'})});
 try{
  const page=await browser.newPage({viewport:{width:960,height:540},deviceScaleFactor:1});
  for(const lesson of lessons){
   await page.goto(pathToFileURL(path.resolve(__dirname,'../references/visual-lessons.html')).href+'?render&lesson='+lesson);
   await page.waitForFunction(()=>typeof window.renderAt==='function');await page.evaluate(()=>document.fonts.ready);
   let stderr='';const file=path.join(out,lesson+'.mp4');
   if(!args.includes('--stills-only')){
   const proc=spawn(ffmpeg,['-y','-hide_banner','-loglevel','error','-threads','1','-f','image2pipe','-framerate',String(fps),'-vcodec','png','-i','pipe:0','-an','-filter_threads','1','-c:v','libx264','-threads','1','-preset','fast','-tune','zerolatency','-crf','21','-profile:v','high','-pix_fmt','yuv420p','-movflags','+faststart',file],{windowsHide:true});
   proc.stderr.on('data',d=>stderr+=d);const finished=new Promise((resolve,reject)=>{proc.once('error',reject);proc.once('close',code=>code===0?resolve():reject(Error(stderr)));});finished.catch(()=>{});
   for(let frame=0;frame<fps*duration;frame++){
    await page.evaluate(({t,lesson})=>window.renderAt(t,{lesson,debug:true}),{t:frame/fps,lesson});
    const png=await page.screenshot({type:'png',animations:'disabled'});await write(proc.stdin,png);
   }
   proc.stdin.end();await finished;
   }
   for(const [label,t] of [['start',0],['middle',2.5],['end',duration-1/fps]]){
    await page.evaluate(({t,lesson})=>window.renderAt(t,{lesson,debug:true}),{t,lesson});
    await page.screenshot({path:path.join(out,lesson+'-'+label+'.png'),type:'png',animations:'disabled'});
   }
   console.log(JSON.stringify({lesson,file,video_written:!args.includes('--stills-only'),frames:fps*duration,fps,duration}));
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
