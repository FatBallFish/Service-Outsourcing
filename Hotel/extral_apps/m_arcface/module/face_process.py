# -*- encoding: utf-8 -*-

"""
@File    : face_process.py
@Time    : 2019/10/18 14:24

人脸特征提取，人脸属性检测

"""
import base64
import logging
import os
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Dict, Tuple, Generator, Optional
from datetime import datetime
import numpy as np

from extral_apps.m_arcface.arcface import ArcFace, image_regularization, Rect
from extral_apps.m_arcface.arcface import FaceInfo as ArcFaceInfo
from extral_apps.m_arcface.arcface import Gender
from extral_apps.m_arcface.module.image_source import get_regular_file, read_image

from Hotel import settings
from extral_apps import MD5
from apps.users.models import Users
from apps.faces.models import FaceData, FaceGroup
from apps.passengerFlow.models import PassengerFace

from django.db.models import Q

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class FaceInfo:
    """
    一些人脸的信息
    """

    def __init__(self, arc_face_info: ArcFaceInfo):
        self.stop_flags = [True, True]

        self.arc_face_info: ArcFaceInfo = arc_face_info
        self._image = np.array([])

        self.ID = ""
        self.threshold: float = 0.0

        self.liveness = None
        self.age = None
        self.gender = None
        self.updated_flags = [False, False]

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image: np.ndarray):
        self._image = image.copy()
        # self._image = capture_image(image, self.rect)

    @property
    def rect(self):
        return self.arc_face_info.rect

    def need_update(self) -> bool:
        """
        :return:
        """
        # id = self.arc_face_info.face_id
        # busy = self._busy()
        # fs = self.futures
        # flags = fs[0].done() if fs[0] is not None else None, fs[1].done() if fs[1] is not None else None
        # _logger.debug("%s busy %s %s" % (self.arc_face_info.face_id, self._busy(), flags))
        return not any((
            self.rect.size < (50, 50),
            self._busy(),
            self.complete(),
        ))

    def cancel(self) -> None:
        """
        取消获取当前的信息
        :return: None
        """
        self.stop_flags[0] = True
        self.stop_flags[1] = True

    def complete(self) -> bool:
        """
        判断人脸所有可显示的信息是否都存在了
        :return: 所有信息都存在返回 True，否则返回 False
        """
        return all((
            bool(self.ID),
            self.liveness is not None,
            self.age is not None,
            self.gender is not None,
        ))

    def _busy(self) -> bool:
        """
        判断是否在更新信息
        :return: 所有线程都在工作返回 True, 否则返回 False
        """
        return all(map(lambda x: not x, self.stop_flags))

    def __str__(self):
        to_str = FaceInfo._to_str
        return "%s,%s,%s,%s,%s" % (
            self.ID,
            to_str(self.threshold, bool(self.ID), "%.2f" % self.threshold, ""),
            to_str(self.liveness, self.liveness, "真", "假"),
            to_str(self.gender, self.gender == Gender.Male, "男", "女"),
            to_str(self.age, True, self.age, self.age)
        )

    def get_gender(self) -> str:
        """
        获取用户性别，自建函数
        """
        if self.gender == Gender.Female:
            return "female"
        elif self.gender == Gender.Male:
            return "male"
        else:
            return ""

    @staticmethod
    def _to_str(v, condition, v1, v2):
        if v is None:
            return ""
        else:
            return v1 if condition else v2


