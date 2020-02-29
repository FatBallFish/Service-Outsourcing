import logging
import os, json
from typing import Dict, Generator
import platform, sys
import numpy as np
import time

from Hotel import settings

from extral_apps.m_arcface.arcface import ArcFace, timer
from extral_apps.m_arcface.arcface import FaceInfo as ArcFaceInfo
from extral_apps.m_arcface.module.face_process import FaceProcess, FaceInfo
from extral_apps.m_arcface.module.image_source import LocalImage, ImageSource, LocalCamera
from extral_apps.m_arcface.module.text_renderer import put_text

_logger = logging.getLogger(__name__)


def _draw_face_info(image: np.ndarray, face_info: FaceInfo) -> dict:
    """
    将人脸的信息绘制到屏幕上
    :param face_info: 人脸信息
    :return: None
    """
    # 绘制人脸位置
    rect = face_info.rect
    # print(face_info.gender, type(face_info.gender))
    json_dict = {
        "face_id":face_info.arc_face_info.face_id,
        "ID": face_info.ID,
        "age": face_info.age,
        "threshold": float("{:.2f}".format(face_info.threshold)),
        "gender": face_info.get_gender(),
        "liveness": True if face_info.liveness else False,
        "top_left": rect.top_left,
        "top_right": rect.top_right,
        "bottom_left": rect.bottom_left,
        "bottom_right": rect.bottom_right,
    }
    # print(json_dict)
    return json_dict
    # color = (255, 0, 0) if face_info.name else (0, 0, 255)
    # cv.rectangle(image, rect.top_left, rect.bottom_right, color, 2)
    # # 绘制人的其它信息
    # x, y = rect.top_middle
    # put_text(image, "%s" % face_info, bottom_middle=(x, y - 2))
    # # 绘制人脸 ID
    # info = "%d" % face_info.arc_face_info.face_id
    # x, y = rect.top_left
    # put_text(image, info, left_top=(x + 2, y + 2))


@timer(output=_logger.info)
def _run_1_n(image_source: ImageSource, face_process: FaceProcess) -> None:
    """
    1:n 的整个处理的逻辑
    :image_source: 识别图像的源头
    :face_process: 用来对人脸信息进行提取
    :return: None
    """
    with ArcFace(ArcFace.VIDEO_MODE) as arcface:

        cur_face_info = None  # 当前的人脸

        # frame_rate_statistics = _frame_rate_statistics_generator()

        while True:
            # 获取视频帧
            image = image_source.read()

            # 检测人脸
            faces_pos = arcface.detect_faces(image)

            if len(faces_pos) == 0:
                # 图片中没有人脸
                cur_face_info = None
            else:
                # 使用曼哈顿距离作为依据找出最靠近中心的人脸
                center_y, center_x = image.shape[:2]
                center_y, center_x = center_y // 2, center_x // 2
                center_face_index = -1
                min_center_distance = center_x + center_y + 4
                cur_face_index = -1
                for i, pos in enumerate(faces_pos):
                    if cur_face_info is not None and pos.face_id == cur_face_info.arc_face_info.face_id:
                        cur_face_index = i
                        break
                    x, y = pos.rect.center
                    if x + y < min_center_distance:
                        center_face_index = i
                        min_center_distance = x + y
                if cur_face_index != -1:
                    # 上一轮的人脸依然在，更新位置信息
                    cur_face_info.arc_face_info = faces_pos[cur_face_index]
                else:
                    # 上一轮的人脸不在了，选择当前所有人脸的最大人脸
                    cur_face_info = FaceInfo(faces_pos[center_face_index])

            if cur_face_info is not None:
                # 异步更新人脸的信息
                if cur_face_info.need_update():
                    face_process.async_update_face_info(image, cur_face_info)

                # 绘制人脸信息
                _draw_face_info(image, cur_face_info)

                # 绘制中心点
                # put_text(image, "x", bottom_middle=(center_x, center_y))

            # 显示到界面上
            # if _show_image(image):
            #     break

            # 统计帧率
            # fps = next(frame_rate_statistics)
            # if fps:
            #     _logger.info("FPS: %.2f" % fps)

            # if all(map(lambda x: x.complete(), faces_info.values())):
            #     break


