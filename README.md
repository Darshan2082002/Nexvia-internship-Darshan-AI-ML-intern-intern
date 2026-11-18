# Nexvia Technologies Internship

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Domain](https://img.shields.io/badge/Domain-Computer%20Vision%20%26%20AI-0A66C2)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Organization](https://img.shields.io/badge/Nexvia%20Technologies-AI%2FML%20Internship-orange)

This repository contains the complete source code, documentation, and deliverables for the **Nexvia Technologies AI/ML Internship**, uniting two core computer vision projects under a single workspace:

- **[Medical Imaging System](./Medical_Imaging_System/)** — Automated medical scan preprocessing, diagnostic classification/segmentation, clinical evaluation, and Grad-CAM visual explainability.
- **[Autonomous Perception Stack](./autonomous-perception-stack/)** — Real-time object detection, obstacle localization, multi-object tracking, and low-latency ONNX Runtime inference for autonomous navigation.

---

## Table of Contents

1. [Repository Folder Structure](#repository-folder-structure)
2. [Python Version & Prerequisites](#python-version--prerequisites)
3. [Library Installation](#library-installation)
4. [Project 1: Medical Imaging System](#project-1-medical-imaging-system)
   - [Project Details](#project-details)
   - [Commands to Run](#commands-to-run)
5. [Project 2: Autonomous Perception Stack](#project-2-autonomous-perception-stack)
   - [Project Details](#project-details-1)
   - [Commands to Run](#commands-to-run-1)
6. [Disclaimer](#disclaimer)
7. [Author](#author)

---

## Repository Folder Structure

```text
Nexvia-Technologies-Internship/
├── Medical_Imaging_System/
│   ├── configs/                  # Model and training hyperparameters (YAML)
│   ├── data/
│   │   ├── raw/                  # Original medical scans (gitignored)
│   │   └── processed/            # Preprocessed tensors/images
│   ├── src/
│   │   ├── data/                 # Preprocessing and dataset loaders
│   │   ├── models/               # Network architectures
│   │   ├── training/             # Training and validation loops
│   │   ├── evaluation/           # Clinical metrics and ROC evaluation
│   │   └── inference/            # Prediction and Grad-CAM scripts
│   ├── weights/                  # Saved model checkpoints (gitignored)
│   ├── app.py                    # Interactive Streamlit web UI
│   └── requirements.txt
│
├── autonomous-perception-stack/
│   ├── configs/                  # Camera and perception pipeline configs
│   ├── data/                     # Sample driving videos and test frames
│   ├── models/                   # YOLOv8 / ONNX detection weights
│   ├── src/
│   │   ├── detection/            # Object detection modules
│   │   ├── tracking/             # Multi-object tracking
│   │   └── utils/                # Visualization and FPS helpers
│   ├── main.py                   # Main perception pipeline entry point
│   └── requirements.txt
│
├── .venv/                        # Shared virtual environment (gitignored)
├── requirements.txt              # Unified dependencies for the workspace
└── README.md                     # Complete repository documentation
```

---

## Python Version & Prerequisites

- **Python Version:** Python 3.10 or higher
- **Package Manager:** `pip` (latest version recommended)
- **Version Control:** `git`
- **Hardware:** CUDA-compatible GPU recommended for model training and real-time inference

Verify your Python version before starting:

```powershell
python --version
```

---

## Library Installation

Clone the repository and install all required dependencies in a single virtual environment from the root directory:

```powershell
# 1. Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/Nexvia-Technologies-Internship.git
cd Nexvia-Technologies-Internship

# 2. Create and activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# For Linux/macOS: source .venv/bin/activate

# 3. Upgrade pip and install from requirements.txt
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Or install all required libraries for both projects directly:

```powershell
pip install torch torchvision ultralytics onnxruntime numpy pandas scipy scikit-learn opencv-python pillow pydicom albumentations matplotlib streamlit pyyaml
```

*(Note: For GPU-accelerated ONNX inference, install `onnxruntime-gpu` instead of `onnxruntime`.)*

---

## Project 1: Medical Imaging System

### Project Details
An AI-powered medical image analysis pipeline for automated diagnostic support. It handles medical scan preprocessing (DICOM/NIfTI/PNG), deep learning model training, clinical metric evaluation (Accuracy, Sensitivity, Specificity, AUC-ROC/Dice), and Grad-CAM visual explainability.

### Commands to Run

Run from the root repository folder:

```powershell
# 1. Preprocess the medical dataset
python Medical_Imaging_System/src/data/preprocess.py --config Medical_Imaging_System/configs/default.yaml

# 2. Train the model
python Medical_Imaging_System/src/training/train.py --config Medical_Imaging_System/configs/default.yaml

# 3. Evaluate on the test split
python Medical_Imaging_System/src/evaluation/evaluate.py --weights Medical_Imaging_System/weights/best_model.pt --split test

# 4. Run single-image inference with Grad-CAM explainability
python Medical_Imaging_System/src/inference/predict.py --image Medical_Imaging_System/data/sample_scan.png --weights Medical_Imaging_System/weights/best_model.pt --gradcam

# 5. Launch the interactive Streamlit web application
streamlit run Medical_Imaging_System/app.py
```

---

## Project 2: Autonomous Perception Stack

### Project Details
A real-time computer vision perception pipeline for autonomous navigation. It processes video feeds or live camera streams to perform low-latency object detection, obstacle localization, multi-object tracking, and live FPS visualization using YOLOv8 and ONNX Runtime.

### Commands to Run

Run from the root repository folder:

```powershell
# 1. Run perception pipeline on a test video file
python autonomous-perception-stack/main.py --source autonomous-perception-stack/data/test_drive.mp4 --weights autonomous-perception-stack/models/yolov8n.onnx --show

# 2. Run on a live webcam or USB camera stream
python autonomous-perception-stack/main.py --source 0 --weights autonomous-perception-stack/models/yolov8n.onnx --show

# 3. Run headless and save the annotated output video
python autonomous-perception-stack/main.py --source autonomous-perception-stack/data/test_drive.mp4 --weights autonomous-perception-stack/models/yolov8n.onnx --save-output
```

---

## Disclaimer

The **Medical Imaging System** is developed strictly for research and educational purposes during the Nexvia Technologies internship. It is not a certified medical device and must not be used for clinical diagnosis.

---

## Author

**Darshan B** — AI/ML Intern, Nexvia Technologies