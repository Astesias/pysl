# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import os
import time
import sys
sys.path.append('PaddleSeg') #配置环境变量
import json
import yaml
from functools import reduce
import multiprocessing

from PIL import Image
import cv2
import numpy as np
import paddle
import paddleseg.transforms as T
from paddle.inference import Config
from paddle.inference import create_predictor
from paddleseg.cvlibs import manager

from multiprocessing.dummy import Pool as ThreadPool

class SegDeployConfig:
    """
    desc: 加载PaddleSeg套件训练导出的模型接口类
    init Args:
        path: str, 模型文件目录
    """
    def __init__(self, path):
        with codecs.open(path, 'r', 'utf-8') as file:
            self.dic = yaml.load(file, Loader=yaml.FullLoader)

        self._transforms = self._load_transforms(
            self.dic['Deploy']['transforms'])
        self._dir = os.path.dirname(path)

    @property
    def transforms(self):
        """
        desc: 加载yml中的预处理
        """
        return self._transforms

    @property
    def model(self):
        """
        desc: 加载yml中的model文件的路径
        """
        return os.path.join(self._dir, self.dic['Deploy']['model'])

    @property
    def params(self):
        """
        desc: 加载yml中的params文件的路径
        """
        return os.path.join(self._dir, self.dic['Deploy']['params'])

    def _load_transforms(self, t_list):
        """
        desc: 加载yml中的预处理，并实例获取可用的预处理接口
        """
        com = manager.TRANSFORMS
        transforms = []
        for t in t_list:
            ctype = t.pop('type')
            transforms.append(com[ctype](**t))

        return T.Compose(transforms)

def get_test_images(infer_file):
    """
    desc: 获取txt文件中的测试文件路径
    Args:
        infer_file: 包含预测文件路径的txt文件
    Return:
        images: 解析好的测试文件路径列表
    """
    with open(infer_file, 'r') as f:
        dirs = f.readlines()
    images = []
    for dir in dirs:
        # print(eval(repr(dir.replace('\n',''))).replace('\\', '/'))
        images.append(eval(repr(dir.replace('\n',''))).replace('\\', '/'))
    assert len(images) > 0, "no image found in {}".format(infer_file)
    return images

class Segmentor:
    """
    desc: 分割推理类
    init Args:
        seg_model_path: 分割模型的目录
    """
    def __init__(self, seg_model_path):
        self.cfg = SegDeployConfig(os.path.join(seg_model_path, 'deploy.yaml'))
        pred_cfg = Config(self.cfg.model, self.cfg.params)
        pred_cfg.disable_glog_info()
        pred_cfg.enable_use_gpu(2000, 0)
        self.predictor = create_predictor(pred_cfg)

    def preprocess(self, img):
        """
        desc: 对输入图像数据执行图像预处理
        Args:
            img: str|numpy.ndarray, 输入原始图像或者路径
        Return:
            self.cfg.transforms(img)[0]: 处理后的图像数据
        """
        return self.cfg.transforms(img)[0]

    def run(self, im):
        """
        desc: 执行推理
        Args:
            im: numpy.ndarray(-1, 3, H, W), 经过预处理的图像数据，可以是批量的
        Return:
            results: numpy.ndarray(-1, H, W), 推理结果，可以是批量的
        """
        input_names = self.predictor.get_input_names()
        input_handle = self.predictor.get_input_handle(input_names[0])
        input_handle.reshape(im.shape)
        input_handle.copy_from_cpu(im)

        self.predictor.run()
        output_names = self.predictor.get_output_names()
        output_handle = self.predictor.get_output_handle(output_names[0])
        results = output_handle.copy_to_cpu()
        return results


def normalize(im, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]):
    """normalize copy from paddleSeg
    desc: 图像归一化
    Args:
        im: numpy.ndarray, 输入图像数据
        mean: list, 每个通道的归一化均值数据
        std: list, 每个通道的归一化方差数据
    Return
        im: numpy.ndarray, 归一化处理好的图像数据
    """
    im = im.astype(np.float32, copy=False) / 255.0
    im -= mean
    im /= std
    return im


