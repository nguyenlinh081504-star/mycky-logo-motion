#!/usr/bin/env python3
"""Build PTS-based, non-destructive evidence for a supplied reference video.
No AI recognition. Requires ffmpeg/ffprobe; Pillow for contact sheet only.
"""
import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def command(executable, args):
    return subprocess.run([executable, *args], check=True, capture_output=True, text=True).stdout


def probe_frames(path, ffprobe):
    payload = json.loads(command(ffprobe, ["-v", "error", "-select_streams", "v:0", "-show_frames", "-show_entries", "frame=best_effort_timestamp_time,pkt_duration_time", "-of", "json", str(path)]))
    frames = []
    for index, item in enumerate(payload.get("frames", [])):
        ts = item.get("best_effort_timestamp_time")
        if ts is None:
            continue
        frames.append({"ordinal": index, "pts_s": float(ts), "duration_s": float(item.get("pkt_duration_time") or 0)})
    if not frames:
        raise ValueError("Cannot find valid presentation timestamps; do not invent frame timestamps")
    return frames


def choose(frames, step, window, cap):
    begin, end = window if window is not None else (frames[0]["pts_s"], frames[-1]["pts_s"])
    if begin > end:
        raise ValueError("Invalid time window")
    shots = []
    t = begin
    while t <= end + 1e-8:
        closest = min(frames, key=lambda x: (abs(x["pts_s"] - t), x["ordinal"]))
        if not shots or shots[-1]["ordinal"] != closest["ordinal"]:
            shots.append(closest)
        t += step
    end_frame = min(frames, key=lambda x: abs(x["pts_s"] - end))
    if not shots or shots[-1]["ordinal"] != end_frame["ordinal"]:
        shots.append(end_frame)
    if len(shots) > cap:
        raise ValueError(f"Requested {len(shots)} stills exceeds --max-shots {cap}; increase step or narrow window")
    return shots


def grab(video, shots, out, ffmpeg):
    out.mkdir(parents=True, exist_ok=True)
    indices = [x["ordinal"] for x in shots]
    # Single decode process; select decoded ordinal rather than -ss rounded time.
    filt = "select=" + "+".join(f"eq(n\\,{k})" for k in indices)
    cmd = ["-v", "error", "-i", str(video), "-vf", filt, "-fps_mode", "passthrough", "-y", str(out / "shot_%03d.png")]
    subprocess.run([ffmpeg, *cmd], check=True, capture_output=True, text=True)
    exported = sorted(out.glob("shot_*.png"))
    if len(exported) != len(shots):
        raise RuntimeError(f"Extracted {len(exported)}/{len(shots)} frames; validate decoder handling of VFR")
    return exported


def sheet(images, shots, out):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return "Pillow missing: PNG frames exported but no contact sheet"
    first = Image.open(images[0]).convert("RGB")
    tile_w = 240
    tile_h = round(first.height / first.width * tile_w)
    columns = 5
    cell_w, cell_h = tile_w + 12, tile_h + 38
    rows = (len(images) + columns - 1) // columns
    board = Image.new("RGB", (columns * cell_w, rows * cell_h), "#eeeeee")
    draw = ImageDraw.Draw(board)
    for i, (path, item) in enumerate(zip(images, shots)):
        im = Image.open(path).convert("RGB")
        im.thumbnail((tile_w, tile_h))
        x = (i % columns) * cell_w + 6
        y = (i // columns) * cell_h + 30
        board.paste(im, (x, y))
        draw.text((x, y - 21), f"F{item['ordinal']} | {item['pts_s']:.4f}s", fill="#151515")
    board.save(out / "contact_pts.jpg", quality=94)
    return "contact_pts.jpg"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--step", type=float, default=.2)
    ap.add_argument("--window", nargs=2, type=float)
    ap.add_argument("--max-shots", type=int, default=80)
    ap.add_argument("--no-images", action="store_true")
    args = ap.parse_args()
    if args.step <= 0 or args.max_shots < 1:
        ap.error("--step and --max-shots must be positive")
    video = args.video.resolve()
    if not video.is_file():
        ap.error("Source video not found")
    ffprobe = os.getenv("MYCKY_FFPROBE") or shutil.which("ffprobe")
    ffmpeg = os.getenv("MYCKY_FFMPEG") or shutil.which("ffmpeg")
    if not ffprobe or (not ffmpeg and not args.no_images):
        ap.error("Install or configure existing ffmpeg/ffprobe; script does not install dependencies")
    frames = probe_frames(video, ffprobe)
    shots = choose(frames, args.step, args.window, args.max_shots)
    args.out.mkdir(parents=True, exist_ok=True)
    intervals = [round(frames[i]["pts_s"] - frames[i-1]["pts_s"], 5) for i in range(1, len(frames))]
    result = {
        "source_file": str(video), "decoded_frames_with_pts": len(frames),
        "first_pts_s": frames[0]["pts_s"], "last_pts_s": frames[-1]["pts_s"],
        "pts_delta_min_s": min(intervals) if intervals else None,
        "pts_delta_max_s": max(intervals) if intervals else None,
        "all_frame_pts": frames, "selected_stills": shots,
        "interpretation": "Frame PTS evidence only; phase labels, glyph anatomy and temporal intent require visual inspection",
    }
    if not args.no_images:
        images = grab(video, shots, args.out / "stills", ffmpeg)
        result["contact_sheet"] = sheet(images, shots, args.out)
    (args.out / "pts_evidence.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf8")
    print(f"PTS={len(frames)} | selected={len(shots)} | output={args.out}")


if __name__ == "__main__":
    main()
