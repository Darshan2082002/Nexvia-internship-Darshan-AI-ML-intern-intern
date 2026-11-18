import os
import glob
import json # Added json import
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest")
def get_latest_scan():
    assets_dir = "medical-viewer/public/assets"
    # Still look for the latest heatmap first
    files = glob.glob(f"{assets_dir}/*_heatmap.png")
    
    if not files:
        return {"status": "waiting"}
    
    latest_file = max(files, key=os.path.getctime)
    filename = os.path.basename(latest_file)
    study_id = filename.replace("_heatmap.png", "")
    
    # Check for the matching JSON file
    meta_path = f"{assets_dir}/{study_id}_meta.json"
    confidence = 0.0
    patient_id = "Unknown"
    
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            meta_data = json.load(f)
            confidence = meta_data.get("confidence", 0.0)
            patient_id = meta_data.get("patientId", "Unknown")
    
    return {
        "status": "success",
        "id": study_id,
        "patientId": patient_id,
        "confidence": confidence,
        "heatmapUrl": f"/assets/{filename}"
    }