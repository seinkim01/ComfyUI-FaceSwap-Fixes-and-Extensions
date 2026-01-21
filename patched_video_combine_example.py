"""
patched_video_combine_example.py

Minimal example showing how to use safe_ffmpeg_process
inside a ComfyUI-style video combine loop.
"""

from video_faceswap_export_utils import safe_ffmpeg_process, send_frame

def export_video(images, args, video_format, metadata, output_path, env):
    process = safe_ffmpeg_process(args, video_format, metadata, output_path, env)
    next(process)

    for img in images:
        if isinstance(img, bytes):
            send_frame(process, img)
        else:
            send_frame(process, img.tobytes())

    try:
        process.send(None)
        process.send(None)
    except StopIteration:
        pass
