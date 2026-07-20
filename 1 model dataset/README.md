---
tags:
- object-detection
- yolo
- drone-detection
- computer-vision
license: cc-by-4.0
task_categories:
- object-detection
pretty_name: Seraphim Drone Dataset
size_categories:
- 10K<n<100K
language:
- en
viewer: false
---

# Seraphim Drone Detection Dataset

<center>
  <img src="assets/logo.png" style="background-color:white;" alt="Seraphim Drone Detection Dataset" width="400">
</center>

## Dataset Overview

This is a comprehensive drone image dataset curated from **23 open-source datasets** and processed through a custom cleaning pipeline. The dataset is designed for training object detection models to identify drones in various environments and conditions. The majority of images feature rotary-wing (multi-rotor) unmanned aerial vehicles (UAVs), with a smaller portion representing fixed-wing and hybrid.

<center>
  <img src="assets/samples.png" alt="Sample Images">
</center>

### Key Features
To ensure interoperability and consistency, all images were resized and padded to a 640×640 format and annotated using the YOLO standard.

- **Format**: YOLO
- **Classes**: 1 (drone)
- **Total Images**: 83,483
- **Train subset**: 75,134
- **Test subset**: 8,349
- **Augmentation**: No extra data augmentation was introduced (except for the 640x640 padding), the dataset retains only the augmentations originally applied in the source datasets
- **Source Datasets**: 23 open-source collections
- **License**: CC BY 4.0

## Dataset Statistics
The following visualizations summarize the dataset’s structure and distribution:
- number of objects per image, 
- distribution of multi-object images (2+ drones per image),
- bounding-box size categories and frequency,  
- spatial density of drone annotation centers. 

Drone size is defined as the ratio of the bounding-box area to the full image area. We use COCO-style buckets 
(scaled to 640×640 = 409,600 px²):
- Tiny: < 0.0625% of image area (below 16x16 pixels for a square object),
- Small: 0.0625%–0.25% of image area (16x16 – 32x32 pixels),
- Medium: 0.25%–2.25% of image area (32x32 – 96x96 pixels),
- Large: ≥ 2.25% of image area (equal or above 96x96 pixels).

Notes:
- Percent ranges refer to bbox_area / image_area × 100%.
- Pixel equivalents assume a roughly square object (for intuition only).
- These thresholds reflect typical detection difficulty bands (tiny/small objects are notably harder).

| ![](assets/object_count_distribution.png) | ![](assets/multiple_object_count_distribution.png) |
|:--:|:--:|
| **Number of objects per image** | **Distribution of multi-object images** |
| ![](assets/drone_bbox_size_treemap.png) | ![](assets/drone_center_heatmap.png) |
| **Bounding-box size categories and frequency** | **Spatial density of drone annotation centers** |

## Dataset Structure
```
dataset/
├── train/
│   ├── images/         # 75,134 image files
│   │   └── *.jpg       # Training images
│   └── labels/          
│       └── *.txt       # YOLO format annotations
├── test/
│   ├── images/         # 8,349 image files
│   │   └── *.jpg       # Test images
│   └── labels/         
│       └── *.txt       # YOLO format annotations
├── assets/             # Documentation assets
├── LICENSE             # CC BY 4.0 license
├── README.md           # Dataset card
└── .gitattributes      # Git LFS rules
```


