# 🚁 · 🛩️ · ✈️ · 🛸Project Seraphim Sky · 🎯 · 📡 · 🔭 · ⚡ · 🤖
### Real-Time Drone Detection · On-Sensor Inference · RPi5 + Sony IMX500


> An end-to-end drone detection system built for industrial plant security — running a quantized YOLO11n model directly on the IMX500 AI Camera sensor, with no host CPU inference overhead.

---

## Overview

Project Seraphim Sky is a self-directed, independent R&D project delivering a working proof-of-concept drone detection pipeline on embedded hardware. The system detects drones in real time using a custom-trained YOLO11n model deployed to the Sony IMX500 AI Camera — meaning inference happens on the sensor chip itself, before any frame reaches the Raspberry Pi 5.

**Hardware:** Raspberry Pi 5 (8GB) + Sony IMX500 AI Camera  
![Project Architecture](https://developer.aitrios.sony-semicon.com/content-assets/ascii_doc/draft/content/UayACUz4Yr/Set%20up%20and%20prepare%20tutorial%20/2025-09-30/images/process_flow.png)
**Model:** YOLO11n (Ultralytics) → INT8 quantized via Sony MCT → deployed as `network.rpk`

![Project Pipeline post training](https://developer.aitrios.sony-semicon.com/content-assets/ascii_doc/draft/content/UayACUz4Yr/RPi%20Converter%20and%20Edge-MDT%20(ssi_converter_docs)/3.18.2/images/rpi_deployment_flow_20240816.png)
**Stack:** Python · Picamera2 · OpenCV · Sony Model Compression Toolkit · Ultralytics · Computer Vision · YOLOv8n · YOLO11n · Raspberry Pi 5 · IMX500

---

## Key Results

| Metric | Value |
|---|---|
| mAP@0.5 | **0.9733** |
| mAP@0.5:0.95 | 0.7052 |
| Precision | **0.9651** |
| Recall | **0.9523** |
| Inference latency (on-sensor) | ~15–17ms/frame |
| Field test | ✅ Pass |

> Pre-quantization metrics. On-device INT8 confidence outputs are hardware-bounded by MCT calibration constraints — see [Technical Notes](#technical-notes).

---

## Repository Structure

```
primary_script/
  demo2.py          — IMX500 inference + MP4 recording (picamera2)
  labels.txt        — class labels
  network.rpk       — quantized model (deploy to IMX500)
  videos/           — recorded output destination

secondary_script.py — modlib/AiCamera inference script
venv/               — Python virtual environment (secondary script only)
requirements.txt    — pip dependencies for venv
```

---

## System Requirements

Run once on the Raspberry Pi before anything else:

```bash
sudo apt update && sudo apt full-upgrade
sudo apt install imx500-all
sudo reboot
```

> `imx500-all` installs `picamera2`, IMX500 firmware tools, and all required drivers.

---

## Usage

### Primary Script — `demo2.py` (IMX500 · picamera2)

No venv needed. Uses system `picamera2`.

```bash
cd primary_script

python3 demo2.py \
  --model network.rpk \
  --labels labels.txt \
  --fps 30 \
  --bbox-normalization \
  --ignore-dash-labels \
  --bbox-order xy \
  --output "videos/recording_$(date +%Y%m%d_%H%M%S).mp4"
```

**Stop:** Press `Ctrl+C` on the terminal
**Output:** Timestamped `.mp4` + `_signed.mp4` (with embedded metadata) saved to `videos/`

> Ensure the `videos/` directory exists: `mkdir -p primary_script/videos`

---

### Secondary Script — `secondary_script.py` (modlib · AiCamera)

```bash
cd scripts

source venv/bin/activate
python3 secondary_script.py
# Stop: Ctrl+C
deactivate
```

---

## Features

- **On-sensor inference** — YOLO11n runs on the IMX500 chip, not the Pi CPU
- **MP4 recording** — annotated video saved with timestamp filename
- **Visible watermark** — `Project Seraphim Sky | devanshj27` burned into every frame
- **Metadata signature** — author/copyright embedded in `_signed.mp4` file properties
- **ESC to exit** — clean shutdown with file finalisation on keypress
- **Sky-background robustness** — model fine-tuned on custom sky-supplement dataset to close plain-sky detection gap

---

## Training & Deployment Pipeline

```
Dataset (~83k images)
  → YOLO11n training (Kaggle · P100)
  → model.export(format='imx')
  → MCT INT8 quantization (Kaggle · T4 · 30GB RAM)
  → packerOut.zip
  → imx500-package (on RPi5 terminal)
  → network.rpk (flashed to IMX500)
```

Datasets:
- [`lgrzybowski/seraphim-drone-detection-dataset`](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset) — ~83,000 images

---

## Technical Notes

**INT8 Confidence Collapse** — On-device confidence scores plateau at fixed values (~0.62–0.73) due to INT8 quantization of the confidence output head under limited MCT calibration (`fraction=0.35`, ~2,810 images). This is a hardware/platform ceiling of the IMX500's fixed-point pipeline, not a model quality issue — pre-quantization metrics confirm the underlying model is sound. Half calibration as per the dataset size (`fraction=0.5`) requires ~280GB RAM, exceeding available compute.

**Sky-Background Gap** — The base dataset exhibited texture/contrast bias, causing near-zero detections against plain sky. Identified during validation and resolved.


---

## Author

**devanshj27** · Independent Contributor  
Project Seraphim Sky · 2026


[https://developer.aitrios.sony-semicon.com/content-assets/ascii_doc/draft/content/UayACUz4Yr/Set%20up%20and%20prepare%20tutorial%20/2025-09-30/images/process_flow.png]: https://developer.aitrios.sony-semicon.com/content-assets/ascii_doc/draft/content/UayACUz4Yr/Set%20up%20and%20prepare%20tutorial%20/2025-09-30/images/process_flow.png