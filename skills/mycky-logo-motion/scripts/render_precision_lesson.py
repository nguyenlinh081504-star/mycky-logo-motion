"""Render the generic precision lesson using existing Node/CairoSVG/FFmpeg.

python scripts/render_precision_lesson.py --out <scratch directory>
Outputs a six-second teaching MP4, a snapshot/contact sheet and resource hashes.
No server, browser, downloads or dependency installs. This is not client QA.
"""
import argparse, hashlib, io, json, shutil, subprocess
from pathlib import Path
import logo_lab as lab
import cairosvg
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out', required=True)
    args = parser.parse_args(); out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    node = shutil.which('node')
    if not node: raise SystemExit('Use the existing Node runtime; no automatic install.')
    module = str(Path(__file__).with_name('precision-lesson.cjs'))
    program = "const m=require(process.argv[1]);process.stdout.write(JSON.stringify(Array.from({length:180},(_,i)=>m.svg(i/30))))"
    svgs = json.loads(subprocess.check_output([node, '-e', program, module], encoding='utf8'))
    video = out/'precision-refinements.mp4'
    encoder = subprocess.Popen([lab.executable('ffmpeg'), '-y', '-v', 'error', '-f', 'rawvideo',
        '-pixel_format', 'rgb24', '-video_size', '960x540', '-framerate', '30', '-i', '-',
        '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', str(video)], stdin=subprocess.PIPE)
    thumbs = []
    try:
        for i, svg in enumerate(svgs):
            png = cairosvg.svg2png(bytestring=svg.encode('utf8'), output_width=960, output_height=540)
            im = Image.open(io.BytesIO(png)).convert('RGB'); encoder.stdin.write(im.tobytes())
            if i == 60: im.save(out/'precision-refinements.png')
            if i in (0, 15, 30, 60, 90, 135):
                small = im.resize((480, 270), Image.Resampling.LANCZOS); thumbs.append(small)
    finally:
        encoder.stdin.close()
    if encoder.wait(): raise RuntimeError('Teaching-video encode failed.')
    sheet = Image.new('RGB', (960, 810), 'white')
    for i, im in enumerate(thumbs): sheet.paste(im, ((i%2)*480, (i//2)*270))
    sheet.save(out/'precision-contact.png')
    # Decode all frames, independent of container declared frame count.
    cap = lab.open_video_capture(video); count = 0
    while True:
        ok, _ = cap.read()
        if not ok: break
        count += 1
    cap.release()
    info = lab.probe(video)
    if count != 180 or info['width'] != 960 or info['height'] != 540 or abs(info['duration']-6) > .001:
        raise RuntimeError(f'Teaching video failed decode/spec check: {count} {info}')
    manifest = {'version':'2.1', 'teaching_not_customer_artwork':True,
        'source':['scripts/precision-lesson.cjs', 'scripts/precision-motion.cjs', 'scripts/lesson-core.js'],
        'decoded_frames':count, 'video':{k:v for k,v in info.items() if k!='path'},
        'visual_review':'pending; inspect precision-contact.png before release',
        'browser_continuous_playback':'not certified by this renderer',
        'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('precision-*')) if p.suffix in ('.png','.mp4')}}
    (out/'precision-resource-index.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'video':str(video), 'decoded_frames':count, 'duration':info['duration']}))


if __name__=='__main__': main()
