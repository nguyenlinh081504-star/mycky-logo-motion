const assert = require('node:assert/strict');
const core = require('./lesson-core.js');

for (const [id, pair] of Object.entries(core.geometry.b)) {
  assert.equal(core.pathData(core.interpolate(pair.source,pair.target,0)),core.pathData(pair.source));
  assert.equal(core.pathData(core.interpolate(pair.source,pair.target,1)),core.pathData(pair.target));
  assert.equal(pair.source.length,pair.target.length,id);
}
assert.throws(()=>core.interpolate([['M',0,0]],[['C',0,0,1,1,2,2]],.5));
for (let i=0;i<=100;i++) {
  const state=core.kjState(i/100);
  assert.equal(state.roles.length,4);
  assert.equal(state.overpassOwner,'K-leg');assert.equal(state.underpassOwner,'J-hook');
  for(const x of state.protectedStemEdges)assert.ok(core.lineResidual(x)<1e-8);
}
assert.ok(core.lineResidual([[0,0],[8,25],[-7,50],[0,75]])>4);
// Mutating the ACTUAL rendered edge must fail, not an independently ideal proxy.
const edge=core.geometry.kj.stem.source[2];const before=edge[1];edge[1]+=20;
assert.ok(core.kjState(0).protectedStemEdges.some(p=>core.lineResidual(p)>1));edge[1]=before;
assert.ok(core.radialDuration(6)>6);
assert.ok(core.radialState(core.radialDuration(6),6).every((s,i)=>s.visible&&Math.abs(s.angle-i*60)<1e-9));
for(let t=0;t<6;t+=.05){
 const active=core.radialState(t).filter(s=>s.id>0&&s.angle>1e-6&&s.angle<90*s.id-1e-6);
 assert.ok(active.length<=1,'Clone rotations must be sequential.');
}
for(let i=0;i<=100;i++){
 const h=core.hState(i/100);assert.deepEqual(h.bridge[0],h.leftJunction);assert.deepEqual(h.bridge[3],h.rightJunction);
}
assert.equal(core.pathData(core.sModulePath(1)),core.pathData(core.modulePath));
const upperTurn=p=>{
 const a=p[0].slice(1),b=p[1].slice(1,3),c=p[1].slice(3,5);
 return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]);
};
assert.ok(upperTurn(core.sModulePath(0))*upperTurn(core.sModulePath(1))>0,'Do not silently reverse the upper-lobe sweep during S morph.');
assert.equal(core.cloneState(.8).cloneVisible,false);
assert.equal(core.cloneState(1.2).cloneAngle,0);
assert.equal(core.cloneState(3.8).cloneAngle,180);
assert.equal(core.cloneState(3.8).originalAngle,0);
assert.equal(core.cloneState(3.8).accentVisible,false);
assert.equal(core.cloneState(4.4).accentVisible,true);
let last=-1;
for(let i=0;i<=100;i++){
 const s=core.cloneState(i*.06);assert.ok(s.cloneAngle>=last);last=s.cloneAngle;
}
const curve=[[0,0],[80,-100],[200,-100],[280,0]];
assert.equal(core.prefixCubic(curve,0).length,0);
const whole=core.prefixCubic(curve,1);assert.deepEqual(whole[0],['M',0,0]);
assert.deepEqual(whole[1].slice(-2),[280,0]);
assert.deepEqual(core.splitCubic(curve,.5)[0][3],core.cubicAt(curve,.5));
console.log('Visual lesson invariants: PASS');
