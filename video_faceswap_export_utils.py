"""
video_faceswap_export_utils.py
Robust ffmpeg streaming utilities for ComfyUI-based video face-swapping pipelines.
"""

import os
import sys
import json
import subprocess
import logging
from typing import Generator, Optional, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_ffmpeg_process(
    args: list,
    video_format: dict,
    video_metadata: dict,
    file_path: str,
    env: Optional[dict] = None
) -> Generator:
    """
    Generator-based ffmpeg writer with strong validation and logging.
    """
    frame_data = yield
    total_frames = 0
    res = None

    def _run_ffmpeg(command):
        nonlocal frame_data, total_frames
        with subprocess.Popen(
            command + [file_path],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        ) as proc:
            try:
                while frame_data is not None:
                    if frame_data:
                        proc.stdin.write(frame_data)
                    else:
                        logger.warning("Empty frame skipped")
                    frame_data = yield
                    total_frames += 1
                proc.stdin.close()
                return proc.stderr.read()
            except BrokenPipeError:
                err = proc.stderr.read()
                raise RuntimeError(err.decode("utf-8"))

    if video_format.get("save_metadata", "False") != "False":
        os.makedirs("temp", exist_ok=True)
        metadata = json.dumps(video_metadata).replace("\\", "\\\\")
        meta_path = os.path.join("temp", "metadata.txt")
        with open(meta_path, "w") as f:
            f.write(";FFMETADATA1\ncomment=" + metadata)
        meta_args = args[:1] + ["-i", meta_path] + args[1:]
        res = yield from _run_ffmpeg(meta_args)

    if not res:
        res = yield from _run_ffmpeg(args)

    yield total_frames
    if res:
        print(res.decode("utf-8"), file=sys.stderr)


def send_frame(process, frame: Union[bytes, bytearray]):
    """Safely send frame data to ffmpeg process."""
    if not isinstance(frame, (bytes, bytearray)):
        raise TypeError("Frame must be bytes or bytearray")
    process.send(frame)
