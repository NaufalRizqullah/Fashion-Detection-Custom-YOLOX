from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from io import BytesIO
from PIL import Image
import numpy as np

from services.core.logic.YOLOX.onnx_inference import fashion_detector

yolox_router = APIRouter()

@yolox_router.post("/detect")
def fashion_detection(im: UploadFile = File(...)):

    if im.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        raise HTTPException(status_code=415, detail="Unsupported Type Image")

    image = Image.open(BytesIO(im.file.read()))
    image = np.array(image)

    return fashion_detector(image)