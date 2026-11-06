/* Self-drawn teaching shapes only. Same SVG drives offline player and MP4. */
(function(root,factory){
 if(typeof module==='object'&&module.exports)module.exports=factory(require('./lesson-core.js'),require('./precision-motion.cjs'));
 else root.MyckyPrecisionLesson=factory(root.MyckyLessons,root.MyckyPrecision);
})(typeof globalThis==='object'?globalThis:this,function(core,m){
const ring=[[[0,92],[-55,92],[-100,52],[-100,0]],[[-100,0],[-100,-52],[-55,-92],[0,-92]],[[0,-92],[55,-92],[100,-52],[100,0]],[[100,0],[100,52],[55,92],[0,92]]];
const table=m.arcTable(ring);
const toPath=curves=>curves.length?'M'+curves[0][0].join(',')+curves.map(p=>' C'+p.slice(1).map(v=>v.join(',')).join(' ')).join(''):'';
function svg(t){
 const q=core.ease(Math.max(0,Math.min(1,t/4.5))),pivot=[160,275],poses=[{x:196,y:239,angle:0}];
 for(let i=1;i<=3;i++){
   // Completed parent pose is independent of the still-running child's pose.
   const prev=i===1?poses[0]:{x:poses[i-1].endX,y:poses[i-1].endY,angle:90*(i-1)};
   const end=m.quarterClone(prev,pivot,1),local=core.ease(Math.max(0,Math.min(1,t-(i-1))));
   const pose=m.quarterClone(prev,pivot,local);
   poses.push({...pose,endX:end.x,endY:end.y,visible:t>=i-1});
 }
 const cloneArt=poses.map((p,i)=>({...p,id:i})).filter(p=>p.visible!==false).reverse().map(p=>`<path d="M-17 -29H17V-15H-3V-4H12V10H-3V29H-17Z" transform="translate(${p.x} ${p.y}) rotate(${p.angle})" fill="${p.id?'#7257cf':'#141826'}"/>`).join('');
 const phase=6*q,rounded=Math.round(phase),grid=Array.from({length:10},(_,i)=>`<path d="M675 ${205+i*8}H925" stroke="#dfe3ec"/>`).join('');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
 <rect width="960" height="540" fill="#f5f6fa"/><g font-family="Arial,sans-serif" fill="#141826">
 <text x="28" y="38" font-size="23" font-weight="bold">MYCKY / PRECISION RECIPES</text>
 <text x="28" y="63" font-size="13">Self-drawn teaching geometry - not customer logo artwork or customer QA</text>
 ${[20,340,660].map(x=>`<rect x="${x}" y="86" width="280" height="412" rx="12" fill="white"/>`).join('')}
 <text x="36" y="119" font-size="17" font-weight="bold">A. CHAINED +90 DEG</text>
 <text x="356" y="119" font-size="17" font-weight="bold">B. GLOBAL ARC LENGTH</text>
 <text x="676" y="119" font-size="17" font-weight="bold">C. FLOAT TRANSLATION</text>
 <text x="36" y="144" font-size="12">One stopped parent per clone</text>
 <text x="356" y="144" font-size="12">One connected multi-cubic prefix</text>
 <text x="676" y="144" font-size="12">Pixel travel enlarged 8x</text>
 <circle cx="160" cy="275" r="51" fill="none" stroke="#dfe3ec" stroke-dasharray="3 5"/>
 ${cloneArt}<circle cx="160" cy="275" r="3" fill="#d35c34"/>
 <g transform="translate(480 275)"><path d="${toPath(ring)}" fill="none" stroke="#e8eaf0" stroke-width="9"/>
 <path d="${toPath(m.prefix(ring,table,q))}" fill="none" stroke="#141826" stroke-width="9" stroke-linecap="butt"/></g>
 ${grid}<text x="683" y="191" font-size="12">rounded</text><text x="813" y="191" font-size="12">float</text>
 <rect x="697" y="${210+rounded*8}" width="55" height="9" fill="#d35c34"/>
 <rect x="829" y="${210+phase*8}" width="55" height="9" fill="#7257cf"/>
 <text x="36" y="418" font-size="13">Original angle stays 0 deg.</text>
 <text x="36" y="440" font-size="13">No shape change during rotation.</text>
 <text x="356" y="418" font-size="13">Split last cubic at distance s.</text>
 <text x="356" y="440" font-size="13">No broad gray feather at tip.</text>
 <text x="676" y="418" font-size="13">Keep coordinates as floats.</text>
 <text x="676" y="440" font-size="13">Rasterize/downsample only once.</text>
 <text x="28" y="526" font-size="13">${t.toFixed(2)} / 6.00 s - Source: precision-lesson.cjs + precision-motion.cjs</text>
 </g></svg>`;
}
return {svg};
});
