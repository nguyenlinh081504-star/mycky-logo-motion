/* Analytic/transfer tests, no packages or browser required. */
const assert=require('node:assert/strict');
const core=require('./lesson-core.js');
const m=require('./precision-motion.cjs');
let count=0;
function test(name,fn){fn(); count++; console.log('PASS '+name);}
const near=(a,b,e=1e-8)=>assert.ok(Math.abs(a-b)<e,`${a} != ${b}`);
test('clones begin at previous stopped parent; original stays frozen',()=>{
  const original={x:8,y:0,angle:0}, pivot=[0,0]; let parent=original;
  for(let j=1;j<=3;j++){
    assert.deepEqual(m.quarterClone(parent,pivot,0),parent);
    const mid=m.quarterClone(parent,pivot,.5); near(Math.hypot(mid.x,mid.y),8);
    parent=m.quarterClone(parent,pivot,1); near(parent.angle,90*j);
  }
  near(parent.x,0);near(parent.y,-8); assert.deepEqual(original,{x:8,y:0,angle:0});
});
test('subdivision preserves the complete source curve, not just endpoint count',()=>{
  const p=[[0,0],[20,80],[90,-30],[100,10]], pieces=m.subdivide(p,7);
  for(let k=0;k<7;k++)for(let i=0;i<=10;i++){
    const a=core.cubicAt(p,(k+i/10)/7),b=core.cubicAt(pieces[k],i/10);
    near(a[0],b[0]);near(a[1],b[1]);
  }
});
test('multi-cubic prefix uses global length instead of equal per-curve time',()=>{
  const line=(x0,x1)=>[[x0,0],[x0+(x1-x0)/3,0],[x0+2*(x1-x0)/3,0],[x1,0]];
  const curves=[line(0,10),line(10,40)], table=m.arcTable(curves,32);
  near(table.total,40);assert.deepEqual(m.prefix(curves,table,0),[]);
  const partial=m.prefix(curves,table,.5); assert.equal(partial.length,2);near(partial.at(-1)[3][0],20);
  assert.deepEqual(m.prefix(curves,table,1),curves);
});
test('projected front moves between samples and fully reaches artwork',()=>{
  const path=[[0,0],[10,0],[10,10]];
  near(m.projectArc([3.25,2],path).s,3.25);
  near(m.projectArc([12,4.5],path).s,14.5);
  assert.equal(m.coverage(20,20,1),1);assert.equal(m.coverage(0,20,0),0);
  near(m.coverage(10.5,20,.5),.5); assert.equal(m.coverage(10,20,.5),1);
});
test('selective shortening keeps 8s only with an explicit hold policy',()=>{
  const o={start:3.6,oldDuration:1.48,newDuration:1,totalDuration:8,policy:'extend-final-hold'};
  const t=m.phaseMap(o);near(t.duration,8);near(t.at(3.6),3.6);near(t.at(4.6),5.08);near(t.at(7.52),8);near(t.at(8),8);
  let previous=-1;for(let i=0;i<=800;i++){let v=t.at(i/100);assert.ok(v>=previous);previous=v;}
  const collapsed=m.phaseMap({...o,policy:'collapse'});near(collapsed.duration,7.52);near(collapsed.duration/2,3.76);
  assert.equal(Math.round(60*collapsed.duration/2),226);
  assert.throws(()=>m.phaseMap({...o,policy:undefined}));
});
test('reject degenerate and non-finite geometry/timing',()=>{
  assert.throws(()=>m.arcTable([[[0,0],[0,0],[0,0],[0,0]]]));
  assert.throws(()=>m.projectArc([0,0],[[0,0],[0,0]]));
  assert.throws(()=>m.quarterClone({x:0,y:0,angle:0},[0,0],NaN));
  assert.throws(()=>m.subdivide([[0,0],[1,1],[2,1],[3,0]],0));
});
console.log(`${count} precision-motion tests passed.`);
const lesson=require('./precision-lesson.cjs');
const middle=lesson.svg(2.25);lesson.svg(5.5);lesson.svg(0);
assert.equal(lesson.svg(2.25),middle,'Teaching lesson must seek deterministically.');
for(let i=0;i<=180;i++)assert.ok(!/NaN|Infinity/.test(lesson.svg(i/30)));
console.log('Teaching lesson finite coordinates and seek replay: PASS');
