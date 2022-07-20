from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from io import BytesIO
from PIL import Image
import numpy as np

from services.core.logic.YOLOX.onnx_inference import fashion_detector
from services.core.schemas.output import APIOutput

yolox_router = APIRouter()

@yolox_router.post("/detect", response_model=APIOutput)
async def fashion_detection(im: UploadFile = File(...)):

    if im.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        raise HTTPException(status_code=415, detail="Unsupported Type Image")

    image = Image.open(BytesIO(im.file.read()))
    image = np.array(image)

    final_output = fashion_detector(image)
    return {
        "time_elapsed": final_output["time_elapsed"],
        "boxes": final_output["boxes"],
        "scores": final_output["scores"],
        "classes": final_output["classes"]
    }