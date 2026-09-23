#!/usr/bin/env python3
"""Download YouTube transcripts as clean text, one file per video.

Usage: python fetch_transcripts.py OUT_DIR URL [URL ...]
Writes OUT_DIR/<video_id>.txt and OUT_DIR/index.tsv (id, title, channel, duration, words).

Tries, in order:
  1. yt-dlp with alternate player clients (android_vr, ios, mweb, tv) — gets past
     "Sign in to confirm you're not a bot" on cloud/server IPs
  2. youtube-transcript-api
Videos that still fail are listed at the end so you can ask the user to paste them.
"""
import os, re, subprocess, sys, time, glob

def ensure(pkg, mod=None):
    try:
        __import__(mod or pkg)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=False)

def vid_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else url.strip()

def clean_vtt(path):
    lines, prev = [], None
    for l in open(path, encoding="utf-8", errors="ignore"):
        l = l.strip()
        if not l or "-->" in l or l.startswith(("WEBVTT", "Kind:", "Language:")) or l.isdigit():
            continue
        l = re.sub(r"<[^>]+>", "", l).strip()
        if l and l != prev:
            lines.append(l); prev = l
    out = []
    for l in lines:  # collapse rolling auto-captions
        if out and l.startswith(out[-1]):
            out[-1] = l
        elif not (out and out[-1].endswith(l)):
            out.append(l)
    return " ".join(out)

def try_ytdlp(url, vid, out_dir):
    meta = ""
    for client in ["android_vr", "ios", "mweb", "tv", "web_safari"]:
        cmd = ["yt-dlp", "-q", "--no-warnings", "--skip-download", "--write-auto-subs", "--write-subs",
               "--sub-langs", "en-orig,en,en-US,en-GB", "--sub-format", "vtt", "--sleep-subtitles", "3",
               "--extractor-args", f"youtube:player_client={client}",
               "--print", "%(title)s\t%(channel)s\t%(duration_string)s", "--no-simulate",
               "-o", os.path.join(out_dir, f"{vid}.%(ext)s"), url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.stdout.strip():
            meta = r.stdout.strip().splitlines()[0]
        vtts = sorted(glob.glob(os.path.join(out_dir, f"{vid}*.vtt")), key=lambda p: ("orig" not in p, p))
        if vtts:
            return clean_vtt(vtts[0]), meta
        time.sleep(2)
    return None, meta

def try_api(vid):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        t = YouTubeTranscriptApi().fetch(vid, languages=["en", "en-US", "en-GB"])
        return " ".join(s.text for s in t)
    except Exception:
        return None

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_dir, urls = sys.argv[1], sys.argv[2:]
    os.makedirs(out_dir, exist_ok=True)
    ensure("yt-dlp", "yt_dlp"); ensure("youtube-transcript-api", "youtube_transcript_api")
    index, failed = [], []
    for url in urls:
        vid = vid_id(url)
        text, meta = try_ytdlp(url, vid, out_dir)
        if not text:
            text = try_api(vid)
        if not text:
            failed.append(url); continue
        open(os.path.join(out_dir, f"{vid}.txt"), "w").write(text)
        title, channel, dur = (meta.split("\t") + ["", "", ""])[:3]
        index.append(f"{vid}\t{title}\t{channel}\t{dur}\t{len(text.split())}")
        print(f"OK   {vid}  {title}  ({len(text.split())} words)")
    open(os.path.join(out_dir, "index.tsv"), "w").write("\n".join(index) + "\n")
    for u in failed:
        print(f"FAIL {u}  -> ask the user to paste the transcript (YouTube: … → Show transcript)")
    if not index and failed:
        print("\nNothing downloaded. If every request failed with a network/403 error, YouTube may be blocked by the environment's network policy.")

if __name__ == "__main__":
    main()
