"""Local evidence tools for Mycky Logo Motion. No downloads or package installs."""
from __future__ import annotations
import argparse,hashlib,json,math,os,re,shutil,subprocess,sys,xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

SKILL=Path(__file__).resolve().parents[1]
CONFIG=json.loads((SKILL/'runtime.local.json').read_text(encoding='utf8')) if (SKILL/'runtime.local.json').exists() else {}
for directory in [*os.environ.get('MYCKY_PYTHON_DEPS','').split(os.pathsep),*CONFIG.get('python_deps',[])]:
    if directory and Path(directory).is_dir():sys.path.insert(0,directory)
try:
    import cv2,numpy as np
    from PIL import Image,ImageDraw
except ImportError as error:
    raise SystemExit(f'Thiếu dependency: {error}. Dùng runtime đã có qua run.ps1; không tự cài lại.')

def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')

def executable(name):
    candidates=[os.environ.get('MYCKY_'+name.upper()),CONFIG.get(name),shutil.which(name)]
    for value in candidates:
        if value and Path(value).is_file():return str(value)
    raise ValueError(f'Không tìm thấy {name}; đặt MYCKY_{name.upper()} hoặc runtime.local.json.')

def probe(path):
    path=Path(path).resolve()
    if not path.is_file():raise ValueError(f'Không có file: {path}')
    data=json.loads(subprocess.check_output([executable('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)],timeout=60))
    video=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    if not video:raise ValueError('File không có video stream.')
    return {'path':str(path),'width':video['width'],'height':video['height'],
      'fps':float(Fraction(video.get('avg_frame_rate','0/1'))),'fps_fraction':video.get('avg_frame_rate'),
      'duration':float(video.get('duration') or data['format']['duration']),
      'declared_frames':int(video['nb_frames']) if video.get('nb_frames','').isdigit() else None,
      'codec':video.get('codec_name'),'profile':video.get('profile'),'pixel_format':video.get('pix_fmt'),
      'audio':any(s['codec_type']=='audio' for s in data['streams'])}

def ink_mask(image,foreground='auto',threshold=24):
    """RGBA array from PIL. Alpha wins for a genuinely transparent artwork."""
    a=np.asarray(image)
    if a.ndim==2:a=np.repeat(a[:,:,None],3,axis=2)
    if a.shape[2]==4:
        alpha=a[:,:,3]
        if foreground=='alpha' or (foreground=='auto' and np.mean(alpha<250)>.01):
            return np.uint8(alpha>threshold)
        rgb=a[:,:,:3].astype(float)*alpha[:,:,None]/255+255*(1-alpha[:,:,None]/255)
    else:rgb=a[:,:,:3].astype(float)
    gray=rgb.mean(axis=2)
    if foreground=='auto':
        border=np.r_[gray[0],gray[-1],gray[:,0],gray[:,-1]]
        foreground='light' if np.median(border)<128 else 'dark'
    return np.uint8(gray>threshold if foreground=='light' else gray<255-threshold)

def mask_metrics(mask,min_area=8):
    binary=np.uint8(mask>0);n,_,stats,centers=cv2.connectedComponentsWithStats(binary,8)
    parts=[{'bbox':list(map(int,s[:4])),'area':int(s[4]),'center':list(map(float,c))}
           for s,c in zip(stats[1:],centers[1:]) if s[4]>=min_area]
    contours,hierarchy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    holes=[]
    if hierarchy is not None:
        for i,c in enumerate(contours):
            depth=0;parent=int(hierarchy[0,i,3])
            while parent>=0:depth+=1;parent=int(hierarchy[0,parent,3])
            if depth%2==1 and cv2.contourArea(c)>=min_area:
                holes.append({'area':float(cv2.contourArea(c)),'bbox':list(map(int,cv2.boundingRect(c)))})
    points=cv2.findNonZero(binary)
    bbox=list(map(int,cv2.boundingRect(points))) if points is not None else None
    center=[bbox[0]+bbox[2]/2,bbox[1]+bbox[3]/2] if bbox else None
    return {'bbox':bbox,'bbox_center':center,'ink_area':int(binary.sum()),'components':len(parts),
            'holes':len(holes),'component_details':parts,'hole_details':holes,
            'threshold_min_area_px':min_area,'note':'Threshold-dependent geometry; not a semantic letter recognition result.'}

def signed_area(points):
    p=np.asarray(points,float);q=np.roll(p,-1,axis=0)
    return float(np.sum(p[:,0]*q[:,1]-q[:,0]*p[:,1])/2)

def correspond(source,target,source_anchors,target_anchors,samples=80):
    """Semantic anchors, per-section arc length; preserve every endpoint vertex."""
    source=np.asarray(source,float);target=np.asarray(target,float)
    if any(p.ndim!=2 or p.shape[1]!=2 or len(p)<3 or not np.isfinite(p).all() for p in (source,target)):
        raise ValueError('Contours must be finite Nx2 loops with at least 3 points.')
    if signed_area(source)*signed_area(target)<=0:raise ValueError('Match winding first; do not reverse only a counter.')
    def roll(points,anchors):
        a=list(anchors)
        if len(a)<2 or len(set(a))!=len(a) or any(not isinstance(i,(int,np.integer)) or i<0 or i>=len(points) for i in a):
            raise ValueError('Need distinct valid integer semantic anchor indices.')
        start=a[0];a=[(i-start)%len(points) for i in a]
        if np.any(np.diff(a)<=0):raise ValueError('Anchors must follow contour order.')
        return np.roll(points,-start,axis=0),a+[len(points)]
    s,si=roll(source,source_anchors);d,di=roll(target,target_anchors)
    if len(si)!=len(di):raise ValueError('Different semantic anchor counts.')
    aa=[];bb=[]
    for sa,sb,da,db in zip(si[:-1],si[1:],di[:-1],di[1:]):
        a=s[sa:sb+1] if sb<len(s) else np.vstack([s[sa:],s[:1]])
        b=d[da:db+1] if db<len(d) else np.vstack([d[da:],d[:1]])
        def arc(p):
            u=np.r_[0.,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
            if u[-1]<=0:raise ValueError('Degenerate segment between semantic anchors.')
            return u/u[-1]
        au=arc(a);bu=arc(b);u=np.unique(np.r_[au,bu,np.linspace(0,1,samples,endpoint=False)]);u=u[u<1]
        aa.append(np.column_stack([np.interp(u,au,a[:,i]) for i in (0,1)]))
        bb.append(np.column_stack([np.interp(u,bu,b[:,i]) for i in (0,1)]))
    return np.vstack(aa),np.vstack(bb)

def fit_matched_cubics(source,target,breaks,tolerance=.5):
    """Fit equal cubic command structures, splitting both paths at the worst error.

    breaks are shared indices at semantic corners (including 0 and last index).
    G1 is maintained at adaptive smooth splits; deliberate landmark corners remain
    corners. Error is sampled correspondence error, not a Hausdorff guarantee.
    """
    a=np.asarray(source,float);b=np.asarray(target,float);breaks=list(breaks)
    if a.shape!=b.shape or a.ndim!=2 or a.shape[1]!=2 or len(a)<2 or tolerance<=0:
        raise ValueError('Need equal finite Nx2 paths and positive fitting tolerance.')
    if not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Nonfinite path.')
    if not breaks or breaks[0]!=0 or breaks[-1]!=len(a)-1 or np.any(np.diff(breaks)<=0):
        raise ValueError('breaks must run strictly from 0 to last shared point index.')
    def unit(v,fallback):
        length=float(np.linalg.norm(v))
        return v/length if length>1e-10 else np.asarray(fallback,float)
    def fit(points,t0,t1):
        arc=np.r_[0.,np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
        if arc[-1]<1e-10:raise ValueError('Degenerate cubic section.')
        u=arc/arc[-1];v=1-u
        weights=np.column_stack([v**3,3*v*v*u,3*v*u*u,u**3])
        p0=points[0];p3=points[-1]
        baseline=(weights[:,0]+weights[:,1])[:,None]*p0+(weights[:,2]+weights[:,3])[:,None]*p3
        A=np.stack([weights[:,1,None]*t0,weights[:,2,None]*t1],axis=2).reshape(-1,2)
        rhs=(points-baseline).reshape(-1)
        alpha=np.linalg.lstsq(A,rhs,rcond=None)[0]
        chord=float(np.linalg.norm(p3-p0));fallback=(chord if chord>1e-8 else arc[-1])/3
        if np.any(alpha<1e-7) or np.any(alpha>arc[-1]*2):alpha=np.array([fallback,fallback])
        curve=np.array([p0,p0+alpha[0]*t0,p3+alpha[1]*t1,p3])
        error=np.linalg.norm(weights@curve-points,axis=1)
        return curve,error
    result_a=[];result_b=[]
    def recurse(sa,sb,ta0,ta1,tb0,tb1,depth=0):
        ca,ea=fit(sa,ta0,ta1);cb,eb=fit(sb,tb0,tb1)
        if max(float(ea.max()),float(eb.max()))<=tolerance or len(sa)==2:
            result_a.append(ca.tolist());result_b.append(cb.tolist());return
        if depth>30:raise ValueError('Cubic fitting did not converge; inspect landmarks.')
        k=int(np.argmax(np.maximum(ea,eb)));k=max(1,min(k,len(sa)-2))
        ma=unit(sa[k-1]-sa[k+1],unit(sa[k-1]-sa[k],[1,0]))
        mb=unit(sb[k-1]-sb[k+1],unit(sb[k-1]-sb[k],[1,0]))
        recurse(sa[:k+1],sb[:k+1],ta0,ma,tb0,mb,depth+1)
        recurse(sa[k:],sb[k:],-ma,ta1,-mb,tb1,depth+1)
    for lo,hi in zip(breaks[:-1],breaks[1:]):
        sa=a[lo:hi+1];sb=b[lo:hi+1]
        recurse(sa,sb,unit(sa[1]-sa[0],[1,0]),unit(sa[-2]-sa[-1],[-1,0]),
                unit(sb[1]-sb[0],[1,0]),unit(sb[-2]-sb[-1],[-1,0]))
    return {'source':result_a,'target':result_b,'cubic_count':len(result_a),
      'tolerance_px':tolerance,'error_measure':'sampled chord-parameter correspondence; inspect rendered contours',
      'warning':'Same commands does not prove intermediate topology, absence of self-intersections, or artistic quality.'}

def motion_progress(u,ramp=.18):
    """Integral of quintic speed ramps: eased ends, steady middle, no bounce."""
    if not 0<ramp<.5:raise ValueError('ramp must be between 0 and 0.5')
    u=np.clip(np.asarray(u,float),0,1)
    def integral(z):return z**6-3*z**5+2.5*z**4
    result=np.where(u<ramp,ramp*integral(u/ramp),
      np.where(u>1-ramp,(1-ramp)-ramp*integral((1-u)/ramp),u-ramp/2))
    return result/(1-ramp)

def retime_spec(duration,speed=2,hold=0,complete_at=None,fps=60):
    if duration<=0 or speed<=0 or hold<0 or fps<=0:raise ValueError('Invalid duration, speed, hold, or FPS.')
    active=duration if complete_at is None else complete_at
    if not 0<active<=duration:raise ValueError('complete-at must be within the input video.')
    active_frames=max(1,round(active/speed*fps));hold_frames=round(hold*fps)
    return {'speed':speed,'fps':fps,'active_source_seconds':active,'active_frames':active_frames,
      'hold_frames':hold_frames,'frames':active_frames+hold_frames,'duration':(active_frames+hold_frames)/fps,
      'hold_mode':'append to existing sped-up video' if complete_at is None else 'replace old hold after explicit complete-at'}

def sheet(images,path,labels,columns=6,tile=(220,414)):
    w,h=tile;out=Image.new('RGB',(columns*w,math.ceil(len(images)/columns)*h),'#eee');draw=ImageDraw.Draw(out)
    for i,(image,label) in enumerate(zip(images,labels)):
        image=image.copy().convert('RGB');image.thumbnail((w-8,h-28),Image.Resampling.LANCZOS)
        x=i%columns*w;y=i//columns*h;out.paste(image,(x+(w-image.width)//2,y+24));draw.text((x+4,y+5),label,fill='black')
    out.save(path,quality=94)

def inspect_logo(args):
    path=Path(args.input).resolve();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if path.suffix.lower()=='.svg':
        root=ET.parse(path).getroot();result={'source':str(path),'kind':'svg','viewBox':root.get('viewBox'),
          'elements':[{'tag':e.tag.split('}')[-1],**{k:e.get(k) for k in ['id','fill','fill-rule','transform'] if e.get(k) is not None}}
            for e in root.iter() if e.tag.split('}')[-1] in ['path','polygon','rect','circle','ellipse','g','text','image']],
          'warning':'Metadata only: render this SVG with the existing browser/engine before measuring contours. SVG text requires original fonts; embedded images are raster.'}
    else:
        image=Image.open(path).convert('RGBA');mask=ink_mask(np.array(image),args.foreground)
        result={'source':str(path),'kind':'raster','canvas':list(image.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**mask_metrics(mask)}
        preview=Image.fromarray(255-mask*255).convert('RGB');draw=ImageDraw.Draw(preview)
        if result['bbox']:
            x,y,w,h=result['bbox'];draw.rectangle((x,y,x+w-1,y+h-1),outline='#dd3322',width=2)
        preview.save(out/'ink-bounds.png');Image.fromarray(mask*255).save(out/'ink-mask.png')
    write_json(out/'logo-analysis.json',result);return result

def analyze_reference(args):
    meta=probe(args.input);fps=meta['fps'];start,end=(0.,meta['duration']) if not args.window else map(float,args.window.split(','))
    if not 0<=start<end<=meta['duration']+.02:raise ValueError('Invalid --window.')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True);cap=cv2.VideoCapture(str(args.input))
    metrics=[];previous=None;i=0;frames=[];labels=[];last_sample=-1e9
    interval=1/args.sample_fps;crop=tuple(map(int,args.crop.split(','))) if args.crop else None
    while True:
        ok,frame=cap.read()
        if not ok:break
        t=i/fps;i+=1
        if t<start:continue
        if t>end:break
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if crop:
            x,y,w,h=crop;gray=gray[y:y+h,x:x+w]
            if gray.size==0:raise ValueError('Empty crop.')
        small=cv2.resize(gray,(180,max(1,round(gray.shape[0]*180/gray.shape[1]))),interpolation=cv2.INTER_AREA)
        change=0. if previous is None else float(np.mean(cv2.absdiff(small,previous)))
        metrics.append({'frame':i-1,'seconds':round(t,6),'mean_abs_change':change});previous=small
        if t-last_sample>=interval-.5/fps:
            image=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));name=f'frame-{i-1:06d}.jpg'
            image.save(out/name,quality=93);frames.append(image.resize((270,480)));labels.append(f'f{i-1} {t:.3f}s');last_sample=t
            if len(frames)>600:raise ValueError('More than 600 evidence frames; use a narrower --window or smaller --sample-fps.')
    cap.release()
    for k in range(0,len(frames),48):sheet(frames[k:k+48],out/f'contact-{k//48:02d}.jpg',labels[k:k+48])
    # Candidate boundaries only; a morph peak is not necessarily a shot cut.
    peaks=[]
    for item in sorted(metrics,key=lambda m:m['mean_abs_change'],reverse=True):
        if all(abs(item['seconds']-p['seconds'])>.2 for p in peaks):peaks.append(item)
        if len(peaks)==12:break
    result={'video':meta,'window':[start,end],'sample_fps':args.sample_fps,'evidence_frames':len(frames),
      'motion_peaks_to_review':sorted(peaks,key=lambda m:m['seconds']),
      'metrics':metrics,'warning':'Measurements propose review times. Codex must look at frames and playback; no automatic aesthetic PASS.'}
    write_json(out/'reference-analysis.json',result)
    return {k:v for k,v in result.items() if k!='metrics'}

def verify_video(args):
    meta=probe(args.input);cap=cv2.VideoCapture(str(args.input));decoded=0;selected=[];labels=[];last=None;diffs=[]
    step=max(1,round(meta['fps']*.25))
    while True:
        ok,frame=cap.read()
        if not ok:break
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if last is not None:diffs.append({'frame':decoded,'mean_abs_change':float(cv2.absdiff(gray,last).mean())})
        if decoded%step==0:selected.append(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)));labels.append(f'{decoded/meta["fps"]:.3f}s')
        last=gray;decoded+=1
    cap.release();expected=round(args.duration*args.fps)
    checks={'codec':meta['codec']=='h264','pixel_format':meta['pixel_format']=='yuv420p',
      'dimensions':[meta['width'],meta['height']]==[args.width,args.height],
      'fps':abs(meta['fps']-args.fps)<1e-6,'frame_count':decoded==expected,
      'duration':abs(meta['duration']-args.duration)<=.5/args.fps}
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if selected:sheet(selected,out/'decoded-review.jpg',labels)
    result={'technical_pass':all(checks.values()),'checks':checks,'video':meta,'decoded_frames':decoded,
      'largest_frame_changes':sorted(diffs,key=lambda x:x['mean_abs_change'],reverse=True)[:15],
      'aesthetic_review':'PENDING: open decoded frames and play actual video; technical_pass is not visual acceptance.'}
    write_json(out/'video-qa.json',result)
    if not result['technical_pass']:raise ValueError(json.dumps(result,ensure_ascii=False))
    return result

def retime(args):
    source=Path(args.input).resolve();target=Path(args.output).resolve()
    if source==target:raise ValueError('Never overwrite the source.')
    if target.exists() and not args.overwrite:raise ValueError('Output exists; choose another path or explicitly --overwrite.')
    meta=probe(source);spec=retime_spec(meta['duration'],args.speed,args.hold,args.complete_at,args.fps)
    target.parent.mkdir(parents=True,exist_ok=True)
    filters=f'trim=end={spec["active_source_seconds"]},setpts=(PTS-STARTPTS)/{args.speed},fps={args.fps},trim=end_frame={spec["active_frames"]},setpts=PTS-STARTPTS'
    command=[executable('ffmpeg'),'-y' if args.overwrite else '-n','-hide_banner','-loglevel','error','-i',str(source)]
    if spec['hold_frames'] and args.complete_at is not None:
        # Hold the first COMPLETED frame, not the last moving frame just before
        # complete-at. Trimming then tpad alone freezes an unfinished logo.
        completed=min(round(args.complete_at*meta['fps']),max(0,(meta['declared_frames'] or round(meta['duration']*meta['fps']))-1))
        tail=f'trim=start_frame={completed}:end_frame={completed+1},setpts=PTS-STARTPTS,loop=loop=-1:size=1:start=0,trim=end_frame={spec["hold_frames"]},setpts=N/({args.fps}*TB)'
        graph=f'[0:v]split=2[m][h];[m]{filters}[moving];[h]{tail}[held];[moving][held]concat=n=2:v=1:a=0[v]'
        command+=['-filter_complex',graph,'-map','[v]']
    else:
        if spec['hold_frames']:filters+=f',tpad=stop_mode=clone:stop={spec["hold_frames"]}'
        command+=['-vf',filters]
    command+=['-frames:v',str(spec['frames'])]
    if meta['audio']:
        if spec['hold_frames'] or args.complete_at is not None:raise ValueError('Audio + changed hold needs an explicit audio-tail plan; do not silently cut or stretch music.')
        rate=args.speed;parts=[]
        while rate>2:parts.append('atempo=2');rate/=2
        while rate<.5:parts.append('atempo=0.5');rate/=.5
        parts.append(f'atempo={rate}');command+=['-af',','.join(parts),'-c:a','aac','-b:a','192k']
    else:command+=['-an']
    command+=['-c:v','libx264','-preset','medium','-crf','16','-profile:v','high','-level:v','4.2','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
    subprocess.run(command,check=True);result={'output':str(target),'timing':spec,'probe':probe(target)}
    write_json(target.with_suffix('.timing.json'),result);return result

def rank_candidates(data):
    """Audit Codex's evidenced assessments; this is not logo recognition or an AI judge."""
    weights={'endpoint_fidelity':.30,'anatomical_continuity':.25,
             'visual_cleanliness':.20,'pacing':.15,'reference_style':.10}
    gates=('artwork_identity','topology','ancestry','connectivity','phase_order','no_spurious_strokes')
    catalog=json.loads((SKILL/'references/formulas.json').read_text(encoding='utf8'))
    known={f['id'] for f in catalog['formulas']};facts=data.get('facts',{})
    clone_required={f['id'] for f in catalog['formulas'] if f.get('requires_repeated_module')}
    def established_text(value):
        if not isinstance(value,str) or not value.strip():return False
        lowered=value.strip().casefold()
        return re.match(r'^(?:pending|todo|tbd|replace|unknown|chưa\s+kiểm(?:\s+tra)?|chưa\s+rõ)\b',lowered) is None
    common_pending=[]
    artwork=facts.get('artwork')
    if not isinstance(artwork,str) or not Path(artwork).is_absolute() or not Path(artwork).is_file():
        common_pending.append('Provide the actual absolute artwork file path before selecting a recipe.')
    invariants=facts.get('counter_and_junction_invariants',[])
    if not isinstance(invariants,list) or not invariants or not all(established_text(i) for i in invariants):
        common_pending.append('Record this artwork\'s counter and junction invariants, including intentional topology changes.')
    rows=[];seen=set()
    candidates=data.get('candidates',[])
    if not isinstance(candidates,list) or not candidates:raise ValueError('Provide at least one assessed candidate.')
    for candidate in candidates:
        name=candidate.get('id')
        if not isinstance(name,str) or not name.strip() or name in seen:raise ValueError('Candidate IDs must be nonempty and unique.')
        seen.add(name);rejected=[];pending=list(common_pending);ids=candidate.get('formula_ids',[])
        if not established_text(candidate.get('why_this_logo')):pending.append('Explain the anatomical source-to-target fit for this candidate.')
        if not isinstance(ids,list) or not ids or any(i not in known for i in ids):
            rejected.append('Missing or unknown formula IDs.');ids=[]
        if facts.get('repeat_structure')=='absent' and clone_required.intersection(ids):
            rejected.append('Artwork has no repeated module; clone/rotational assembly cannot preserve the target.')
        elif clone_required.intersection(ids) and facts.get('repeat_structure')!='verified':
            pending.append('Verify repeated-module fit against the actual artwork before choosing clone assembly.')
        elif clone_required.intersection(ids) and not established_text(facts.get('repeat_fit_evidence')):
            pending.append('Repeated-module verification needs actual overlay/contour-fit evidence, not a placeholder.')
        if set(facts.get('forbidden_formula_ids',[])).intersection(ids):rejected.append('Violates a locked forbidden formula.')
        required=set(facts.get('required_formula_ids',[]))
        if required-set(ids):rejected.append('Omits a locked required formula.')
        checks=candidate.get('checks',{})
        for key in gates:
            if checks.get(key) is False:rejected.append(f'Failed mandatory check: {key}.')
            elif checks.get(key) is not True:pending.append(f'Mandatory check not established: {key}.')
        review=candidate.get('visual_review',{})
        if review.get('status')=='fail':rejected.append('Actual motion failed visual review.')
        evidence=review.get('evidence',[])
        if review.get('status')!='pass' or not isinstance(evidence,list) or not evidence or not all(established_text(e) for e in evidence):
            pending.append('Needs actual frame/playback review with evidence locations.')
        total=0.;complete=True
        for key,weight in weights.items():
            assessment=candidate.get('scores',{}).get(key,{})
            value=assessment.get('value');basis=assessment.get('basis')
            if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or not 0<=value<=1 or not established_text(basis):
                complete=False;pending.append(f'Missing evidenced score: {key}.')
            else:total+=value*weight
        status='rejected' if rejected else ('pending' if pending else 'eligible')
        rows.append({'id':name,'formula_ids':ids,'status':status,
                     'weighted_score':round(total,6) if complete else None,
                     'rejection_reasons':rejected,'pending_reasons':pending})
    ranking=sorted([r for r in rows if r['status']=='eligible'],key=lambda r:r['weighted_score'],reverse=True)
    tied=len(ranking)>1 and ranking[0]['weighted_score']-ranking[1]['weighted_score']<.03
    return {'best_tested_candidate':ranking[0]['id'] if ranking and not tied else None,
            'near_tie':tied,'ranking':[r['id'] for r in ranking],'candidates':rows,'weights':weights,
            'next_action':'Review the top two difficult motion windows or resolve the art-direction tradeoff.' if tied else ('Use the best tested candidate; continue its project QA.' if ranking else 'Resolve pending checks or build a geometry-feasible candidate.'),
            'claim_boundary':'Best among submitted, visually tested candidates only. Scores are Codex assessments with evidence, not a computed universal optimum or autonomous logo understanding.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    a=sub.add_parser('logo');a.add_argument('input');a.add_argument('--out',required=True);a.add_argument('--foreground',choices=['auto','dark','light','alpha'],default='auto')
    a=sub.add_parser('reference');a.add_argument('input');a.add_argument('--out',required=True);a.add_argument('--window');a.add_argument('--crop');a.add_argument('--sample-fps',type=float,default=2)
    a=sub.add_parser('qa');a.add_argument('input');a.add_argument('--out',required=True);a.add_argument('--duration',type=float,required=True);a.add_argument('--fps',type=float,default=60);a.add_argument('--width',type=int,default=1080);a.add_argument('--height',type=int,default=1920)
    a=sub.add_parser('retime');a.add_argument('input');a.add_argument('output');a.add_argument('--speed',type=float,default=2);a.add_argument('--hold',type=float,default=0);a.add_argument('--complete-at',type=float);a.add_argument('--fps',type=int,default=60);a.add_argument('--overwrite',action='store_true')
    a=sub.add_parser('pair');a.add_argument('input',help='JSON: source,target,source_anchors,target_anchors');a.add_argument('--out',required=True);a.add_argument('--cubic-tolerance',type=float)
    a=sub.add_parser('select');a.add_argument('input',help='JSON with logo facts and evidenced candidate assessments');a.add_argument('--out',required=True)
    args=p.parse_args()
    if args.command=='doctor':result={'python':sys.executable,'opencv':cv2.__version__,'ffmpeg':executable('ffmpeg'),'ffprobe':executable('ffprobe'),'automatic_installs':False}
    elif args.command=='logo':result=inspect_logo(args)
    elif args.command=='reference':
        if not 0<args.sample_fps<=60:raise ValueError('sample-fps must be in (0,60].')
        result=analyze_reference(args)
    elif args.command=='qa':result=verify_video(args)
    elif args.command=='retime':result=retime(args)
    elif args.command=='select':
        result=rank_candidates(json.loads(Path(args.input).read_text(encoding='utf8')));write_json(args.out,result)
    elif args.command=='pair':
        data=json.loads(Path(args.input).read_text(encoding='utf8'));a,b=correspond(data['source'],data['target'],data['source_anchors'],data['target_anchors'])
        result={'source':a.tolist(),'target':b.tolist(),'points':len(a),'warning':'Inspect interpolated silhouettes for self-intersections/topology and render with subpixel coverage.'}
        if args.cubic_tolerance is not None:
            marks=[]
            for si,di in zip(data['source_anchors'],data['target_anchors']):
                distance=np.sum((a-np.array(data['source'][si]))**2,axis=1)+np.sum((b-np.array(data['target'][di]))**2,axis=1)
                marks.append(int(np.argmin(distance)))
            marks=sorted(set(marks))
            if marks[0]!=0:raise ValueError('First paired landmark must be index 0.')
            result['cubics']=fit_matched_cubics(np.vstack([a,a[:1]]),np.vstack([b,b[:1]]),marks+[len(a)],args.cubic_tolerance)
        write_json(args.out,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.SubprocessError,ET.ParseError) as error:
        print(f'ERROR: {error}',file=sys.stderr);sys.exit(2)
