import importlib.util,sys,unittest,tempfile,subprocess
from argparse import Namespace
from pathlib import Path

SCRIPT=Path(__file__).with_name('logo_lab.py')
spec=importlib.util.spec_from_file_location('logo_lab',SCRIPT)
lab=importlib.util.module_from_spec(spec);sys.modules[spec.name]=lab;spec.loader.exec_module(lab)
np=lab.np;cv2=lab.cv2

class GeometryTests(unittest.TestCase):
    def test_native_cubics_share_commands_and_preserve_corner(self):
        s=np.array([[0,0],[1,0],[2,0],[2,1],[2,2]],float)
        d=np.array([[0,0],[2,0],[4,0],[4,2],[4,4]],float)
        result=lab.fit_matched_cubics(s,d,[0,2,4],tolerance=.01)
        self.assertEqual(len(result['source']),len(result['target']))
        self.assertTrue(np.allclose(result['source'][0][-1],[2,0]))
        self.assertTrue(np.allclose(result['target'][0][-1],[4,0]))
        self.assertEqual(len(result['source']),2)

    def test_cubic_pair_handles_different_curvature_without_command_mismatch(self):
        x=np.linspace(0,1,81);s=np.column_stack([x,np.sin(x*np.pi)])
        d=np.column_stack([x*2,np.sin(x*np.pi)*.5])
        result=lab.fit_matched_cubics(s,d,[0,80],tolerance=.01)
        self.assertGreater(len(result['source']),0)
        self.assertEqual(len(result['source']),len(result['target']))
        self.assertTrue(np.allclose(result['source'][0][0],s[0]))
        self.assertTrue(np.allclose(result['source'][-1][-1],s[-1]))

    def test_transparent_black_canvas_does_not_become_black_block(self):
        rgba=np.zeros((120,100,4),np.uint8)
        rgba[10:110,20:80,3]=255;rgba[25:50,35:65,3]=0;rgba[70:95,35:65,3]=0
        mask=lab.ink_mask(rgba)
        result=lab.mask_metrics(mask)
        self.assertEqual(result['components'],1);self.assertEqual(result['holes'],2)
        self.assertEqual(result['bbox'],[20,10,60,100])

    def test_bounds_are_ink_bounds_not_image_canvas(self):
        a=np.zeros((200,300),np.uint8);a[40:100,170:200]=1
        result=lab.mask_metrics(a)
        self.assertEqual(result['bbox'],[170,40,30,60]);self.assertEqual(result['bbox_center'],[185.,70.])

    def test_landmarks_keep_stem_corners_paired(self):
        s=np.array([[0,0],[0,10],[4,10],[8,10],[10,8],[10,4],[7,2],[4,0]],float)
        d=np.array([[0,0],[0,10],[4,10],[8,10],[10,8],[10,4],[5,0],[3,-2]],float)
        a,b=lab.correspond(s,d,[0,1,2,6,7],[0,1,2,6,7],samples=8)
        for i,j in [(0,0),(1,1),(2,2),(6,6),(7,7)]:
            k=np.argmin(np.linalg.norm(a-s[i],axis=1));self.assertTrue(np.allclose(b[k],d[j]))
        self.assertTrue(all(np.min(np.linalg.norm(a-p,axis=1))<1e-8 for p in s))
        self.assertTrue(all(np.min(np.linalg.norm(b-p,axis=1))<1e-8 for p in d))

    def test_reject_unordered_anchors_and_opposite_winding(self):
        square=np.array([[0,0],[0,10],[10,10],[10,0]],float)
        with self.assertRaises(ValueError):lab.correspond(square,square,[0,2,1],[0,1,2])
        with self.assertRaises(ValueError):lab.correspond(square,square[::-1],[0,1,2],[0,1,2])

    def test_easing_monotone_at_endpoints(self):
        p=lab.motion_progress(np.linspace(0,1,1001),ramp=.18)
        self.assertEqual(float(p[0]),0.);self.assertEqual(float(p[-1]),1.)
        self.assertTrue(np.all(np.diff(p)>=0));self.assertLess(p[1],.00001)

class TimingTests(unittest.TestCase):
    def test_replace_existing_hold_2x(self):
        self.assertEqual(lab.retime_spec(8,2,1,complete_at=7,fps=60)['frames'],270)
    def test_append_hold_2x(self):
        self.assertEqual(lab.retime_spec(8,2,1,fps=60)['frames'],300)
    def test_plain_speed_2x(self):
        self.assertEqual(lab.retime_spec(8,2,0,fps=60)['frames'],240)
    def test_bad_timing_rejected(self):
        for kwargs in [dict(speed=0),dict(speed=2,complete_at=9),dict(speed=2,hold=-1)]:
            with self.assertRaises(ValueError):lab.retime_spec(8,**kwargs)

