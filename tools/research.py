#!/usr/bin/env python3
"""Content-Research: holt Videos, Metadaten und Transkripte von YouTube und Instagram.

Alles landet unter research/<datum>_<quelle>_<name>/:
  meta.json        Metadaten (Titel, Views, Likes, Beschreibung/Caption, ...)
  transkript.txt   Transkript (YouTube-Untertitel bzw. Whisper, falls installiert)
  media/           heruntergeladene Videos (nur mit --media, wird nicht committet)

Beispiele:
  python3 tools/research.py youtube "https://www.youtube.com/watch?v=..."
  python3 tools/research.py youtube-kanal "https://www.youtube.com/@kanal" --limit 30
  python3 tools/research.py instagram natgeo --limit 20 --media
  python3 tools/research.py instagram-post "https://www.instagram.com/reel/SHORTCODE/"
  python3 tools/research.py transkribieren research/.../media/video.mp4
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"


def slug(text, max_len=50):
    text = re.sub(r"[^\w\-]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    return text[:max_len] or "unbenannt"


def out_dir(source, name):
    d = RESEARCH / f"{dt.date.today():%Y-%m-%d}_{source}_{slug(name)}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def vtt_to_text(vtt):
    """Untertitel (VTT) zu Fließtext; entfernt Zeitstempel, Tags und die Wiederholungen von Auto-Untertiteln."""
    lines, last = [], None
    for line in vtt.splitlines():
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line or "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")) or line.isdigit():
            continue
        if line != last:
            lines.append(line)
        last = line
    return "\n".join(lines)


# ---------------------------------------------------------------- YouTube

def youtube(args):
    import yt_dlp

    opts = {
        "skip_download": not args.media,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": args.lang.split(","),
        "subtitlesformat": "vtt",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL({**opts, "skip_download": True}) as ydl:
        info = ydl.extract_info(args.url, download=False)
    d = out_dir("yt", info.get("title", info["id"]))
    opts["outtmpl"] = str(d / "media" / "%(id)s.%(ext)s")
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([args.url])

    meta = {k: info.get(k) for k in (
        "id", "title", "channel", "channel_url", "upload_date", "duration",
        "view_count", "like_count", "comment_count", "tags", "description", "webpage_url")}
    write_json(d / "meta.json", meta)

    subs = sorted((d / "media").glob("*.vtt"))
    if subs:
        (d / "transkript.txt").write_text(vtt_to_text(subs[0].read_text(encoding="utf-8")), encoding="utf-8")
    else:
        print("Keine Untertitel gefunden – ggf. mit --media laden und 'transkribieren' nutzen.", file=sys.stderr)
    print(d)


def youtube_kanal(args):
    """Listet die Videos eines Kanals/einer Playlist, sortiert nach Views – zum Finden der Top-Performer."""
    import yt_dlp

    url = args.url.rstrip("/")
    if "/@" in url and not url.endswith(("/videos", "/shorts")):
        url += "/videos"
    with yt_dlp.YoutubeDL({"extract_flat": True, "playlistend": args.limit, "quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    videos = [{"title": e.get("title"), "url": e.get("url"), "views": e.get("view_count"),
               "duration": e.get("duration")} for e in info.get("entries", [])]
    videos.sort(key=lambda v: v["views"] or 0, reverse=True)
    d = out_dir("yt-kanal", info.get("title", "kanal"))
    write_json(d / "videos.json", videos)
    for v in videos[:15]:
        print(f'{v["views"] or "?":>12}  {v["title"]}  {v["url"]}')
    print(d)


# ---------------------------------------------------------------- Instagram

def insta_loader(args):
    import instaloader

    L = instaloader.Instaloader(download_pictures=False, download_video_thumbnails=False,
                                save_metadata=False, compress_json=False, quiet=True)
    user = os.environ.get("IG_RESEARCH_USER")
    if user:
        try:
            L.load_session_from_file(user)
        except FileNotFoundError:
            print(f"Keine Session für {user}. Einmalig ausführen: instaloader --login {user}", file=sys.stderr)
    return L


def post_meta(p):
    return {
        "shortcode": p.shortcode, "url": f"https://www.instagram.com/p/{p.shortcode}/",
        "datum": p.date_utc, "typ": p.typename, "ist_video": p.is_video,
        "likes": p.likes, "kommentare": p.comments, "video_views": p.video_view_count if p.is_video else None,
        "caption": p.caption, "hashtags": p.caption_hashtags,
    }


def save_post_video(L, p, d):
    if p.is_video:
        L.dirname_pattern = str(d / "media")
        L.download_post(p, target=p.owner_username)


def instagram(args):
    import instaloader

    L = insta_loader(args)
    profile = instaloader.Profile.from_username(L.context, args.profil)
    d = out_dir("ig", args.profil)
    posts = []
    for i, p in enumerate(profile.get_posts()):
        if i >= args.limit:
            break
        posts.append(post_meta(p))
        if args.media:
            save_post_video(L, p, d)
    posts.sort(key=lambda x: x["video_views"] or x["likes"] or 0, reverse=True)
    write_json(d / "meta.json", {"profil": args.profil, "follower": profile.followers,
                                 "bio": profile.biography, "posts": posts})
    for p in posts[:15]:
        print(f'{p["video_views"] or p["likes"]:>10}  {p["url"]}  {(p["caption"] or "")[:60]!r}')
    print(d)


def instagram_post(args):
    import instaloader

    L = insta_loader(args)
    m = re.search(r"/(?:p|reel|tv)/([\w-]+)", args.url)
    p = instaloader.Post.from_shortcode(L.context, m.group(1) if m else args.url)
    d = out_dir("ig-post", f"{p.owner_username}-{p.shortcode}")
    write_json(d / "meta.json", post_meta(p))
    save_post_video(L, p, d)
    print(d)


# ---------------------------------------------------------------- Transkription

def transkribieren(args):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Dafür einmalig: pip install faster-whisper (lädt beim ersten Lauf ein Modell von huggingface.co)")
    model = WhisperModel(args.modell, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(args.datei)
    text = "\n".join(s.text.strip() for s in segments)
    target = Path(args.datei).resolve().parent.parent / "transkript.txt"
    target.write_text(text, encoding="utf-8")
    print(target)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("youtube", help="Ein YouTube-Video: Metadaten + Transkript")
    s.add_argument("url")
    s.add_argument("--lang", default="de,en", help="Untertitel-Sprachen, Komma-getrennt")
    s.add_argument("--media", action="store_true", help="Video auch herunterladen")
    s.set_defaults(func=youtube)

    s = sub.add_parser("youtube-kanal", help="Videos eines Kanals nach Views sortiert")
    s.add_argument("url")
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(func=youtube_kanal)

    s = sub.add_parser("instagram", help="Letzte Posts eines öffentlichen Profils")
    s.add_argument("profil")
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--media", action="store_true", help="Videos herunterladen")
    s.set_defaults(func=instagram)

    s = sub.add_parser("instagram-post", help="Ein einzelner Post/Reel")
    s.add_argument("url")
    s.set_defaults(func=instagram_post)

    s = sub.add_parser("transkribieren", help="Video/Audio mit Whisper transkribieren")
    s.add_argument("datei")
    s.add_argument("--modell", default="small")
    s.set_defaults(func=transkribieren)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
