/* Supplemental geometry recipes; no installs. Same coordinate convention as SVG:
 * x right, y down; a positive angle is clockwise. Progress is already eased.
 * These helpers do not infer anatomy, fix topology, or certify visual quality. */
(function(root,factory){
  if(typeof module==='object'&&module.exports)module.exports=factory(require('./lesson-core.js'));
  else root.MyckyPrecision=factory(root.MyckyLessons);
})(typeof globalThis==='object'?globalThis:this,function(core){
'use strict';
const {cubicAt,splitCubic}=core;
const clamp=x=>Math.max(0,Math.min(1,x));
function finite(...xs){if(!xs.every(Number.isFinite))throw Error('Expected finite numbers.');}
function curve(p){if(!Array.isArray(p)||p.length!==4||p.some(v=>!Array.isArray(v)||v.length!==2||!v.every(Number.isFinite)))throw Error('Expected four finite 2D cubic controls.');}
function quarterClone(parent,pivot,q){
  finite(parent.x,parent.y,parent.angle,...pivot,q);
  const a=clamp(q)*Math.PI/2,dx=parent.x-pivot[0],dy=parent.y-pivot[1];
  if(q<=0)return {...parent};
  const c=q>=1?0:Math.cos(a),s=q>=1?1:Math.sin(a);
  return {x:pivot[0]+c*dx-s*dy,y:pivot[1]+s*dx+c*dy,angle:parent.angle+90*clamp(q)};
}
function subdivide(p,n){
  curve(p);if(!Number.isInteger(n)||n<1)throw Error('Positive integer subdivision count required.');
  let rest=p;const out=[];
  for(let i=0;i<n-1;i++){const pair=splitCubic(rest,1/(n-i));out.push(pair[0]);rest=pair[1];}
  out.push(rest);return out;
}
function arcTable(curves,samples=256){
  if(!curves.length||!Number.isInteger(samples)||samples<2)throw Error('Curves and at least two samples required.');
  let total=0;const rows=[];
  for(let k=0;k<curves.length;k++){
    const p=curves[k];curve(p);
    if(k && Math.hypot(p[0][0]-curves[k-1][3][0],p[0][1]-curves[k-1][3][1])>1e-7)throw Error('Draw-on path must be connected.');
    let prev=p[0]; const length=[0]; const start=total;
    for(let i=1;i<=samples;i++){const v=cubicAt(p,i/samples);total+=Math.hypot(v[0]-prev[0],v[1]-prev[1]);length.push(total-start);prev=v;}
    if(total===start)throw Error('Remove zero-length cubic before arc lookup.');
    rows.push({start,end:total,length});
  }
  return {total,rows,samples};
}
function prefix(curves,table,q){
  finite(q);if(q<=0)return [];if(q>=1)return curves.map(p=>p.map(v=>v.slice()));
  if(table.rows.length!==curves.length)throw Error('Arc table does not match curve count.');
  const target=q*table.total,out=[];
  for(let k=0;k<curves.length;k++){
    const row=table.rows[k];if(target>=row.end){out.push(curves[k]);continue;}
    const d=target-row.start;if(d<=0)break;
    let i=1;while(i<table.samples && row.length[i]<d)i++;
    const span=row.length[i]-row.length[i-1];
    const t=(i-1+(span?(d-row.length[i-1])/span:0))/table.samples;
    out.push(splitCubic(curves[k],t)[0]);break;
  }
  return out;
}
function projectArc(point,polyline){
  finite(...point);if(polyline.length<2)throw Error('Polyline needs two points.');
  let best=Infinity,s=0,total=0,found=false;
  for(let i=0;i<polyline.length-1;i++){
    const a=polyline[i],b=polyline[i+1];finite(...a,...b);
    const dx=b[0]-a[0],dy=b[1]-a[1],l2=dx*dx+dy*dy;
    if(!l2)continue;found=true;const len=Math.sqrt(l2);
    const u=clamp(((point[0]-a[0])*dx+(point[1]-a[1])*dy)/l2);
    const d2=(point[0]-a[0]-u*dx)**2+(point[1]-a[1]-u*dy)**2;
    if(d2<best){best=d2;s=total+u*len;}total+=len;
  }
  if(!found)throw Error('Polyline has no length.');
  return {s,total,distance:Math.sqrt(best)};
}
function coverage(s,total,q,width=1){
  finite(s,total,q,width);if(total<=0||width<=0)throw Error('Positive length and front width required.');
  if(q<=0)return 0;if(q>=1)return 1;
  return clamp(((total+width)*q-s+width*.5)/width);
}
function phaseMap({start,oldDuration,newDuration,totalDuration,policy}){
  finite(start,oldDuration,newDuration,totalDuration);
  if(start<0||oldDuration<=0||newDuration<=0||start+oldDuration>totalDuration||!['collapse','extend-final-hold'].includes(policy))throw Error('Invalid phase or missing explicit duration policy.');
  const delta=oldDuration-newDuration;
  if(policy==='extend-final-hold' && delta<0)throw Error('Lengthening needs an explicit new timeline; this policy only shortens.');
  const duration=policy==='collapse'?totalDuration-delta:totalDuration;
  return {duration,at(t){finite(t);t=Math.max(0,Math.min(duration,t));
    return Math.min(totalDuration,t<=start?t:t<start+newDuration?start+(t-start)*oldDuration/newDuration:t+delta);
  }};
}
return {quarterClone,subdivide,arcTable,prefix,projectArc,coverage,phaseMap};
});