class SelectionTests(unittest.TestCase):
    def facts(self,**updates):
        return {'artwork':str(lab.SKILL/'assets/examples/B-target.png'),
                'counter_and_junction_invariants':['B remains connected with two counters'],**updates}
    def candidate(self,name,formulas,score=.9):
        return {'id':name,'formula_ids':formulas,'why_this_logo':'B bowls and two counters map to the same target anatomy',
          'checks':{k:True for k in ['artwork_identity','topology','ancestry','connectivity','phase_order','no_spurious_strokes']},
          'scores':{k:{'value':score,'basis':'test fixture visual/geometry evidence'} for k in ['endpoint_fidelity','anatomical_continuity','visual_cleanliness','pacing','reference_style']},
          'visual_review':{'status':'pass','evidence':['test fixture frames']}}
    def test_radial_formula_cannot_win_for_nonrepeating_B(self):
        a=self.candidate('direct',['F02'],.8);b=self.candidate('radial',['F25'],1.)
        result=lab.rank_candidates({'facts':self.facts(repeat_structure='absent'),'candidates':[a,b]})
        self.assertEqual(result['best_tested_candidate'],'direct')
        self.assertEqual(result['candidates'][1]['status'],'rejected')
    def test_unwatched_candidate_is_not_claimed_optimal(self):
        c=self.candidate('unseen',['F02']);c['visual_review']={'status':'pending','evidence':[]}
        result=lab.rank_candidates({'facts':{},'candidates':[c]})
        self.assertIsNone(result['best_tested_candidate'])
    def test_high_score_cannot_hide_topology_failure(self):
        c=self.candidate('bad',['F02'],1.);c['checks']['topology']=False
        result=lab.rank_candidates({'facts':{},'candidates':[c]})
        self.assertEqual(result['candidates'][0]['status'],'rejected')
    def test_missing_evidence_does_not_become_passing_score(self):
        c=self.candidate('guessed',['F02']);c['scores']['visual_cleanliness']['basis']=''
        result=lab.rank_candidates({'facts':{},'candidates':[c]})
        self.assertIsNone(result['best_tested_candidate'])
    def test_unknown_repetition_requires_fit_review(self):
        result=lab.rank_candidates({'facts':{},'candidates':[self.candidate('radial',['F25'])]})
        self.assertIsNone(result['best_tested_candidate'])
        self.assertEqual(result['candidates'][0]['status'],'pending')
    def test_near_tie_requires_review_not_arbitrary_winner(self):
        result=lab.rank_candidates({'facts':self.facts(),'candidates':[self.candidate('a',['F02'],.91),self.candidate('b',['F02'],.90)]})
        self.assertTrue(result['near_tie']);self.assertIsNone(result['best_tested_candidate'])
    def test_all_clone_recipes_require_repetition(self):
        for formula in ['F04','F06','F15','F37']:
            result=lab.rank_candidates({'facts':self.facts(repeat_structure='absent'),'candidates':[self.candidate('bad',[formula])]})
            self.assertEqual(result['candidates'][0]['status'],'rejected')
    def test_pending_text_is_not_evidence(self):
        c=self.candidate('pretend',['F02']);c['visual_review']['evidence']=['PENDING']
        result=lab.rank_candidates({'facts':self.facts(),'candidates':[c]})
        self.assertIsNone(result['best_tested_candidate'])
    def test_missing_logo_dna_prevents_selection(self):
        result=lab.rank_candidates({'facts':{},'candidates':[self.candidate('no-dna',['F02'])]})
        self.assertIsNone(result['best_tested_candidate'])
    def test_verified_repetition_needs_fit_evidence(self):
        facts=self.facts(repeat_structure='verified',repeat_fit_evidence='PENDING: overlay')
        result=lab.rank_candidates({'facts':facts,'candidates':[self.candidate('unproven',['F25'])]})
        self.assertIsNone(result['best_tested_candidate'])
    def test_completed_review_can_mention_resolved_pending_work(self):
        c=self.candidate('reviewed',['F02'])
        c['visual_review']['evidence']=['Khong con pending work; reviewed replacement contour frames']
        result=lab.rank_candidates({'facts':self.facts(),'candidates':[c]})
        self.assertEqual(result['best_tested_candidate'],'reviewed')

class ExportTests(unittest.TestCase):
    def test_hold_uses_completed_frame_not_frame_before_completion(self):
        with tempfile.TemporaryDirectory(prefix='mycky-hold-',dir=lab.CONFIG.get('scratch_root')) as directory:
            source=Path(directory)/'input.mp4';target=Path(directory)/'out.mp4'
            subprocess.run([lab.executable('ffmpeg'),'-y','-loglevel','error','-f','lavfi','-i','color=red:s=64x64:r=10:d=1','-f','lavfi','-i','color=blue:s=64x64:r=10:d=1','-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0','-c:v','libx264','-pix_fmt','yuv420p',str(source)],check=True)
            lab.retime(Namespace(input=str(source),output=str(target),speed=2.,hold=1.,complete_at=1.,fps=10,overwrite=False))
            cap=cv2.VideoCapture(str(target));frames=[]
            while True:
                ok,frame=cap.read()
                if not ok:break
                frames.append(frame)
            cap.release()
            self.assertEqual(len(frames),15)
            self.assertGreater(float(frames[0][:,:,2].mean()),180)
            self.assertGreater(float(frames[8][:,:,0].mean()),180)

if __name__=='__main__':unittest.main(verbosity=2)
