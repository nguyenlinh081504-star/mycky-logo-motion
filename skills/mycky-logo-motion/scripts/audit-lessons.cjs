/* Browser-native geometry audit, not an aesthetic certification.
 * Reuse an installed Playwright module and Chrome; no downloads.
 */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');const args=process.argv.slice(2),get=k=>args[args.indexOf(k)+1];
if(!args.includes('--playwright-module'))throw Error('Specify an existing --playwright-module.');
const {chromium}=require(get('--playwright-module'));
(async()=>{
 const browser=await chromium.launch({headless:true,...(args.includes('--browser-executable')?{executablePath:get('--browser-executable')}:{channel:'chrome'})});
 try{
  const page=await browser.newPage({viewport:{width:960,height:540}});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../references/visual-lessons.html')).href+'?render');
  const result=await page.evaluate(()=>{
   const c=MyckyLessons,canvas=document.createElement('canvas');canvas.width=360;canvas.height=400;const ctx=canvas.getContext('2d',{willReadFrequently:true});
   function components(mask,w,h){let count=0;const seen=new Uint8Array(mask.length),stack=new Int32Array(mask.length);
    for(let seed=0;seed<mask.length;seed++)if(mask[seed]&&!seen[seed]){
     count++;let n=0;stack[n++]=seed;seen[seed]=1;
     while(n){const p=stack[--n],x=p%w,y=Math.floor(p/w);for(const i of [x? p-1:-1,x<w-1?p+1:-1,y?p-w:-1,y<h-1?p+w:-1])if(i>=0&&mask[i]&&!seen[i]){seen[i]=1;stack[n++]=i;}}
    }return count;
   }
   const topology=[];
   for(let i=0;i<=100;i++){
    const p=c.bPaths(i/100),path=new Path2D(c.pathData([...p.outer,...p.upper,...p.lower]));
    ctx.clearRect(0,0,360,400);ctx.fill(path,'evenodd');const rgba=ctx.getImageData(0,0,360,400).data;
    const ink=new Uint8Array(360*400),white=new Uint8Array(360*400);
    for(let j=0;j<ink.length;j++){ink[j]=rgba[j*4+3]>127?1:0;white[j]=1-ink[j];}
    topology.push([components(ink,360,400),components(white,360,400)-1]);
    // The Motion Canvas adapter's nonzero winding must create identical pixels.
    ctx.clearRect(0,0,360,400);ctx.fill(new Path2D(c.pathData([...p.outer,...c.reverseClosed(p.upper),...c.reverseClosed(p.lower)])),'nonzero');
    const other=ctx.getImageData(0,0,360,400).data;
    for(let j=3;j<rgba.length;j+=4)if(rgba[j]!==other[j])throw Error('Fill-rule mismatch at q='+i/100);
   }
   const hStates=[];
   for(let i=0;i<=100;i++){
    const state=c.hState(i/100);ctx.clearRect(0,0,360,400);ctx.save();ctx.translate(-300,0);ctx.lineWidth=state.width;
    for(const p of [state.left,state.right,state.bridge]){ctx.beginPath();ctx.moveTo(...p[0]);ctx.bezierCurveTo(...p[1],...p[2],...p[3]);ctx.stroke();}
    ctx.restore();const data=ctx.getImageData(0,0,360,400).data,ink=new Uint8Array(360*400);
    for(let j=0;j<ink.length;j++)ink[j]=data[j*4+3]>127?1:0;
    hStates.push(components(ink,360,400));
   }
   if(hStates.some(n=>n!==1))throw Error('Rendered H/bridge disconnected.');
   const deterministic=[];
   for(const lesson of ['counter','interweave','clone','draw','radial','retract','placement','hbridge','sassembly']){
    renderAt(2.5,{lesson,debug:true});const a=document.getElementById('art').innerHTML;
    renderAt(5,{lesson,debug:false});renderAt(2.5,{lesson,debug:true});const b=document.getElementById('art').innerHTML;
    if(a!==b)throw Error('Nondeterministic seek: '+lesson);
    const ids=[...document.querySelectorAll('#art [id]')].map(n=>n.id);if(new Set(ids).size!==ids.length)throw Error('Duplicate SVG mask IDs.');
    if(/NaN|Infinity/.test(b))throw Error('Nonfinite geometry: '+lesson);deterministic.push(lesson);
   }
   if(renderAt(2,{lesson:'placement'}).q!==0)throw Error('Placement q metadata must stay zero during rigid placement.');
   if(renderAt(1.5,{lesson:'sassembly'}).q!==1)throw Error('S geometry must be complete before clone phase.');
   return {b_native_topology_samples:topology.length,b_topology_states:[...new Set(topology.map(x=>x.join(',')))],h_native_connected_samples:hStates.length,nonzero_evenodd_match:true,seek_deterministic:deterministic};
  });
  assert.deepEqual(result.b_topology_states,['1,2']);console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