def resize(im, target_size=480, interp=cv2.INTER_LINEAR):
    """resize copy from paddleSeg
    desc: 图像缩放
    Args:
        im: numpy.ndarray, 输入图像数据
        target_size: int|list|tuple, 缩放目标大小
        interp: cv2.INTER_TYPE, opencv的插值类型
    Return
        im: numpy.ndarray, 缩放处理好的图像数据
    """
    if isinstance(target_size, list) or isinstance(target_size, tuple):
        w = target_size[0]
        h = target_size[1]
    else:
        w = target_size
        h = target_size
    im = cv2.resize(im, (w, h), interpolation=interp)
    return im


def seg_transforms(im, target_size=480, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]):
    """自构的预处理 -- 只需要关注target_size即可
    desc: 分割模型需要的预处理方法集合
    Args:
        im: numpy.ndarray, 输入图像数据
        target_size: int|list|tuple, 缩放目标大小
        mean: list, 每个通道的归一化均值数据
        std: list, 每个通道的归一化方差数据
    Return
        im: numpy.ndarray, 预处理好的图像数据
    """
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im = resize(im, target_size=target_size)
    im = normalize(im, mean=mean, std=std)
    im = np.transpose(im, (2, 0, 1))
    return im


def find_border(seg_result_and_kind):
    """查询指定类别的分割区域边界
    desc: 寻找模型输出中某一类别的分割边界
    Args:
        seg_result_and_kind: list[seg_result, kind], 分割结果与当前查找类别
    Return:
        [kind, contours]:
            kind: 当前边界类别
            contours: 所有找到的边界坐标
    """
    # kind: 1, 2, 3
    seg_kind_map, kind = seg_result_and_kind # [seg_result, kind]
    # 当前类别分割区域设置为255，其它像素值设置为0
    # set 255 and 0 value
    seg_kind_map = np.where(seg_kind_map==kind, np.full_like(seg_kind_map, fill_value=255), np.zeros_like(seg_kind_map)).astype('uint8')
    # 根据黑白值进行边界搜索，返回各边界的边界坐标集合
    contours, hierarchy = cv2.findContours(seg_kind_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return [kind, contours]


def predict_image(segmentor, image_list, result_path):
    """
    desc: 利用分割模型去推理测试文件，并保存推理结果
    Args:
        segmentor: class, 分割推理器
        image_list: list, 要预测的图片路径List
        result_path: str, 预测结果要保存的路径
    Return:
        None
    """
    c_results = {"result": []}
    pool = ThreadPool(processes=8) # 多线程处理输入图像，预处理速度快一些
    img_length = len(image_list)
    img_iter_filter = 8 # 根据评估数据自行调整每次多线程处理的样本数量, len(image_list) >= img_iter_filter
    img_iter_range = list(range(img_length//img_iter_filter))

    for start_index in img_iter_range:
        if start_index == img_iter_range[-1]:
            im_paths = image_list[start_index*img_iter_filter:]
        else:
            im_paths = image_list[start_index*img_iter_filter:(start_index+1)*img_iter_filter]
        image_ids = [int(os.path.basename(im_p).split('.')[0]) for im_p in im_paths]

        ims = pool.map(cv2.imread, im_paths) # 阻塞调用: 根据需要自行设计异步队列等形式的多线程数据读取与处理来加速
        im_origin_shapes = [i.shape for i in ims]
        ims = pool.map(seg_transforms, ims)
        im_resize_shapes = [i.shape for i in ims]
        
        for idx, im in enumerate(ims):
            im_origin_shape = im_origin_shapes[idx]
            im_resize_shape = im_resize_shapes[idx]
            image_id = image_ids[idx]

            # 语义分割模型 -- Run Model
            seg_results = segmentor.run(im[np.newaxis, :, :, :]) # shape: [1, -1, -1, -1]

            # 语义分割模型: Post Process: 0,1,2,3
            seg_result = np.squeeze(seg_results[0, :, :])

            # 语义分割模型: Search segmentation
            contour_list = []
            cls_set = np.unique(seg_result) # 查看当前输出结果包含的类别情况
            cls_set = [ [seg_result, i] for i in cls_set.tolist() if i!=0 ]
            if len(cls_set) == 0: # 仅包含0背景类时，不必往后进行数据处理与保存
                # 当模型预测能力较差时，可能存在部分预测图片中仅仅预测出背景
                # 从而导致当前样本没有保存相应的预测result结果
                # 为了保证评测数据对应，因此针对仅预测出背景的预测图片——给予一个空的result
                c_results["result"].append({"image_id": image_id, 
                                            "type": 1,   # 实际类别
                                            "segmentation": [[0, 0, 0, 0]]})
                continue
            contour_list = pool.map(find_border,
                                    cls_set) # [[kind, contour], ...]

            # find_border实现原型: 供参考
            # if 1 in cls_set:
            #     seg_kind1_map = seg_result
            #     # set 255 + 0 value
            #     seg_kind1_map = np.where(seg_kind1_map==1, np.full_like(seg_kind1_map, fill_value=255), np.zeros_like(seg_kind1_map)).astype('uint8')
            #     contours, hierarchy = cv2.findContours(seg_kind1_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #     contour_list.append([1, contours])
            # if 2 in cls_set:
            #     seg_kind2_map = seg_result
            #     # set 255 + 0 value
            #     seg_kind2_map = np.where(seg_kind2_map==2, np.full_like(seg_kind2_map, fill_value=255), np.zeros_like(seg_kind2_map)).astype('uint8')
            #     contours, hierarchy = cv2.findContours(seg_kind2_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #     contour_list.append([2, contours])
            # if 3 in cls_set:
            #     seg_kind3_map = seg_result
            #     # set 255 + 0 value
            #     seg_kind3_map = np.where(seg_kind3_map==3, np.full_like(seg_kind3_map, fill_value=255), np.zeros_like(seg_kind3_map)).astype('uint8')
            #     contours, hierarchy = cv2.findContours(seg_kind3_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #     contour_list.append([3, contours])

            # 语义分割模型: Search segmentation
            # 使用检测模型的预处理，计算一下原图的尺寸，然后再计算分割图需要还原的比例
            w_ratio = float(im_origin_shape[1] / im_resize_shape[2])
            h_ratio = float(im_origin_shape[0] / im_resize_shape[1])
            
            for contours in contour_list:
                contour_kind = contours[0] # 实际分类
                for contour in  contours[1]: # 实际的contours
                    segmentations = []
                    for point in contour:
                        segmentations.append(round(point[0][0] * w_ratio, 1))
                        segmentations.append(round(point[0][1] * h_ratio, 1))
                    c_results["result"].append({"image_id": image_id, 
                                                "type": contour_kind,   # 实际类别
                                                "segmentation": [segmentations]})


    # 写文件
    with open(result_path, 'w') as ft:
        json.dump(c_results, ft)

def main(infer_txt, result_path, seg_model_path):
    """
    desc: 推理主函数
    Args:
        infer_txt: str, 包含要预测的图片路径的txt文件路径
        result_path: str, 预测结果要保存的路径
        seg_model_path: str, 分割模型所在目录
    """
    # create predictor
    segmentor = Segmentor(seg_model_path)

    # predict from image
    img_list = get_test_images(infer_txt)

    predict_image(segmentor, img_list, result_path)

if __name__ == '__main__':
    seg_model_path = "./model/bisenet/"

    paddle.enable_static()
    infer_txt = sys.argv[1]
    result_path = sys.argv[2]

    main(infer_txt, result_path, seg_model_path)