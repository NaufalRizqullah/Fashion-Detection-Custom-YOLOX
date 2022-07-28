from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

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

@yolox_router.post("/detectv2")
async def fashion_detection_v2(im: UploadFile = File(...)):

    if im.filename.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
        raise HTTPException(status_code=415, detail="Unsupported Type Image")

    image = Image.open(BytesIO(im.file.read()))
    image = np.array(image)

    final_output = fashion_detector(np.array(image), True)

    # Source: https://www.pythonfixing.com/2022/04/fixed-render-numpy-array-in-fastapi.html
    
    success, img = cv2.imencode('.png', final_output)

    headers = {'Content-Disposition': f'inline; filename="{im.filename}"'}
    return Response(img.tobytes(), headers=headers, media_type='image/png')


@yolox_router.post("/detect/streamlit/demo")
async def fashion_detection_v2(im: UploadFile = File(...)):

    image = Image.open(BytesIO(im.file.read()))

    final_output = fashion_detector(np.array(image), True)

    success, img = cv2.imencode('.png', final_output)

    headers = {'Content-Disposition': f'inline; filename="{im.filename}"'}
    return Response(img.tobytes(), headers=headers, media_type='image/png')