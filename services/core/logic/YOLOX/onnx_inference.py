#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import time

import cv2
import numpy as np

from services.core.logic.YOLOX.yolox.data.data_augment import preproc as preprocess
from services.core.logic.YOLOX.yolox.data.datasets import COCO_CLASSES
from services.core.logic.YOLOX.yolox.utils import mkdir, multiclass_nms, demo_postprocess, vis
from services.core.logic.YOLOX.yolox.data.datasets import COCO_CLASSES

import services.main as s

def fashion_detector(images, return_image: bool = False):

    SCORE_THRESHOLD = 0.1

    time_init = time.time()

    input_shape = (640, 640)
    origin_img = images
    
    # change BGR to RGB layer images
    origin_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)

    img, ratio = preprocess(origin_img, input_shape)

    ort_inputs = {s.session.get_inputs()[0].name: img[None, :, :, :]}
    output = s.session.run(None, ort_inputs)
    predictions = demo_postprocess(output[0], input_shape, p6=False)[0]

    boxes = predictions[:, :4]
    scores = predictions[:, 4:5] * predictions[:, 5:]

    boxes_xyxy = np.ones_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2]/2.
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3]/2.
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2]/2.
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3]/2.
    boxes_xyxy /= ratio
    dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=SCORE_THRESHOLD)
    if dets is not None:
        final_boxes, final_scores, final_cls_inds = dets[:, :4], dets[:, 4], dets[:, 5]
        origin_img = vis(origin_img, final_boxes, final_scores, final_cls_inds,
                         conf=SCORE_THRESHOLD, class_names=COCO_CLASSES)

    
    time_elapsed = time.time() - time_init

    print(f"Time -------------- {time_elapsed}")
    # Render Output
    # cv2.imwrite("services/core/output/output.jpg", origin_img)

    if (return_image):
        return origin_img

    classes_list = final_cls_inds.tolist()
    classes_list = [COCO_CLASSES[int(idx)] for idx in classes_list]

    return {
        "time_elapsed": str(time_elapsed),
        "boxes": final_boxes.tolist(),
        "scores": final_scores.tolist(),
        "classes": classes_list
    }
