========================================
 PROJECT SERAPHIM SKY — Scripts Readme
 devanshj27 | 2026
========================================

DIRECTORY STRUCTURE
-------------------
primary_script/
  demo2.py       — IMX500 inference + recording script (picamera2)
  labels.txt     — class labels (drone)
  network.rpk    — quantized model flashed to IMX500
  videos/        — recorded output saved here

secondary_script.py  — modlib/AiCamera inference script
venv/                — Python virtual environment (secondary script only)
requirements.txt     — pip dependencies for venv


========================================
 SYSTEM REQUIREMENTS (run once)
========================================
Required before either script will work.
Run on Raspberry Pi terminal:

  sudo apt update && sudo apt full-upgrade
  sudo apt install imx500-all
  sudo reboot


========================================
 PRIMARY SCRIPT (demo2.py)
========================================
No venv needed. Uses system picamera2.

Navigate to primary_script directory:
  cd /home/maxx/Desktop/july2026/scripts/primary_script

Run:
  python3 demo2.py \
    --model network.rpk \
    --labels labels.txt \
    --fps 30 \
    --bbox-normalization \
    --ignore-dash-labels \
    --bbox-order xy \
    --output "videos/recording_$(date +%Y%m%d_%H%M%S).mp4"

Stop: Press Ctrl+C on the terminal
Output: timestamped .mp4 + _signed.mp4 saved to videos/


========================================
 SECONDARY SCRIPT (secondary_script.py)
========================================
Requires venv.

Navigate to scripts directory:
  cd /home/maxx/Desktop/july2026/scripts

Activate venv:
  source venv/bin/activate

Run:
  python3 secondary_script.py

Stop: Ctrl+C
Deactivate venv when done:
  deactivate


========================================
 NOTES
========================================
- primary_script requires IMX500 camera connected via CSI
- network.rpk must match the labels in labels.txt
- videos/ folder must exist before running (mkdir -p videos)
- requirements.txt: pip freeze > requirements.txt (inside venv)
