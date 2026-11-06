/* Native cubic teaching geometry. These are teaching glyphs, not client artwork.
 * The same functions drive SVG preview, frames, tests and the Motion Canvas demo.
 */
(function(root,factory){const api=factory();if(typeof module==='object')module.exports=api;else root.MyckyLessons=api;})(typeof globalThis==='object'?globalThis:this,function(){
  const clamp=x=>Math.min(1,Math.max(0,x));
  const ease=x=>{x=clamp(x);return x*x*x*(10+x*(-15+6*x));};
  const phase=(t,a,b)=>ease((t-a)/(b-a));
  const lerp=(a,b,q)=>a+(b-a)*q;
  function interpolate(a,b,q){
    if(a.length!==b.length)throw Error('Match semantic sections before interpolation.');
    return a.map((s,i)=>{if(s[0]!==b[i][0]||s.length!==b[i].length)throw Error('Cubic command mismatch.');return s.map((v,j)=>j?lerp(v,b[i][j],clamp(q)):v);});
  }
  const pathData=p=>p.map(x=>x.join(' ')).join(' ');
  function reverseClosed(p){
    let start=p[0].slice(1),segments=[];
    for(const command of p.slice(1))if(command[0]==='C'){
      segments.push({start,c1:command.slice(1,3),c2:command.slice(3,5),end:command.slice(5,7)});start=command.slice(5,7);
    }
    return [['M',...p[0].slice(1)],...segments.reverse().map(s=>['C',...s.c2,...s.c1,...s.start]),['Z']];
  }
  const P=(start,...curves)=>[['M',...start],...curves.map(c=>['C',...c]),['Z']];
  const polygon=points=>P(points[0],...points.map((p,i)=>{const n=points[(i+1)%points.length];return [...p,...n,...n];}));
  const geometry={b:{
    outer:{source:P([50,30],[50,30,180,30,180,30],[250,30,270,60,270,110],[270,145,245,170,215,180],[265,185,290,210,290,260],[290,320,250,350,180,350],[180,350,50,350,50,350],[50,350,50,30,50,30]),
           target:P([50,30],[50,30,168,30,168,30],[235,30,255,60,255,107],[255,142,226,159,190,178],[245,176,296,211,296,265],[296,321,248,350,180,350],[180,350,50,350,50,350],[50,350,50,30,50,30])},
    upper:{source:P([100,78],[100,78,175,78,175,78],[210,78,220,90,220,112],[220,140,205,150,175,150],[175,150,100,150,100,150],[100,150,100,78,100,78]),
           target:P([66,44],[66,44,163,44,163,44],[212,44,235,65,235,107],[235,142,204,157,182,164],[145,176,95,188,66,195],[66,195,66,44,66,44])},
    lower:{source:P([100,209],[100,209,178,209,178,209],[220,209,239,232,239,267],[239,292,210,302,178,302],[178,302,100,302,100,302],[100,302,100,209,100,209]),
           target:P([66,238],[99,213,144,193,178,193],[235,193,277,224,277,267],[277,311,230,336,179,336],[179,336,66,336,66,336],[66,336,66,238,66,238])}
  }};
  const kj={
    stem:{source:polygon([[80,50],[116,50],[116,330],[80,330]]),target:polygon([[89,50],[107,50],[107,330],[89,330]])},
    arm:{source:P([105,178],[105,178,233,50,233,50],[233,50,270,50,270,50],[270,50,124,200,124,200],[124,200,105,178,105,178]),
         target:P([103,178],[139,144,185,80,229,50],[229,50,248,50,248,50],[222,84,167,153,109,198],[109,198,103,178,103,178])},
    leg:{source:P([108,176],[108,176,282,330,282,330],[282,330,239,330,239,330],[239,330,101,200,101,200],[101,200,108,176,108,176]),
         target:P([108,176],[173,191,238,313,320,330],[320,330,278,330,278,330],[216,319,172,222,101,200],[101,200,108,176,108,176])},
    hook:{source:P([270,50],[270,50,306,50,306,50],[306,50,306,256,306,256],[306,337,227,358,195,306],[195,306,221,284,221,284],[243,320,270,302,270,256],[270,256,270,50,270,50]),
          target:P([274,50],[274,50,294,50,294,50],[294,50,294,264,294,264],[294,343,256,371,210,370],[210,370,210,359,210,359],[262,355,274,317,274,264],[274,264,274,50,274,50])}
  };
  geometry.kj=kj;
  function bPaths(q){return Object.fromEntries(Object.entries(geometry.b).map(([id,p])=>[id,interpolate(p.source,p.target,q)]));}
  function kjState(q){
    q=clamp(q);const roles=Object.entries(kj).map(([id,p])=>({id,path:interpolate(p.source,p.target,q)}));
    const stem=roles.find(r=>r.id==='stem').path;
    const edges=[2,4].map(index=>{const a=stem[index-1].slice(-2),cmd=stem[index],curve=[a,cmd.slice(1,3),cmd.slice(3,5),cmd.slice(5,7)];return Array.from({length:21},(_,i)=>cubicAt(curve,i/20));});
    return {roles,overpassOwner:'K-leg',underpassOwner:'J-hook',protectedStemEdges:edges};
  }
  function lineResidual(points){
    const a=points[0],b=points[points.length-1],dx=b[0]-a[0],dy=b[1]-a[1],n=Math.hypot(dx,dy);
    if(!n)throw Error('Degenerate protected edge.');
    return Math.max(...points.map(p=>Math.abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/n));
  }
  function cloneState(t){return {cloneVisible:t>=1,originalAngle:0,cloneAngle:180*phase(t,1.5,3.5),accentVisible:t>=4};}
  // Explicit S upper lobe / waist / lower terminal correspondence. Stroke example,
  // not a font substitution; use filled outlines for contrast in customer artwork.
  const sSource=[['M',65,-110],['C',10,-160,-100,-120,-62,-50],['C',-25,5,100,15,61,92],['C',24,153,-65,125,-75,80]];
  const modulePath=[['M',120,-130],['C',55,-155,-10,-110,25,-75],['C',50,-35,132,-60,110,-15],['C',88,0,24,-5,0,0]];
  const sModulePath=q=>interpolate(sSource,modulePath,q);
  function cubicAt(p,t){const u=1-t;return [0,1].map(k=>u*u*u*p[0][k]+3*u*u*t*p[1][k]+3*u*t*t*p[2][k]+t*t*t*p[3][k]);}
  const mix=(a,b,t)=>a.map((v,i)=>lerp(v,b[i],t));
  function splitCubic(p,t){const a=mix(p[0],p[1],t),b=mix(p[1],p[2],t),c=mix(p[2],p[3],t),d=mix(a,b,t),e=mix(b,c,t),f=mix(d,e,t);return [[p[0],a,d,f],[f,e,c,p[3]]];}
  function prefixCubic(p,q){
    q=clamp(q);if(q===0)return [];
    const lut=[0];let last=p[0];for(let i=1;i<=200;i++){const next=cubicAt(p,i/200);lut.push(lut.at(-1)+Math.hypot(next[0]-last[0],next[1]-last[1]));last=next;}
    const target=q*lut.at(-1);let i=1;while(i<200&&lut[i]<target)i++;
    const t=(i-1+(target-lut[i-1])/(lut[i]-lut[i-1]))/200;
    const c=splitCubic(p,t)[0];return [['M',...c[0]],['C',...c[1],...c[2],...c[3]]];
  }
  function radialDuration(k=4,hold=.4){if(!Number.isInteger(k)||k<2||hold<0)throw Error('Invalid radial count/hold.');return .9+(k-2)*1.3+1.1+hold;}
  function radialState(t,k=4){radialDuration(k);return Array.from({length:k},(_,i)=>{const start=.9+(i-1)*1.3;return {id:i,visible:i===0||t>=start,angle:i===0?0:(360*i/k)*phase(t,start+.15,start+1.1)};});}
  function hState(q){
    q=clamp(q);
    const left=[[400,70],[400,140],[400,225],[400,280]].map((p,i)=>mix(p,[[400,70],[400,220],[455,285],[535,280]][i],q));
    const right=[[560,70],[560,140],[560,225],[560,280]].map((p,i)=>mix(p,[[405,55],[520,45],[560,175],[560,280]][i],q));
    const leftJunction=cubicAt(left,.43),rightJunction=cubicAt(right,.43);
    const bridge=[leftJunction,mix(leftJunction,rightJunction,1/3),mix(leftJunction,rightJunction,2/3),rightJunction];
    return {left,right,bridge,leftJunction,rightJunction,width:lerp(27,15,q)};
  }
  function contractStem(anchorTop,anchorBottom,wTop,wBottom){
    if(wTop<=0||wBottom<=0)throw Error('Primary stem cannot collapse.');
    return polygon([[anchorTop[0]-wTop/2,anchorTop[1]],[anchorTop[0]+wTop/2,anchorTop[1]],[anchorBottom[0]+wBottom/2,anchorBottom[1]],[anchorBottom[0]-wBottom/2,anchorBottom[1]]]);
  }
  return {clamp,ease,phase,lerp,interpolate,pathData,reverseClosed,geometry,bPaths,kjState,lineResidual,cloneState,modulePath,sModulePath,hState,cubicAt,splitCubic,prefixCubic,radialState,radialDuration,contractStem};
});
