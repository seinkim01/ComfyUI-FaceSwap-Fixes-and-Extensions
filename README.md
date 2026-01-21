# ComfyUI-FaceSwap-Fixes-and-Extensions

Enhancements and bug fixes for ComfyUI-based video face-swapping pipelines.

---

## 🎯 Overview

This repository documents **practical fixes and extensions for ComfyUI video face-swapping workflows**, with a focus on resolving critical issues in the `VHS_VideoCombine` function.

📍 The work was carried out during an internship at **Hana Financial Group – AI Vision Cell**, where ComfyUI was used to build and evaluate face-swapping pipelines for video-based AI applications.

The primary goal of this project is to improve **stability, compatibility, and robustness** of video export operations using `ffmpeg` within ComfyUI.

---

## 🧠 Background

ComfyUI provides a powerful node-based interface for generative AI workflows.  
However, when performing **video face swapping**, several runtime errors were encountered during the final video composition stage.

These issues caused pipeline failures even when face swapping itself completed successfully.

This repository captures:
- The errors encountered
- The root causes
- The concrete code-level fixes applied

---

## ❗ Issues Encountered

### 1. Invalid Argument Error (ffmpeg)

```
Error occurred when executing VHS_VideoCombine:
[Errno 22] Invalid argument
```

**Cause**  
Invalid or empty frame data was being written directly to the `ffmpeg` subprocess.

---

### 2. Bytes Object Attribute Error

```
AttributeError: 'bytes' object has no attribute 'tobytes'
```

**Cause**  
The pipeline attempted to call `.tobytes()` on frame data that was already of type `bytes`.

---

## ✅ Implemented Fixes

### 🔧 1. `ffmpeg_process` Function

Key improvements:
- Added validation for `None` or empty frame data
- Introduced detailed logging for debugging subprocess behavior
- Improved error handling for broken pipes during video writing

**Key Concepts**
- Defensive programming for streaming frame buffers
- Safe interaction with `ffmpeg` via `subprocess.Popen`

---

### 🔧 2. `combine_video` Function

Key improvements:
- Explicit handling of both `bytes` and non-`bytes` frame inputs
- Prevented invalid calls to `.tobytes()`
- Improved frame iteration stability

**Before**
```python
output_process.send(image.tobytes())
```

**After**
```python
if isinstance(image, bytes):
    output_process.send(image)
else:
    output_process.send(image.tobytes())
```

---

## 📁 Repository Structure

```
.
├── MobileFaceSwap.ipynb     # Colab-based face swap pipeline
├── roop_v1_3.ipynb          # Roop-based face swapping experiments
├── nodes.py                 # Patched ComfyUI node implementation
├── README.md                # Project documentation
└── LICENSE
```

---

## 💡 Use Cases

- Stabilizing ComfyUI video export for face-swapped videos
- Debugging ffmpeg-related runtime errors
- Reference implementation for handling mixed frame data types
- Educational resource for ComfyUI node development

---

## 🔗 References

- ComfyUI Reactor Node  
  https://github.com/Gourieff/comfyui-reactor-node

- VHS_VideoCombine Troubleshooting  
  https://github.com/Gourieff/comfyui-reactor-node?tab=readme-ov-file#troubleshooting

---

## 📜 License

This repository is intended for **research, educational, and experimental purposes**.

Please ensure compliance with local regulations and ethical guidelines when applying face-swapping technologies.

---

## ⭐ Notes

This project focuses on **engineering reliability rather than model training**.  
Contributions, suggestions, and discussions are welcome.
