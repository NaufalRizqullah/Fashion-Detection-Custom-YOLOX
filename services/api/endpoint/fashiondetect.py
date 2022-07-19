from fastapi import APIRouter, UploadFile, HTTPException
from io import BytesIO
from PIL import Image
import numpy as np

from services.core.logic.YOLOX.onnx_inference import fashion_detector

yolox_router = APIRouter()

@yolox_router.post("/detect")
async def fashion_detection(img: UploadFile):

    if img.filename.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=415, detail="Unsupported Type Image")

    image = Image.open(BytesIO(img.file.read()))
    image = np.array(image)
    return {"Hello": 'WoW'}