import cv2
import os
import numpy as np
from PIL import Image
import cfg

class Goods():
    def __init__(self):
        self.ptdir = cfg.ptdir
        self.tadirs = [os.path.join(self.ptdir, name) for name in os.listdir(self.ptdir)]  # 模板图片的绝对路径
        self.tplnames = [os.path.splitext(name)[0] for name in os.listdir(self.ptdir)]  # 所有模板名字
        self.goods_position = cfg.goods_position
        self.goods_abs_position = cfg.goods_abs_position
        self.slen = 30  # 货物框1/2边长
        self.tplimgs = [Image.fromarray(cv2.imread(tdir, 1), 'RGB') for tdir in self.tadirs]    # 模板图片

    def get_lt_rb(self,pt):
        """由中心坐标和正方形的1/2边长获取左上和右下坐标"""
        lt = (pt[0] - self.slen, pt[1] - self.slen)
        rb = (pt[0] + self.slen, pt[1] + self.slen)
        return [lt, rb]

    def get_roi(self,img, pt):
        """获取货物"""
        pt = np.array(pt).flatten()
        roi = img[pt[1]:pt[3], pt[0]:pt[2]]
        return roi

    def calc_similar(self,li, ri):
        """计算图像相似度"""
        lh = li.histogram()
        rh = ri.histogram()
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)

    def match_goods(self,img):
        """匹配货物，返回货物和建筑的坐标"""
        if img is None:
            return [],[]
        img = img[1400:-200, 400:]
        if img is None:
            return [],[]
        goods_pts, bld_pts = [], []
        for gidx,cpt in enumerate(self.goods_position):
            pts = self.get_lt_rb(cpt)
            roi = self.get_roi(img, pts)
            roi_n = Image.fromarray(roi, 'RGB')
            res = []
            for tpl in self.tplimgs:
                res.append(self.calc_similar(roi_n, tpl))
            idx = res.index(max(res))
            print(gidx,":",self.tplnames[idx])
            if self.tplnames[idx] in cfg.goods_mapping.keys():
                goods_pts.append(self.goods_abs_position[gidx])
                bld_pts.append(cfg.bld_positions[cfg.goods_mapping.get(self.tplnames[idx])])
        return goods_pts,bld_pts