@timer(output=_logger.info)
def _run_m_n(image_source: ImageSource, face_process: FaceProcess, type: str = "name") -> dict:
    """
    m:n 的整个处理的逻辑
    :image_source: 识别图像的源头
    :face_process: 用来对人脸信息进行提取
    :return: None
    """
    time1 = time.time()
    with ArcFace(ArcFace.VIDEO_MODE) as arcface:

        faces_info: Dict[int, FaceInfo] = {}

        # frame_rate_statistics = _frame_rate_statistics_generator()
        # 统计视频帧率

        # while True:
        # 获取视频帧
        image = image_source.read()

        face_list = []  # 统计识别到的人脸数
        check_num = 0  # 检查次数，暂定为10次
        while check_num <= 10:
            # 检测人脸
            faces_pos: Dict[int, ArcFaceInfo] = {}
            for face_pos in arcface.detect_faces(image):
                faces_pos[face_pos.face_id] = face_pos

            # 删除过期 id, 添加新的 id
            cur_faces_id = faces_pos.keys()
            last_faces_id = faces_info.keys()
            for face_id in last_faces_id - cur_faces_id:
                faces_info[face_id].cancel()  # 如果有操作在进行，这将取消操作
                faces_info.pop(face_id)
            for face_id in cur_faces_id:
                if face_id in faces_info:
                    # 人脸已经存在，只需更新位置就好了
                    faces_info[face_id].arc_face_info = faces_pos[face_id]
                else:
                    faces_info[face_id] = FaceInfo(faces_pos[face_id])

            # 更新人脸的信息
            # for face_info in faces_info:
            #     face_process.async_update_face_info(image, face_info)
            opt_face_info = None
            for face_info in filter(lambda x: x.need_update(), faces_info.values()):
                if opt_face_info is None or opt_face_info.rect.size < face_info.rect.size:
                    opt_face_info = face_info

            if opt_face_info is not None:
                face_process.async_update_face_info(image, opt_face_info)

                # cv.imshow("temp", opt_face_info.image)
                # print(opt_face_info.image.shape)
            # time.sleep(1)
            # 绘制人脸信息
            # flag = False
            num = len(faces_info)  # 人脸数，可能会变
            for face_info in faces_info.values():
                while face_info._busy():
                    continue
                if face_list.count(face_info) == 0:
                    face_list.append(face_info)
                if len(face_list) == num:
                    pass
                # json_dict = _draw_face_info(image, face_info)
                # return json_dict
            check_num += 1
        time2 = time.time()
        _logger.debug("人脸检索用时：", time2 - time1)
        data_list = []
        for face in face_list:
            list_json = _draw_face_info(image, face)
            data_list.append(list_json)
        data_json = {"num": len(data_list), "list": data_list}
        return data_json


@timer(output=_logger.info)
def addFace(path: str, name: str, ID: str):
    face_process.add_features(path_name=path, ID=ID)
    face_process.dump_features_append(name, ID)


@timer(output=_logger.info)
def checkFace(path: str, db: int = -1, user=None) -> dict:
    reload_features(db=db, user=user)
    image_source = LocalImage(path=path)
    json_dict = {}
    # run = _run_m_n
    with image_source:
        json_dict = run(image_source, face_process)
    return json_dict


@timer(output=_logger.info)
def reload_features(db: int = -1, user=None):
    face_process.reload_features(db=db, user=user)


@timer(output=_logger.info)
def Initialize(single: bool = False):
    logging.basicConfig(
        format="[%(levelname)s] %(message)s [%(threadName)s:%(name)s:%(lineno)s]",
        level=logging.INFO
    )
    ArcFace.APP_ID = settings.ARCFACE_APPID.encode("utf8")
    system = platform.system()
    bits = "32" if platform.architecture()[0] == "32bit" else "64"
    _logger.info("System:{} {}bit".format(system, bits))
    if system == "Windows":
        if bits == "64":
            ArcFace.SDK_KEY = settings.ARCFACE_KEY_Win64.encode("utf8")
        elif bits == "32":
            ArcFace.SDK_KEY = settings.ARCFACE_KEY_Win32.encode("utf8")
    elif system == "Linux":
        if bits == "64":
            ArcFace.SDK_KEY = settings.ARCFACE_KEY_Linux64.encode("utf8")
        elif bits == "32":
            _logger.error("Unsupported System bits")
            sys.exit()
    else:
        _logger.error("Unknown System, can't choose sdk lib")
        sys.exit()
    # pic_path = "./database"
    # cache_path = './cache/cache.txt'

    global face_process
    face_process = FaceProcess()
    face_process.load_features()
    # else:
    # face_process.add_features(pic_path)
    # face_process.dump_features(cache_path)

    # image_source = LocalImage(os.path.join(settings.BASE_DIR,"media","tmp","19.jpeg"))

    global run
    run = _run_1_n if single else _run_m_n

    # with image_source:
    #     run(image_source, face_process)

    print(settings.ARCFACE_APPID)
    # print(settings.ARCFACE_KEY)


if __name__ == '__main__':
    Initialize()
