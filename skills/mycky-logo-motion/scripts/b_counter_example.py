"""Measured/anatomical correspondence example for the two bundled B silhouettes.

This is an educational geometry check, not a final logo or production renderer.
Do not reuse these pixel anchors on other glyphs.
"""
import argparse
from pathlib import Path
from logo_lab import SKILL,cv2,np,Image,mask_metrics,ink_mask,correspond,write_json,sheet

# Pixel coordinates visually identified on THESE original glyphs. Nearest contour
# vertices retain the full raster endpoint, with distinct semantic corner labels.
LABELS=[['stem_top','stem_bottom','lower_baseline_bowl','lower_bowl_right','waist','upper_bowl_right','upper_cap_bowl'],
        ['inner_stem_top','upper_counter_cap_bowl','upper_counter_right','upper_counter_waist','inner_stem_lower'],
        ['lower_counter_stem_top','lower_counter_waist','lower_counter_right','lower_counter_floor_bowl','lower_counter_stem_bottom']]
SOURCE=[[(0,0),(0,501),(231,501),(382,365),(268,236),(356,125),(220,0)],
        [(88,69),(205,69),(269,140),(204,212),(89,213)],
        [(89,277),(210,277),(291,356),(210,433),(89,433)]]
TARGET=[[(0,0),(0,634),(250,634),(497,436),(264,237),(378,124),(200,0)],
        [(68,18),(177,18),(310,126),(250,235),(69,334)],
        [(68,394),(249,254),(421,422),(215,616),(69,616)]]

def build(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    masks=[];contours=[]
    for filename in ['B-source.png','B-target.png']:
        mask=ink_mask(np.array(Image.open(SKILL/'assets/examples'/filename).convert('RGBA')))
        cs,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        cs=sorted(cs,key=lambda c:abs(cv2.contourArea(c)),reverse=True)
        cs=[cs[0]]+sorted(cs[1:],key=lambda c:cv2.boundingRect(c)[1])
        assert len(cs)==3
        masks.append(mask);contours.append([c[:,0,:].astype(float) for c in cs])
    paired=[];report=[]
    for k,(s,d) in enumerate(zip(*contours)):
        si=[int(np.argmin(np.sum((s-np.array(point))**2,axis=1))) for point in SOURCE[k]]
        di=[int(np.argmin(np.sum((d-np.array(point))**2,axis=1))) for point in TARGET[k]]
        data={'source':s.tolist(),'target':d.tolist(),'source_anchors':si,'target_anchors':di,
              'labels':LABELS[k],'warning':'Indices apply only to the bundled images; annotate a new logo from its own anatomy.'}
        write_json(out/f'B-pair-{k}.json',data)
        a,b=correspond(s,d,si,di);paired.append((a,b))
        report.append({'contour':k,'labels':LABELS[k],'source_anchor_xy':[s[i].tolist() for i in si],
                       'target_anchor_xy':[d[i].tolist() for i in di],'paired_points':len(a)})
    def stage(points,shape):
        height,width=shape;scale=600/height
        return points*scale+[(640-width*scale)/2,80]
    paired=[(stage(a,masks[0].shape),stage(b,masks[1].shape)) for a,b in paired]
    tiles=[];labels=[];topology=[]
    for i,q in enumerate(np.linspace(0,1,101)):
        canvas=np.zeros((760,640),np.uint8)
        cv2.fillPoly(canvas,[np.rint(a*(1-q)+b*q).astype(np.int32) for a,b in paired],1)
        metrics=mask_metrics(canvas,min_area=24);topology.append([metrics['components'],metrics['holes']])
        if i%10==0:tiles.append(Image.fromarray(255-canvas*255));labels.append(f'q={q:.1f}')
    assert all(t==[1,2] for t in topology),'Topology failed: recheck corner anchors, not easing.'
    sheet(tiles,out/'B-anatomical-mapping.jpg',labels,columns=6,tile=(260,340))
    result={'purpose':'Illustrated semantic counter mapping; polygon example, not a native cubic final render',
            'source':'assets/examples/B-source.png','target':'assets/examples/B-target.png',
            'topology_samples':len(topology),'components':[1],'holes':[2],'contours':report}
    write_json(out/'B-anchor-report.json',result);return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True)
    print(build(parser.parse_args().out))
