<div align="center">

# Project Seraphim Sky

🚁 · 🛩️ · ✈️ · 🛸 · 🎯 · 📡 · 🔭 · ⚡ · 🤖

### Real-Time Drone Detection · On-Sensor Inference · RPi5 + Sony IMX500

[![Model: YOLO11n](https://img.shields.io/badge/model-YOLO11n-0B23A9)](https://docs.ultralytics.com/models/yolo11/)
[![Raspberry Pi 5](https://img.shields.io/badge/Raspberry%20Pi-5-A22846?logo=raspberrypi&logoColor=white)](https://www.raspberrypi.com/products/raspberry-pi-5/)
[![Sony IMX500](https://img.shields.io/badge/Sony-IMX500%20AI%20Camera-000000?logo=sony&logoColor=white)](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)
[![Quantization: INT8](https://img.shields.io/badge/quantization-INT8%20%C2%B7%20Sony%20MCT-6A1B9A)](https://github.com/SonySemiconductorSolutions/mct-model-optimization)
[![Dataset](https://img.shields.io/badge/dataset-83k%20images-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

<a href="https://youtu.be/Hb2t5CzQXDM"><img src="test%20recordings/out-door/final-attempts/final_iteration_2.gif" width="640" alt="Outdoor field test: a drone over an open field is boxed and labelled 'drone (0.73)'"></a>

<sub>Outdoor field test (final iteration 2): detection runs on the camera sensor itself. Click for the full video.</sub>

[Overview](#overview) · [Results](#key-results) · [Field tests](#field-tests) · [Pipeline](#training--deployment-pipeline) · [Quick start](#quick-start) · [Repository](#repository-structure) · [Technical notes](#technical-notes) · [Author](#author)

</div>

---

## Overview

> An end-to-end drone detection system built for industrial plant security — running a quantized YOLO11n model directly on the IMX500 AI Camera sensor, with no host CPU inference overhead.

Project Seraphim Sky is a self-directed, independent R&D project delivering a working proof-of-concept drone detection pipeline on embedded hardware. The system detects drones in real time using a custom-trained YOLO11n model deployed to the Sony IMX500 AI Camera — meaning inference happens on the sensor chip itself, before any frame reaches the Raspberry Pi 5.

- **Hardware:** Raspberry Pi 5 (8 GB) + Sony IMX500 AI Camera
- **Model:** YOLO11n (Ultralytics), one class (`drone`), 640 × 640 input → INT8 quantized via Sony MCT → deployed as `network.rpk`
- **Stack:** Python · Ultralytics (YOLO11n, YOLOv8n) · Sony Model Compression Toolkit · IMX500 Converter · Picamera2 · modlib · OpenCV · Kaggle · Google Colab

---

## Features

- **On-sensor inference** — YOLO11n runs on the IMX500 chip, not the Pi CPU
- **MP4 recording** — annotated video saved with a timestamped filename
- **Visible watermark** — `Project Seraphim Sky | devanshj27` burned into every frame
- **Metadata signature** — author/copyright embedded in a `_signed.mp4` copy (written with `ffmpeg`)
- **Clean shutdown** — `Ctrl+C` stops capture and finalises the recording
- **Sky-background robustness** — model fine-tuned on a custom sky-supplement dataset to close the plain-sky detection gap
- **Two runtimes, one model** — run the same packaged network through Picamera2 (`demo2.py`) or Sony's modlib (`secondary_script.py`)

---

## Key Results

| Metric | Value |
|---|---|
| mAP@0.5 | **0.9733** |
| mAP@0.5:0.95 | 0.7052 |
| Precision | **0.9651** |
| Recall | **0.9523** |
| Inference latency (on-sensor) | ~15–17 ms/frame |
| IMX500 on-chip memory used | 7.16 MB of 8 MB (90%) |
| Field test | ✅ Pass — see [recordings](#field-tests) |

> Accuracy metrics are pre-quantization. On-device INT8 confidence outputs are hardware-bounded by MCT calibration constraints — see [Technical Notes](#technical-notes).

<details>
<summary><b>Training curves and validation predictions</b> (YOLO11n, epochs 71–95)</summary>
<br>

<img src="3%20model%20training%20%28nb1%29/yolo11n/output/epoch-71_to_95/results.png" width="100%" alt="YOLO11n training and validation loss, precision, recall and mAP curves">

<img src="3%20model%20training%20%28nb1%29/yolo11n/output/epoch-71_to_95/val_batch0_pred.jpg" width="100%" alt="Grid of validation images with predicted drone boxes">

PR/F1 curves, confusion matrices and the trained weights (`best.pt`, `best.onnx`) are in [`3 model training (nb1)/yolo11n/output/epoch-71_to_95/`](3%20model%20training%20%28nb1%29/yolo11n/output/epoch-71_to_95).

</details>

---

## Field Tests

Real-world recordings from the Raspberry Pi 5 + IMX500 setup, from bench test to open field.

| Set | Scene | GIF | Video |
|---|---|---|---|
| **Final attempts** | Open field — drone against a cloudy sky | [1](test%20recordings/out-door/final-attempts/final_iteration_1.md) · [2](test%20recordings/out-door/final-attempts/final_iteration_2.md) · [3](test%20recordings/out-door/final-attempts/final_iteration_3.md) · [4](test%20recordings/out-door/final-attempts/final_iteration_4.md) · [5](test%20recordings/out-door/final-attempts/final_iteration_5.md) | [1](https://youtu.be/t2ZcmzPuLWs) · [2](https://youtu.be/Hb2t5CzQXDM) · [3](https://youtu.be/-Y4pE9_w-u8) · [4](https://youtu.be/1RETE5MvYhY) · [5](https://youtu.be/0m6LsMKaPNc) |
| **Trials** | Campus — between trees and buildings | [1](test%20recordings/out-door/trials-1/take1.md) · [2](test%20recordings/out-door/trials-1/take2.md) · [3](test%20recordings/out-door/trials-1/take3.md) · [4](test%20recordings/out-door/trials-1/take4.md) | [1](https://youtu.be/478HzCcQR3A) · [2](https://youtu.be/O8dWyrXIT6c) · [3](https://youtu.be/XoHap88_YrY) · [4](https://youtu.be/ha9-GHH9w2I) |
| **Indoor** | Bench test — drone image on a laptop screen | [GIF](test%20recordings/in-door/indoor%20recording%20image.md) | [Video](https://youtu.be/j-8RWpgCHyM) |

> The constant 0.73 score on every box is the INT8 confidence plateau explained in [Technical Notes](#technical-notes). Each GIF is 28–87 MB, so the YouTube videos load faster.

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

| Stage | What happens |
|---|---|
| **[1 model dataset](1%20model%20dataset)** | [Seraphim Drone Detection Dataset](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset) — 83,483 images (75,134 train / 8,349 test), one class, YOLO format, 640 × 640 |
| **[2 model pipeline](2%20model%20pipeline)** | Reference diagrams of Sony's IMX500 toolchain (below) |
| **[3 model training (nb1)](3%20model%20training%20%28nb1%29)** | `kaggle.ipynb` fine-tunes COCO-pretrained YOLO11n (imgsz 640, batch 64, patience 15) in resumable Kaggle sessions; `colab.ipynb` holds the earlier YOLOv8n baseline |
| **[4 model quantization (nb2)](4%20model%20quantization%20%28nb2%29)** | `model.export(format="imx", int8=True)` runs MCT post-training quantization, the IMX500 converter (Java 17) and the packer → `packerOut.zip` |
| **[5 deployment (on rpi5)](5%20deployment%20%28on%20rpi5%29)** | `imx500-package` turns `packerOut.zip` into `network.rpk`; Picamera2 and modlib scripts run it on the Pi |

Notebook 2 pins the export toolchain (e.g. `model-compression-toolkit==2.4.5`, `imx500-converter[pt]==3.17.3`), because Ultralytics otherwise swaps packages mid-export.

<p align="center">
  <img src="2%20model%20pipeline/process_flow.png" width="100%" alt="IMX500 toolchain: PyTorch or TensorFlow model, Model Compression Toolkit and IMX500 Converter on the PC, IMX500 Packager on the Raspberry Pi, then the AI Camera">
  <img src="2%20model%20pipeline/rpi_deployment_flow_20240816.png" width="100%" alt="Deployment flow: floating-point model, Model Compression Toolkit, Converter, Post-Converter and Packager, AI Camera">
  <br>
  <sub>Diagrams: Sony Semiconductor Solutions, AITRIOS developer documentation.</sub>
</p>

---

## Quick Start

Everything below runs on the Raspberry Pi 5 with the AI Camera connected over CSI.

### 1. System requirements (run once)

```bash
sudo apt update && sudo apt full-upgrade
sudo apt install imx500-all
sudo reboot
```

> `imx500-all` installs the IMX500 firmware, drivers and packaging tools (`imx500-package`); Picamera2 ships with Raspberry Pi OS. `demo2.py` also calls `ffmpeg` to write the signed copy, so run `sudo apt install ffmpeg` if it is missing.

### 2. Get the code

```bash
git clone https://github.com/retromonalisa/seraphim-sky.git
cd seraphim-sky
```

The full clone is about 1 GB, mostly test-recording GIFs. To fetch only the deployment folder:

```bash
git clone --filter=blob:none --sparse https://github.com/retromonalisa/seraphim-sky.git
cd seraphim-sky
git sparse-checkout set "5 deployment (on rpi5)"
```

### 3. Primary script — `demo2.py` (IMX500 · Picamera2)

No venv needed. Uses system `picamera2`.

```bash
cd "5 deployment (on rpi5)/scripts/primary_script"
mkdir -p videos

python3 demo2.py \
  --model network.rpk \
  --labels labels.txt \
  --fps 30 \
  --bbox-normalization \
  --ignore-dash-labels \
  --bbox-order xy \
  --output "videos/recording_$(date +%Y%m%d_%H%M%S).mp4"
```

- **Stop:** press `Ctrl+C` in the terminal
- **Output:** timestamped `.mp4` + `_signed.mp4` (with embedded metadata) saved to `videos/`
- Drop `--output` to watch the live preview without recording

| Option | Default | Purpose |
|---|---|---|
| `--threshold` | `0.55` | Minimum confidence for a box to be drawn |
| `--fps` | network inference rate | Frames per second (also sets the recording FPS) |
| `--output` | off | Save the annotated video to this path |
| `--print-intrinsics` | off | Print the network intrinsics and exit |

### 4. Secondary script — `secondary_script.py` (modlib · AiCamera)

Runs the same model through Sony's [Application Module Library](https://github.com/SonySemiconductorSolutions/aitrios-rpi-application-module-library) inside a virtual environment.

```bash
cd "5 deployment (on rpi5)/scripts"
python3 -m venv venv                  # first run only
source venv/bin/activate
pip install -r requirements.txt       # first run only

cd secondary_script                   # the script loads files/ relative to this folder
python3 secondary_script.py           # Ctrl+C to stop
deactivate
```

---

## Repository Structure

```
seraphim-sky/
├── 1 model dataset/
│   └── README.md                     — dataset card (Seraphim Drone Detection Dataset)
├── 2 model pipeline/                 — Sony IMX500 toolchain diagrams
├── 3 model training (nb1)/
│   ├── yolo11n/
│   │   ├── kaggle.ipynb              — Notebook 1: YOLO11n fine-tuning (Kaggle)
│   │   └── output/epoch-71_to_95/    — best.pt, best.onnx, curves, confusion matrices
│   └── yolov8n/
│       ├── colab.ipynb               — earlier YOLOv8n baseline (Colab)
│       └── output/epoch-37_to_43/    — weights (zip) + training curves
├── 4 model quantization (nb2)/
│   ├── quantization-kaggle-imx500-export.ipynb   — Notebook 2: MCT INT8 + IMX500 export
│   └── output/drone_imx_model.zip    — packerOut.zip, model_imx.onnx, dnnParams.xml, memory report
├── 5 deployment (on rpi5)/
│   └── scripts/
│       ├── primary_script/
│       │   ├── demo2.py              — IMX500 inference + MP4 recording (picamera2)
│       │   ├── labels.txt            — class labels
│       │   └── network.rpk           — quantized model (deploy to IMX500)
│       ├── secondary_script/
│       │   ├── secondary_script.py   — modlib/AiCamera inference script
│       │   └── files/                — packerOut.zip, labels.txt, model_imx.*, pack/network.rpk
│       ├── requirements.txt          — pip dependencies for the venv (secondary script)
│       └── readme.txt                — plain-text run notes
├── test recordings/
│   ├── in-door/                      — indoor bench test
│   └── out-door/
│       ├── trials-1/                 — take1 – take4
│       └── final-attempts/           — final_iteration_1 – final_iteration_5
├── LICENSE
└── README.md
```

---

## Technical Notes

**INT8 Confidence Collapse** — On-device confidence scores plateau at fixed values (~0.62–0.73) due to INT8 quantization of the confidence output head under limited MCT calibration (`fraction=0.35`, ~2,810 images). This is a hardware/platform ceiling of the IMX500's fixed-point pipeline, not a model quality issue — pre-quantization metrics confirm the underlying model is sound. Half calibration as per the dataset size (`fraction=0.5`) requires ~280GB RAM, exceeding available compute.

**Sky-Background Gap** — The base dataset exhibited texture/contrast bias, causing near-zero detections against plain sky. Identified during validation and resolved.

---

## Dataset & Acknowledgements

- **Dataset** — [Seraphim Drone Detection Dataset](https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset) by Łukasz Grzybowski (Seraphim Defence Systems): 83,483 images curated from 23 open-source datasets, licensed CC BY 4.0. Its dataset card is mirrored in [`1 model dataset/README.md`](1%20model%20dataset/README.md).
- **Sony Semiconductor Solutions** — the IMX500 sensor, [Model Compression Toolkit](https://github.com/SonySemiconductorSolutions/mct-model-optimization), [Application Module Library](https://github.com/SonySemiconductorSolutions/aitrios-rpi-application-module-library) and the pipeline diagrams in `2 model pipeline/`.
- **Ultralytics** — YOLO11 / YOLOv8 training and the [Sony IMX500 export integration](https://docs.ultralytics.com/integrations/sony-imx500/).
- **Raspberry Pi** — Picamera2 and the IMX500 packaging tools.

---

## License

Code in this repository is released under the [MIT License](LICENSE) © 2026 Devansh Jaiswal. The dataset (CC BY 4.0) and Sony's diagrams remain under their owners' terms.

---

## Author

<a href="https://github.com/retromonalisa"><img src="https://avatars.githubusercontent.com/u/70763278?v=4" width="80" alt="retromonalisa on GitHub"></a>

**Devansh Jaiswal** (`devanshj27`) · GitHub [@retromonalisa](https://github.com/retromonalisa)<br>
Independent Contributor · Project Seraphim Sky · 2026