class FaceProcess:
    """
    使用 ArcFace 进行特征提取，人脸属性检测
    """

    def __init__(self):
        # 这里假设在外面已经配置好了 ArcFace 的 APP_ID 和 SDK_KEY
        self._arcface = ArcFace(ArcFace.IMAGE_MODE)
        self._features: Dict[str, bytes] = {}  # 人脸数据库

        # max_workers 必须为 1，因为 SDK 对并行的支持有限
        self._executors = (ThreadPoolExecutor(max_workers=1), ThreadPoolExecutor(max_workers=1))

    def async_update_face_info(self, image: np.ndarray, face_info: FaceInfo) -> None:
        """
        更新单个人脸的信息。
        :param image: 包含人脸的图片
        :param face_info: 人脸信息
        :return: None
        """
        _logger.info("人脸 %d: 开始获取信息" % face_info.arc_face_info.face_id)

        face_info.image = image

        if face_info.stop_flags[0]:
            _logger.debug("人脸 %d: 获取身份ID" % face_info.arc_face_info.face_id)
            face_info.stop_flags[0] = False
            future: Future = self._executors[0].submit(self._update_name, face_info)
            future.add_done_callback(lambda x: FaceProcess._update_name_done(face_info, x))

        if face_info.stop_flags[1]:
            _logger.debug("人脸 %d: 活体检测、性别、年龄" % face_info.arc_face_info.face_id)
            face_info.stop_flags[1] = False
            future: Future = self._executors[1].submit(self._update_other, face_info)
            future.add_done_callback(lambda x: FaceProcess._update_other_done(face_info, x))

    def _update_other(self, face_info: FaceInfo) -> Tuple[Optional[bool], Optional[int], Optional[Gender]]:
        """
        更新其它信息，比如 活体、性别、年龄
        :param face_info:
        :return: 识别成功的信息数
        """

        image, orient = face_info.image, face_info.arc_face_info.orient
        face_id = face_info.arc_face_info.face_id
        arc_face_info = face_info.arc_face_info
        # arc_face_info = ArcFace.FaceInfo(Rect(0, 0, image.shape[1], image.shape[0]), orient)

        # cv.imshow("other", image)
        # cv.moveWindow("other", 400, 400)
        # cv.waitKey(1)
        if face_info.stop_flags[1]:
            return None, None, None
        if not self._arcface.process_face(
                image,
                arc_face_info,
                ArcFace.LIVENESS | ArcFace.AGE | ArcFace.GENDER
        ):
            _logger.debug("人脸 %d: 处理失败" % face_id)
            return None, None, None
        arcface = self._arcface
        return arcface.is_liveness(), arcface.get_age(), arcface.get_gender()

    @staticmethod
    def _update_other_done(face_info: FaceInfo, future: Future):
        face_info.liveness, face_info.age, face_info.gender = future.result()
        face_info.stop_flags[1] = True
        face_info.updated_flags[1] = True

    def _update_name(self, face_info: FaceInfo) -> Tuple[str, float]:
        """
        提取特征，再在人脸数据库查找符合条件的特征
        :return: 成功返回 True，失败返回 False
        """

        image, orient = face_info.image, face_info.arc_face_info.orient
        face_id = face_info.arc_face_info.face_id
        # (x1, y1), (x2, y2) = face_info.rect.top_left, face_info.rect.bottom_right
        # cv.imshow("name", image[y1:y2, x1:x2])
        # cv.moveWindow("name", 200, 200)
        # cv.waitKey(1)
        arc_face_info = face_info.arc_face_info
        # arc_face_info = ArcFace.FaceInfo(Rect(0, 0, image.shape[1], image.shape[0]), orient)
        feature = self._arcface.extract_feature(image, arc_face_info)
        if not feature:
            _logger.debug("人脸 %d: 提取特征值失败(%s)" % (face_id, "%dx%d" % face_info.rect.size))
            return "", 0.0

        if face_info.stop_flags[0]:
            # 被取消了
            _logger.debug("人脸 %d: 取消识别人脸" % face_id)
            return "", 0.0

        max_threshold = 0.0
        opt_ID = ""
        for ID, feature_ in self._features.items():
            # todo 修改name为ID
            try:
                threshold = self._arcface.compare_feature(feature, feature_)
            except Exception as e:
                _logger.warning(e)
                return "", 0.0
            if max_threshold < threshold:
                max_threshold = threshold
                opt_ID = ID
        if 0.8 < max_threshold:
            _logger.debug("人脸 %d: 识别成功，与 %s 相似度 %.2f" % (face_id, opt_ID, max_threshold))
            return opt_ID, max_threshold
        _logger.debug("人脸 %d: 识别失败，与最像的 %s 的相似度 %.2f" % (face_id, opt_ID, max_threshold))
        return "", 0.0

    @staticmethod
    def _update_name_done(face_info: FaceInfo, future: Future):
        face_info.ID, face_info.threshold = future.result()
        face_info.stop_flags[0] = True
        face_info.updated_flags[0] = True

    def dump_features(self) -> int:
        """
        将已有的人脸数据库保存到文件
        :filename: 保存人脸数据库的文件名
        :return: 保存的人脸数
        """
        for ID, feature in self._features.items():
            facedata = FaceData()
            facedata.ID = ID
            facedata.sign = base64.b64encode(feature).decode()
            # facedata.pic = settings.COS_ROOTURL + "facedata/" + MD5.md5(name) + ".jpg"
            facedata.pic = "faces_data/" + MD5.md5(ID) + ".face"
            facedata.update_time = datetime.now()
            facedata.save()
        return len(self._features)

    def dump_features_append(self, name: str, ID: str) -> int:
        """
        将已有的人脸数据库追加保存到文件
        :filename: 保存人脸数据库的文件名
        :return: 保存的人脸数
        """
        # TODO 将所有的name改成ID，ID改成name
        for key in self._features.keys():
            if key == ID:
                break
        else:
            _logger.error("{ID}的人脸信息不存在！".format(ID=ID))
            return 0
        # with open(filename, "a", encoding="utf-8") as file:
        #     feature = self._features[name]
        #     file.write(name)
        #     file.write(":")
        #     file.write(base64.b64encode(feature).decode())
        #     file.write("\n")
        feature = self._features[ID]
        base_data: str = base64.b64encode(feature).decode()
        # pic = settings.COS_ROOTURL + "facedata/" + MD5.md5(name) + ".jpg"
        pic = "faces_data/" + MD5.md5(ID) + ".face"

        defaults = {"sign": base_data, "pic": pic, "update_time": datetime.now()}
        FaceData.objects.update_or_create(defaults=defaults, ID=ID, name=name)
        return len(self._features)

    def load_features(self, db: int = -1) -> int:
        """
        从先前保存的人脸数据库加载数据
        :param filename: 保存人脸数据库的文件名
        :return: 加载的人脸数
        """
        count = 0
        # with open(filename, encoding="utf-8") as file:
        #     line = file.readline()
        #     while line:
        #         name, feature = line.split(":")
        #         feature = base64.b64decode(feature)
        #         self._features[name] = feature
        #         count += 1
        #         line = file.readline()
        face_list = []
        if db == -1:
            face_list = FaceData.objects.all()
        else:
            try:
                face_group = FaceGroup.objects.get(id=db)
                face_list = FaceData.objects.filter(faces_group=face_group)
            except Exception as e:
                _logger.info("人员库id[{}] 对应的人员库不存在".format(db))
        for face_data in face_list:
            ID = face_data.ID
            name = face_data.name
            feature = base64.b64decode(face_data.sign)
            # print("[{}]:{}".format(name, feature))
            self._features[ID] = feature
            count += 1
        _logger.info("从 \"数据库\" 中加载了 %d 个特征值" % (count))
        return count

    def reload_features(self, db: int = -1, user: Users = None) -> int:
        """
        从先前保存的人脸数据库加载数据，db和user模式二选一

        :param db: 人员库id
        :param user: 用户信息
        :return: 加载的人脸数
        """
        # todo 更改name为ID
        count = 0
        face_list = []
        face_group = None
        self._features.clear()
        if user:
            face_data = user.face
            ID = face_data.ID
            name = face_data.name
            feature = base64.b64decode(face_data.sign)
            self._features[ID] = feature
            count += 1
        else:
            if db == -1:
                face_list = FaceData.objects.all()
            else:
                try:
                    face_group = FaceGroup.objects.get(id=db)
                    face_list = FaceData.objects.filter(faces_group=face_group)
                except Exception as e:
                    _logger.info("人员库id[{}] 对应的人员库不存在".format(db))
            for face_data in face_list:
                ID = face_data.ID
                name = face_data.name
                feature = base64.b64decode(face_data.sign)
                self._features[ID] = feature
                count += 1
            if face_group:
                _logger.info("从 人员库\"%s\" 中重加载了 %d 个特征值" % (face_group.name, count))
            else:
                _logger.info("从 \"全部人员库\" 中重加载了 %d 个特征值" % (count))
        return count

    def load_passenger_features(self):
        """
        重载客流分析数据库

        :return:
        """
        count = 0
        face_list = []
        self._features.clear()
        face_list = PassengerFace.objects.exclude(sign=None)
        for face_data in face_list:
            ID = face_data.ID
            name = face_data.name
            feature = base64.b64decode(face_data.sign)
            self._features[ID] = feature
            count += 1
        _logger.info("从 客流人员库 中重加载了 %d 个特征值" % (count))
        return count

    def add_features(self, path_name: str, ID: str) -> int:
        """
        将本地文件夹或者本地图片所有用户的特征值添加人脸数据库
        :param path_name: 文件夹名或者图片路径名
        :param ID: 人脸身份ID
        :return: 成功添加的人脸数
        """
        features = self._load_all_features(path_name, ID)
        print("features:", features)
        self._features.update(features)
        return len(features)

    def _load_all_features(self, path_name: str, ID: str) -> Dict[str, bytes]:
        """
        从本地文件夹或者本地图片加载所有用户的特征值
        如果从图片中加载，则用户名是数字 ID（类型依然是字符串）
        如果指定文件夹则遍历所有合法的图片，用户名是 <图片文件名-数字 ID>，如果只有一张图片则没有数字 ID
        :type path_name: 文件夹名或者图片路径名
        :return: 包含所有特征值的 map<姓名, 特征值>
        """
        # TODO 更改name为ID
        if not os.path.exists(path_name):
            raise ValueError("不存在的路径 \"%s\"" % path_name)
        _logger.info("从 \"%s\" 中加载所有的人脸特征值" % path_name)

        total_faces_number = 0
        files_number = 0
        features = {}
        count = 0
        for filename in get_regular_file(path_name):
            count += 1
            print("\r已经加载了 %d 个文件" % count, end="")
            files_number += 1
            # TODO: name 类型的问题
            # name: str = os.path.basename(filename)
            # name: str = name.split(".")[0]
            faces_number, features_ = self._load_features_from_image(ID, read_image(filename))
            total_faces_number += faces_number
            if faces_number == 0:
                _logger.warning("\n\"%s\" 中没有发现人脸" % filename)
            features.update(features_)
        print()
        _logger.info("在 %d 个文件中，一共发现 %d 张人脸，其中 %d 张清晰有效" % (files_number, total_faces_number, len(features)))

        return features

    def _load_features_from_image(self, ID: str, image: np.ndarray) -> Tuple[int, Dict[str, bytes]]:
        """
        从图片中加载特征值
        如果 name 为空，名字按数字编号来
        否则，如果只有一个特征，使用 name 的值作为名称
        否则，使用 <name-数字编号> 来命名
        :param ID: 图片中人的身份id
        :param image: 需要提取特征的图片
        :return: 总的人脸数（包含不清晰无法提取特征值的人脸）, Dict[姓名, 特征值]
        """
        if image.size == 0:
            return 0, {}
        image = image_regularization(image)
        # 检测人脸位置
        faces = self._arcface.detect_faces(image)
        # 提取所有人脸特征
        features = map(lambda x: self._arcface.extract_feature(image, x), faces)
        # 删除空的人脸特征
        features = list(filter(lambda feature: feature, features))

        # 按一定规则生成名字
        def get_name() -> Generator[str, None, None]:
            for i in range(len(features)):
                if len(ID) == 0:
                    yield "%d" % i
                if len(features) == 1:
                    yield ID
                else:
                    yield "%s-%d" % (ID, i)

        # 将所有特征和名字拼接起来
        def assemble() -> Dict[str, bytes]:
            res = {}
            for name_, feature in zip(get_name(), features):
                res[name_] = feature
            return res

        return len(faces), assemble()

    def release(self):
        for executor in self._executors:
            executor.shutdown()
        self._arcface.release()

    def face_compare(self, feature: bytes) -> tuple:
        """
        仅通过人脸特征进行人脸查找匹配

        :param feature: 人脸特征数据
        :return: 返回(opt_ID,max_threshold)元组，其中max_threshold仅在0.8以上才会正常返回，否则皆为0.0
        """
        self.reload_features(-1)
        max_threshold = 0.0
        opt_ID = ""
        for ID, feature_ in self._features.items():
            threshold = self._arcface.compare_feature(feature, feature_)
            if max_threshold < threshold:
                max_threshold = threshold
                opt_ID = ID
        if 0.8 < max_threshold:
            _logger.debug("识别成功，与 %s 相似度 %.2f" % (opt_ID, max_threshold))
            return opt_ID, max_threshold
        _logger.debug("识别失败，与最像的 %s 的相似度 %.2f" % (opt_ID, max_threshold))
        # face_info.updated_flags[0] = True
        return "", 0.0

    def face_compare_only(self, feature1: bytes, feature2: bytes) -> float:
        max_threshold = 0.0
        opt_ID = ""
        max_threshold = self._arcface.compare_feature(feature1, feature2)

        if max_threshold > 0.8:
            _logger.debug("识别成功，相似度 %.2f" % (max_threshold))
            return max_threshold
        return 0.0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


if __name__ == "__main__":
    arc = ArcFaceInfo(Rect(0, 0, 0, 0), 0)
    face = FaceInfo(arc)

    print("%s" % face)
