# Medical Imaging Diagnostic System

A Docker-based medical imaging prototype that receives DICOM studies through Orthanc, runs DenseNet121 inference with Grad-CAM visualization, and presents the results in a React viewer.

> **Educational use only:** This project is not a medical device and must not be used for clinical diagnosis or patient care.

## Features

- Orthanc DICOM server integration
- Automatic polling for newly uploaded studies
- DenseNet121 image classification
- PyTorch Grad-CAM heatmap generation
- FastAPI endpoint for the latest processed scan
- React viewer with confidence and radiologist decision controls
- Docker Compose deployment

## Architecture

```text
DICOM client or PACS
        |
        v
     Orthanc :8042
        |
        v
 Inference worker ---- generates ----> Shared assets
        |                                  |
        v                                  v
  FastAPI :8000 ----------------> React/Vite :5174
```

The inference worker checks Orthanc every five seconds. Processed heatmaps and metadata are stored in `medical-viewer/public/assets` and served by the frontend.

## Technology

- **Backend:** Python, FastAPI, Uvicorn
- **AI:** PyTorch, MONAI, torchvision, Grad-CAM
- **DICOM:** Orthanc
- **Frontend:** React, Vite, Axios, Tailwind CSS
- **Deployment:** Docker and Docker Compose

## Project Structure

```text
.
|-- api.py                         # FastAPI latest-study endpoint
|-- inference_service.py           # Orthanc polling and AI inference
|-- densenet_model_v1.pth          # Pretrained model weights
|-- requirements.txt               # Python dependencies
|-- Dockerfile.backend             # Python API and worker image
|-- docker-compose.yml             # Full application stack
|-- medical-viewer/
|   |-- src/App.jsx                # Diagnostic viewer interface
|   |-- public/assets/             # Generated heatmaps and metadata
|   |-- Dockerfile                 # React/Vite development container
|   `-- package.json
`-- Demo video.mp4
```

## Prerequisites

- Docker with Docker Compose
- A DICOM upload tool such as Orthanc, DICOM client software, or PACS
- Alternatively, Python 3.10+ and Node.js 20+ for local development

## Run with Docker Compose

From the repository root:

```powershell
docker compose up --build
```

Open the application:

- Viewer: http://localhost:5174
- API: http://localhost:8000/api/latest
- API documentation: http://localhost:8000/docs
- Orthanc: http://localhost:8042

Orthanc is configured in this project to use the local credentials `orthanc` / `orthanc`. After the stack starts, upload a DICOM study to Orthanc. The inference worker will detect it and generate a heatmap and metadata.

Stop the stack:

```powershell
docker compose down
```

To remove the shared asset volume as well:

```powershell
docker compose down -v
```

## Run Locally

### 1. Start Orthanc

The easiest option is to start only Orthanc:

```powershell
docker compose up orthanc
```

### 2. Start the Python backend

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn api:app --host 0.0.0.0 --port 8000
```

Start the inference worker in a separate terminal:

```powershell
python inference_service.py
```

When running outside Docker, ensure `inference_service.py` can reach Orthanc at `http://orthanc:8042`. Change `ORTHANC_URL` to `http://localhost:8042` if Orthanc is accessible through the host.

### 3. Start the React viewer

```powershell
cd medical-viewer
npm install
npm run dev -- --host 0.0.0.0 --port 5174
```

## API

### `GET /api/latest`

Returns the latest successfully processed heatmap.

Example response:

```json
{
  "status": "success",
  "id": "instance-id",
  "patientId": "Patient-xxxx",
  "confidence": 92.5,
  "heatmapUrl": "/assets/instance-id_heatmap.png"
}
```

When no processed heatmap is available, the response is:

```json
{
  "status": "waiting"
}
```

## Output Files

Each processed instance produces:

- `<instance-id>_heatmap.png`: Grad-CAM overlay
- `<instance-id>_meta.json`: Instance ID, generated patient label, and confidence
