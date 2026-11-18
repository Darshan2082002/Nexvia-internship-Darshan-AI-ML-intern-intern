import json
import os
import requests
import torch
import numpy as np
import matplotlib.pyplot as plt
import time
from monai.networks.nets import DenseNet121
from monai.transforms import Compose, LoadImage, EnsureChannelFirst, ScaleIntensity, ToTensor
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from monai.transforms import Compose, LoadImage, EnsureChannelFirst, ScaleIntensity, ToTensor, Rotate90
ORTHANC_URL = "http://orthanc:8042"
MODEL_PATH = "densenet_model_v1.pth"
OUTPUT_DIR = "medical-viewer/public/assets" # Where we will save images for React

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Initialize Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DenseNet121(spatial_dims=2, in_channels=1, out_channels=2).to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# 2. Setup Preprocessing and Grad-CAM
transforms = Compose([
    LoadImage(image_only=True),
    EnsureChannelFirst(),
    Rotate90(k=3, spatial_axes=(0, 1)), # k=3 rotates 270 degrees (-90). Change to k=1 if it rotates the wrong way.
    ScaleIntensity(),
    ToTensor()
])
target_layers = [model.features[-1]]
cam = GradCAM(model=model, target_layers=target_layers)

def get_new_studies():
    """Fetch a list of patient studies from Orthanc."""
    response = requests.get(f"{ORTHANC_URL}/studies", auth=("orthanc", "orthanc"))
    if response.status_code != 200:
        return []
    return response.json()

def process_study(study_id):
    """Download DICOM, run AI inference, and save Grad-CAM."""
    print(f"Fetching instances for study: {study_id}...")
    instances = requests.get(f"{ORTHANC_URL}/studies/{study_id}/instances", auth=("orthanc", "orthanc")).json()
    
    for instance in instances:
        instance_id = instance['ID']
        dicom_data = requests.get(f"{ORTHANC_URL}/instances/{instance_id}/file", auth=("orthanc", "orthanc")).content
        
        temp_dcm = "temp.dcm"
        with open(temp_dcm, "wb") as f:
            f.write(dicom_data)
            
        print("Running AI inference...")
        # Preprocess
        input_tensor = transforms(temp_dcm).unsqueeze(0).to(device)
        
        # FIX: Convert MONAI MetaTensor to standard PyTorch Tensor
        input_tensor = input_tensor.as_tensor()
        
        # Predict
        with torch.no_grad():
            outputs = model(input_tensor)
            confidence = torch.softmax(outputs, dim=1)[0][1].item() * 100 # Confidence for disease class
            
        # Generate Heatmap
        targets = [ClassifierOutputTarget(1)]
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)[0, :]
        original_img = input_tensor.squeeze().cpu().numpy()
        rgb_img = np.stack((original_img,)*3, axis=-1)
        visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        
        # Save image output for React frontend
        output_path = os.path.join(OUTPUT_DIR, f"{instance_id}_heatmap.png")
        plt.imsave(output_path, visualization)

        # Save metadata output for FastAPI
        metadata = {
            "id": instance_id,
            "patientId": f"Patient-{study_id[:4]}",
            "confidence": round(confidence, 2)
        }
        json_path = os.path.join(OUTPUT_DIR, f"{instance_id}_meta.json")
        with open(json_path, "w") as json_file:
            json.dump(metadata, json_file)
        
        print(f"[SUCCESS] Analyzed {instance_id}")
        print(f"Disease Confidence: {confidence:.2f}%")
        print(f"Heatmap saved to {output_path}")
        print(f"Metadata saved to {json_path}")

if __name__ == "__main__":
    print("Starting Inference Service...")
    print("Listening for new DICOM studies on Orthanc (Press Ctrl+C to stop)...")
    
    processed_studies = set() # Ignore already uploaded files
    
    while True:
        try:
            current_studies = set(get_new_studies())
            print(f"Checked server: found {len(current_studies)} valid studies")
            new_studies = current_studies - processed_studies
            
            for study_id in new_studies:
                print(f"\n[+] New study detected! ID: {study_id}")
                process_study(study_id)
                processed_studies.add(study_id)
                
        except requests.exceptions.ConnectionError:
            print("Cannot connect to Orthanc...")
            
        time.sleep(5)