Note on archives:
- Images and labels are stored on HuggingFace in zipped batches (e.g., train/images/batch_001.zip, train/labels/batch_001.zip) to make uploads/downloads faster and more reliable.
- You can selectively fetch only the batches you need and after extraction the layout becomes standard YOLO (.../images/*.jpg, .../labels/*.txt).
- Below is a code snippet showing how to download and extract the dataset from HuggingFace.

## Data Processing
This dataset underwent a custom processing pipeline:
1. **Consolidation:** Merged 23 source datasets (~268,957 original images).
2. **Missing labels and invalid images removal:** Removed images without labels and invalid images.
3. **Exact-duplicate filtering:** Removed identical images and near-duplicates measured by mean pixel difference.
4. **Near-duplicate filtering:** Removed visually similar ones based on perceptual hashing with image rotation and flipping.
5. **Resolution Standardization:** Resized all images to 640x640.

## Limitations
- **Label Accuracy:** The dataset was cleaned for duplicates and standardized in format, but no additional quality improvements or manual relabeling were applied. The accuracy of annotations reflects the quality of the source datasets. Future improvements may include bounding-box refinement and manual content validation.
- **Image Characteristics:** The dataset includes a diverse mix of real drone photographs, marketing images (e.g., promotional materials or product visualizations), and computer-generated (synthetic) images. While this diversity increases coverage of different visual conditions and drone types, it may also affect model generalization to real-world aerial scenarios. Future updates will aim to tag or separate these subsets and potentially filter them out.

## Usage

### Loading with HuggingFace Hub    

```python
from huggingface_hub import snapshot_download
import zipfile
from pathlib import Path

# --- Configuration ---
REPO_ID = "lgrzybowski/seraphim-drone-detection-dataset"
LOCAL_DIR = Path("repository_location") # TODO: change to your local directory

# --- Step 1: Download the entire repo ---
repo_path = Path(snapshot_download(repo_id=REPO_ID, repo_type="dataset", local_dir=LOCAL_DIR))

# --- Step 2: Unzip all .zip files in place ---
zip_files = list(repo_path.rglob("*.zip"))
print(f"Found {len(zip_files)} zip files to extract")

for zip_path in zip_files:
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(zip_path.parent)
        print(f"✅ Extracted: {zip_path.relative_to(repo_path)}")
        zip_path.unlink()  # remove the zip file
    except zipfile.BadZipFile:
        print(f"⚠️ Skipping invalid zip: {zip_path}")

print("🎉 All zips extracted and removed.")
print(f"📂 Dataset ready at: {repo_path.resolve()}")
```

### Downloading the dataset with HuggingFace CLI
```bash
hf download lgrzybowski/seraphim-drone-detection-dataset --repo-type dataset
```

## Source Datasets

This dataset aggregates **23 open-source drone detection datasets**:

### Kaggle
1. [dasmehdixtr/drone-dataset-uav](https://www.kaggle.com/datasets/dasmehdixtr/drone-dataset-uav) (MIT)
2. [sshikamaru/drone-yolo-detection](https://www.kaggle.com/datasets/sshikamaru/drone-yolo-detection) (CC BY 4.0)
3. [nyahmet/fixed-wing-uav-dataset](https://www.kaggle.com/datasets/nyahmet/fixed-wing-uav-dataset) (CC0)

### Roboflow Universe (all CC BY 4.0)
4. [drone-rwsrk/drone-cmxwz](https://universe.roboflow.com/drone-rwsrk/drone-cmxwz)
5. [test-gaiza/drone-fm51j](https://universe.roboflow.com/test-gaiza/drone-fm51j)
6. [guide-mnmib/drone-uxto9](https://universe.roboflow.com/guide-mnmib/drone-uxto9)
7. [project-986i8/drone-uskpc](https://universe.roboflow.com/project-986i8/drone-uskpc)
8. [drone-6awy5/drone-tbxzo](https://universe.roboflow.com/drone-6awy5/drone-tbxzo)
9. [solar-jivmt/drone-vizwp](https://universe.roboflow.com/solar-jivmt/drone-vizwp)
10. [drone-l3ty9/drone-6cbn9](https://universe.roboflow.com/drone-l3ty9/drone-6cbn9)
11. [khanhlatao/drone-w607c](https://universe.roboflow.com/khanhlatao/drone-w607c)
12. [drone-ldsbj/drone-ntvhe](https://universe.roboflow.com/drone-ldsbj/drone-ntvhe)
13. [drone-gpmet/drone-xyhff](https://universe.roboflow.com/drone-gpmet/drone-xyhff)
14. [ilay-asis-ohxec/drone-144la](https://universe.roboflow.com/ilay-asis-ohxec/drone-144la)
15. [njit-6mjxn/drone-detection-fmgs5](https://universe.roboflow.com/njit-6mjxn/drone-detection-fmgs5)
16. [rohit-gopalan/drone-detection-kmtxt](https://universe.roboflow.com/rohit-gopalan/drone-detection-kmtxt)
17. [truffier-nicolas-vnjqt/drone-11-gymdz](https://universe.roboflow.com/truffier-nicolas-vnjqt/drone-11-gymdz)
18. [tracker-qjlj1/drones_new](https://universe.roboflow.com/tracker-qjlj1/drones_new)
19. [uavs-7l7kv/uavs-vqpqt](https://universe.roboflow.com/uavs-7l7kv/uavs-vqpqt)
20. [military-drone/drone_mil-u8fqk](https://universe.roboflow.com/military-drone/drone_mil-u8fqk)
21. [kitkk/ip-proj-2-quadcopter](https://universe.roboflow.com/kitkk/ip-proj-2-quadcopter)
22. [paresh-makwana/drone-detect-suvzw](https://universe.roboflow.com/paresh-makwana/drone-detect-suvzw)

### HuggingFace
23. [pathikg/drone-detection-dataset](https://huggingface.co/datasets/pathikg/drone-detection-dataset) (MIT)

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{seraphim_drone_detection_dataset_2025,
  title={Seraphim Drone Detection Dataset},
  author={Łukasz Grzybowski},
  year={2025},
  organization = {Seraphim Defence Systems},
  publisher={HuggingFace},
  url={https://huggingface.co/datasets/lgrzybowski/seraphim-drone-detection-dataset},
  note={Curated from 23 open-source datasets, CC BY 4.0 license}
}
```

## License

This dataset is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Contact

- **Author**: [Łukasz Grzybowski](https://www.linkedin.com/in/lukasz-grzybowski/)
- **Organization**: [Seraphim Defence Systems](https://seraphim-systems.com/)
© 2025 

## Acknowledgments

Special thanks to all the original dataset creators and contributors who made their datasets available under open licenses. This curated dataset builds upon their valuable work in the drone detection research community.
