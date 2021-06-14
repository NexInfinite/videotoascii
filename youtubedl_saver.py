from __future__ import unicode_literals

import youtube_dl


def save_file(url):
    ydl_opts = {"format": "worst", "outtmpl": "video"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            info = ydl.extract_info(url=url, download=False)
            fps = info['fps']
            total_frames = fps * info['duration']
            duration = info['duration']
        except:
            return "error", 0, 0
        return "video", fps, total_frames, duration
