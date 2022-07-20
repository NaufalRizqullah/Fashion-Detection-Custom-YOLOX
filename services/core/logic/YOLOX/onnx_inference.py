#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import argparse
import os

import cv2
import numpy as np

import onnxruntime

from services.core.logic.YOLOX.yolox.data.data_augment import preproc as preprocess
from services.core.logic.YOLOX.yolox.data.datasets import COCO_CLASSES
from services.core.logic.YOLOX.yolox.utils import mkdir, multiclass_nms, demo_postprocess, vis
from services.core.logic.YOLOX.yolox.data.datasets import COCO_CLASSES

def fashion_detector(images):
    
    PATH_ONNX_MODEL = "services/core/model/fashion_best_yolox_s.onnx"
    SCORE_THRESHOLD = 0.1

    input_shape = (640, 640)
    origin_img = images
    
    # change BGR to RGB layer images
    origin_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)

    img, ratio = preprocess(origin_img, input_shape)

    session = onnxruntime.InferenceSession(PATH_ONNX_MODEL)

    ort_inputs = {session.get_inputs()[0].name: img[None, :, :, :]}
    output = session.run(None, ort_inputs)
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

    cv2.imwrite("services/core/output/output.jpg", origin_img)

    classes_list = final_cls_inds.tolist()
    classes_list = [COCO_CLASSES[int(idx)] for idx in classes_list]

    return {
        "boxes": final_boxes.tolist(),
        "scores": final_scores.tolist(),
        "classes": classes_list
    }
