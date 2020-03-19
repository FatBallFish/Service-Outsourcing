# -*- coding:utf-8 -*-
import cv2
import time

import argparse
import numpy as np
from PIL import Image
from extral_apps.m_facemask.utils.anchor_generator import generate_anchors
from extral_apps.m_facemask.utils.anchor_decode import decode_bbox
from extral_apps.m_facemask.utils.nms import single_class_non_max_suppression
from extral_apps.m_facemask.load_model.pytorch_loader import load_pytorch_model, pytorch_inference

import logging, os
from pathlib import Path

log_img = logging.getLogger("FaceMask")


def Initialize(main_path: str):
    """
ImgCaptcha 模块初始化，此函数应在所有函数之前调用
    :param cfg_path: 配置文件地址。
    :param main_path: 程序主目录地址。
    """
    global Main_filepath
    Main_filepath = main_path
    # print(Main_filepath)

    global model, feature_map_sizes, anchor_sizes, anchor_ratios, anchors, anchors_exp, id2class
    model_path = os.path.join(Main_filepath, "extral_apps", "m_facemask", "models", "face_mask_detection.pth")
    # print(model_path)
    model = load_pytorch_model(model_path)

    # anchor configuration
    feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
    anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
    anchor_ratios = [[1, 0.62, 0.42]] * 5

    # generate anchors
    anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

    # for inference , the batch size is 1, the model output shape is [1, N, 4],
    # so we expand dim for anchors to [1, anchor_num, 4]
    anchors_exp = np.expand_dims(anchors, axis=0)

    id2class = {0: 'Mask', 1: 'NoMask'}

    log_img.info("Module FaceMask loaded")
    print("[FaceMask] Module FaceMask loaded")


class FaceMask:
    def __init__(self, path: str = "", conf_thresh: float = 0.5, iou_thresh: float = 0.4,
                 target_shape: tuple = (260, 260),
                 draw_result: bool = False, show_result: bool = False):
        """
        Main function of detection inference

        :param image: 3D numpy array of image
        :param conf_thresh: the min threshold of classification probabity.
        :param iou_thresh: the IOU threshold of NMS
        :param target_shape: the model input size.
        :param draw_result: whether to daw bounding box to the image.
        :param show_result: whether to display the image.
        :return:
        """
        if path:
            self.path = path
            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.image = img
        else:
            self.image = None
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.target_shape = target_shape
        self.draw_result = draw_result
        self.show_result = show_result

    def setImgPath(self, path: str):
        self.path = path
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image = img

    def _dojob(self) -> list:
        """
        进行人脸口罩检测

        :return: 返回图像中的人脸口罩信息数据
        """
        # image = np.copy(image)
        output_info = []
        height, width, _ = self.image.shape
        image_resized = cv2.resize(self.image, self.target_shape)
        image_np = image_resized / 255.0  # 归一化到0~1
        image_exp = np.expand_dims(image_np, axis=0)

        image_transposed = image_exp.transpose((0, 3, 1, 2))

        y_bboxes_output, y_cls_output = pytorch_inference(model, image_transposed)
        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = decode_bbox(anchors_exp, y_bboxes_output)[0]
        y_cls = y_cls_output[0]
        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                     bbox_max_scores,
                                                     conf_thresh=self.conf_thresh,
                                                     iou_thresh=self.iou_thresh,
                                                     )

        for idx in keep_idxs:
            conf = float(bbox_max_scores[idx])
            class_id = bbox_max_score_classes[idx]
            bbox = y_bboxes[idx]
            # clip the coordinate, avoid the value exceed the image boundary.
            xmin = max(0, int(bbox[0] * width))
            ymin = max(0, int(bbox[1] * height))
            xmax = min(int(bbox[2] * width), width)
            ymax = min(int(bbox[3] * height), height)

            if self.draw_result:
                if class_id == 0:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
                cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), color, 2)
                cv2.putText(self.image, "%s: %.2f" % (id2class[class_id], conf), (xmin + 2, ymin - 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
            output_info.append([class_id, conf, xmin, ymin, xmax, ymax])

        if self.show_result:
            Image.fromarray(self.image).show()
        return output_info

    def faceMaskCheck(self, img_path: str = "") -> list:
        if not img_path:
            if not self.path:
                return []
        else:
            self.setImgPath(path=img_path)
        face_list = self._dojob()
        num = len(face_list)
        data_list = []
        for face in face_list:
            # "threshold": face[1]
            # 上面字段已去除，暂时不知道干什么用
            face_dict = {"class_id": face[0], "top_left": (face[2], face[3]),
                         "top_right": (face[4], face[3]), "bottom_left": (face[2], face[5]),
                         "bottom_right": (face[4], face[5]),
                         "center": ((face[2] + face[4]) / 2, (face[3] + face[5]) / 2)}
            data_list.append(face_dict)
        print(data_list)
        return data_list


if __name__ == '__main__':
    faceMask = FaceMask("./test/1.jpg")
    data_list = faceMask.faceMaskCheck()
