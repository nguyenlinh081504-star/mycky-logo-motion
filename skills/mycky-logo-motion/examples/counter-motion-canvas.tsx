/** Motion Canvas 3.17.2 — copy into an EXISTING project scene.
 * Educational glyph only: replace geometry with measured customer artwork.
 */
import {makeScene2D, Node, Path} from '@motion-canvas/2d';
import {createSignal, easeInOutCubic, waitFor} from '@motion-canvas/core';
import geometry from './counter-paths.json';

type Command = (string | number)[];
function tweenCommands(a: Command[], b: Command[], q: number): Command[] {
  if (a.length !== b.length) throw new Error('Unmatched anatomy/commands');
  return a.map((c, i) => {
    if (c[0] !== b[i][0] || c.length !== b[i].length) throw new Error('Command mismatch');
    return c.map((v, k) => k === 0 ? v : Number(v) * (1-q) + Number(b[i][k]) * q);
  });
}
function reverseClosed(p: Command[]): Command[] {
  let start=p[0].slice(1); const segments: {start: (string|number)[]; c: Command}[]=[];
  for (const c of p.slice(1)) if (c[0] === 'C') {
    segments.push({start, c}); start=c.slice(5,7);
  }
  return [['M',...p[0].slice(1)],...segments.reverse().map(s=>['C',...s.c.slice(3,5),...s.c.slice(1,3),...s.start]),['Z']];
}
const serialize=(p: Command[])=>p.map(c=>c.join(' ')).join(' ');

export default makeScene2D(function* (view) {
  view.fill('#f7f5ef');
  const progress=createSignal(0);
  view.add(<Node scale={2.2} position={[-380,-420]}>
    <Path fill={'#111111'} data={()=>{
      const q=progress();
      const outer=tweenCommands(geometry.outer.source,geometry.outer.target,q);
      const upper=tweenCommands(geometry.upper.source,geometry.upper.target,q);
      const lower=tweenCommands(geometry.lower.source,geometry.lower.target,q);
      // Path2D uses nonzero winding: reverse holes, never paint white shapes.
      return serialize([...outer,...reverseClosed(upper),...reverseClosed(lower)]);
    }}/>
  </Node>);
  yield* waitFor(.8);
  yield* progress(1,3,easeInOutCubic);
  yield* waitFor(2.2); // Six-second teaching scene; final user timing is independent.
});
